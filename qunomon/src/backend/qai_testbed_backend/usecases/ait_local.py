# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import os
import zipfile
import json
import asyncio
from pathlib import Path
import shutil
import datetime
import docker
from flask import request

from qlib.utils.logging import get_logger, log

from ..controllers.dto import Result
from ..controllers.dto.ait_local import GetAITLocalListRes, PostAITLocalListRes, ValidationOutputRes
from ..controllers.dto.ait_manifest import AITManifestSchema
from ..entities.setting import SettingMapper
from ..entities.test_runner import TestRunnerMapper
from ..entities.test_runner_reference import TestRunnerReferenceMapper
from ..entities.downloadable_template import DownloadableTemplateMapper
from ..entities.quality_measurement import QualityMeasurementMapper
from ..entities.graph_template import GraphTemplateMapper
from ..entities.structure import StructureMapper
from ..entities.test_runner_param_template import TestRunnerParamTemplateMapper
from ..entities.test_inventory_template import TestInventoryTemplateMapper
from ..entities.test_runner import TestRunnerMapper
from ..entities.format import FormatMapper
from ..entities.test_inventory_template_format import TestInventoryTemplateFormatMapper
from ..entities.test_inventory_template_compatible_package import TestInventoryTemplateCompatiblePackageMapper
from ..entities.test_inventory_template_additional_info import TestInventoryTemplateAdditionalInfoMapper
from ..entities.resource_type import ResourceTypeMapper
from ..entities.data_type import DataTypeMapper
from ..across.exception import QAIBadRequestException
from ..gateways.extensions import sql_db
from sqlalchemy.exc import SQLAlchemyError
from threading import Thread
from threading import BoundedSemaphore

logger = get_logger()

semaphore = BoundedSemaphore(1)


class AITLocalService:

    @log(logger)
    def get_ait_local_list(self) -> GetAITLocalListRes:

        ait_local_list = TestRunnerMapper.query. \
                        filter(TestRunnerMapper.delete_flag == False). \
                        filter(TestRunnerMapper.install_mode == '0'). \
                        all()

        return GetAITLocalListRes(
            result=Result(code='AL0000', message="get ait local list success."),
            ait_Local_list= [t.to_template_dto() for t in ait_local_list]
        )

    @log(logger)
    def post_ait_local_list(self) -> PostAITLocalListRes:

        try:
            # zipの受信
            ait_zip = request.files['ait_zip']
            upload_path = os.getenv('UPLOAD_PATH')
            dt_now = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
            zip_path = f'{upload_path}/zip/{ait_zip.filename[:-4]}.{dt_now}.zip'
            ait_zip.save(zip_path)
    
            # ファイルサイズチェック
            file_size = os.path.getsize(zip_path)
            limit_size = 5
            if file_size > limit_size * 1024 * 1024:
                raise QAIBadRequestException('AL1400', 'File size is too large. Registration is rejected.')

            # zipの解凍
            dir_name = ait_zip.filename[:-4]
            file_path = f'{upload_path}/{dir_name}.1'

            # 同じフォルダ名が存在する場合は番号をインクリメントする
            for i in range(1, 5):
                if os.path.exists(file_path):
                    file_path = f'{file_path}.{i+1}'
                else:
                    break
    
            with zipfile.ZipFile(zip_path) as zip:
                zip.extractall(file_path)
    
           # ファイル存在チェック
            file_path_repo = f'{file_path}/repository'
            validation_outputs = []
            if not os.path.isfile(f'{file_path}/dockerfile') and not os.path.isfile(f'{file_path}/Dockerfile'):
                validation_outputs.append(ValidationOutputRes(
                    f'{dir_name}/Dockerfile', 'FileNotFoundError'))
            if not os.path.isfile(f'{file_path_repo}/ait.manifest.json'):
                validation_outputs.append(ValidationOutputRes(
                    f'{dir_name}/repository/ait.manifest.json', 'FileNotFoundError'))
            if not os.path.isfile(f'{file_path_repo}/my_ait.py'):
                validation_outputs.append(ValidationOutputRes(
                f'{dir_name}/repository/my_ait.py', 'FileNotFoundError'))
            if not os.path.isfile(f'{file_path_repo}/requirements.txt'):
                validation_outputs.append(ValidationOutputRes(
                    f'{dir_name}/repository/requirements.txt', 'FileNotFoundError'))
            if validation_outputs != []:
                return PostAITLocalListRes(
                    result=Result(
                        code='AL1400', message="Invalid AIT. 'Registration is rejected."),
                    validation_outputs=validation_outputs
                )
    
            # AITマニフェストの乖離チェック
            with open(f'{file_path_repo}/ait.manifest.json') as f:
                mnf = json.load(f)
    
            location = f'in file: /{ait_zip.filename}/repository/ait.manifest.json'
            validation_outputs = self.__check_manifest(mnf, location)
            if validation_outputs != []:
                return PostAITLocalListRes(
                    result=Result(code='AL1400', message="Invalid AIT. 'Registration is rejected."),
                    validation_outputs=validation_outputs
                )


            # データ登録中チェック
            dupli_ait = TestRunnerMapper.query\
                .filter(TestRunnerMapper.name == mnf['name'])\
                .filter(TestRunnerMapper.version == mnf['version'])\
                .filter(TestRunnerMapper.delete_flag.is_(False))\
                .first()

            if dupli_ait is not None:
                return PostAITLocalListRes(
                    result=Result(code='AL1400', message="Invalid AIT. 'Registration is rejected."),
                    validation_outputs=[ValidationOutputRes(
                        location,
                        'This AIT is currently being registered.'
                    )]
                )
    
            # AIT登録
            ait_mapper = TestRunnerMapper(
                name=mnf['name'],
                version=mnf['version'],
                quality=mnf['quality'],
                landing_page='',
                install_mode='0',
                install_status='registration in progress'
            )
            sql_db.session.add(ait_mapper)
            sql_db.session.commit()

            # 非同期処理
            loop = asyncio.new_event_loop()
            thread = Thread(target=self.__thread_worker, args=(file_path, mnf, ait_mapper.id, zip_path, loop))
            thread.start()

            return PostAITLocalListRes(
                result=Result(code='AL1000', message="Registration is accepted."))

        except SQLAlchemyError:
            sql_db.session.rollback()
            raise QAIBadRequestException('AL1500-1', 'unexpected error.')

        finally:
            sql_db.session.close()
    
    @staticmethod
    def _replace_template(docker_host_name, ait_name, ait_version, in_file, out_file, encoding):
        with open(in_file, encoding=encoding) as f:
            data_lines = f.read()
        data_lines = data_lines.replace('{DOCKER_HOST_NAME}', docker_host_name)
        data_lines = data_lines.replace('{AIT_NAME}', ait_name)
        data_lines = data_lines.replace('{AIT_VERSION}', ait_version)
        with open(out_file, mode='w', encoding=encoding, newline="\r\n") as f:
            f.write(data_lines)

    @log(logger)
    def __thread_worker(self, file_path, mnf, ait_id, zip_path, loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.__push_docker_private_registry(file_path, mnf, ait_id, zip_path))

    @log(logger)
    async def __push_docker_private_registry(self, file_path, mnf, ait_id, zip_path):

        import entrypoint

        with entrypoint.app.app_context():
            try:
                # AIT
                manifest = AITManifestSchema().load(mnf)

                logger.debug(manifest)

                # ローカル登録ユーザアカウント
                create_user_account = SettingMapper.query.get('local_create_user_account').value
                create_user_name = SettingMapper.query.get('local_create_user_name').value

                # dagファイル保存
                docker_host = 'localhost:5050'
                dag_template = Path(__file__).parent.joinpath('../../../dag/dag_template.py')
                # dockerイメージ名は小文字のname + 登録ユーザアカウント
                ait_name = manifest.name.lower()
                docker_image_name = ait_name  + '-' + create_user_account
                ait_dir_name = docker_image_name + '_' + manifest.version.lower()
                dir_path = Path(__file__).parent.joinpath('../../../dag', ait_dir_name)
                sava_dag_file_path = dir_path.joinpath('dag.py')
                sava_manifest_file_path = dir_path.joinpath('ait.manifest.json')
                if not dir_path.exists():
                    dir_path.mkdir(parents=True)
                else:
                    shutil.rmtree(str(dir_path))
                    dir_path.mkdir(parents=True)
                self._replace_template(docker_host, docker_image_name, manifest.version.lower(), dag_template, sava_dag_file_path, 'utf-8')
                # マニフェストファイル保存
                # TODO ダミーAITHubからはマニフェストファイルが取得できないので、json.dumpsで作成し直す
                with open(str(sava_manifest_file_path), mode='w', encoding='utf-8', newline="\n") as f:
                    f.write(json.dumps(mnf, ensure_ascii=False, indent=4))

                ait_local_mapper = TestRunnerMapper.query.get(ait_id)
                ait_local_mapper.description = manifest.description
                ait_local_mapper.source_repository = manifest.source_repository
                ait_local_mapper.create_user_account=create_user_account
                ait_local_mapper.create_user_name=create_user_name
                ait_local_mapper.keywords=','.join(manifest.keywords)
                ait_local_mapper.licenses=','.join(manifest.licenses)
                sql_db.session.flush()

                # references
                test_runner_reference_mapper_list = []
                if manifest.references is not None:
                    for reference in manifest.references:
                        test_runner_reference_mapper_list.append(
                            TestRunnerReferenceMapper(test_runner_id=ait_local_mapper.id,
                                                      bib_info=reference.bib_info,
                                                      additional_info=reference.additional_info,
                                                      url_=reference.url))
                sql_db.session.add_all(test_runner_reference_mapper_list)

                # downloadable_template
                downloadable_data_mapper_list = []
                for download in manifest.downloads:
                    downloadable_data_mapper_list.append(
                        DownloadableTemplateMapper(name=download.name, 
                                                   description=download.description,
                                                   test_runner_id=ait_local_mapper.id))
                sql_db.session.add_all(downloadable_data_mapper_list)

                # quality_measurement
                quality_measurement_mapper_list = []

                for measure in manifest.report.measures:
                    # structure
                    structure = StructureMapper.query.filter(StructureMapper.structure == measure.structure).first()
                    if structure is None:
                        structure = StructureMapper(structure=measure.structure)
                        sql_db.session.add(structure)
                        sql_db.session.flush()
                    # quality_measurement
                    quality_measurement_mapper_list.append(
                        QualityMeasurementMapper(name=measure.name, 
                                                 description=measure.description, 
                                                 type=measure.type,
                                                 min_value=measure.min_value, 
                                                 max_value=measure.max_value,
                                                 structure_id=structure.id, 
                                                 test_runner_id=ait_local_mapper.id))
                sql_db.session.add_all(quality_measurement_mapper_list)

                # graph_template
                graph_template_mapper_list = []
                for resource in manifest.report.resources:

                    # リソースタイプ取得
                    res_type = ResourceTypeMapper.query.filter(ResourceTypeMapper.type == resource.type).first()
                    if res_type is None:
                        res_type = ResourceTypeMapper(type=resource.type)
                        sql_db.session.add(res_type)
                        sql_db.session.flush()

                    graph_template_mapper_list.append(
                        GraphTemplateMapper(resource_type_id=res_type.id, 
                                            name=resource.name,
                                            description=resource.description,
                                            test_runner_id=ait_local_mapper.id))
                sql_db.session.add_all(graph_template_mapper_list)

                # test_runner_param_template
                test_runner_param_template_mapper_list = []
                for parameter in manifest.parameters:
                    test_runner_param_template_mapper_list.append(
                        TestRunnerParamTemplateMapper(name=parameter.name, 
                                                      value_type=parameter.type,
                                                      description=parameter.description,
                                                      default_value=parameter.default_value,
                                                      min_value=parameter.min_value,
                                                      max_value=parameter.max_value,
                                                      test_runner_id=ait_local_mapper.id,
                                                      depends_on_parameter=parameter.depends_on_parameter))
                sql_db.session.add_all(test_runner_param_template_mapper_list)

                # test_inventory_template
                test_inventory_template_mapper_list = []
                for inventory in manifest.inventories:
                    data_type_mapper = DataTypeMapper.query.filter(DataTypeMapper.name == inventory.type).first()
                    if data_type_mapper is None:
                        raise QAIBadRequestException('AJ1400', 'inventory type must be dataset, model or feature')
                    test_inventory_template_mapper = TestInventoryTemplateMapper(
                                                        name=inventory.name,
                                                        type_id=data_type_mapper.id,
                                                        description=inventory.description,
                                                        test_runner_id=ait_local_mapper.id,
                                                        depends_on_parameter=inventory.depends_on_parameter,
                                                        min=inventory.requirement.min,
                                                        max=inventory.requirement.max)
                    sql_db.session.add(test_inventory_template_mapper)
                    sql_db.session.flush()

                    # format
                    for format_ in inventory.requirement.format:
                        format_mapper = FormatMapper.query.filter(FormatMapper.format_ == format_).first()
                        if format_mapper is None:
                            format_mapper = FormatMapper(format_=format_)
                            sql_db.session.add(format_mapper)
                            sql_db.session.flush()
                        test_inventory_template_mapper_list.append(
                            TestInventoryTemplateFormatMapper(inventory_template_id=test_inventory_template_mapper.id_,
                                                              format_id=format_mapper.id))
                    
                    # compatible_packages
                    if inventory.requirement.compatible_packages is not None:
                        for compatible_package in inventory.requirement.compatible_packages:
                            test_inventory_template_mapper_list.append(
                                TestInventoryTemplateCompatiblePackageMapper(
                                    inventory_template_id=test_inventory_template_mapper.id_,
                                    name=compatible_package.name,
                                    version=compatible_package.version,
                                    additional_info=compatible_package.additional_info))
                            
                    # additional_info
                    if inventory.requirement.additional_info is not None:
                        for addi in inventory.requirement.additional_info:
                            for key, value in addi.items():
                                if isinstance(value, list):
                                    value = " , ".join(value)
                                test_inventory_template_mapper_list.append(
                                    TestInventoryTemplateAdditionalInfoMapper(
                                        inventory_template_id=test_inventory_template_mapper.id_,
                                        key=key,
                                        value=value))

                sql_db.session.add_all(test_inventory_template_mapper_list)
                sql_db.session.commit()

                # Docker private registry 
                ait_nm = mnf['name'].lower()
                ait_ver = mnf['version'].lower()
                client = docker.from_env()
                tag = f'localhost:5050/{ait_nm}-{create_user_account.lower()}:{ait_ver}'
                client.images.build(path=f'{file_path}/', tag=tag, forcerm=True)
                
                # セマフォにより排他制御
                with semaphore:
                    client.images.push(tag)

                    # # ローカルイメージ削除
                    # client.images.remove(image=tag)

                    # イベント情報登録
                    reg_ait_local_mapper = TestRunnerMapper.query.get(ait_id)
                    reg_ait_local_mapper.install_status = 'OK'

                    sql_db.session.add(reg_ait_local_mapper)
                    sql_db.session.commit()

                    # アップロードファイル削除
                    self.__delete_upload_file(file_path, zip_path)

            except SQLAlchemyError:
                sql_db.session.rollback()
                self.__delete_upload_file(file_path, zip_path)
                self.__update_event_failed(ait_id)
                raise QAIBadRequestException('AL1500-2', 'unexpected error.')

            except Exception:
                sql_db.session.rollback()
                self.__delete_upload_file(file_path, zip_path)
                self.__update_event_failed(ait_id)
                raise QAIBadRequestException('AL1500-3', 'unexpected error.')

            finally:
                sql_db.session.close()

    @log(logger)
    def __delete_upload_file(self, file_path, zip_path):
        shutil.rmtree(f'{file_path}/')
        os.remove(zip_path)

    @log(logger)
    def __update_event_failed(self, ait_id):
        try:
            # failedにして登録
            ait_local_mapper = TestRunnerMapper.query.get(ait_id)
            ait_local_mapper.install_status = 'registration failed'
            ait_local_mapper.delete_flag = True
            sql_db.session.commit()

        except SQLAlchemyError:
            sql_db.session.rollback()
            raise QAIBadRequestException('AL1500-4', 'unexpected error.')
        except Exception:
            sql_db.session.rollback()
            raise QAIBadRequestException('AL1500-5', 'unexpected error.')

    @log(logger)
    def __check_manifest(self, mnf, location):
        validation_outputs = []
        msg_required = 'required field type: {} is not specified.'
        msg_not_list = 'field type: {} is not list.'
        msg_illegal = 'field type: {} is illegal. '
        msg_choose = 'Please choose from the following: {}.'
        msg_match = '{0} should match the {1}.'
        msg_minmax = 'min should be less than max.'
        msg_duplicated = 'field type: {} is duplicated.'

        # name
        if not mnf.get('name'):
            validation_outputs.append(ValidationOutputRes(
                location,
                msg_required.format('name')))
        # description
        if not mnf.get('description'):
            validation_outputs.append(ValidationOutputRes(
                location,
                msg_required.format('description')))
        # version
        if not mnf.get('version'):
            validation_outputs.append(ValidationOutputRes(
                location,
                msg_required.format('version')))
        # quality
        if not mnf.get('quality'):
            validation_outputs.append(ValidationOutputRes(
                location,
                msg_required.format('quality')))
        # keywords
        if mnf.get('keywords') is not None\
                and not isinstance(mnf['keywords'], list):
            validation_outputs.append(ValidationOutputRes(
                location,
                msg_not_list.format('keywords')))
        # references
        if mnf.get('references') is not None:
            if not isinstance(mnf['references'], list):
                validation_outputs.append(ValidationOutputRes(
                    location,
                    msg_not_list.format('references')))
            else:
                for i, refer in enumerate(mnf['references']):
                    # references.bib_info
                    if not refer.get('bib_info'):
                        validation_outputs.append(ValidationOutputRes(
                            location,
                            msg_required.format(f'references[{i}].bib_info')))
        # licenses
        if mnf.get('licenses') is not None\
                and not isinstance(mnf['licenses'], list):
            validation_outputs.append(ValidationOutputRes(
                location,
                msg_not_list.format('licenses')))
        # parameters
        param_names = []
        if mnf.get('parameters') is None:
            validation_outputs.append(ValidationOutputRes(
                location,
                msg_required.format('parameters')))
        elif not isinstance(mnf['parameters'], list):
            validation_outputs.append(ValidationOutputRes(
                location,
                msg_not_list.format('parameters')))
        else:
            param_types = ['int', 'float', 'bool', 'str']
            for i, parameter in enumerate(mnf['parameters']):
                # parameters.name
                if not parameter.get('name'):
                    validation_outputs.append(ValidationOutputRes(
                        location,
                        msg_required.format(f'parameters[{i}].name')))
                else:
                    param_names.append(parameter['name'])
                # parameters.type
                if not parameter.get('type'):
                    validation_outputs.append(ValidationOutputRes(
                        location,
                        msg_required.format(f'parameters[{i}].type')))
                else:
                    if parameter['type'] not in param_types:
                        validation_outputs.append(ValidationOutputRes(
                            location,
                            msg_illegal.format(f'parameters[{i}].type')
                            + msg_choose.format(param_types)))
                # parameters.description
                if not parameter.get('description'):
                    validation_outputs.append(ValidationOutputRes(
                        location,
                        msg_required.format(f'parameters[{i}].description')))
                # parameters.default_val
                if parameter.get('default_val')\
                        and parameter.get('type') in param_types:
                    try:
                        eval(parameter['type'])(parameter['default_val'])
                    except ValueError:
                        validation_outputs.append(ValidationOutputRes(
                            location,
                            msg_illegal.format(f'parameters[{i}].default_val')
                            + msg_match.format('default_val', f'parameters[{i}].type')))
                # parameters.min
                is_param_min_numeric = False
                if parameter.get('min')\
                        and parameter.get('type') in ['int', 'float']:
                    try:
                        eval(parameter['type'])(parameter['min'])
                        is_param_min_numeric = True
                    except ValueError:
                        validation_outputs.append(ValidationOutputRes(
                            location,
                            msg_illegal.format(f'parameters[{i}].min')
                            + msg_match.format('min', f'parameters[{i}].type')))
                # parameters.max
                is_param_max_numeric = False
                if parameter.get('max')\
                        and parameter.get('type') in ['int', 'float']:
                    try:
                        eval(parameter['type'])(parameter['max'])
                        is_param_max_numeric = True
                    except ValueError:
                        validation_outputs.append(ValidationOutputRes(
                            location,
                            msg_illegal.format(f'parameters[{i}].max')
                            + msg_match.format('max', f'parameters[{i}].type')))
                # parameters.min < max
                if is_param_min_numeric\
                        and is_param_max_numeric\
                        and parameter['min'] >= parameter['max']:
                    validation_outputs.append(ValidationOutputRes(
                        location,
                        msg_illegal.format(f'parameters[{i}].min max')
                        + msg_minmax))
            if len(param_names) != len(set(param_names)):
                validation_outputs.append(ValidationOutputRes(
                    location,
                    msg_duplicated.format('parameters.name')))
        # inventories
        if not mnf.get('inventories'):
            validation_outputs.append(ValidationOutputRes(
                location,
                msg_required.format('inventories')))
        elif not isinstance(mnf['inventories'], list):
            validation_outputs.append(ValidationOutputRes(
                location,
                msg_not_list.format('inventories')))
        else:
            inv_names = []
            inv_types = ['dataset', 'executable_model',
                         'model', 'attribute set']
            for i, inventory in enumerate(mnf['inventories']):
                # inventories.name
                if not inventory.get('name'):
                    validation_outputs.append(ValidationOutputRes(
                        location,
                        msg_required.format(f'inventories[{i}].name')))
                else:
                    inv_names.append(inventory['name'])
                # inventories.type
                if not inventory.get('type'):
                    validation_outputs.append(ValidationOutputRes(
                        location,
                        msg_required.format(f'inventories[{i}].type')))
                else:
                    if inventory['type'] not in inv_types:
                        validation_outputs.append(ValidationOutputRes(
                            location,
                            msg_illegal.format(f'inventories[{i}].type')
                            + msg_choose.format(inv_types)))
                # inventories.description
                if not inventory.get('description'):
                    validation_outputs.append(ValidationOutputRes(
                        location,
                        msg_required.format(f'inventories[{i}].description')))
                # inventories.requirement
                if not inventory.get('requirement'):
                    validation_outputs.append(ValidationOutputRes(
                        location,
                        msg_required.format(f'inventories[{i}].requirement')))
                else:
                    inv_req = inventory['requirement']
                    # inventories.requirement.format
                    if not inv_req.get('format'):
                        validation_outputs.append(ValidationOutputRes(
                            location,
                            msg_required.format(f'inventories[{i}].requirement.format')))
                    elif not isinstance(inv_req['format'], list):
                        validation_outputs.append(ValidationOutputRes(
                            location,
                            msg_not_list.format(f'inventories[{i}].requirement.format')))
                    # inventories.requirement.depends_on_parameter
                    if inv_req.get('depends_on_parameter')\
                            and inv_req['depends_on_parameter'] not in param_names:
                        validation_outputs.append(ValidationOutputRes(
                            location,
                            msg_illegal.format(f'inventories[{i}].requirement'
                                               '.depends_on_parameter')
                            + 'Please choose from parameters.name'))
                    # inventories.requirement.compatible_packages
                    if inv_req.get('compatible_packages') is not None:
                        if not isinstance(inv_req['compatible_packages'], list):
                            validation_outputs.append(ValidationOutputRes(
                                location,
                                msg_not_list.format(f'inventories[{i}].requirement.compatible_packages')))
                        else:
                            depend_names = [i.get('name')
                                            for i in inv_req['compatible_packages']
                                            if i.get('name') is not None]
                            if len(depend_names) != len(set(depend_names)):
                                validation_outputs.append(ValidationOutputRes(
                                    location,
                                    msg_duplicated.format(f'inventories[{i}].requirement.compatible_packages.name')))
            if len(inv_names) != len(set(inv_names)):
                validation_outputs.append(ValidationOutputRes(
                    location,
                    msg_duplicated.format('inventories.name')))
        # report
        if not mnf.get('report'):
            validation_outputs.append(ValidationOutputRes(
                location,
                msg_required.format('report')))
        else:
            report = mnf['report']
            # measures
            if report.get('measures') is None or report['measures'] == '':
                validation_outputs.append(ValidationOutputRes(
                    location,
                    msg_required.format('measures')))
            elif not isinstance(report['measures'], list):
                validation_outputs.append(ValidationOutputRes(
                    location,
                    msg_not_list.format('measures')))
            else:
                measure_names = []
                measure_types = ['int', 'float', 'bool', 'str']
                measure_structures = ['single', 'sequence']
                for i, measure in enumerate(report['measures']):
                    # report.measures.name
                    if not measure.get('name'):
                        validation_outputs.append(ValidationOutputRes(
                            location,
                            msg_required.format(f'report.measures[{i}].name')))
                    else:
                        measure_names.append(measure['name'])
                    # report.measures.type
                    if not measure.get('type'):
                        validation_outputs.append(ValidationOutputRes(
                            location,
                            msg_required.format(f'report.measures[{i}].type')))
                    else:
                        if measure['type'] not in measure_types:
                            validation_outputs.append(ValidationOutputRes(
                                location,
                                msg_illegal.format(f'report.measures[{i}].type')
                                + msg_choose.format(measure_types)))
                    # report.measures.description
                    if not measure.get('description'):
                        validation_outputs.append(ValidationOutputRes(
                            location,
                            msg_required.format(f'report.measures[{i}].description')))
                    # report.measures.structure
                    if not measure.get('structure'):
                        validation_outputs.append(ValidationOutputRes(
                            location,
                            msg_required.format(f'report.measures[{i}].structure')))
                    elif measure['structure'] not in measure_structures:
                        validation_outputs.append(ValidationOutputRes(
                            location,
                            msg_illegal.format(f'report.measures[{i}].structure')
                            + msg_choose.format(measure_structures)))
                    # report.measures.min
                    is_measure_min_numeric = False
                    if measure.get('min')\
                            and measure.get('type') in ['int', 'float']:
                        try:
                            eval(measure['type'])(measure['min'])
                            is_measure_min_numeric = True
                        except ValueError:
                            validation_outputs.append(ValidationOutputRes(
                                location,
                                msg_illegal.format(f'report.measures[{i}].min')
                                + msg_match.format('min', f'report.measures[{i}].type')))
                    # report.measures.max
                    is_measure_max_numeric = False
                    if measure.get('max')\
                            and measure.get('type') in ['int', 'float']:
                        try:
                            eval(measure['type'])(measure['max'])
                            is_measure_max_numeric = True
                        except ValueError:
                            validation_outputs.append(ValidationOutputRes(
                                location,
                                msg_illegal.format(f'report.measures[{i}].max')
                                + msg_match.format('max', f'report.measures[{i}].type')))
                    # report.measures.min < max
                    if is_measure_min_numeric\
                            and is_measure_max_numeric\
                            and measure['min'] >= measure['max']:
                        validation_outputs.append(ValidationOutputRes(
                            location,
                            msg_illegal.format(f'report.measures[{i}].min max')
                            + msg_minmax))
                if len(measure_names) != len(set(measure_names)):
                    validation_outputs.append(ValidationOutputRes(
                        location,
                        msg_duplicated.format('report.measures.name')))
            # resources
            if report.get('resources') is None or report['resources'] == '':
                validation_outputs.append(ValidationOutputRes(
                    location,
                    msg_required.format('resources')))
            elif not isinstance(report['resources'], list):
                validation_outputs.append(ValidationOutputRes(
                    location,
                    msg_not_list.format('resources')))
            else:
                resource_names = []
                resource_types = ['text', 'picture', 'table']
                for i, resource in enumerate(report['resources']):
                    # report.resources.name
                    if not resource.get('name'):
                        validation_outputs.append(ValidationOutputRes(
                            location,
                            msg_required.format(f'report.resources[{i}].name')))
                    else:
                        resource_names.append(resource['name'])
                    # report.resources.type
                    if not resource.get('type'):
                        validation_outputs.append(ValidationOutputRes(
                            location,
                            msg_required.format(f'report.resources[{i}].type')))
                    else:
                        if resource['type'] not in resource_types:
                            validation_outputs.append(ValidationOutputRes(
                                location,
                                msg_illegal.format(f'report.resources[{i}].type')
                                + msg_choose.format(resource_types)))
                    # report.resources.description
                    if not resource.get('description'):
                        validation_outputs.append(ValidationOutputRes(
                            location,
                            msg_required.format(f'report.resources[{i}].description')))
                if len(resource_names) != len(set(resource_names)):
                    validation_outputs.append(ValidationOutputRes(
                        location,
                        msg_duplicated.format('report.resources.name')))
        # downloads
        if mnf.get('downloads') is None or mnf['downloads'] == '':
            validation_outputs.append(ValidationOutputRes(
                location,
                msg_required.format('downloads')))
        elif not isinstance(mnf['downloads'], list):
            validation_outputs.append(ValidationOutputRes(
                location,
                msg_not_list.format('downloads')))
        else:
            download_names = []
            for i, download in enumerate(mnf['downloads']):
                # downloads.name
                if not download.get('name'):
                    validation_outputs.append(ValidationOutputRes(
                        location,
                        msg_required.format(f'downloads[{i}].name')))
                else:
                    download_names.append(download['name'])
                # downloads.description
                if not download.get('description'):
                    validation_outputs.append(ValidationOutputRes(
                        location,
                        msg_required.format(f'downloads[{i}].description')))
            if len(download_names) != len(set(download_names)):
                validation_outputs.append(ValidationOutputRes(
                    location,
                    msg_duplicated.format('downloads.name')))

        return validation_outputs
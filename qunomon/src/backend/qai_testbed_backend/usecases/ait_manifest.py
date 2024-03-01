# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from pathlib import Path
import json
import shutil
import requests
import docker

from injector import singleton
import werkzeug
from tempfile import TemporaryDirectory
from marshmallow import ValidationError
from qlib.utils.logging import get_logger, log

from ..across.exception import QAIException, \
    QAIInvalidRequestException, QAIBadRequestException, QAINotFoundException, QAIInternalServerException
from ..controllers.dto.testrunner import Result
from ..controllers.dto.ait_manifest import AITManifest, AITManifestSchema, PostAITManifestRes, GetTestRunnerRes
from ..entities.test_runner_reference import TestRunnerReferenceMapper
from ..entities.downloadable_template import DownloadableTemplateMapper
from ..entities.quality_measurement import QualityMeasurementMapper
from ..entities.structure import StructureMapper
from ..entities.setting import SettingMapper
from ..entities.graph_template import GraphTemplateMapper
from ..entities.test_description import TestDescriptionMapper
from ..entities.test_runner_param_template import TestRunnerParamTemplateMapper
from ..entities.test_inventory_template import TestInventoryTemplateMapper
from ..entities.test_runner import TestRunnerMapper
from ..entities.format import FormatMapper
from ..entities.test_inventory_template_format import TestInventoryTemplateFormatMapper
from ..entities.test_inventory_template_compatible_package import TestInventoryTemplateCompatiblePackageMapper
from ..entities.test_inventory_template_additional_info import TestInventoryTemplateAdditionalInfoMapper
from ..entities.resource_type import ResourceTypeMapper
from ..entities.data_type import DataTypeMapper
from ..gateways.extensions import sql_db
from sqlalchemy import asc
from sqlalchemy.exc import SQLAlchemyError
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


logger = get_logger()


@singleton
class AITManifestService:
    def __init__(self):
        pass

    @log(logger)
    def get(self) -> GetTestRunnerRes:
        # organizer_id, ml_component_idに関わらずすべて取得
        test_runners = TestRunnerMapper.query. \
                        filter(TestRunnerMapper.delete_flag == False). \
                        order_by(asc(TestRunnerMapper.name)).\
                        order_by(asc(TestRunnerMapper.version)).\
                        all()

        return GetTestRunnerRes(
            result=Result(code='A00000', message="get test runners success."),
            test_runners= [t.to_template_dto() for t in test_runners]
        )

    @log(logger)
    def post(self, request) -> PostAITManifestRes:
        # AITHubからAITをインストールする場合
        manifest_json = {}
        create_user_account = ''
        create_user_name = ''
        install_mode = ''

        json_input = {}
        json_type_flag = False
        # requestのContent-Typeがjsonの場合はget_json()で値を取得する
        if "json" in request.headers['Content-Type']:
            json_type_flag = True
            json_input = request.get_json()

        if json_type_flag:
            if json_input is not None and json_input["installAITFromAITHub"]:
                manifest_json = json.loads(json_input["aitManifest"])
                manifest = AITManifestSchema().load(json.loads(json_input["aitManifest"]))

                # フロントエンドからAITHUBの登録ユーザアカウントを設定
                create_user_account = json_input["create_user_account"]
                create_user_name = json_input["create_user_name"]

                # インストールモードに'2'(AITHUB)を設定
                install_mode = '2'
            else:
                raise QAIInvalidRequestException(result_code='A01400', result_msg='uploadFile is required.')

        # ait.manifest.jsonからAITをインストールする場合
        else:
            with TemporaryDirectory() as temp_dir:
                # マニフェストファイル保存
                manifest_file = self._save_manifest(request, Path(temp_dir))

                # マニフェストファイルシリアライズ
                with open(str(manifest_file), encoding='utf-8') as f:
                    manifest_json = json.load(f)
                    manifest = AITManifestSchema().load(manifest_json)

                # aircの登録ユーザアカウントを設定
                create_user_account = SettingMapper.query.get('airc_create_user_account').value
                create_user_name = SettingMapper.query.get('airc_create_user_name').value

                # インストールモードに'1'(プリインストール)を設定
                install_mode = '1'

        # dagファイル保存
        docker_host = SettingMapper.query.get('docker_host_name').value
        dag_template = Path(__file__).parent.joinpath('../../../dag/dag_template.py')
        # dockerイメージ名は小文字のname + 登録ユーザアカウント
        ait_name = manifest.name.lower()
        docker_image_name = ait_name + '-' + create_user_account.lower()
        # ait_dir_name = manifest.name + '_' + manifest.version
        ait_dir_name = docker_image_name + '_' + manifest.version.lower()
        dir_path = Path(__file__).parent.joinpath('../../../dag', ait_dir_name)
        sava_dag_file_path = dir_path.joinpath('dag.py')
        sava_manifest_file_path = dir_path.joinpath('ait.manifest.json')
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
        else:
            shutil.rmtree(str(dir_path))
            dir_path.mkdir(parents=True)
        # self._replace_template(docker_host, manifest.name, manifest.version, dag_template, sava_dag_file_path, 'utf-8')
        self._replace_template(docker_host, docker_image_name, manifest.version.lower(), dag_template, sava_dag_file_path, 'utf-8')
        # マニフェストファイル保存
        # TODO ダミーAITHubからはマニフェストファイルが取得できないので、json.dumpsで作成し直す
        with open(str(sava_manifest_file_path), mode='w', encoding='utf-8', newline="\n") as f:
            f.write(json.dumps(manifest_json, ensure_ascii=False, indent=4))

        # DB登録
        test_runner_id_ = self._add_ait(manifest, create_user_account, create_user_name, install_mode)

        return PostAITManifestRes(
                result=Result(code='A01000', message='Add AIT manifest success'), 
                test_runner_id=test_runner_id_)

    @staticmethod
    def _replace_template(docker_host_name, ait_name, ait_version, in_file, out_file, encoding):
        with open(in_file, encoding=encoding) as f:
            data_lines = f.read()
        data_lines = data_lines.replace('{DOCKER_HOST_NAME}', docker_host_name)
        data_lines = data_lines.replace('{AIT_NAME}', ait_name)
        data_lines = data_lines.replace('{AIT_VERSION}', ait_version)
        with open(out_file, mode='w', encoding=encoding, newline="\r\n") as f:
            f.write(data_lines)

    @staticmethod
    def _save_manifest(request, save_dir_path: Path) -> Path:

        if 'ait.manifest' not in request.files:
            raise QAIInvalidRequestException(result_code='A01400', result_msg='uploadFile is required.')

        file = request.files['ait.manifest']
        filename = file.filename
        if '' == filename:
            raise QAIInvalidRequestException(result_code='A01400', result_msg='filename must not empty.')

        if not filename.endswith('.json'):
            raise QAIInvalidRequestException(result_code='A01400', result_msg='file extension must be json.')

        save_filename = werkzeug.utils.secure_filename(filename)
        save_path = save_dir_path.joinpath(save_filename)
        file.save(str(save_path))

        return save_path

    @staticmethod
    def _add_ait(manifest: AITManifest, create_user_account: str, create_user_name: str, install_mode: str) -> int:

        try:
            # 重複するname、version、Quality、create_user_accountがすでに登録済みの場合、400エラー返却
            already_exist_ait = TestRunnerMapper.query. \
                filter(TestRunnerMapper.name == manifest.name). \
                filter(TestRunnerMapper.version == manifest.version). \
                filter(TestRunnerMapper.quality == manifest.quality). \
                filter(TestRunnerMapper.create_user_account == create_user_account). \
                filter(TestRunnerMapper.delete_flag == False).first()
                
            if already_exist_ait is not None:
                raise QAIBadRequestException('A01400', f'already exist ait = {manifest.name}-{create_user_account}-{manifest.version}-{manifest.quality}')

            # test_runner
            # TODO: ランディングページはAIT登録後に発行されるURLを登録する。本APIは暫定版なので、AIT登録時に''空文字も登録
            test_runner_mapper = TestRunnerMapper(name=manifest.name,
                                                  description=manifest.description,
                                                  source_repository=manifest.source_repository,
                                                  create_user_account=create_user_account,
                                                  create_user_name=create_user_name,
                                                  version=manifest.version,
                                                  quality=manifest.quality,
                                                  keywords=','.join(manifest.keywords),
                                                  licenses=','.join(manifest.licenses),
                                                  landing_page='',
                                                  install_mode=install_mode,
                                                  install_status='OK')
            sql_db.session.add(test_runner_mapper)
            sql_db.session.flush()

            # references
            test_runner_reference_mapper_list = []
            if manifest.references is not None:
                for reference in manifest.references:
                    test_runner_reference_mapper_list.append(
                        TestRunnerReferenceMapper(test_runner_id=test_runner_mapper.id,
                                                  bib_info=reference.bib_info,
                                                  additional_info=reference.additional_info,
                                                  url_=reference.url))
            sql_db.session.add_all(test_runner_reference_mapper_list)

            # downloadable_template
            downloadable_data_mapper_list = []
            for download in manifest.downloads:
                downloadable_data_mapper_list.append(
                    DownloadableTemplateMapper(name=download.name, description=download.description,
                                               test_runner_id=test_runner_mapper.id))
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
                                             test_runner_id=test_runner_mapper.id))
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
                    GraphTemplateMapper(resource_type_id=res_type.id, name=resource.name,
                                        description=resource.description,
                                        test_runner_id=test_runner_mapper.id))
            sql_db.session.add_all(graph_template_mapper_list)

            # test_runner_param_template
            test_runner_param_template_mapper_list = []
            for parameter in manifest.parameters:
                test_runner_param_template_mapper_list.append(
                    TestRunnerParamTemplateMapper(name=parameter.name, value_type=parameter.type,
                                                  description=parameter.description,
                                                  default_value=parameter.default_value,
                                                  min_value=parameter.min_value,
                                                  max_value=parameter.max_value,
                                                  test_runner_id=test_runner_mapper.id,
                                                  depends_on_parameter=parameter.depends_on_parameter))
            sql_db.session.add_all(test_runner_param_template_mapper_list)

            # test_inventory_template
            test_inventory_template_mapper_list = []
            for inventory in manifest.inventories:
                data_type_mapper = DataTypeMapper.query.filter(DataTypeMapper.name == inventory.type).first()
                if data_type_mapper is None:
                    raise QAIBadRequestException('T54001', 'inventory type must be dataset, model or feature')

                test_inventory_template_mapper = TestInventoryTemplateMapper(
                                                   name=inventory.name,
                                                   type_id=data_type_mapper.id,
                                                   description=inventory.description,
                                                   test_runner_id=test_runner_mapper.id,
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

            return test_runner_mapper.id

        except QAIException as e:
            sql_db.session.rollback()
            raise e
        except SQLAlchemyError as e:
            sql_db.session.rollback()
            raise QAIInvalidRequestException('A09999', 'database error: {}'.format(e))

    @log(logger)
    def delete(self, test_runner_id: int) -> Result:
        try:
            # 削除対象のAITが存在するか確認
            target_ait = TestRunnerMapper.query. \
                filter(TestRunnerMapper.id == test_runner_id). \
                filter(TestRunnerMapper.delete_flag == False).first()
            if target_ait is None:
                raise QAINotFoundException('A02901', 'not found AIT')

            # AITがTDで使用されていないことを確認
            already_exist_td = TestDescriptionMapper.query.\
                          filter(TestDescriptionMapper.test_runner_id == test_runner_id).\
                          filter(TestDescriptionMapper.delete_flag == False).first()
            if already_exist_td is not None:
                raise QAINotFoundException('A02400', 'AIT is used in the TestDescription')
            
            # AITのDockerイメージを削除
            docker_host = SettingMapper.query.get('docker_host_name').value
            ait_nm = target_ait.name
            ait_ver = target_ait.version
            ait_acc = target_ait.create_user_account
            client = docker.from_env()
            if target_ait.install_mode == '1':
                tag = f'{docker_host}/{ait_nm}-{ait_acc}:{ait_ver}'
                if 0 < len(client.api.images(name=tag,quiet=True)):
                    client.images.remove(tag)
            elif target_ait.install_mode == '0':
                tag = f'localhost:5050/{ait_nm}-{ait_acc}:{ait_ver}'
                client.images.remove(tag)

            target_ait.delete_flag = True
            sql_db.session.commit()

        except QAIException as e:
            sql_db.session.rollback()
            raise e
        except SQLAlchemyError as e:
            sql_db.session.rollback()
            raise QAIInvalidRequestException('P39000', 'database error: {}'.format(e))
        except Exception as e:
            sql_db.session.rollback()
            raise QAIInternalServerException(result_code='P39999', result_msg='internal server error: {}'.format(e))

        return Result(code='A02000', message='Add AIT manifest success')

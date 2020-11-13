# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from pathlib import Path
import json
from injector import singleton
import werkzeug
from tempfile import TemporaryDirectory

from ..across.exception import QAIException, \
    QAIInvalidRequestException, QAIBadRequestException
from ..across.utils import get_last_url_element
from ..controllers.dto.testrunner import Result
from ..controllers.dto.ait_manifest import AITManifest, AITManifestSchema
from ..entities.downloadable_template import DownloadableTemplateMapper
from ..entities.quality_dimension import QualityDimensionMapper
from ..entities.quality_measurement import QualityMeasurementMapper
from ..entities.structure import StructureMapper
from ..entities.graph_template import GraphTemplateMapper
from ..entities.test_runner_param_template import TestRunnerParamTemplateMapper
from ..entities.test_inventory_template import TestInventoryTemplateMapper
from ..entities.test_runner import TestRunnerMapper
from ..entities.format import FormatMapper
from ..entities.test_inventory_template_format import TestInventoryTemplateFormatMapper
from ..entities.resource_type import ResourceTypeMapper
from  ..entities.data_type import DataTypeMapper
from ..gateways.extensions import sql_db
from sqlalchemy.exc import SQLAlchemyError


@singleton
class AITManifestService:
    def __init__(self):
        pass

    def post(self, request) -> Result:
        with TemporaryDirectory() as temp_dir:
            # マニフェストファイル保存
            manifest_file = self._save_manifest(request, Path(temp_dir))

            # マニフェストファイルシリアライズ
            with open(str(manifest_file), encoding='utf-8') as f:
                manifest_json = json.load(f)
                manifest = AITManifestSchema().load(manifest_json)

            # DB登録
            self._add_ait(manifest)

        return Result(code='M00001', message='Add AIT manifest success')

    @staticmethod
    def _save_manifest(request, save_dir_path: Path) -> Path:

        if 'ait.manifest' not in request.files:
            raise QAIInvalidRequestException(result_code='M10001', result_msg='uploadFile is required.')

        file = request.files['ait.manifest']
        filename = file.filename
        if '' == filename:
            raise QAIInvalidRequestException(result_code='M10001', result_msg='filename must not empty.')

        if not filename.endswith('.json'):
            raise QAIInvalidRequestException(result_code='M10001', result_msg='file extension must be json.')

        save_filename = werkzeug.utils.secure_filename(filename)
        save_path = save_dir_path.joinpath(save_filename)
        file.save(str(save_path))

        return save_path

    @staticmethod
    def _add_ait(manifest: AITManifest):

        try:
            # 重複するname、versionがすでに登録済みの場合、400エラー返却
            already_exist_ait = TestRunnerMapper.query. \
                filter(TestRunnerMapper.name == manifest.name). \
                filter(TestRunnerMapper.version == manifest.version).first()
            if already_exist_ait is not None:
                raise QAIBadRequestException('T54000', f'already exist ait = {manifest.name}-{manifest.version}')

            # test_runner
            # TODO: ランディングページはAIT登録後に発行されるURLを登録する。本APIは暫定版なので、AIT登録時に''空文字も登録
            test_runner_mapper = TestRunnerMapper(name=manifest.name, description=manifest.description,
                                                  author=manifest.author, email=manifest.email,
                                                  version=manifest.version, quality=manifest.quality,
                                                  landing_page='')
            sql_db.session.add(test_runner_mapper)
            sql_db.session.flush()

            # downloadable_template
            downloadable_data_mapper_list = []
            for download in manifest.downloads:
                if not download.path.startswith('/usr/local/qai/'):
                    raise QAIBadRequestException('T54001', 'download path mus start /usr/local/qai/')
                downloadable_data_mapper_list.append(
                    DownloadableTemplateMapper(name=download.name, path=download.path, description=download.description,
                                               test_runner_id=test_runner_mapper.id))
            sql_db.session.add_all(downloadable_data_mapper_list)

            # quality_measurement
            quality_measurement_mapper_list = []

            # quality_dimensionの取得と、存在しなければ追加
            qd_name = get_last_url_element(manifest.quality)
            quality_dim = QualityDimensionMapper.query.filter(QualityDimensionMapper.name == qd_name).first()
            if quality_dim is None:
                quality_dim = QualityDimensionMapper(name=qd_name)
                sql_db.session.add(quality_dim)
                sql_db.session.flush()

            for measure in manifest.report.measures:
                # structure
                structure = StructureMapper.query.filter(StructureMapper.structure == measure.structure).first()
                if structure is None:
                    structure = StructureMapper(structure=measure.structure)
                    sql_db.session.add(structure)
                    sql_db.session.flush()
                # quality_measurement
                quality_measurement_mapper_list.append(
                    QualityMeasurementMapper(name=measure.name, description=measure.description, type=measure.type,
                                             structure_id=structure.id, test_runner_id=test_runner_mapper.id,
                                             quality_dimension_id=quality_dim.id))
            sql_db.session.add_all(quality_measurement_mapper_list)

            # graph_template
            graph_template_mapper_list = []
            for resource in manifest.report.resources:
                if not resource.path.startswith('/usr/local/qai/'):
                    raise QAIBadRequestException('T54001', 'resource path mus start /usr/local/qai/')

                # リソースタイプ取得
                res_type = ResourceTypeMapper.query.filter(ResourceTypeMapper.type == resource.type).first()
                if res_type is None:
                    res_type = ResourceTypeMapper(type=resource.type)
                    sql_db.session.add(res_type)
                    sql_db.session.flush()

                graph_template_mapper_list.append(
                    GraphTemplateMapper(resource_type_id=res_type.id, name=resource.name, path=resource.path,
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
                                                  test_runner_id=test_runner_mapper.id))
            sql_db.session.add_all(test_runner_param_template_mapper_list)

            # test_inventory_template
            test_inventory_template_mapper_list = []
            for inventory in manifest.inventories:
                data_type_mapper = DataTypeMapper.query.filter(DataTypeMapper.name == inventory.type).first()
                if data_type_mapper is None:
                    raise QAIBadRequestException('T54001', 'inventory type must be dataset, model or feature')
                test_inventory_template_mapper = TestInventoryTemplateMapper(name=inventory.name,
                                                                             type_id=data_type_mapper.id,
                                                                             description=inventory.description,
                                                                             schema=inventory.schema,
                                                                             test_runner_id=test_runner_mapper.id)
                sql_db.session.add(test_inventory_template_mapper)
                sql_db.session.flush()

                # format
                for format_ in inventory.format:
                    format_mapper = FormatMapper.query.filter(FormatMapper.format_ == format_).first()
                    if format_mapper is None:
                        # 拡張子からリソースタイプを自動判断することは難しいため、（あらかじめ初期値で登録）
                        # binaryタイプで登録する
                        binary_type = ResourceTypeMapper.query.filter(ResourceTypeMapper.type == 'binary').first()
                        format_mapper = FormatMapper(format_=format_, resource_type_id=binary_type.id)
                        sql_db.session.add(format_mapper)
                        sql_db.session.flush()
                    test_inventory_template_mapper_list.append(
                        TestInventoryTemplateFormatMapper(inventory_template_id=test_inventory_template_mapper.id_,
                                                          format_id=format_mapper.id))
            sql_db.session.add_all(test_inventory_template_mapper_list)

            # FIXME test_runner_reference

            sql_db.session.commit()
        except QAIException as e:
            sql_db.session.rollback()
            raise e
        except SQLAlchemyError as e:
            sql_db.session.rollback()
            raise QAIInvalidRequestException('T59000', 'database error: {}'.format(e))

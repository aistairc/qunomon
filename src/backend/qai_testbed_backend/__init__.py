# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import flask
from itertools import chain
from flask_injector import FlaskInjector
from pathlib import Path
import shutil
import os

from .entities.organization import OrganizationMapper
from .entities.ml_component import MLComponentMapper
from .entities.relational_operator import RelationalOperatorMapper
from .entities.test import TestMapper
from .entities.test_description import TestDescriptionMapper
from .entities.quality_dimension import QualityDimensionMapper
from .entities.inventory import InventoryMapper
from .entities.inventory_td import InventoryTDMapper
from .entities.quality_measurement import QualityMeasurementMapper
from .entities.operand import OperandMapper
from .entities.test_runner import TestRunnerMapper
from .entities.test_runner_param import TestRunnerParamMapper
from .entities.test_runner_param_template import TestRunnerParamTemplateMapper
from .entities.test_inventory_template import TestInventoryTemplateMapper
from .entities.test_inventory_template_tag import TestInventoryTemplateTagMapper
from .entities.graph_template import GraphTemplateMapper
from .entities.graph import GraphMapper
from .entities.job import JobMapper
from .entities.run import RunMapper
from .entities.setting import SettingMapper
from .entities.dowmload import DownloadMapper
from .entities.tag import TagMapper
from .entities.downloadable_data import DownloadableDataMapper
from .entities.downloadable_template import DownloadableTemplateMapper
from .entities.test_runner_reference import TestRunnerReferenceMapper
from .entities.structure import StructureMapper
from .entities.test_inventory_template_format import TestInventoryTemplateFormatMapper
from .entities.inventory_format import InventoryFormatMapper
from .entities.format import FormatMapper
from .entities.resource_type import ResourceTypeMapper
from .entities.ml_framework import MLFrameworkMapper
from .entities.data_type import DataTypeMapper
from .entities.file_system import FileSystemMapper
from .controllers import api
from .gateways import extensions, config
from .gateways.auth import jwt
from .di_module import di_module


def create_app(config_name='default', is_init_db: bool = True):
    """Flask app factory
    :config_name: a string object.
    :returns: flask.Flask object
    """

    app = flask.Flask(__name__)

    # set the config vars using the config name and current_app
    config.config[config_name](app)

    jwt.set_jwt_handlers(extensions.jwt)

    register_extensions(app)
    register_blueprints(app)

    if is_init_db:
        init_db(app, config_name=config_name)

    FlaskInjector(app=app, modules=[di_module])

    return app


def register_extensions(app):
    """Call the method 'init_app' to register the extensions in the flask.Flask
    object passed as parameter.
    :app: flask.Flask object
    :returns: None
    """
    extensions.nosql_db.init_app(app)
    extensions.jwt.init_app(app)
    extensions.sql_db.init_app(app)
    extensions.ma.init_app(app)


def register_blueprints(app):
    """Register all blueprints.
    :app: flask.Flask object
    :returns: None
    """
    app.register_blueprint(api.blueprint)


def init_db(app, config_name):
    with app.app_context():
        extensions.sql_db.drop_all()
        extensions.sql_db.create_all()

        _init_db_common(config_name)

        _init_db_demo_2()

        extensions.sql_db.session.commit()


def _init_db_common(config_name):
    """共通のDBレコード"""

    db_common = config.db_common[config_name]
    settings = []
    for k, v in db_common.items():
        settings.append(SettingMapper(key=k, value=v))
    extensions.sql_db.session.add_all(settings)
    extensions.sql_db.session.flush()

    quality_props = [QualityDimensionMapper(name='Completeness_of_problem_domain_analysis'),
                     QualityDimensionMapper(name='Coverage_for_distinguished_problem_cases'),
                     QualityDimensionMapper(name='Diversity_of_test_data'),
                     QualityDimensionMapper(name='Distribution_of_training_data'),
                     QualityDimensionMapper(name='Accuracy_of_trained_model'),
                     QualityDimensionMapper(name='Robustness_of_trained_model'),
                     QualityDimensionMapper(name='Stability_Maintainability_of_quality'),
                     QualityDimensionMapper(name='Dependability_of_underlying_software')]
    extensions.sql_db.session.add_all(quality_props)
    extensions.sql_db.session.flush()

    relational_operator = [RelationalOperatorMapper(expression='==', description='値が等しければTrue'),
                           RelationalOperatorMapper(expression='!=', description='値が等しくなければTrue'),
                           RelationalOperatorMapper(expression='>', description='値が大きければTrue'),
                           RelationalOperatorMapper(expression='<', description='値が小さければTrue'),
                           RelationalOperatorMapper(expression='>=', description='値が同じか大きければTrue'),
                           RelationalOperatorMapper(expression='<=', description='値が同じか小さければTrue')]
    extensions.sql_db.session.add_all(relational_operator)
    extensions.sql_db.session.flush()

    resource_type = [ResourceTypeMapper(type='text'),
                     ResourceTypeMapper(type='picture'),
                     ResourceTypeMapper(type='table'),
                     ResourceTypeMapper(type='binary')]
    extensions.sql_db.session.add_all(resource_type)
    extensions.sql_db.session.flush()

    format_ = [FormatMapper(format_='png', resource_type_id=resource_type[1].id),
               FormatMapper(format_='jpg', resource_type_id=resource_type[1].id),
               FormatMapper(format_='jpeg', resource_type_id=resource_type[1].id),
               FormatMapper(format_='jpe', resource_type_id=resource_type[1].id),
               FormatMapper(format_='tif', resource_type_id=resource_type[1].id),
               FormatMapper(format_='tiff', resource_type_id=resource_type[1].id),
               FormatMapper(format_='bmp', resource_type_id=resource_type[1].id),
               FormatMapper(format_='csv', resource_type_id=resource_type[2].id),
               FormatMapper(format_='tsv', resource_type_id=resource_type[2].id),
               FormatMapper(format_='onnx', resource_type_id=resource_type[3].id),
               FormatMapper(format_='txt', resource_type_id=resource_type[0].id),
               FormatMapper(format_='text', resource_type_id=resource_type[0].id),
               FormatMapper(format_='json', resource_type_id=resource_type[0].id),
               FormatMapper(format_='xml', resource_type_id=resource_type[0].id),
               FormatMapper(format_='md', resource_type_id=resource_type[0].id),
               FormatMapper(format_='h5', resource_type_id=resource_type[3].id),
               FormatMapper(format_='zip', resource_type_id=resource_type[3].id),
               FormatMapper(format_='gz', resource_type_id=resource_type[3].id),
               FormatMapper(format_='7z', resource_type_id=resource_type[3].id),
               FormatMapper(format_='dump', resource_type_id=resource_type[3].id),
               FormatMapper(format_='dmp', resource_type_id=resource_type[3].id),
               FormatMapper(format_='bin', resource_type_id=resource_type[3].id),
               FormatMapper(format_='dat', resource_type_id=resource_type[3].id),
               FormatMapper(format_='data', resource_type_id=resource_type[3].id),
               FormatMapper(format_='*', resource_type_id=resource_type[3].id)]
    extensions.sql_db.session.add_all(format_)
    extensions.sql_db.session.flush()

    data_types = [DataTypeMapper(name='dataset'),
                  DataTypeMapper(name='model'),
                  DataTypeMapper(name='attribute set')]
    extensions.sql_db.session.add_all(data_types)
    extensions.sql_db.session.flush()

    file_systems = [FileSystemMapper(name='UNIX_FILE_SYSTEM'),
                    FileSystemMapper(name='WINDOWS_FILE')]
    extensions.sql_db.session.add_all(file_systems)
    extensions.sql_db.session.flush()

    ml_frameworks = [MLFrameworkMapper(name='Tensorflow-2.3')]
    extensions.sql_db.session.add_all(ml_frameworks)
    extensions.sql_db.session.flush()


def _init_db_demo_1():
    """デモ用（最初期）"""

    quality_props = QualityDimensionMapper.query.all()
    relational_operator = RelationalOperatorMapper.query.all()

    meas = [QualityMeasurementMapper(name='Coverage of activated neurons',
                                     version='0.1',
                                     description='学習モデルの安定性評価指標',
                                     quality_dimension_id=quality_props[5].id),
            QualityMeasurementMapper(name='モデル精度計測',
                                     version='0.1',
                                     description='学習モデルの正確性評価指標',
                                     quality_dimension_id=quality_props[4].id)]
    extensions.sql_db.session.add_all(meas)
    extensions.sql_db.session.flush()

    test_runners = [
        TestRunnerMapper(name='neuron_coverage_v3.py', dag_name='eval_coverage_3.0'),
        TestRunnerMapper(name='neuron_coverage_v6.py', dag_name='eval_coverage_6.0')
    ]
    extensions.sql_db.session.add_all(test_runners)
    extensions.sql_db.session.flush()

    test_runner_param_templates = [
        TestRunnerParamTemplateMapper(name='Threshold', value_type='float', test_runner_id=test_runners[0].id),
        TestRunnerParamTemplateMapper(name='Lower Limit', value_type='float', test_runner_id=test_runners[0].id),
        TestRunnerParamTemplateMapper(name='Upper Limit', value_type='float', test_runner_id=test_runners[0].id)]
    extensions.sql_db.session.add_all(test_runner_param_templates)
    extensions.sql_db.session.flush()

    graph_templates = [GraphTemplateMapper(type="picture", test_runner_id=test_runners[0].id),
                       GraphTemplateMapper(type="picture", test_runner_id=test_runners[0].id),
                       GraphTemplateMapper(type="picture", test_runner_id=test_runners[0].id),
                       GraphTemplateMapper(type="picture", test_runner_id=test_runners[2].id),
                       GraphTemplateMapper(type="picture", test_runner_id=test_runners[2].id),
                       GraphTemplateMapper(type="picture", test_runner_id=test_runners[2].id),
                       GraphTemplateMapper(type="picture", test_runner_id=test_runners[2].id)]
    extensions.sql_db.session.add_all(graph_templates)
    extensions.sql_db.session.flush()

    orgs = [OrganizationMapper(id='dep-a', name='部署A'),
            OrganizationMapper(id='dep-b', name='部署B'),
            OrganizationMapper(id='dep-c', name='部署C')]
    extensions.sql_db.session.add_all(orgs)
    extensions.sql_db.session.flush()

    projs = [MLComponentMapper(name='A社住宅価格予測システム', org_id=orgs[0].id),
             MLComponentMapper(name='B社文字認識システム', org_id=orgs[0].id),
             MLComponentMapper(name='C社ゴルフスコア読み取りシステム', org_id=orgs[0].id)]
    extensions.sql_db.session.add_all(projs)
    extensions.sql_db.session.flush()

    tags = [TagMapper(name='CSV', type='INVENTORY'),
            TagMapper(name='TF_MODEL', type='INVENTORY'),
            TagMapper(name='ZIP', type='INVENTORY')]
    extensions.sql_db.session.add_all(tags)
    extensions.sql_db.session.flush()

    test_inventory_templates = [
        TestInventoryTemplateMapper(name='TestDataSet', test_runner_id=test_runners[0].id),
        TestInventoryTemplateMapper(name='TrainedModel', test_runner_id=test_runners[0].id),
        TestInventoryTemplateMapper(name='TestMetaDataSet', test_runner_id=test_runners[1].id),
        TestInventoryTemplateMapper(name='TestDataSet', test_runner_id=test_runners[1].id),
        TestInventoryTemplateMapper(name='TrainedModel', test_runner_id=test_runners[1].id),
        TestInventoryTemplateMapper(name='TrainedModel', test_runner_id=test_runners[2].id)]
    extensions.sql_db.session.add_all(test_inventory_templates)
    extensions.sql_db.session.flush()

    test_inventory_templates_tag = [
        TestInventoryTemplateTagMapper(inventory_template_id=test_inventory_templates[0].id_, tag_id=tags[0].id),
        TestInventoryTemplateTagMapper(inventory_template_id=test_inventory_templates[1].id_, tag_id=tags[1].id),
        TestInventoryTemplateTagMapper(inventory_template_id=test_inventory_templates[2].id_, tag_id=tags[0].id),
        TestInventoryTemplateTagMapper(inventory_template_id=test_inventory_templates[3].id_, tag_id=tags[2].id),
        TestInventoryTemplateTagMapper(inventory_template_id=test_inventory_templates[4].id_, tag_id=tags[1].id),
        TestInventoryTemplateTagMapper(inventory_template_id=test_inventory_templates[5].id_, tag_id=tags[1].id)]
    extensions.sql_db.session.add_all(test_inventory_templates_tag)
    extensions.sql_db.session.flush()

    invs = [InventoryMapper(name='TestDataset_0818',
                            type='UNIX_FILE_SYSTEM',
                            address='/mnt/xxx/1',
                            description='0818用のデータセット',
                            delete_flag=False,
                            ml_component_id=projs[0].id),
            InventoryMapper(name='TestDataset_0918',
                            type='UNIX_FILE_SYSTEM',
                            address='/mnt/xxx/2',
                            description='0918用のデータセット',
                            delete_flag=False,
                            ml_component_id=projs[0].id),
            InventoryMapper(name='TrainedModel_0907',
                            type='UNIX_FILE_SYSTEM',
                            address='/mnt/xxx/3',
                            description='0907用のモデル',
                            delete_flag=False,
                            ml_component_id=projs[0].id),
            InventoryMapper(name='TestDataset_1018',
                            type='UNIX_FILE_SYSTEM',
                            address='/mnt/xxx/4',
                            description='1018用のデータセット',
                            delete_flag=False,
                            ml_component_id=projs[0].id),
            InventoryMapper(name='TrainedModel_1007',
                            type='UNIX_FILE_SYSTEM',
                            address='/mnt/xxx/5',
                            description='1007用のモデル',
                            delete_flag=False,
                            ml_component_id=projs[0].id)]
    extensions.sql_db.session.add_all(invs)
    extensions.sql_db.session.flush()

    tests = [TestMapper(ml_component_id=projs[0].id)]
    extensions.sql_db.session.add_all(tests)
    extensions.sql_db.session.flush()

    test_descriptions = [TestDescriptionMapper(name='NeuronCoverage',
                                               test_id=tests[0].id, opinion='見解',
                                               delete_flag=False,
                                               value_target=True,
                                               quality_dimension_id=quality_props[4].id,
                                               quality_measurement_id=meas[0].id,
                                               test_runner_id=test_runners[0].id),
                         TestDescriptionMapper(name='MetamorphicTesting',
                                               test_id=tests[0].id, opinion='見解',
                                               delete_flag=False,
                                               value_target=True,
                                               quality_dimension_id=quality_props[4].id,
                                               quality_measurement_id=meas[1].id,
                                               test_runner_id=test_runners[0].id),
                         TestDescriptionMapper(name='AttributeCoverage',
                                               test_id=tests[0].id, opinion='見解',
                                               delete_flag=False,
                                               value_target=True,
                                               quality_dimension_id=quality_props[4].id,
                                               quality_measurement_id=meas[1].id,
                                               test_runner_id=test_runners[0].id),
                         TestDescriptionMapper(name='AttributeCoverage2',
                                               test_id=tests[0].id, opinion='見解',
                                               delete_flag=False,
                                               value_target=True,
                                               quality_dimension_id=quality_props[4].id,
                                               quality_measurement_id=meas[1].id,
                                               test_runner_id=test_runners[0].id),
                         TestDescriptionMapper(name='AttributeCoverage3',
                                               test_id=tests[0].id, opinion='見解',
                                               delete_flag=False,
                                               value_target=True,
                                               quality_dimension_id=quality_props[4].id,
                                               quality_measurement_id=meas[1].id,
                                               test_runner_id=test_runners[0].id),
                         TestDescriptionMapper(name='AttributeCoverage4',
                                               test_id=tests[0].id, opinion='見解',
                                               delete_flag=False,
                                               value_target=True,
                                               quality_dimension_id=quality_props[4].id,
                                               quality_measurement_id=meas[1].id,
                                               test_runner_id=test_runners[0].id)
                         ]
    extensions.sql_db.session.add_all(test_descriptions)
    extensions.sql_db.session.flush()
    test_descriptions[3].parent_id = test_descriptions[2].id
    test_descriptions[4].parent_id = test_descriptions[3].id
    test_descriptions[5].parent_id = test_descriptions[4].id

    inv_tds = [InventoryTDMapper(inventory_id=invs[3].id,
                                 test_description_id=test_descriptions[0].id,
                                 template_inventory_id=test_inventory_templates[0].id_),
               InventoryTDMapper(inventory_id=invs[4].id,
                                 test_description_id=test_descriptions[0].id,
                                 template_inventory_id=test_inventory_templates[1].id_),
               InventoryTDMapper(inventory_id=invs[0].id,
                                 test_description_id=test_descriptions[1].id,
                                 template_inventory_id=test_inventory_templates[0].id_),
               InventoryTDMapper(inventory_id=invs[4].id,
                                 test_description_id=test_descriptions[2].id,
                                 template_inventory_id=test_inventory_templates[1].id_),
               InventoryTDMapper(inventory_id=invs[2].id,
                                 test_description_id=test_descriptions[3].id,
                                 template_inventory_id=test_inventory_templates[0].id_),
               InventoryTDMapper(inventory_id=invs[3].id,
                                 test_description_id=test_descriptions[4].id,
                                 template_inventory_id=test_inventory_templates[1].id_),
               InventoryTDMapper(inventory_id=invs[4].id,
                                 test_description_id=test_descriptions[5].id,
                                 template_inventory_id=test_inventory_templates[0].id_),
               InventoryTDMapper(inventory_id=invs[0].id,
                                 test_description_id=test_descriptions[5].id,
                                 template_inventory_id=test_inventory_templates[1].id_)]
    extensions.sql_db.session.add_all(inv_tds)
    extensions.sql_db.session.flush()

    operands = [OperandMapper(value=80, enable=True,
                              quality_measurement_id=meas[0].id, test_description_id=test_descriptions[0].id,
                              relational_operator_id=relational_operator[2].id),
                OperandMapper(value=81, enable=True,
                              quality_measurement_id=meas[1].id, test_description_id=test_descriptions[1].id,
                              relational_operator_id=relational_operator[3].id),
                OperandMapper(value=82, enable=True,
                              quality_measurement_id=meas[1].id, test_description_id=test_descriptions[2].id,
                              relational_operator_id=relational_operator[4].id),
                OperandMapper(value=83, enable=True,
                              quality_measurement_id=meas[1].id, test_description_id=test_descriptions[3].id,
                              relational_operator_id=relational_operator[5].id),
                OperandMapper(value=84, enable=True,
                              quality_measurement_id=meas[1].id, test_description_id=test_descriptions[4].id,
                              relational_operator_id=relational_operator[0].id),
                OperandMapper(value=85, enable=True,
                              quality_measurement_id=meas[1].id, test_description_id=test_descriptions[5].id,
                              relational_operator_id=relational_operator[1].id)]
    extensions.sql_db.session.add_all(operands)
    extensions.sql_db.session.flush()

    test_runner_params = list(chain.from_iterable([
        [TestRunnerParamMapper(value='0.5',
                               test_runner_param_template_id=test_runner_param_templates[0].id,
                               test_description_id=td.id),
         TestRunnerParamMapper(value='0.3',
                               test_runner_param_template_id=test_runner_param_templates[1].id,
                               test_description_id=td.id),
         TestRunnerParamMapper(value='1.0',
                               test_runner_param_template_id=test_runner_param_templates[2].id,
                               test_description_id=td.id)
         ] for td in test_descriptions]))
    extensions.sql_db.session.add_all(test_runner_params)
    extensions.sql_db.session.flush()

    jobs = [JobMapper(status='DONE', result='SUCCESS', result_detail='OK:2 NG:0 ERR:0 NA:0', test_id=tests[0].id)]
    extensions.sql_db.session.add_all(jobs)
    extensions.sql_db.session.flush()

    runs = [RunMapper(status='DONE',
                      result='SUCCESS', detail_result='SUCCESS',
                      job_id=jobs[0].id, test_description_id=test_descriptions[0].id),
            RunMapper(status='DONE',
                      result='SUCCESS', detail_result='SUCCESS',
                      job_id=jobs[0].id, test_description_id=test_descriptions[1].id)
            ]
    extensions.sql_db.session.add_all(runs)
    extensions.sql_db.session.flush()

    downloads = [DownloadMapper(path='C:\\Windows\\System32\\nvidia-smi.1.pdf')]
    extensions.sql_db.session.add_all(downloads)
    extensions.sql_db.session.flush()

    graphs = list(chain.from_iterable([
        [GraphMapper(report_required='TRUE', graph_address='http://XXX',
                     report_index=1, report_name=graph_templates[0].name,
                     graph_template_id=graph_templates[0].id, run_id=r.id, download_id=downloads[0].id),
         GraphMapper(report_required='TRUE', graph_address='http://YYY',
                     report_index=2, report_name=graph_templates[1].name,
                     graph_template_id=graph_templates[1].id, run_id=r.id, download_id=downloads[0].id),
         GraphMapper(report_required='TRUE', graph_address='http://ZZZ',
                     report_index=2, report_name=graph_templates[2].name,
                     graph_template_id=graph_templates[2].id, run_id=r.id, download_id=downloads[0].id),
         ] for r in runs]))
    extensions.sql_db.session.add_all(graphs)
    extensions.sql_db.session.flush()


def _init_db_demo_2():
    """デモ用（レポート機能）"""
    relational_operator = RelationalOperatorMapper.query.all()
    structures = [StructureMapper(structure='single')]
    extensions.sql_db.session.add_all(structures)
    extensions.sql_db.session.flush()

    quality_props = QualityDimensionMapper.query.all()

    test_runners = [
        TestRunnerMapper(name='acc_check_1.0.py', description='eval_acc_check_by_tfmodel_1.0', author='John Smith',
                         email='John_Smith@aaa.com', version='1',
                         quality='https://airc.aist.go.jp/aiqm/quality/internal/Accuracy_of_trained_model',
                         landing_page='https://aithub.com/acc_check/1.0'),
        TestRunnerMapper(name='adversarial_example_acc_test_1.0.py',
                         description='eval_adversarial_example_acc_test_by_tfmodel_1.0',
                         author='John Smith', email='John_Smith@aaa.com', version='1',
                         quality='https://airc.aist.go.jp/aiqm/quality/internal/Robustness_of_trained_model',
                         landing_page='https://aithub.com/adversarial_example_acc_test/1.0'),
        TestRunnerMapper(name='dev_hello_world',
                         description='dev_hello_world_0.1', author='John Smith', email='John_Smith@aaa.com',
                         version='0.1',
                         quality='https://airc.aist.go.jp/aiqm/quality/internal/Robustness_of_trained_model',
                         landing_page='https://aithub.com/dev_hello_world/')
    ]
    extensions.sql_db.session.add_all(test_runners)
    extensions.sql_db.session.flush()

    meas = [QualityMeasurementMapper(name='学習モデルの精度計測',
                                     description='学習モデルの正確性評価指標',
                                     quality_dimension_id=quality_props[4].id,
                                     type='float',
                                     structure_id=structures[0].id,
                                     test_runner_id=test_runners[0].id),
            QualityMeasurementMapper(name='学習モデルの敵対的サンプル安定性計測',
                                     description='学習モデルの安定性評価指標',
                                     quality_dimension_id=quality_props[5].id,
                                     type='float',
                                     structure_id=structures[0].id,
                                     test_runner_id=test_runners[1].id),
            QualityMeasurementMapper(name='学習モデルの敵対的サンプル安定性計測2',
                                     description='学習モデルの安定性評価指標',
                                     quality_dimension_id=quality_props[5].id,
                                     type='float',
                                     structure_id=structures[0].id,
                                     test_runner_id=test_runners[2].id)]
    extensions.sql_db.session.add_all(meas)
    extensions.sql_db.session.flush()

    test_runner_param_templates = [
        TestRunnerParamTemplateMapper(name='Threshold', value_type='float',
                                      description='敵対的生成のずらし具合, \\epsilon \\in \\{0.0, 1.0\\',
                                      default_value='0.5', test_runner_id=test_runners[0].id),
        TestRunnerParamTemplateMapper(name='Lower Limit', value_type='float',
                                      description='敵対的生成のずらし具合, \\epsilon \\in \\{0.0, 1.0\\',
                                      default_value='0.3', test_runner_id=test_runners[0].id),
        TestRunnerParamTemplateMapper(name='Upper Limit', value_type='float',
                                      description='敵対的生成のずらし具合, \\epsilon \\in \\{0.0, 1.0\\',
                                      default_value='1.0', test_runner_id=test_runners[0].id),
        TestRunnerParamTemplateMapper(name='select', value_type='string', description='select',
                                      default_value='', test_runner_id=test_runners[1].id),
        TestRunnerParamTemplateMapper(name='nb_examples', value_type='int', description='単純ベイズ分類器',
                                      default_value='', test_runner_id=test_runners[1].id),
        TestRunnerParamTemplateMapper(name='balance_sampling', value_type='string',
                                      description='母集団からユニットをランダムに選択する方法',
                                      default_value='', test_runner_id=test_runners[1].id),
        TestRunnerParamTemplateMapper(name='test_mode', value_type='string', description='test_mode',
                                      default_value='', test_runner_id=test_runners[1].id),
        TestRunnerParamTemplateMapper(name='attacks', value_type='string', description='attacks',
                                      default_value='', test_runner_id=test_runners[1].id),
        TestRunnerParamTemplateMapper(name='robustness', value_type='string',
                                      description='ニューラルネットワークのトレーニング、評価、探索',
                                      default_value='', test_runner_id=test_runners[1].id),
        TestRunnerParamTemplateMapper(name='detection', value_type='string', description='detection',
                                      default_value='', test_runner_id=test_runners[1].id),
        TestRunnerParamTemplateMapper(name='Name', value_type='string', description='Name',
                                      default_value='', test_runner_id=test_runners[2].id)]
    extensions.sql_db.session.add_all(test_runner_param_templates)
    extensions.sql_db.session.flush()

    resource_type = ResourceTypeMapper.query.all()

    graph_templates = [GraphTemplateMapper(resource_type_id=resource_type[1].id, name='log.png',
                                           description='one image',
                                           test_runner_id=test_runners[0].id),
                       GraphTemplateMapper(resource_type_id=resource_type[1].id, name='log.png',
                                           description='one image',
                                           test_runner_id=test_runners[0].id),
                       GraphTemplateMapper(resource_type_id=resource_type[2].id, name='distribution_graph',
                                           description='image', test_runner_id=test_runners[0].id),
                       GraphTemplateMapper(resource_type_id=resource_type[2].id, name='acc.csv',
                                           description='acc csv',
                                           test_runner_id=test_runners[2].id),
                       GraphTemplateMapper(resource_type_id=resource_type[1].id, name='acc.png',
                                           description='acc image',
                                           test_runner_id=test_runners[2].id),
                       GraphTemplateMapper(resource_type_id=resource_type[1].id, name='images.png',
                                           description='image',
                                           test_runner_id=test_runners[2].id),
                       GraphTemplateMapper(resource_type_id=resource_type[2].id, name='Incorrect_data.csv',
                                           description='incorrect data csv', test_runner_id=test_runners[2].id)]
    extensions.sql_db.session.add_all(graph_templates)
    extensions.sql_db.session.flush()

    downloadable_data = [DownloadableTemplateMapper(name="log.txt", description='log data',
                                                    test_runner_id=test_runners[0].id),
                         DownloadableTemplateMapper(name="log.txt", description='log data',
                                                    test_runner_id=test_runners[1].id),
                         DownloadableTemplateMapper(name="log.txt", description='log data',
                                                    test_runner_id=test_runners[2].id),
                         DownloadableTemplateMapper(name="adversarial_samples", description='log data',
                                                    test_runner_id=test_runners[2].id),
                         DownloadableTemplateMapper(name="adversarial_samples", description='log data',
                                                    test_runner_id=test_runners[2].id)]
    extensions.sql_db.session.add_all(downloadable_data)
    extensions.sql_db.session.flush()

    orgs = [OrganizationMapper(id='dep-a', name='部署A'),
            OrganizationMapper(id='dep-b', name='部署B'),
            OrganizationMapper(id='dep-c', name='部署C')]
    extensions.sql_db.session.add_all(orgs)
    extensions.sql_db.session.flush()

    ml_frameworks = MLFrameworkMapper.query.all()
    ml_components = [MLComponentMapper(name='A社住宅価格予測-機械学習コンポーネント', org_id=orgs[0].id,
                                       description='A社の住宅価格を予測する機械学習コンポーネント',
                                       problem_domain='重回帰分析',
                                       ml_framework_id=ml_frameworks[0].id),
                     MLComponentMapper(name='B社文字認識-機械学習コンポーネント', org_id=orgs[0].id,
                                       description='B社の文字を認識する機械学習コンポーネント',
                                       problem_domain='画像分類',
                                       ml_framework_id=ml_frameworks[0].id),
                     MLComponentMapper(name='C社ゴルフスコア読取-機械学習コンポーネント', org_id=orgs[0].id,
                                       description='C社のスコア表枠組み、文字を認識する機械学習コンポーネント',
                                       problem_domain='レイアウト認識、画像分類',
                                       ml_framework_id=ml_frameworks[0].id)]
    extensions.sql_db.session.add_all(ml_components)
    extensions.sql_db.session.flush()

    tags = [TagMapper(name='CSV', type='INVENTORY'),
            TagMapper(name='TF_MODEL', type='INVENTORY'),
            TagMapper(name='ZIP', type='INVENTORY')]
    extensions.sql_db.session.add_all(tags)
    extensions.sql_db.session.flush()

    data_types = DataTypeMapper.query.all()
    file_systems = FileSystemMapper.query.all()
    test_inventory_templates = [
        TestInventoryTemplateMapper(name='TestDataSet', type_id=data_types[0].id, description='28x28のpng',
                                    schema='http://yann.lecun.com/exdb/mnist/',
                                    test_runner_id=test_runners[0].id),
        TestInventoryTemplateMapper(name='TrainedModel', type_id=data_types[1].id, description='ONNXファイル',
                                    schema='https://onnx.ai/about.html',
                                    test_runner_id=test_runners[0].id),
        TestInventoryTemplateMapper(name='TestMetaDataSet', type_id=data_types[0].id, description='jpg, jpeg',
                                    schema='http://yann.lecun.com/exdb/mnist/',
                                    test_runner_id=test_runners[1].id),
        TestInventoryTemplateMapper(name='TestDataSet', type_id=data_types[0].id, description='csv, tsv',
                                    schema='http://yann.lecun.com/exdb/mnist/',
                                    test_runner_id=test_runners[1].id),
        TestInventoryTemplateMapper(name='TrainedModel', type_id=data_types[1].id, description='ONNXファイル',
                                    schema='https://onnx.ai/about.html',
                                    test_runner_id=test_runners[1].id),
        TestInventoryTemplateMapper(name='TrainedModel', type_id=data_types[1].id, description='ONNXファイル',
                                    schema='https://onnx.ai/about.html',
                                    test_runner_id=test_runners[2].id)]
    extensions.sql_db.session.add_all(test_inventory_templates)
    extensions.sql_db.session.flush()

    test_inventory_templates_tag = [
        TestInventoryTemplateTagMapper(inventory_template_id=test_inventory_templates[0].id_, tag_id=tags[0].id),
        TestInventoryTemplateTagMapper(inventory_template_id=test_inventory_templates[1].id_, tag_id=tags[1].id),
        TestInventoryTemplateTagMapper(inventory_template_id=test_inventory_templates[2].id_, tag_id=tags[0].id),
        TestInventoryTemplateTagMapper(inventory_template_id=test_inventory_templates[3].id_, tag_id=tags[2].id),
        TestInventoryTemplateTagMapper(inventory_template_id=test_inventory_templates[4].id_, tag_id=tags[1].id),
        TestInventoryTemplateTagMapper(inventory_template_id=test_inventory_templates[5].id_, tag_id=tags[1].id)]
    extensions.sql_db.session.add_all(test_inventory_templates_tag)
    extensions.sql_db.session.flush()

    invs = [InventoryMapper(name='TestDataset_0818',
                            type_id=data_types[0].id,
                            file_system_id=file_systems[0].id,
                            file_path=str(Path(SettingMapper.query.get('mount_dst_path').value)
                                        / 'ip' / 'dummyInventory' / 'test.csv'),
                            description='0818用のデータセット',
                            delete_flag=False,
                            ml_component_id=ml_components[0].id,
                            schema='http://yann.lecun.com/exdb/mnist/'),
            InventoryMapper(name='TrainedModel_0907',
                            type_id=data_types[1].id,
                            file_system_id=file_systems[0].id,
                            file_path=str(Path(SettingMapper.query.get('mount_dst_path').value)
                                        / 'ip' / 'dummyInventory' / 'test.csv'),
                            description='0918用のデータセット',
                            delete_flag=False,
                            ml_component_id=ml_components[0].id,
                            schema='http://yann.lecun.com/exdb/mnist/'),
            InventoryMapper(name='TestDataset_0918',
                            type_id=data_types[0].id,
                            file_system_id=file_systems[0].id,
                            file_path=str(Path(SettingMapper.query.get('mount_dst_path').value)
                                        / 'ip' / 'dummyInventory' / 'test.csv'),
                            description='0907用のモデル',
                            delete_flag=False,
                            ml_component_id=ml_components[0].id,
                            schema='https://support.hdfgroup.org/HDF5/doc/index.html'),
            InventoryMapper(name='TestDataset_1002',
                            type_id=data_types[0].id,
                            file_system_id=file_systems[0].id,
                            file_path=str(Path(SettingMapper.query.get('mount_dst_path').value)
                                        / 'ip' / 'dummyInventory' / 'test.csv'),
                            description='1007用のモデル',
                            delete_flag=False,
                            ml_component_id=ml_components[0].id,
                            schema='https://support.hdfgroup.org/HDF5/doc/index.html'),
            InventoryMapper(name='DUMMY1_ONNX',
                            type_id=data_types[1].id,
                            file_system_id=file_systems[1].id,
                            file_path=str(Path(SettingMapper.query.get('mount_dst_path').value)
                                        / 'ip' / 'dummyInventory' / 'test.csv'),
                            description='開発用ダミーデータ',
                            delete_flag=False,
                            ml_component_id=ml_components[0].id,
                            schema='http://www.kasai.fm/wiki/rfc4180jp'),
            InventoryMapper(name='DUMMY2_ONNX',
                            type_id=data_types[1].id,
                            file_system_id=file_systems[1].id,
                            file_path=str(Path(SettingMapper.query.get('mount_dst_path').value)
                                        / 'ip' / 'dummyInventory' / 'test.csv'),
                            description='開発用ダミーデータ',
                            delete_flag=False,
                            ml_component_id=ml_components[0].id,
                            schema='http://www.kasai.fm/wiki/rfc4180jp')]
    extensions.sql_db.session.add_all(invs)
    extensions.sql_db.session.flush()

    # dummy data create
    # windowsとLinuxでダミーデータ格納先を変更する
    if os.name == 'nt':
        dummy_file_path = Path(SettingMapper.query.get('mount_src_path').value) / 'ip' / 'dummyInventory' / 'test.csv'
    else:
        dummy_file_path = Path(SettingMapper.query.get('mount_dst_path').value) / 'ip' / 'dummyInventory' / 'test.csv'

    dummy_dir = dummy_file_path.parent
    if dummy_dir.exists():
        shutil.rmtree(str(dummy_dir))
    dummy_dir.mkdir(parents=True)
    with open(str(dummy_file_path), mode='w') as f:
        f.write('dummy_inventory,hello_world')

    tests = [TestMapper(ml_component_id=ml_components[0].id),
             TestMapper(ml_component_id=ml_components[1].id),
             TestMapper(ml_component_id=ml_components[2].id)]
    extensions.sql_db.session.add_all(tests)
    extensions.sql_db.session.flush()

    test_descriptions = [TestDescriptionMapper(name='ACC_check_v1',
                                               test_id=tests[0].id, opinion='精度について問題なし。',
                                               delete_flag=False,
                                               value_target=True,
                                               quality_dimension_id=quality_props[4].id,
                                               test_runner_id=test_runners[0].id),
                         TestDescriptionMapper(name='Adversarial Example ACC testing Test_v1',
                                               test_id=tests[0].id, opinion='adversarial exampleにより、'
                                                                            '精度が悪化しているが、'
                                                                            '運用上悪意ある画像が入力される可能性が'
                                                                            'ないため、指標を満たしていないが、'
                                                                            '本件問題なしとする。',
                                               delete_flag=False,
                                               value_target=True,
                                               quality_dimension_id=quality_props[5].id,
                                               test_runner_id=test_runners[1].id),
                         TestDescriptionMapper(name='dag_test',
                                               test_id=tests[0].id, opinion='精度について問題なし。',
                                               delete_flag=False,
                                               value_target=True,
                                               quality_dimension_id=quality_props[5].id,
                                               test_runner_id=test_runners[2].id)
                         ]
    extensions.sql_db.session.add_all(test_descriptions)
    extensions.sql_db.session.flush()

    inv_tds = [InventoryTDMapper(inventory_id=invs[0].id,
                                 test_description_id=test_descriptions[0].id,
                                 template_inventory_id=test_inventory_templates[0].id_),
               InventoryTDMapper(inventory_id=invs[1].id,
                                 test_description_id=test_descriptions[0].id,
                                 template_inventory_id=test_inventory_templates[1].id_),
               InventoryTDMapper(inventory_id=invs[2].id,
                                 test_description_id=test_descriptions[1].id,
                                 template_inventory_id=test_inventory_templates[2].id_),
               InventoryTDMapper(inventory_id=invs[3].id,
                                 test_description_id=test_descriptions[1].id,
                                 template_inventory_id=test_inventory_templates[3].id_),
               InventoryTDMapper(inventory_id=invs[4].id,
                                 test_description_id=test_descriptions[1].id,
                                 template_inventory_id=test_inventory_templates[4].id_),
               InventoryTDMapper(inventory_id=invs[5].id,
                                 test_description_id=test_descriptions[2].id,
                                 template_inventory_id=test_inventory_templates[5].id_)]
    extensions.sql_db.session.add_all(inv_tds)
    extensions.sql_db.session.flush()

    operands = [OperandMapper(value='80', enable=True,
                              quality_measurement_id=meas[0].id, test_description_id=test_descriptions[0].id,
                              relational_operator_id=relational_operator[2].id),
                OperandMapper(value='50', enable=True,
                              quality_measurement_id=meas[1].id, test_description_id=test_descriptions[1].id,
                              relational_operator_id=relational_operator[3].id),
                OperandMapper(value='10', enable=True,
                              quality_measurement_id=meas[2].id, test_description_id=test_descriptions[2].id,
                              relational_operator_id=relational_operator[4].id)]
    extensions.sql_db.session.add_all(operands)
    extensions.sql_db.session.flush()

    test_runner_params = [
        TestRunnerParamMapper(value='0.5',
                              test_runner_param_template_id=test_runner_param_templates[0].id_,
                              test_description_id=test_descriptions[0].id),
        TestRunnerParamMapper(value='0.3',
                              test_runner_param_template_id=test_runner_param_templates[1].id_,
                              test_description_id=test_descriptions[0].id),
        TestRunnerParamMapper(value='1.0',
                              test_runner_param_template_id=test_runner_param_templates[2].id_,
                              test_description_id=test_descriptions[1].id),
        TestRunnerParamMapper(value='select',
                              test_runner_param_template_id=test_runner_param_templates[3].id_,
                              test_description_id=test_descriptions[1].id),
        TestRunnerParamMapper(value='2000',
                              test_runner_param_template_id=test_runner_param_templates[4].id_,
                              test_description_id=test_descriptions[1].id),
        TestRunnerParamMapper(value='balance',
                              test_runner_param_template_id=test_runner_param_templates[5].id_,
                              test_description_id=test_descriptions[1].id),
        TestRunnerParamMapper(value='None',
                              test_runner_param_template_id=test_runner_param_templates[6].id_,
                              test_description_id=test_descriptions[1].id),
        TestRunnerParamMapper(value='FGSM?eps=0.1;',
                              test_runner_param_template_id=test_runner_param_templates[7].id_,
                              test_description_id=test_descriptions[1].id),
        TestRunnerParamMapper(value='none;FeatureSqueezing?squeezer=bit_depth_1;',
                              test_runner_param_template_id=test_runner_param_templates[8].id_,
                              test_description_id=test_descriptions[1].id),
        TestRunnerParamMapper(value='FeatureSqueezing?squeezers=bit_depth_1,median_filter_2_2&'
                                    'distance_measure=l1&fpr=0.05;',
                              test_runner_param_template_id=test_runner_param_templates[9].id_,
                              test_description_id=test_descriptions[1].id),
        TestRunnerParamMapper(value='ODAIBA',
                              test_runner_param_template_id=test_runner_param_templates[10].id_,
                              test_description_id=test_descriptions[2].id)
    ]
    extensions.sql_db.session.add_all(test_runner_params)
    extensions.sql_db.session.flush()

    downloads = [DownloadMapper(path='C:\\Windows\\System32\\nvidia-smi.1.pdf')]
    extensions.sql_db.session.add_all(downloads)

    format_ = FormatMapper.query.all()

    inventory_format = [
        InventoryFormatMapper(inventory_id=invs[0].id, format_id=format_[0].id),
        InventoryFormatMapper(inventory_id=invs[1].id, format_id=format_[5].id),
        InventoryFormatMapper(inventory_id=invs[2].id, format_id=format_[1].id),
        InventoryFormatMapper(inventory_id=invs[2].id, format_id=format_[2].id),
        InventoryFormatMapper(inventory_id=invs[3].id, format_id=format_[3].id),
        InventoryFormatMapper(inventory_id=invs[3].id, format_id=format_[4].id),
        InventoryFormatMapper(inventory_id=invs[4].id, format_id=format_[5].id),
        InventoryFormatMapper(inventory_id=invs[5].id, format_id=format_[5].id)
    ]
    extensions.sql_db.session.add_all(inventory_format)
    extensions.sql_db.session.flush()

    test_inventory_templates_format = [
        TestInventoryTemplateFormatMapper(inventory_template_id=test_inventory_templates[0].id_,
                                          format_id=format_[0].id),
        TestInventoryTemplateFormatMapper(inventory_template_id=test_inventory_templates[1].id_,
                                          format_id=format_[5].id),
        TestInventoryTemplateFormatMapper(inventory_template_id=test_inventory_templates[2].id_,
                                          format_id=format_[1].id),
        TestInventoryTemplateFormatMapper(inventory_template_id=test_inventory_templates[2].id_,
                                          format_id=format_[2].id),
        TestInventoryTemplateFormatMapper(inventory_template_id=test_inventory_templates[3].id_,
                                          format_id=format_[3].id),
        TestInventoryTemplateFormatMapper(inventory_template_id=test_inventory_templates[3].id_,
                                          format_id=format_[4].id),
        TestInventoryTemplateFormatMapper(inventory_template_id=test_inventory_templates[4].id_,
                                          format_id=format_[5].id),
        TestInventoryTemplateFormatMapper(inventory_template_id=test_inventory_templates[5].id_,
                                          format_id=format_[5].id),
    ]
    extensions.sql_db.session.add_all(test_inventory_templates_format)
    extensions.sql_db.session.flush()

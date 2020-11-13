# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import flask
from flask_injector import FlaskInjector
from itertools import chain
from sqlalchemy import Table

from .entities.organization import OrganizationMapper
from .entities.ml_component import MLComponentMapper
from .entities.test import TestMapper
from .entities.test_description import TestDescriptionMapper
from .entities.quality_dimension import QualityDimensionMapper
from .entities.tag import TagMapper
from .entities.test_inventory_template import TestInventoryTemplateMapper
from .entities.test_inventory_template_tag import TestInventoryTemplateTagMapper
from .entities.inventory import InventoryMapper
from .entities.inventory_td import InventoryTDMapper
from .entities.inventory_format import InventoryFormatMapper
from .entities.format import FormatMapper
from .entities.quality_measurement import QualityMeasurementMapper
from .entities.operand import OperandMapper
from .entities.test_runner import TestRunnerMapper
from .entities.test_runner_param import TestRunnerParamMapper
from .entities.test_runner_param_template import TestRunnerParamTemplateMapper
from .entities.test_runner_reference import TestRunnerReferenceMapper
from .entities.test_inventory_template_format import TestInventoryTemplateFormatMapper
from .entities.graph_template import GraphTemplateMapper
from .entities.graph import GraphMapper
from .entities.dowmload import DownloadMapper
from .entities.downloadable_data import DownloadableDataMapper
from .entities.relational_operator import RelationalOperatorMapper
from .entities.structure import StructureMapper
from .entities.resource_type import ResourceTypeMapper
from .entities.ml_framework import MLFrameworkMapper
from .entities.data_type import DataTypeMapper
from .entities.file_system import FileSystemMapper
from .controllers import api
from .gateways import extensions, config
from .di_module import di_module
# from .gateways.auth import jwt


def create_app(config_name='default'):
    """Flask app factory
    :config_name: a string object.
    :returns: flask.Flask object
    """

    app = flask.Flask(__name__)

    # set the config vars using the config name and current_app
    config.config[config_name](app)

    # jwt.set_jwt_handlers(extensions.jwt)

    register_extensions(app)
    register_blueprints(app)

    init_db(app)

    FlaskInjector(app=app, modules=[di_module])

    return app


def register_extensions(app):
    """Call the method 'init_app' to register the extensions in the flask.Flask
    object passed as parameter.
    :app: flask.Flask object
    :returns: None
    """
    extensions.nosql_db.init_app(app)
    # extensions.jwt.init_app(app)
    extensions.sql_db.init_app(app)
    extensions.ma.init_app(app)


def register_blueprints(app):
    """Register all blueprints.
    :app: flask.Flask object
    :returns: None
    """
    app.register_blueprint(api.blueprint)


def init_db(app):
    pass
    # with app.app_context():
    #     extensions.sql_db.drop_all()
    #     extensions.sql_db.create_all()
    #
    #     meas = [QualityMeasurementMapper(name='Coverage of activated neurons'),
    #             QualityMeasurementMapper(name='モデル精度計測')]
    #     extensions.sql_db.session.add_all(meas)
    #     extensions.sql_db.session.flush()
    #
    #     ope_temps = [OperandTemplateMapper(name='GoalCoverage', unit='%', quality_measurement_id=meas[0].id),
    #                  OperandTemplateMapper(name='ACC', unit='%', quality_measurement_id=meas[1].id)]
    #     extensions.sql_db.session.add_all(ope_temps)
    #     extensions.sql_db.session.flush()
    #
    #     quality_props = [QualityDimensionMapper(name='要求分析の完全性'),
    #                      QualityDimensionMapper(name='データセットの完全性'),
    #                      QualityDimensionMapper(name='データセットの被覆性'),
    #                      QualityDimensionMapper(name='データセットの均一性'),
    #                      QualityDimensionMapper(name='学習の正確性'),
    #                      QualityDimensionMapper(name='学習の安定性'),
    #                      QualityDimensionMapper(name='性能の維持性'),
    #                      QualityDimensionMapper(name='ソフト信頼性')]
    #     extensions.sql_db.session.add_all(quality_props)
    #     extensions.sql_db.session.flush()
    #
    #     test_runners = [TestRunnerMapper(name='neuron_coverage_v3.py', quality_measurement_id=meas[0].id)]
    #     extensions.sql_db.session.add_all(test_runners)
    #     extensions.sql_db.session.flush()
    #
    #     test_runner_param_templates = [
    #         TestRunnerParamTemplateMapper(name='Threshold', value_type='float', test_runner_id=test_runners[0].id),
    #         TestRunnerParamTemplateMapper(name='Lower Limit', value_type='float', test_runner_id=test_runners[0].id),
    #         TestRunnerParamTemplateMapper(name='Upper Limit', value_type='float', test_runner_id=test_runners[0].id)]
    #     extensions.sql_db.session.add_all(test_runner_param_templates)
    #     extensions.sql_db.session.flush()
    #
    #     graph_templates = [GraphTemplateMapper(type="1", test_runner_id=test_runners[0].id),
    #                        GraphTemplateMapper(type="2", test_runner_id=test_runners[0].id),
    #                        GraphTemplateMapper(type="3", test_runner_id=test_runners[0].id)]
    #     extensions.sql_db.session.add_all(graph_templates)
    #     extensions.sql_db.session.flush()
    #
    #     orgs = [OrganizationMapper(id='dep-a', name='部署A'),
    #             OrganizationMapper(id='dep-b', name='部署B'),
    #             OrganizationMapper(id='dep-c', name='部署C')]
    #     extensions.sql_db.session.add_all(orgs)
    #     extensions.sql_db.session.flush()
    #
    #     projs = [MLComponentMapper(name='A社住宅価格予測システム', org_id=orgs[0].id),
    #              MLComponentMapper(name='B社文字認識システム', org_id=orgs[0].id),
    #              MLComponentMapper(name='C社ゴルフスコア読み取りシステム', org_id=orgs[0].id)]
    #     extensions.sql_db.session.add_all(projs)
    #     extensions.sql_db.session.flush()
    #
    #     invs = [InventoryMapper(name='TestDataset_0818', type='UNIX_FILE_SYSTEM',
    #                             address='/mnt/xxx/1', prj_id=projs[0].id),
    #             InventoryMapper(name='TestDataset_0918', type='UNIX_FILE_SYSTEM',
    #                             address='/mnt/xxx/2', prj_id=projs[0].id),
    #             InventoryMapper(name='TrainedModel_0907', type='UNIX_FILE_SYSTEM',
    #                             address='/mnt/xxx/3', prj_id=projs[0].id),
    #             InventoryMapper(name='TestDataset_1018', type='UNIX_FILE_SYSTEM',
    #                             address='/mnt/xxx/4', prj_id=projs[0].id),
    #             InventoryMapper(name='TrainedModel_1007', type='UNIX_FILE_SYSTEM',
    #                             address='/mnt/xxx/5', prj_id=projs[0].id)]
    #     extensions.sql_db.session.add_all(invs)
    #     extensions.sql_db.session.flush()
    #
    #     tests = [TestMapper(status='Complete', result='OK 4 / NG 2', prj_id=projs[0].id)]
    #     extensions.sql_db.session.add_all(tests)
    #     extensions.sql_db.session.flush()
    #
    #     test_descriptions = [TestDescriptionMapper(name='NeuronCoverage',
    #                                                status='Complete',
    #                                                result='OK',
    #                                                test_id=tests[0].id, opinion='見解',
    #                                                delete_flag=None,
    #                                                quality_dimension_id=quality_props[4].id,
    #                                                quality_measurement_id=meas[0].id,
    #                                                test_runner_id=test_runners[0].id),
    #                          TestDescriptionMapper(name='MetamorphicTesting',
    #                                                status='Complete',
    #                                                result='OK',
    #                                                test_id=tests[0].id, opinion='見解',
    #                                                delete_flag=None,
    #                                                quality_dimension_id=quality_props[4].id,
    #                                                quality_measurement_id=meas[1].id,
    #                                                test_runner_id=test_runners[0].id),
    #                          TestDescriptionMapper(name='AttributeCoverage',
    #                                                status='Complete',
    #                                                result='NG',
    #                                                test_id=tests[0].id, opinion='見解',
    #                                                delete_flag=None,
    #                                                quality_dimension_id=quality_props[4].id,
    #                                                quality_measurement_id=meas[1].id,
    #                                                test_runner_id=test_runners[0].id),
    #                          TestDescriptionMapper(name='AttributeCoverage2',
    #                                                status='Complete',
    #                                                result='OK',
    #                                                test_id=tests[0].id, opinion='見解',
    #                                                delete_flag=None,
    #                                                quality_dimension_id=quality_props[4].id,
    #                                                quality_measurement_id=meas[1].id,
    #                                                test_runner_id=test_runners[0].id),
    #                          TestDescriptionMapper(name='AttributeCoverage3',
    #                                                status='Complete',
    #                                                result='NG',
    #                                                test_id=tests[0].id, opinion='見解',
    #                                                delete_flag=None,
    #                                                quality_dimension_id=quality_props[4].id,
    #                                                quality_measurement_id=meas[1].id,
    #                                                test_runner_id=test_runners[0].id),
    #                          TestDescriptionMapper(name='AttributeCoverage4',
    #                                                status='Complete',
    #                                                result='OK',
    #                                                test_id=tests[0].id, opinion='見解',
    #                                                delete_flag=None,
    #                                                quality_dimension_id=quality_props[4].id,
    #                                                quality_measurement_id=meas[1].id,
    #                                                test_runner_id=test_runners[0].id)
    #                          ]
    #     extensions.sql_db.session.add_all(test_descriptions)
    #     extensions.sql_db.session.flush()
    #
    #     inv_tds = [InventoryTDMapper(inventory_id=invs[3].id, test_description_id=test_descriptions[0].id),
    #                InventoryTDMapper(inventory_id=invs[4].id, test_description_id=test_descriptions[0].id),
    #                InventoryTDMapper(inventory_id=invs[0].id, test_description_id=test_descriptions[1].id),
    #                InventoryTDMapper(inventory_id=invs[4].id, test_description_id=test_descriptions[2].id),
    #                InventoryTDMapper(inventory_id=invs[2].id, test_description_id=test_descriptions[3].id),
    #                InventoryTDMapper(inventory_id=invs[3].id, test_description_id=test_descriptions[4].id),
    #                InventoryTDMapper(inventory_id=invs[4].id, test_description_id=test_descriptions[5].id),
    #                InventoryTDMapper(inventory_id=invs[0].id, test_description_id=test_descriptions[5].id)]
    #     extensions.sql_db.session.add_all(inv_tds)
    #     extensions.sql_db.session.flush()
    #
    #     operands = [OperandMapper(value=80,
    #                               operand_template_id=ope_temps[0].id, test_description_id=test_descriptions[0].id),
    #                 OperandMapper(value=81,
    #                               operand_template_id=ope_temps[1].id, test_description_id=test_descriptions[1].id),
    #                 OperandMapper(value=82,
    #                               operand_template_id=ope_temps[1].id, test_description_id=test_descriptions[2].id),
    #                 OperandMapper(value=83,
    #                               operand_template_id=ope_temps[1].id, test_description_id=test_descriptions[3].id),
    #                 OperandMapper(value=84,
    #                               operand_template_id=ope_temps[1].id, test_description_id=test_descriptions[4].id),
    #                 OperandMapper(value=85,
    #                               operand_template_id=ope_temps[1].id, test_description_id=test_descriptions[5].id)]
    #     extensions.sql_db.session.add_all(operands)
    #     extensions.sql_db.session.flush()
    #
    #     test_runner_params = list(chain.from_iterable([
    #         [TestRunnerParamMapper(value='0.5',
    #                                test_runner_param_template_id=test_runner_param_templates[0].id,
    #                                test_description_id=td.id),
    #          TestRunnerParamMapper(value='0.3',
    #                                test_runner_param_template_id=test_runner_param_templates[1].id,
    #                                test_description_id=td.id),
    #          TestRunnerParamMapper(value='1.0',
    #                                test_runner_param_template_id=test_runner_param_templates[2].id,
    #                                test_description_id=td.id)
    #          ] for td in test_descriptions]))
    #     extensions.sql_db.session.add_all(test_runner_params)
    #     extensions.sql_db.session.flush()
    #
    #     td_results = [
    #         TestDescriptionResultMapper(summary='OK', detail='Current Coverage 85%', test_description_id=td.id)
    #         for td in test_descriptions]
    #     extensions.sql_db.session.add_all(td_results)
    #     extensions.sql_db.session.flush()
    #
    #     graphs = list(chain.from_iterable([
    #         [GraphMapper(graph_address='http://XXX',
    #                      graph_template_id=graph_templates[0].id, test_description_result_id=tdr.id),
    #          GraphMapper(graph_address='http://YYY',
    #                      graph_template_id=graph_templates[1].id, test_description_result_id=tdr.id),
    #          GraphMapper(graph_address='http://ZZZ',
    #                      graph_template_id=graph_templates[2].id, test_description_result_id=tdr.id),
    #          ] for tdr in td_results]))
    #     extensions.sql_db.session.add_all(graphs)
    #     extensions.sql_db.session.commit()

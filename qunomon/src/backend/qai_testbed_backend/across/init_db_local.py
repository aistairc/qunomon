# Copyright c 2019 National Institute of Advanced Industrial Science and Technology �iAIST�j. All rights reserved.

import os
import datetime
from pathlib import Path
from itertools import chain

from ..entities.organization import OrganizationMapper
from ..entities.ml_component import MLComponentMapper
from ..entities.relational_operator import RelationalOperatorMapper
from ..entities.test import TestMapper
from ..entities.test_description import TestDescriptionMapper
from ..entities.quality_dimension import QualityDimensionMapper
from ..entities.quality_dimension_level import QualityDimensionLevelMapper
from ..entities.inventory import InventoryMapper
from ..entities.inventory_td import InventoryTDMapper
from ..entities.quality_measurement import QualityMeasurementMapper
from ..entities.operand import OperandMapper
from ..entities.test_runner import TestRunnerMapper
from ..entities.test_runner_param import TestRunnerParamMapper
from ..entities.test_runner_param_template import TestRunnerParamTemplateMapper
from ..entities.test_inventory_template import TestInventoryTemplateMapper
from ..entities.test_inventory_template_tag import TestInventoryTemplateTagMapper
from ..entities.graph_template import GraphTemplateMapper
from ..entities.graph import GraphMapper
from ..entities.job import JobMapper
from ..entities.run import RunMapper
from ..entities.run_measure import RunMeasureMapper
from ..entities.setting import SettingMapper
from ..entities.dowmload import DownloadMapper
from ..entities.tag import TagMapper
from ..entities.downloadable_data import DownloadableDataMapper
from ..entities.downloadable_template import DownloadableTemplateMapper
from ..entities.test_runner_reference import TestRunnerReferenceMapper
from ..entities.structure import StructureMapper
from ..entities.test_inventory_template_format import TestInventoryTemplateFormatMapper
from ..entities.test_inventory_template_compatible_package import TestInventoryTemplateCompatiblePackageMapper
from ..entities.inventory_format import InventoryFormatMapper
from ..entities.format import FormatMapper
from ..entities.resource_type import ResourceTypeMapper
from ..entities.ml_framework import MLFrameworkMapper
from ..entities.data_type import DataTypeMapper
from ..entities.file_system import FileSystemMapper
from ..entities.role import RoleMapper
from ..entities.user import UserMapper
from ..entities.user_role_ml_component import UserRoleMLComponentMapper
from ..entities.guideline import GuidelineMapper
from ..entities.guideline_schema_file import GuidelineSchemaFileMapper
from ..entities.scope import ScopeMapper
from ..entities.scope_quality_dimension import ScopeQualityDimensionMapper
from ..entities.report_template import ReportTemplateMapper
from ..gateways import extensions, config
from .file_checker import FileChecker


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

    guidelines = [GuidelineMapper(name='AIQM_Guideline', description='AI Quality Management Guideline', creator='AIQM_members', publisher='aist',
                                  identifier='https://www.digiarc.aist.go.jp/publication/aiqm/AIQM-Guideline-2.1.0.pdf',
                                  publish_datetime=datetime.datetime.strptime('2020-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
                                  aithub_delete_flag=False),
                  GuidelineMapper(name='ML_Guideline', description='Machine Learning Guideline', creator='ML_members', publisher='aist',
                                  identifier='https://www.digiarc.aist.go.jp/publication/aiqm/AIQM-Guideline-2.1.0.pdf',
                                  publish_datetime=datetime.datetime.strptime('2021-11-11 00:00:00', '%Y-%m-%d %H:%M:%S'),
                                  aithub_delete_flag=False),
                  GuidelineMapper(name='Machine_learning_quality_management_guidelines_2.1.0', description='Machine Learning Guideline', creator='ML_members', publisher='aist',
                                  identifier='https://www.digiarc.aist.go.jp/publication/aiqm/AIQM-Guideline-2.1.0.pdf',
                                  publish_datetime=datetime.datetime.strptime('2022-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
                                  aithub_delete_flag=False)]
    extensions.sql_db.session.add_all(guidelines)
    extensions.sql_db.session.flush()

    quality_props = [QualityDimensionMapper(name='Completeness_of_problem_domain_analysis', guideline_id=1, json_id='a', description='description_Completeness_of_problem_domain_analysis', url='url_Completeness_of_problem_domain_analysis'),
                     QualityDimensionMapper(name='Coverage_for_distinguished_problem_cases', guideline_id=1, json_id='b', description='description_Coverage_for_distinguished_problem_cases', url='url_Coverage_for_distinguished_problem_cases'),
                     QualityDimensionMapper(name='Diversity_of_test_data', guideline_id=1, json_id='c', description='description_Diversity_of_test_data', url='url_Diversity_of_test_data'),
                     QualityDimensionMapper(name='Distribution_of_training_data', guideline_id=1, json_id='d', description='description_Distribution_of_training_data', url='url_Distribution_of_training_data'),
                     QualityDimensionMapper(name='Accuracy_of_trained_model', guideline_id=1, json_id='e', description='description_Accuracy_of_trained_model', url='url_Accuracy_of_trained_model'),
                     QualityDimensionMapper(name='Robustness_of_trained_model', guideline_id=1, json_id='f', description='description_Robustness_of_trained_model', url='url_Robustness_of_trained_model'),
                     QualityDimensionMapper(name='Stability_Maintainability_of_quality', guideline_id=1, json_id='g', description='description_Stability_Maintainability_of_quality', url='url_Stability_Maintainability_of_quality'),
                     QualityDimensionMapper(name='Dependability_of_underlying_software', guideline_id=1, json_id='h', description='description_Dependability_of_underlying_software', url='url_Dependability_of_underlying_software')]
    extensions.sql_db.session.add_all(quality_props)
    extensions.sql_db.session.flush()

    quality_levels = [QualityDimensionLevelMapper(quality_dimension_id=1, quality_dimension_level_id='A1', name='name_A1', description='description_A1', level=0),
                      QualityDimensionLevelMapper(quality_dimension_id=1, quality_dimension_level_id='A2', name='name_A2', description='description_A2', level=1),
                      QualityDimensionLevelMapper(quality_dimension_id=2, quality_dimension_level_id='B1', name='name_B1', description='description_B1', level=0),
                      QualityDimensionLevelMapper(quality_dimension_id=2, quality_dimension_level_id='B2', name='name_B2', description='description_B2', level=1),
                      QualityDimensionLevelMapper(quality_dimension_id=3, quality_dimension_level_id='C1', name='name_C1', description='description_C1', level=0),
                      QualityDimensionLevelMapper(quality_dimension_id=3, quality_dimension_level_id='C2', name='name_C2', description='description_C2', level=1),
                      QualityDimensionLevelMapper(quality_dimension_id=4, quality_dimension_level_id='D1', name='name_D1', description='description_D1', level=0),
                      QualityDimensionLevelMapper(quality_dimension_id=4, quality_dimension_level_id='D2', name='name_D2', description='description_D2', level=1),
                      QualityDimensionLevelMapper(quality_dimension_id=5, quality_dimension_level_id='E1', name='name_E1', description='description_E1', level=0),
                      QualityDimensionLevelMapper(quality_dimension_id=5, quality_dimension_level_id='E2', name='name_E2', description='description_E2', level=1),
                      QualityDimensionLevelMapper(quality_dimension_id=6, quality_dimension_level_id='F1', name='name_F1', description='description_F1', level=0),
                      QualityDimensionLevelMapper(quality_dimension_id=6, quality_dimension_level_id='F2', name='name_F2', description='description_F2', level=1),
                      QualityDimensionLevelMapper(quality_dimension_id=7, quality_dimension_level_id='G1', name='name_G1', description='description_G1', level=0),
                      QualityDimensionLevelMapper(quality_dimension_id=7, quality_dimension_level_id='G2', name='name_G2', description='description_G2', level=1),
                      QualityDimensionLevelMapper(quality_dimension_id=8, quality_dimension_level_id='H1', name='name_H1', description='description_H1', level=0),
                      QualityDimensionLevelMapper(quality_dimension_id=8, quality_dimension_level_id='H2', name='name_H2', description='description_H2', level=1),]
    extensions.sql_db.session.add_all(quality_levels)
    extensions.sql_db.session.flush()

    scopes = [ScopeMapper(guideline_id=1, name='DummyScope1'),
              ScopeMapper(guideline_id=1, name='DummyScope2')]
    extensions.sql_db.session.add_all(scopes)
    extensions.sql_db.session.flush()

    scopes_qds = [ScopeQualityDimensionMapper(guideline_id=1, scope_id=1, quality_dimension_id=1),
                  ScopeQualityDimensionMapper(guideline_id=1, scope_id=1, quality_dimension_id=2),
                  ScopeQualityDimensionMapper(guideline_id=1, scope_id=1, quality_dimension_id=3),
                  ScopeQualityDimensionMapper(guideline_id=1, scope_id=1, quality_dimension_id=4),
                  ScopeQualityDimensionMapper(guideline_id=1, scope_id=1, quality_dimension_id=5),
                  ScopeQualityDimensionMapper(guideline_id=1, scope_id=1, quality_dimension_id=6),
                  ScopeQualityDimensionMapper(guideline_id=1, scope_id=1, quality_dimension_id=7),
                  ScopeQualityDimensionMapper(guideline_id=1, scope_id=1, quality_dimension_id=8)]
    extensions.sql_db.session.add_all(scopes_qds)
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
                     ResourceTypeMapper(type='binary'),
                     ResourceTypeMapper(type='directory')]
    extensions.sql_db.session.add_all(resource_type)
    extensions.sql_db.session.flush()

    format_ = [FormatMapper(format_='png'),
               FormatMapper(format_='jpeg'),
               FormatMapper(format_='tiff'),
               FormatMapper(format_='bmp'),
               FormatMapper(format_='csv'),
               FormatMapper(format_='tsv'),
               FormatMapper(format_='onnx'),
               FormatMapper(format_='txt'),
               FormatMapper(format_='json'),
               FormatMapper(format_='xml'),
               FormatMapper(format_='md'),
               FormatMapper(format_='h5'),
               FormatMapper(format_='zip'),
               FormatMapper(format_='gz'),
               FormatMapper(format_='7z'),
               FormatMapper(format_='dump'),
               FormatMapper(format_='bin'),
               FormatMapper(format_='data'),
               FormatMapper(format_='pt'),
               FormatMapper(format_='pth'),
               FormatMapper(format_='DIR'),
               FormatMapper(format_='*')]
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

    ml_frameworks = [MLFrameworkMapper(name='-None-'),
                     MLFrameworkMapper(name='Tensorflow-2.3')]
    extensions.sql_db.session.add_all(ml_frameworks)
    extensions.sql_db.session.flush()

    roles = [RoleMapper(name='admin'),
             RoleMapper(name='mlmanager'),
             RoleMapper(name='user')]
    extensions.sql_db.session.add_all(roles)
    extensions.sql_db.session.flush()

    report_template = [ReportTemplateMapper(name='AIQM_report_template', guideline_id=guidelines[0].id)]
    extensions.sql_db.session.add_all(report_template)
    extensions.sql_db.session.flush()

    guideline_json = [GuidelineSchemaFileMapper(guideline_id=1, name='AIQM Guideline',
        guideline_schema_file={
            "guideline": {
                "scopes": [
                    {
                        "name": "DummyScope1",
                        "scope_descriptors": [
                            {
                                "title": "プロセススコープ",
                                "description": "想定するガイドライン適用プロセスは4段階からなる。"
                            },
                            {
                                "title": "製品・システムスコープ",
                                "description": "情報処理システムの一部に機械学習技術を組み込んだソフトウェアを用いたもの"
                            }
                        ],
                        "quality_scopes": {
                            "quality_dimensions": [
                                "a",
                                "b",
                                "c",
                                "d",
                                "e",
                                "f",
                                "g"
                            ],
                            "ext_quality_dimensions": [
                                "EXT1"
                            ]
                        }
                    }
                ],
                "quality_dimensions": [
                    {
                        "id": "a",
                        "name": "Completeness_of_problem_domain_analysis",
                        "description": "description_Completeness_of_problem_domain_analysis",
                        "levels": [
                            {
                                "id": "A1",
                                "name": "name_A1",
                                "description": "description_A1",
                                "level": 0
                            },
                            {
                                "id": "A2",
                                "name": "name_A1",
                                "description": "description_A2",
                                "level": 1
                            }
                        ],
                        "measurements": [
                            "A-1-1",
                            "A-1-2"
                        ]
                    },
                    {
                        "id": "b",
                        "name": "Coverage_for_distinguished_problem_cases",
                        "description": "description_Coverage_for_distinguished_problem_cases",
                        "levels": [
                            {
                                "id": "B1",
                                "name": "name_B1",
                                "description": "description_B1",
                                "level": 0
                            },
                            {
                                "id": "B2",
                                "name": "name_B1",
                                "description": "description_B2",
                                "level": 1
                            }
                        ],
                        "measurements": [
                            "A-1-1",
                            "A-1-2"
                        ]
                    },
                    {
                        "id": "c",
                        "name": "Diversity_of_test_data",
                        "description": "description_Diversity_of_test_data",
                        "levels": [
                            {
                                "id": "C1",
                                "name": "name_C1",
                                "description": "description_C1",
                                "level": 0
                            },
                            {
                                "id": "C2",
                                "name": "name_C1",
                                "description": "description_C2",
                                "level": 1
                            }
                        ],
                        "measurements": [
                            "A-1-1",
                            "A-1-2"
                        ]
                    },
                    {
                        "id": "d",
                        "name": "Distribution_of_training_data",
                        "description": "description_Distribution_of_training_data",
                        "levels": [
                            {
                                "id": "D1",
                                "name": "name_D1",
                                "description": "description_D1",
                                "level": 0
                            },
                            {
                                "id": "D2",
                                "name": "name_D1",
                                "description": "description_D2",
                                "level": 1
                            }
                        ],
                        "measurements": [
                            "A-1-1",
                            "A-1-2"
                        ]
                    },
                    {
                        "id": "e",
                        "name": "Accuracy_of_trained_model",
                        "description": "description_Accuracy_of_trained_model",
                        "levels": [
                            {
                                "id": "E1",
                                "name": "name_E1",
                                "description": "description_E1",
                                "level": 0
                            },
                            {
                                "id": "E2",
                                "name": "name_E1",
                                "description": "description_E2",
                                "level": 1
                            }
                        ],
                        "measurements": [
                            "A-1-1",
                            "A-1-2"
                        ]
                    },
                    {
                        "id": "f",
                        "name": "Robustness_of_trained_model",
                        "description": "description_Robustness_of_trained_model",
                        "levels": [
                            {
                                "id": "F1",
                                "name": "name_F1",
                                "description": "description_F1",
                                "level": 0
                            },
                            {
                                "id": "F2",
                                "name": "name_F1",
                                "description": "description_F2",
                                "level": 1
                            }
                        ],
                        "measurements": [
                            "A-1-1",
                            "A-1-2"
                        ]
                    },
                    {
                        "id": "g",
                        "name": "Stability_Maintainability_of_quality",
                        "description": "description_Stability_Maintainability_of_quality",
                        "levels": [
                            {
                                "id": "G1",
                                "name": "name_G1",
                                "description": "description_G1",
                                "level": 0
                            },
                            {
                                "id": "G2",
                                "name": "name_G1",
                                "description": "description_G2",
                                "level": 1
                            }
                        ],
                        "measurements": [
                            "A-1-1",
                            "A-1-2"
                        ]
                    },
                    {
                        "id": "h",
                        "name": "Dependability_of_underlying_software",
                        "description": "description_Dependability_of_underlying_software",
                        "levels": [
                            {
                                "id": "H1",
                                "name": "name_H1",
                                "description": "description_H1",
                                "level": 0
                            },
                            {
                                "id": "H2",
                                "name": "name_H1",
                                "description": "description_H2",
                                "level": 1
                            }
                        ],
                        "measurements": [
                            "A-1-1",
                            "A-1-2"
                        ]
                    }
                ],
                "quality_inhibitor": {
                    "name": "dummy quality_inhibitor 1",
                    "description": "dummy quality_inhibitor description 1",
                    "countermeasures": [
                        {
                            "id": "countermeasures1",
                            "description": "countermeasures description 1"
                        },
                        {
                            "id": "countermeasures2",
                            "description": "countermeasures description 2"
                        }
                    ]
                },
                "measurements": [
                    {
                        "id": "A-1-1",
                        "name": "属性（特徴の軸）及び属性値（具体的な特徴）の列挙，リスク検討，取り扱いの決定",
                        "type": "conditional",
                        "description": "システム全体について分析された要求などから属性および属性値の候補を列挙すること",
                        "sub_measurements": [
                        "A-1-1-1"
                        ]
                    },
                    {
                        "id": "A-1-1-1",
                        "name": "属性及び属性値の列挙",
                        "type": "other",
                        "description": "次にあげる観点から属性の候補として考えられる特徴を列挙する。"
                    },
                    {
                        "id": "A-1-2",
                        "name": "除外する属性組み合わせの検討",
                        "type": "conditional",
                        "description": "「あり得ない属性値の組み合わせ」についても検討を行うこと。"
                    }
                ],
                "meta_info": [
                    {
                        "property": "title",
                        "term": "dummy term 1",
                        "content": "Dummy_Guideline"
                    },
                    {
                        "property": "description",
                        "content": "Dummy_Guideline_description"
                    },
                    {
                        "property": "creator",
                        "content": "Dummy_Members"
                    },
                    {
                        "property": "publisher",
                        "content": "AIST"
                    },
                    {
                        "property": "date",
                        "term": "issued",
                        "content": "2021-04-01"
                    },
                    {
                        "property": "identifier",
                        "content": "https://www.digiarc.aist.go.jp/publication/aiqm/AIQM-Guideline-2.1.0.pdf"
                    }
                ]
            }
        })]
    extensions.sql_db.session.add_all(guideline_json)
    extensions.sql_db.session.flush()

# def _init_db_demo_1():
#     """デモ用（最初期）"""

#     quality_props = QualityDimensionMapper.query.all()
#     relational_operator = RelationalOperatorMapper.query.all()

#     meas = [QualityMeasurementMapper(name='Coverage of activated neurons',
#                                      version='0.1',
#                                      description='学習モデルの安定性評価指標'),
#             QualityMeasurementMapper(name='モデル精度計測',
#                                      version='0.1',
#                                      description='学習モデルの正確性評価指標')]
#     extensions.sql_db.session.add_all(meas)
#     extensions.sql_db.session.flush()

#     test_runners = [
#         TestRunnerMapper(name='neuron_coverage_v3.py', dag_name='eval_coverage_3.0'),
#         TestRunnerMapper(name='neuron_coverage_v6.py', dag_name='eval_coverage_6.0')
#     ]
#     extensions.sql_db.session.add_all(test_runners)
#     extensions.sql_db.session.flush()

#     test_runner_param_templates = [
#         TestRunnerParamTemplateMapper(name='Threshold', value_type='float', test_runner_id=test_runners[0].id),
#         TestRunnerParamTemplateMapper(name='Lower Limit', value_type='float', test_runner_id=test_runners[0].id),
#         TestRunnerParamTemplateMapper(name='Upper Limit', value_type='float', test_runner_id=test_runners[0].id)]
#     extensions.sql_db.session.add_all(test_runner_param_templates)
#     extensions.sql_db.session.flush()

#     graph_templates = [GraphTemplateMapper(type="picture", test_runner_id=test_runners[0].id),
#                        GraphTemplateMapper(type="picture", test_runner_id=test_runners[0].id),
#                        GraphTemplateMapper(type="picture", test_runner_id=test_runners[0].id),
#                        GraphTemplateMapper(type="picture", test_runner_id=test_runners[2].id),
#                        GraphTemplateMapper(type="picture", test_runner_id=test_runners[2].id),
#                        GraphTemplateMapper(type="picture", test_runner_id=test_runners[2].id),
#                        GraphTemplateMapper(type="picture", test_runner_id=test_runners[2].id)]
#     extensions.sql_db.session.add_all(graph_templates)
#     extensions.sql_db.session.flush()

#     orgs = [OrganizationMapper(id=1, organizer_id='dep-a', name='部署A', delete_flag=False),
#             OrganizationMapper(id=2, organizer_id='dep-b', name='部署B', delete_flag=False),
#             OrganizationMapper(id=3, organizer_id='dep-c', name='部署C', delete_flag=False),
#             OrganizationMapper(id=4, organizer_id='dep-d', name='部署D', delete_flag=True)]
#     extensions.sql_db.session.add_all(orgs)
#     extensions.sql_db.session.flush()

#     projs = [MLComponentMapper(name='A社住宅価格予測システム', org_id=orgs[0].id, delete_flag=False),
#              MLComponentMapper(name='B社文字認識システム', org_id=orgs[0].id, delete_flag=False),
#              MLComponentMapper(name='C社ゴルフスコア読み取りシステム', org_id=orgs[0].id, delete_flag=False)]
#     extensions.sql_db.session.add_all(projs)
#     extensions.sql_db.session.flush()

#     users = [UserMapper(org_id=1, account_id='admin', user_name='administrator', password_hash='qwertyuiopasdfghjkl'),
#              UserMapper(org_id=1, account_id='user', user_name='user01', password_hash='qwertyuiopasdfghjkl')]
#     extensions.sql_db.session.add_all(users)
#     extensions.sql_db.session.flush()

#     user_Role_ml_component = [UserRoleMLComponentMapper(user_id=users[0].id, role_id=1 ,ml_component_id=projs[0].id),
#                               UserRoleMLComponentMapper(user_id=users[0].id, role_id=2 ,ml_component_id=projs[1].id)]
#     extensions.sql_db.session.add_all(user_Role_ml_component)
#     extensions.sql_db.session.flush()

#     tags = [TagMapper(name='CSV', type='INVENTORY'),
#             TagMapper(name='TF_MODEL', type='INVENTORY'),
#             TagMapper(name='ZIP', type='INVENTORY')]
#     extensions.sql_db.session.add_all(tags)
#     extensions.sql_db.session.flush()

#     test_inventory_templates = [
#         TestInventoryTemplateMapper(name='TestDataSet', test_runner_id=test_runners[0].id),
#         TestInventoryTemplateMapper(name='TrainedModel', test_runner_id=test_runners[0].id),
#         TestInventoryTemplateMapper(name='TestMetaDataSet', test_runner_id=test_runners[1].id),
#         TestInventoryTemplateMapper(name='TestDataSet', test_runner_id=test_runners[1].id),
#         TestInventoryTemplateMapper(name='TrainedModel', test_runner_id=test_runners[1].id),
#         TestInventoryTemplateMapper(name='TrainedModel', test_runner_id=test_runners[2].id)]
#     extensions.sql_db.session.add_all(test_inventory_templates)
#     extensions.sql_db.session.flush()

#     test_inventory_templates_tag = [
#         TestInventoryTemplateTagMapper(inventory_template_id=test_inventory_templates[0].id_, tag_id=tags[0].id),
#         TestInventoryTemplateTagMapper(inventory_template_id=test_inventory_templates[1].id_, tag_id=tags[1].id),
#         TestInventoryTemplateTagMapper(inventory_template_id=test_inventory_templates[2].id_, tag_id=tags[0].id),
#         TestInventoryTemplateTagMapper(inventory_template_id=test_inventory_templates[3].id_, tag_id=tags[2].id),
#         TestInventoryTemplateTagMapper(inventory_template_id=test_inventory_templates[4].id_, tag_id=tags[1].id),
#         TestInventoryTemplateTagMapper(inventory_template_id=test_inventory_templates[5].id_, tag_id=tags[1].id)]
#     extensions.sql_db.session.add_all(test_inventory_templates_tag)
#     extensions.sql_db.session.flush()

#     invs = [InventoryMapper(name='TestDataset_0818',
#                             type='UNIX_FILE_SYSTEM',
#                             address='/mnt/xxx/1',
#                             description='0818用のデータセット',
#                             delete_flag=False,
#                             ml_component_id=projs[0].id),
#             InventoryMapper(name='TestDataset_0918',
#                             type='UNIX_FILE_SYSTEM',
#                             address='/mnt/xxx/2',
#                             description='0918用のデータセット',
#                             delete_flag=False,
#                             ml_component_id=projs[0].id),
#             InventoryMapper(name='TrainedModel_0907',
#                             type='UNIX_FILE_SYSTEM',
#                             address='/mnt/xxx/3',
#                             description='0907用のモデル',
#                             delete_flag=False,
#                             ml_component_id=projs[0].id),
#             InventoryMapper(name='TestDataset_1018',
#                             type='UNIX_FILE_SYSTEM',
#                             address='/mnt/xxx/4',
#                             description='1018用のデータセット',
#                             delete_flag=False,
#                             ml_component_id=projs[0].id),
#             InventoryMapper(name='TrainedModel_1007',
#                             type='UNIX_FILE_SYSTEM',
#                             address='/mnt/xxx/5',
#                             description='1007用のモデル',
#                             delete_flag=False,
#                             ml_component_id=projs[0].id)]
#     extensions.sql_db.session.add_all(invs)
#     extensions.sql_db.session.flush()

#     tests = [TestMapper(ml_component_id=projs[0].id)]
#     extensions.sql_db.session.add_all(tests)
#     extensions.sql_db.session.flush()

#     test_descriptions = [TestDescriptionMapper(name='NeuronCoverage',
#                                                test_id=tests[0].id, opinion='見解',
#                                                delete_flag=False,
#                                                value_target=True,
#                                                quality_dimension_id=quality_props[4].id,
#                                                quality_measurement_id=meas[0].id,
#                                                test_runner_id=test_runners[0].id),
#                          TestDescriptionMapper(name='MetamorphicTesting',
#                                                test_id=tests[0].id, opinion='見解',
#                                                delete_flag=False,
#                                                value_target=True,
#                                                quality_dimension_id=quality_props[4].id,
#                                                quality_measurement_id=meas[1].id,
#                                                test_runner_id=test_runners[0].id),
#                          TestDescriptionMapper(name='AttributeCoverage',
#                                                test_id=tests[0].id, opinion='見解',
#                                                delete_flag=False,
#                                                value_target=True,
#                                                quality_dimension_id=quality_props[4].id,
#                                                quality_measurement_id=meas[1].id,
#                                                test_runner_id=test_runners[0].id),
#                          TestDescriptionMapper(name='AttributeCoverage2',
#                                                test_id=tests[0].id, opinion='見解',
#                                                delete_flag=False,
#                                                value_target=True,
#                                                quality_dimension_id=quality_props[4].id,
#                                                quality_measurement_id=meas[1].id,
#                                                test_runner_id=test_runners[0].id),
#                          TestDescriptionMapper(name='AttributeCoverage3',
#                                                test_id=tests[0].id, opinion='見解',
#                                                delete_flag=False,
#                                                value_target=True,
#                                                quality_dimension_id=quality_props[4].id,
#                                                quality_measurement_id=meas[1].id,
#                                                test_runner_id=test_runners[0].id),
#                          TestDescriptionMapper(name='AttributeCoverage4',
#                                                test_id=tests[0].id, opinion='見解',
#                                                delete_flag=False,
#                                                value_target=True,
#                                                quality_dimension_id=quality_props[4].id,
#                                                quality_measurement_id=meas[1].id,
#                                                test_runner_id=test_runners[0].id)
#                          ]
#     extensions.sql_db.session.add_all(test_descriptions)
#     extensions.sql_db.session.flush()
#     test_descriptions[3].parent_id = test_descriptions[2].id
#     test_descriptions[4].parent_id = test_descriptions[3].id
#     test_descriptions[5].parent_id = test_descriptions[4].id

#     inv_tds = [InventoryTDMapper(inventory_id=invs[3].id,
#                                  test_description_id=test_descriptions[0].id,
#                                  template_inventory_id=test_inventory_templates[0].id_),
#                InventoryTDMapper(inventory_id=invs[4].id,
#                                  test_description_id=test_descriptions[0].id,
#                                  template_inventory_id=test_inventory_templates[1].id_),
#                InventoryTDMapper(inventory_id=invs[0].id,
#                                  test_description_id=test_descriptions[1].id,
#                                  template_inventory_id=test_inventory_templates[0].id_),
#                InventoryTDMapper(inventory_id=invs[4].id,
#                                  test_description_id=test_descriptions[2].id,
#                                  template_inventory_id=test_inventory_templates[1].id_),
#                InventoryTDMapper(inventory_id=invs[2].id,
#                                  test_description_id=test_descriptions[3].id,
#                                  template_inventory_id=test_inventory_templates[0].id_),
#                InventoryTDMapper(inventory_id=invs[3].id,
#                                  test_description_id=test_descriptions[4].id,
#                                  template_inventory_id=test_inventory_templates[1].id_),
#                InventoryTDMapper(inventory_id=invs[4].id,
#                                  test_description_id=test_descriptions[5].id,
#                                  template_inventory_id=test_inventory_templates[0].id_),
#                InventoryTDMapper(inventory_id=invs[0].id,
#                                  test_description_id=test_descriptions[5].id,
#                                  template_inventory_id=test_inventory_templates[1].id_)]
#     extensions.sql_db.session.add_all(inv_tds)
#     extensions.sql_db.session.flush()

#     operands = [OperandMapper(value=80, enable=True,
#                               quality_measurement_id=meas[0].id, test_description_id=test_descriptions[0].id,
#                               relational_operator_id=relational_operator[2].id),
#                 OperandMapper(value=81, enable=True,
#                               quality_measurement_id=meas[1].id, test_description_id=test_descriptions[1].id,
#                               relational_operator_id=relational_operator[3].id),
#                 OperandMapper(value=82, enable=True,
#                               quality_measurement_id=meas[1].id, test_description_id=test_descriptions[2].id,
#                               relational_operator_id=relational_operator[4].id),
#                 OperandMapper(value=83, enable=True,
#                               quality_measurement_id=meas[1].id, test_description_id=test_descriptions[3].id,
#                               relational_operator_id=relational_operator[5].id),
#                 OperandMapper(value=84, enable=True,
#                               quality_measurement_id=meas[1].id, test_description_id=test_descriptions[4].id,
#                               relational_operator_id=relational_operator[0].id),
#                 OperandMapper(value=85, enable=True,
#                               quality_measurement_id=meas[1].id, test_description_id=test_descriptions[5].id,
#                               relational_operator_id=relational_operator[1].id)]
#     extensions.sql_db.session.add_all(operands)
#     extensions.sql_db.session.flush()

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

#     jobs = [JobMapper(status='DONE', result='SUCCESS', result_detail='OK:2 NG:0 ERR:0 NA:0', test_id=tests[0].id)]
#     extensions.sql_db.session.add_all(jobs)
#     extensions.sql_db.session.flush()

#     runs = [RunMapper(status='DONE',
#                       result='SUCCESS', detail_result='SUCCESS',
#                       job_id=jobs[0].id, test_description_id=test_descriptions[0].id),
#             RunMapper(status='DONE',
#                       result='SUCCESS', detail_result='SUCCESS',
#                       job_id=jobs[0].id, test_description_id=test_descriptions[1].id)
#             ]
#     extensions.sql_db.session.add_all(runs)
#     extensions.sql_db.session.flush()

#     downloads = [DownloadMapper(path='C:\\Windows\\System32\\nvidia-smi.1.pdf')]
#     extensions.sql_db.session.add_all(downloads)
#     extensions.sql_db.session.flush()

#     graphs = list(chain.from_iterable([
#         [GraphMapper(report_required='TRUE', graph_address='http://XXX',
#                      report_index=1, report_name=graph_templates[0].name,
#                      graph_template_id=graph_templates[0].id, run_id=r.id, download_id=downloads[0].id),
#          GraphMapper(report_required='TRUE', graph_address='http://YYY',
#                      report_index=2, report_name=graph_templates[1].name,
#                      graph_template_id=graph_templates[1].id, run_id=r.id, download_id=downloads[0].id),
#          GraphMapper(report_required='TRUE', graph_address='http://ZZZ',
#                      report_index=2, report_name=graph_templates[2].name,
#                      graph_template_id=graph_templates[2].id, run_id=r.id, download_id=downloads[0].id),
#          ] for r in runs]))
#     extensions.sql_db.session.add_all(graphs)
#     extensions.sql_db.session.flush()


def _init_db_demo_2():
    """デモ用（レポート機能）"""
    relational_operator = RelationalOperatorMapper.query.all()
    structures = [StructureMapper(structure='single')]
    extensions.sql_db.session.add_all(structures)
    extensions.sql_db.session.flush()

    quality_props = QualityDimensionMapper.query.all()

    test_runners = [
        TestRunnerMapper(name='acc_check_1.0.py', 
                         description='eval_acc_check_by_tfmodel_1.0', 
                         source_repository='https://dummyrepository/acc_check_1.0',
                         create_user_account='local_developer',
                         create_user_name='開発者A', 
                         version='1',
                         quality='https://airc.aist.go.jp/aiqm/quality/internal/Accuracy_of_trained_model',
                         keywords='dummykeywords1,dummykeywords2,dummykeywords3',
                         licenses='dummylicenses1,dummylicenses2,dummylicenses3',
                         landing_page='https://aithub.com/acc_check/1.0'),
        TestRunnerMapper(name='adversarial_example_acc_test_1.0.py',
                         description='eval_adversarial_example_acc_test_by_tfmodel_1.0',
                         source_repository='https://dummyrepository/adversarial_example_acc_test_1.0',
                         create_user_account='local_developer',
                         create_user_name='開発者A', 
                         version='1',
                         quality='https://airc.aist.go.jp/aiqm/quality/internal/Robustness_of_trained_model',
                         keywords='dummykeywords1',
                         licenses='dummylicenses1',
                         landing_page='https://aithub.com/adversarial_example_acc_test/1.0'),
        TestRunnerMapper(name='dev_hello_world',
                         description='dev_hello_world_0.1', 
                         source_repository='https://dummyrepository/dev_hello_world_0.1',
                         create_user_account='local_developer',
                         create_user_name='開発者A', 
                         version='0.1',
                         quality='https://airc.aist.go.jp/aiqm/quality/internal/Robustness_of_trained_model',
                         keywords='',
                         licenses='',
                         landing_page='https://aithub.com/dev_hello_world/')
    ]
    extensions.sql_db.session.add_all(test_runners)
    extensions.sql_db.session.flush()

    test_runner_references = [
        TestRunnerReferenceMapper(bib_info='dummybib_info1_1',
                                  additional_info='dummyadditional_info1_1',
                                  url_='dummyurl_1_1',
                                  test_runner_id=test_runners[0].id),
        TestRunnerReferenceMapper(bib_info='dummybib_info1_2',
                                  additional_info='dummyadditional_info1_2',
                                  url_='dummyurl_1_2',
                                  test_runner_id=test_runners[0].id),
        TestRunnerReferenceMapper(bib_info='dummybib_info2_1',
                                  additional_info='dummyadditional_info2_1',
                                  url_='dummyurl_2_1',
                                  test_runner_id=test_runners[1].id)
    ]
    extensions.sql_db.session.add_all(test_runner_references)
    extensions.sql_db.session.flush()

    meas = [QualityMeasurementMapper(name='学習モデルの精度計測',
                                     description='学習モデルの正確性評価指標',
                                     type='float',
                                     structure_id=structures[0].id,
                                     min_value=0.0,
                                     max_value=100.0,
                                     test_runner_id=test_runners[0].id),
            QualityMeasurementMapper(name='学習モデルの敵対的サンプル安定性計測',
                                     description='学習モデルの安定性評価指標',
                                     type='float',
                                     structure_id=structures[0].id,
                                     min_value=1.23,
                                     test_runner_id=test_runners[1].id),
            QualityMeasurementMapper(name='学習モデルの敵対的サンプル安定性計測2',
                                     description='学習モデルの安定性評価指標',
                                     type='float',
                                     max_value=123.45,
                                     structure_id=structures[0].id,
                                     test_runner_id=test_runners[2].id)]
    extensions.sql_db.session.add_all(meas)
    extensions.sql_db.session.flush()

    test_runner_param_templates = [
        TestRunnerParamTemplateMapper(name='Threshold', value_type='float',
                                      description='敵対的生成のずらし具合, \\epsilon \\in \\{0.0, 1.0\\',
                                      default_value='0.5', min_value=0.0, max_value=1.0,
                                      test_runner_id=test_runners[0].id),
        TestRunnerParamTemplateMapper(name='Lower Limit', value_type='float',
                                      description='敵対的生成のずらし具合, \\epsilon \\in \\{0.0, 1.0\\',
                                      default_value='0.3', min_value=0.0, max_value=1.0,
                                      test_runner_id=test_runners[0].id,
                                      depends_on_parameter='Threshold'),
        TestRunnerParamTemplateMapper(name='Upper Limit', value_type='float',
                                      description='敵対depends_on_parameter的生成のずらし具合, \\epsilon \\in \\{0.0, 1.0\\',
                                      default_value='1.0', min_value=0.0, max_value=1.0,
                                      test_runner_id=test_runners[0].id,
                                      depends_on_parameter='Threshold'),
        TestRunnerParamTemplateMapper(name='select', value_type='string', description='select',
                                      default_value='',
                                      test_runner_id=test_runners[1].id),
        TestRunnerParamTemplateMapper(name='nb_examples', value_type='int', description='単純ベイズ分類器',
                                      default_value='',
                                      test_runner_id=test_runners[1].id),
        TestRunnerParamTemplateMapper(name='balance_sampling', value_type='string',
                                      description='母集団からユニットをランダムに選択する方法',
                                      default_value='',
                                      test_runner_id=test_runners[1].id),
        TestRunnerParamTemplateMapper(name='test_mode', value_type='string', description='test_mode',
                                      default_value='',
                                      test_runner_id=test_runners[1].id,
                                      depends_on_parameter='balance_sampling'),
        TestRunnerParamTemplateMapper(name='attacks', value_type='string', description='attacks',
                                      default_value='',
                                      test_runner_id=test_runners[1].id,
                                      depends_on_parameter='balance_sampling'),
        TestRunnerParamTemplateMapper(name='robustness', value_type='string',
                                      description='ニューラルネットワークのトレーニング、評価、探索',
                                      default_value='',
                                      test_runner_id=test_runners[1].id,
                                      depends_on_parameter='balance_sampling'),
        TestRunnerParamTemplateMapper(name='detection', value_type='string', description='detection',
                                      default_value='',
                                      test_runner_id=test_runners[1].id),
        TestRunnerParamTemplateMapper(name='Name', value_type='string', description='Name',
                                      default_value='',
                                      test_runner_id=test_runners[2].id)]
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

    orgs = [OrganizationMapper(id=1, organizer_id='dep-a', name='部署A', delete_flag=False),
            OrganizationMapper(id=2, organizer_id='dep-b', name='部署B', delete_flag=False),
            OrganizationMapper(id=3, organizer_id='dep-c', name='部署C', delete_flag=False),
            OrganizationMapper(id=4, organizer_id='dep-d', name='部署D', delete_flag=True)]
    extensions.sql_db.session.add_all(orgs)
    extensions.sql_db.session.flush()

    ml_frameworks = MLFrameworkMapper.query.all()
    guidelines = GuidelineMapper.query.all()
    scopes = ScopeMapper.query.all()
    ml_components = [MLComponentMapper(name='A社住宅価格予測-機械学習コンポーネント', org_id=orgs[0].id,
                                       description='A社の住宅価格を予測する機械学習コンポーネント',
                                       problem_domain='重回帰分析',
                                       ml_framework_id=ml_frameworks[0].id,
                                       guideline_id=guidelines[0].id,
                                       scope_id=scopes[0].id,
                                       guideline_reason='ガイドラインを選択した理由',
                                       scope_reason='スコープを選択した理由',
                                       delete_flag=False),
                     MLComponentMapper(name='B社文字認識-機械学習コンポーネント', org_id=orgs[0].id,
                                       description='B社の文字を認識する機械学習コンポーネント',
                                       problem_domain='画像分類',
                                       ml_framework_id=ml_frameworks[0].id,
                                       guideline_id=guidelines[0].id,
                                       scope_id=scopes[0].id,
                                       guideline_reason='ガイドラインを選択した理由',
                                       scope_reason='スコープを選択した理由',
                                       delete_flag=False),
                     MLComponentMapper(name='C社ゴルフスコア読取-機械学習コンポーネント', org_id=orgs[0].id,
                                       description='C社のスコア表枠組み、文字を認識する機械学習コンポーネント',
                                       problem_domain='レイアウト認識、画像分類',
                                       ml_framework_id=ml_frameworks[0].id,
                                       guideline_id=guidelines[0].id,
                                       scope_id=scopes[0].id,
                                       guideline_reason='ガイドラインを選択した理由',
                                       scope_reason='スコープを選択した理由',
                                       delete_flag=False)]
    extensions.sql_db.session.add_all(ml_components)
    extensions.sql_db.session.flush()

    users = [UserMapper(org_id=1, account_id='admin', user_name='administrator', password_hash='qwertyuiopasdfghjkl'),
             UserMapper(org_id=1, account_id='user', user_name='user01', password_hash='qwertyuiopasdfghjkl')]
    extensions.sql_db.session.add_all(users)
    extensions.sql_db.session.flush()

    user_Role_ml_component = [UserRoleMLComponentMapper(user_id=users[0].id, role_id=1 ,ml_component_id=ml_components[0].id),
                              UserRoleMLComponentMapper(user_id=users[0].id, role_id=2 ,ml_component_id=ml_components[1].id)]
    extensions.sql_db.session.add_all(user_Role_ml_component)
    extensions.sql_db.session.flush()

    tags = [TagMapper(name='CSV', type='INVENTORY'),
            TagMapper(name='TF_MODEL', type='INVENTORY'),
            TagMapper(name='ZIP', type='INVENTORY')]
    extensions.sql_db.session.add_all(tags)
    extensions.sql_db.session.flush()

    data_types = DataTypeMapper.query.all()
    file_systems = FileSystemMapper.query.all()
    test_inventory_templates = [
        TestInventoryTemplateMapper(name='TestDataSet', 
                                    type_id=data_types[0].id, 
                                    description='28x28のpng',
                                    test_runner_id=test_runners[0].id,
                                    min="1",
                                    max="3"),
        TestInventoryTemplateMapper(name='TrainedModel', type_id=data_types[1].id, description='ONNXファイル',
                                    test_runner_id=test_runners[0].id,
                                    depends_on_parameter='Threshold'),
        TestInventoryTemplateMapper(name='TestMetaDataSet', type_id=data_types[0].id, description='jpg, jpeg',
                                    test_runner_id=test_runners[1].id,
                                    depends_on_parameter='balance_sampling'),
        TestInventoryTemplateMapper(name='TestDataSet', type_id=data_types[0].id, description='csv, tsv',
                                    test_runner_id=test_runners[1].id,
                                    depends_on_parameter=''),
        TestInventoryTemplateMapper(name='TrainedModel', type_id=data_types[1].id, description='ONNXファイル',
                                    test_runner_id=test_runners[1].id),
        TestInventoryTemplateMapper(name='TrainedModel', type_id=data_types[1].id, description='ONNXファイル',
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

    # インベントリファイル
    inv_file_list = ['test.png', 'test.tiff', 'test.jpg', 'test.jpe', 'test.tiff', 'test.tiff']

    if os.name == 'nt':
        files_dir = Path(__file__).parent.parent.parent / 'tests' / 'files'
        inv_path_list = [str(files_dir/f) for f in inv_file_list]

        file_system_id = file_systems[1].id
    else:
        file_system_id = [f for f in file_systems if f.name == os.getenv('QAI_HOST_FILE_SYSTEM')][0].id

        if os.getenv('QAI_HOST_FILE_SYSTEM') == 'WINDOWS_FILE':
            split_char = '\\'
        else:
            split_char = '/'

        files_dir = os.getenv('QAI_HOST_DIR') + split_char + 'tests' + split_char + 'files'
        inv_path_list = [files_dir + split_char + f for f in inv_file_list]

    file_check_result_list = []
    for inv_path in inv_path_list:
        file_check_result_list.append(FileChecker().execute(inv_path, file_system_id))

    invs = [InventoryMapper(name='TestDataset_0818',
                            type_id=data_types[0].id,
                            file_system_id=file_system_id,
                            file_path=inv_path_list[0],
                            description='0818用のデータセット',
                            delete_flag=False,
                            ml_component_id=ml_components[0].id,
                            file_hash_sha256=file_check_result_list[0]['hash_sha256']),
            InventoryMapper(name='TrainedModel_0907',
                            type_id=data_types[1].id,
                            file_system_id=file_system_id,
                            file_path=inv_path_list[1],
                            description='0918用のデータセット',
                            delete_flag=False,
                            ml_component_id=ml_components[0].id,
                            file_hash_sha256=file_check_result_list[1]['hash_sha256']),
            InventoryMapper(name='TestDataset_0918',
                            type_id=data_types[0].id,
                            file_system_id=file_system_id,
                            file_path=inv_path_list[2],
                            description='0907用のモデル',
                            delete_flag=False,
                            ml_component_id=ml_components[0].id,
                            file_hash_sha256=file_check_result_list[2]['hash_sha256']),
            InventoryMapper(name='TestDataset_1002',
                            type_id=data_types[0].id,
                            file_system_id=file_system_id,
                            file_path=inv_path_list[3],
                            description='1007用のモデル',
                            delete_flag=False,
                            ml_component_id=ml_components[0].id,
                            file_hash_sha256=file_check_result_list[3]['hash_sha256']),
            InventoryMapper(name='DUMMY1_ONNX',
                            type_id=data_types[1].id,
                            file_system_id=file_system_id,
                            file_path=inv_path_list[4],
                            description='開発用ダミーデータ',
                            delete_flag=False,
                            ml_component_id=ml_components[0].id,
                            file_hash_sha256=file_check_result_list[4]['hash_sha256']),
            InventoryMapper(name='DUMMY2_ONNX',
                            type_id=data_types[1].id,
                            file_system_id=file_system_id,
                            file_path=inv_path_list[5],
                            description='開発用ダミーデータ',
                            delete_flag=False,
                            ml_component_id=ml_components[0].id,
                            file_hash_sha256=file_check_result_list[5]['hash_sha256']),
            InventoryMapper(name='TestDataset_0818_2',
                            type_id=data_types[0].id,
                            file_system_id=file_system_id,
                            file_path=inv_path_list[0],
                            description='0818用のデータセット_2',
                            delete_flag=False,
                            ml_component_id=ml_components[0].id,
                            file_hash_sha256=file_check_result_list[0]['hash_sha256']),
            InventoryMapper(name='TestDataset_0818_3',
                            type_id=data_types[0].id,
                            file_system_id=file_system_id,
                            file_path=inv_path_list[0],
                            description='0818用のデータセット_3',
                            delete_flag=False,
                            ml_component_id=ml_components[0].id,
                            file_hash_sha256=file_check_result_list[0]['hash_sha256'])]
    extensions.sql_db.session.add_all(invs)
    extensions.sql_db.session.flush()

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
               InventoryTDMapper(inventory_id=invs[6].id,
                                 test_description_id=test_descriptions[0].id,
                                 template_inventory_id=test_inventory_templates[0].id_),
               InventoryTDMapper(inventory_id=invs[7].id,
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
        InventoryFormatMapper(inventory_id=invs[5].id, format_id=format_[5].id),
        InventoryFormatMapper(inventory_id=invs[6].id, format_id=format_[0].id),
        InventoryFormatMapper(inventory_id=invs[7].id, format_id=format_[0].id)
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

    test_inventory_templates_dependency = [
        TestInventoryTemplateCompatiblePackageMapper(inventory_template_id=test_inventory_templates[0].id_,
                                              name='dummydependency1_1',
                                              version='0.1',
                                              additional_info='dummyadditional_info1_1'),
        TestInventoryTemplateCompatiblePackageMapper(inventory_template_id=test_inventory_templates[0].id_,
                                              name='dummydependency1_2',
                                              version='0.2',
                                              additional_info='dummyadditional_info1_2'),
        TestInventoryTemplateCompatiblePackageMapper(inventory_template_id=test_inventory_templates[1].id_,
                                              name='dummydependency2_1',
                                              version='0.3',
                                              additional_info='dummyadditional_info2_1')
    ]
    extensions.sql_db.session.add_all(test_inventory_templates_dependency)
    extensions.sql_db.session.flush()
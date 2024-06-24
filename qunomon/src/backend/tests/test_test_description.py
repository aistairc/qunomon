# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from datetime import datetime
from nose2.tools import such

from . import app
from qai_testbed_backend.usecases.test_description import TestDescriptionService
from qai_testbed_backend.controllers.dto.test_description import AppendTestDescriptionReqSchema, \
    PutTestDescriptionsReqSchema
from qai_testbed_backend.across.exception import QAIException, QAINotFoundException, QAIInvalidRequestException


with such.A('/<organizer_id>/ml_components/<ml_component_id>/testDescriptions') as it:

    # テスト実行時に1回実行
    @it.has_setup
    def setup():
        pass

    @it.has_teardown
    def teardown():
        pass

    # テスト関数読むたびに実行
    @it.has_test_setup
    def setup_each_test_case():
        pass

    @it.has_test_teardown
    def teardown_setup_each_test_case():
        pass

    def _add_dummy_td(organizer_id='dep-a', ml_component_id=1, parent_id=1) -> int:
        if parent_id == -1:
            post_json = {
                "Name": "Neuron Coverage",
                "QualityDimensionID": 5,
                "QualityMeasurements": [
                    {"Id": 1, "Value": "60", "RelationalOperatorId": 1, "Enable": True}
                ],
                "TargetInventories": [
                    {"Id": 1, "InventoryId": 1, "TemplateInventoryId": 1},
                    {"Id": 2, "InventoryId": 2, "TemplateInventoryId": 2}
                ],
                "TestRunner": {
                    "Id": 1,
                    "Params": [
                        {"TestRunnerParamTemplateId": 1, "Value": "0.5"},
                        {"TestRunnerParamTemplateId": 2, "Value": "0.3"},
                        {"TestRunnerParamTemplateId": 3, "Value": "1.0"}
                    ]
                }
            }
        else:
            post_json = {
                "Name": "Neuron Coverage",
                "QualityDimensionID": 5,
                "ParentID": parent_id,
                "QualityMeasurements": [
                    {"Id": 1, "Value": "60", "RelationalOperatorId": 1, "Enable": True}
                ],
                "TargetInventories": [
                    {"Id": 1, "InventoryId": 1, "TemplateInventoryId": 1},
                    {"Id": 2, "InventoryId": 2, "TemplateInventoryId": 2}
                ],
                "TestRunner": {
                    "Id": 1,
                    "Params": [
                        {"TestRunnerParamTemplateId": 1, "Value": "0.5"},
                        {"TestRunnerParamTemplateId": 2, "Value": "0.3"},
                        {"TestRunnerParamTemplateId": 3, "Value": "1.0"}
                    ]
                }
            }
        req = AppendTestDescriptionReqSchema().load(post_json)
        TestDescriptionService().append_test_description(organizer_id=organizer_id, ml_component_id=ml_component_id, req=req)

        res = TestDescriptionService().get_list(organizer_id=organizer_id, ml_component_id=ml_component_id)
        return res.test.test_descriptions[-1].id_

    with it.having('GET /<organizer_id>/ml_components/<ml_component_id>/testDescriptions'):
        @it.should('should return T12000.')
        def test():
            with app.app_context():
                res = TestDescriptionService().get_list(organizer_id='dep-a', ml_component_id=1)
                it.assertEqual(res.result.code, 'T12000')

        @it.should('should return test descriptions.')
        def test():
            with app.app_context():
                res = TestDescriptionService().get_list(organizer_id='dep-a', ml_component_id=1)
                it.assertIsInstance(res.test.id_, int)
                it.assertIsInstance(res.test.result, str)
                it.assertIsInstance(res.test.status, str)
                it.assertIsInstance(res.test.result_detail, str)
                it.assertNotEqual(res.test.id_, 0)
                it.assertNotEqual(res.test.result, '')
                it.assertNotEqual(res.test.status, '')
                it.assertNotEqual(res.test.result_detail, '')
                it.assertGreaterEqual(len(res.test.test_descriptions), 1)
                for td in res.test.test_descriptions:
                    it.assertIsInstance(td.id_, int)
                    it.assertIsInstance(td.name, str)
                    it.assertIsInstance(td.result, str)
                    it.assertIsInstance(td.result_detail, str)
                    it.assertIsInstance(td.creation_datetime, datetime)
                    it.assertIsInstance(td.update_datetime, datetime)
                    it.assertIsInstance(td.target_inventories, list)
                    for i in td.target_inventories:
                        it.assertIsInstance(i.id_, int)
                        it.assertIsInstance(i.name, str)
                        it.assertIsInstance(i.type_.id_, int)
                        it.assertIsInstance(i.type_.name, str)
                        it.assertIsInstance(i.description, str)
                        it.assertIsInstance(i.template_inventory_id, int)
                    it.assertIsInstance(td.opinion, str)

                    it.assertNotEqual(td.id_, 0)
                    it.assertNotEqual(td.name, '')
                    it.assertNotEqual(td.result, '')
                    it.assertNotEqual(td.result_detail, '')
                    it.assertIsNotNone(td.creation_datetime)
                    it.assertIsNotNone(td.update_datetime)
                    for i in td.target_inventories:
                        it.assertNotEqual(i.id_, 0)
                        it.assertNotEqual(i.name, '')
                        it.assertNotEqual(i.type_, '')
                        it.assertNotEqual(i.description, '')
                        it.assertNotEqual(i.template_inventory_id, 0)
                    it.assertIsNotNone(td.opinion)
                    it.assertIsInstance(td.star, bool)
                    it.assertNotEqual(td.test_runner_id, 0)
                    it.assertIsInstance(td.test_runner_id, int)

        @it.should('Organization is not Exists. should return T14001.')
        def test():
            with app.app_context():
                try:
                    res = TestDescriptionService().get_list(organizer_id='dep-hoge', ml_component_id=1)
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'T14001')

    with it.having('GET /<organizer_id>/ml_components/<ml_component_id>/testDescriptions/<testdescription_id>'):
        @it.should('should return T32000.')
        def test():
            with app.app_context():
                res = TestDescriptionService().get(organizer_id='dep-a', ml_component_id=1, testdescription_id=3)
                it.assertEqual(res.result.code, 'T32000')

        @it.should('Organization is not Exists. should return I34002.')
        def test():
            with app.app_context():
                try:
                    res = TestDescriptionService().get(organizer_id='dep-hoge', ml_component_id=1, testdescription_id=1)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'I34002')

    with it.having('POST /<organizer_id>/ml_components/<ml_component_id>/testDescriptions'):
        @it.should('should return T22000.')
        def test():
            post_json = {
                "Name": "Neuron Coverage",
                "QualityDimensionID": 5,
                "ParentID": 1,
                "QualityMeasurements": [
                    {"Id": 1, "Value": "60", "RelationalOperatorId": 1, "Enable": True}
                ],
                "TargetInventories": [
                    {"Id": 1, "InventoryId": 1, "TemplateInventoryId": 1},
                    {"Id": 2, "InventoryId": 2, "TemplateInventoryId": 2}
                ],
                "TestRunner": {
                    "Id": 1,
                    "Params": [
                        {"TestRunnerParamTemplateId": 1, "Value": "0.5"},
                        {"TestRunnerParamTemplateId": 2, "Value": "0.3"},
                        {"TestRunnerParamTemplateId": 3, "Value": "1.0"}
                    ]
                }
            }
            req = AppendTestDescriptionReqSchema().load(post_json)

            with app.app_context():
                res = TestDescriptionService().get_list(organizer_id='dep-a', ml_component_id=1)
                td_count = len(res.test.test_descriptions)

                res = TestDescriptionService().append_test_description(organizer_id='dep-a', ml_component_id=1, req=req)
                it.assertEqual(res.result.code, 'T22000')

                res = TestDescriptionService().get_list(organizer_id='dep-a', ml_component_id=1)
                td_count_2 = len(res.test.test_descriptions)

                it.assertEqual(td_count+1, td_count_2)

                it.assertFalse(res.test.test_descriptions[-1].star)


        @it.should('should add test description.')
        def test():
            post_json = {
                "Name": "TestAddTD",
                "QualityDimensionID": 5,
                "ParentID": 2,
                "QualityMeasurements": [
                    {"Id": 1, "Value": "70", "RelationalOperatorId": 2, "Enable": False}
                ],
                "TargetInventories": [
                    {"Id": 1, "InventoryId": 3, "TemplateInventoryId": 1},
                    {"Id": 2, "InventoryId": 4, "TemplateInventoryId": 2}
                ],
                "TestRunner": {
                    "Id": 1,
                    "Params": [
                        {"TestRunnerParamTemplateId": 1, "Value": "0.1"},
                        {"TestRunnerParamTemplateId": 2, "Value": "0.2"},
                        {"TestRunnerParamTemplateId": 3, "Value": "0.3"}
                    ]
                }
            }
            req = AppendTestDescriptionReqSchema().load(post_json)

            with app.app_context():
                res = TestDescriptionService().append_test_description(organizer_id='dep-a', ml_component_id=1,
                                                                       req=req)
                it.assertEqual(res.result.code, 'T22000')

                # 一覧取得が正しいか確認
                res = TestDescriptionService().get_list(organizer_id='dep-a', ml_component_id=1)
                it.assertEqual(res.test.test_descriptions[-1].name, post_json['Name'])
                it.assertEqual(res.test.test_descriptions[-1].parent_id, post_json['ParentID'])

                # 詳細取得が正しいか確認
                td_id = res.test.test_descriptions[-1].id_
                res = TestDescriptionService().get(organizer_id='dep-a', ml_component_id=1,
                                                   testdescription_id=td_id)
                it.assertEqual(res.test_description_detail.name, post_json['Name'])
                it.assertEqual(res.test_description_detail.parent_id, post_json['ParentID'])
                it.assertEqual(res.test_description_detail.quality_dimension.id_, post_json['QualityDimensionID'])
                it.assertEqual(res.test_description_detail.test_runner.id_, post_json['TestRunner']['Id'])
                for m in res.test_description_detail.quality_measurements:
                    measure_json = [j for j in post_json['QualityMeasurements'] if j['Id'] == m.id_][0]
                    it.assertEqual(m.value, measure_json['Value'])
                    it.assertEqual(m.relational_operator_id, measure_json['RelationalOperatorId'])
                    it.assertEqual(m.enable, measure_json['Enable'])
                for t in res.test_description_detail.target_inventories:
                    inv_json = [j for j in post_json['TargetInventories']
                                if j['TemplateInventoryId'] == t.template_inventory_id][0]
                    it.assertEqual(t.id_, inv_json['InventoryId'])

                for p in res.test_description_detail.test_runner.params:
                    param_json = [j for j in post_json['TestRunner']['Params']
                                  if j['TestRunnerParamTemplateId'] == p.test_runner_param_template_id][0]
                    it.assertEqual(p.value, param_json['Value'])

                it.assertFalse(res.test_description_detail.star)

        @it.should('should be value_target true if QualityMeasurements is Exists.')
        def test():
            post_json = {
                "Name": "Neuron Coverage",
                "QualityDimensionID": 5,
                "ParentID": 1,
                "QualityMeasurements": [
                    {"Id": 1, "Value": "60", "RelationalOperatorId": 1, "Enable": True}
                ],
                "TargetInventories": [
                    {"Id": 1, "InventoryId": 1, "TemplateInventoryId": 1},
                    {"Id": 2, "InventoryId": 2, "TemplateInventoryId": 2}
                ],
                "TestRunner": {
                    "Id": 1,
                    "Params": [
                        {"TestRunnerParamTemplateId": 1, "Value": "0.5"},
                        {"TestRunnerParamTemplateId": 2, "Value": "0.3"},
                        {"TestRunnerParamTemplateId": 3, "Value": "1.0"}
                    ]
                }
            }
            req = AppendTestDescriptionReqSchema().load(post_json)

            with app.app_context():
                from qai_testbed_backend.entities.test_description import TestDescriptionMapper

                res = TestDescriptionService().append_test_description(organizer_id='dep-a', ml_component_id=1, req=req)
                it.assertEqual(res.result.code, 'T22000')

                res = TestDescriptionService().get_list(organizer_id='dep-a', ml_component_id=1)
                td_id = res.test.test_descriptions[-1].id_

                it.assertTrue(TestDescriptionMapper.query.get(td_id).value_target)

        @it.should('should be value_target false if QualityMeasurements is not Exists.')
        def test():
            post_json = {
                "Name": "Neuron Coverage",
                "QualityDimensionID": 5,
                "ParentID": 1,
                "QualityMeasurements": [],
                "TargetInventories": [
                    {"Id": 1, "InventoryId": 1, "TemplateInventoryId": 1},
                    {"Id": 2, "InventoryId": 2, "TemplateInventoryId": 2}
                ],
                "TestRunner": {
                    "Id": 1,
                    "Params": [
                        {"TestRunnerParamTemplateId": 1, "Value": "0.5"},
                        {"TestRunnerParamTemplateId": 2, "Value": "0.3"},
                        {"TestRunnerParamTemplateId": 3, "Value": "1.0"}
                    ]
                }
            }
            req = AppendTestDescriptionReqSchema().load(post_json)

            with app.app_context():
                from qai_testbed_backend.entities.test_description import TestDescriptionMapper

                res = TestDescriptionService().append_test_description(organizer_id='dep-a', ml_component_id=1, req=req)
                it.assertEqual(res.result.code, 'T22000')

                res = TestDescriptionService().get_list(organizer_id='dep-a', ml_component_id=1)
                td_id = res.test.test_descriptions[-1].id_

                it.assertFalse(TestDescriptionMapper.query.get(td_id).value_target)

    with it.having('PUT /<organizer_id>/ml_components/<ml_component_id>/testDescriptions/<testdescription_id>'):
        @it.should('should return T42000.')
        def test():
            post_json = {
                "Name": "Neuron Coverage2",
                "QualityDimensionID": 5,
                "QualityMeasurements": [
                    {"Id": 1, "Value": "70", "RelationalOperatorId": 1, "Enable": False}
                ],
                "TargetInventories": [
                    {"Id": 1, "InventoryId": 3, "TemplateInventoryId": 3},
                    {"Id": 2, "InventoryId": 4, "TemplateInventoryId": 4}
                ],
                "TestRunner": {
                    "Id": 1,
                    "Params": [
                        {"TestRunnerParamTemplateId": 1, "Value": "0.6"},
                        {"TestRunnerParamTemplateId": 2, "Value": "0.4"},
                        {"TestRunnerParamTemplateId": 3, "Value": "1.0"},
                        # ブランク時にも登録可能
                        {"TestRunnerParamTemplateId": 4, "Value": ""}
                    ]
                }
            }
            req = PutTestDescriptionsReqSchema().load(post_json)

            with app.app_context():
                td_id = 1

                before_change_td = TestDescriptionService().get(
                    organizer_id='dep-a', ml_component_id=1, testdescription_id=td_id).test_description_detail

                res = TestDescriptionService().put_test_descriptions(organizer_id='dep-a', ml_component_id=1,
                                                                     testdescription_id=td_id, req=req)
                it.assertEqual(res.result.code, 'T42000')

                # 一覧取得が正しいか確認
                res = TestDescriptionService().get_list(organizer_id='dep-a', ml_component_id=1)
                it.assertEqual([t.name for t in res.test.test_descriptions if t.id_ == td_id][0], post_json['Name'])
                it.assertEqual([t.parent_id for t in res.test.test_descriptions if t.id_ == td_id][0],
                               before_change_td.parent_id)

                # 詳細取得が正しいか確認
                res = TestDescriptionService().get(organizer_id='dep-a', ml_component_id=1, testdescription_id=td_id)
                it.assertEqual(res.test_description_detail.name, post_json['Name'])
                it.assertEqual(res.test_description_detail.parent_id, before_change_td.parent_id)
                it.assertEqual(res.test_description_detail.quality_dimension.id_, post_json['QualityDimensionID'])
                it.assertEqual(res.test_description_detail.test_runner.id_, post_json['TestRunner']['Id'])
                for m in res.test_description_detail.quality_measurements:
                    measure_json = [j for j in post_json['QualityMeasurements'] if j['Id'] == m.id_][0]
                    it.assertEqual(m.value, measure_json['Value'])
                    it.assertEqual(m.relational_operator_id, measure_json['RelationalOperatorId'])
                    it.assertEqual(m.enable, measure_json['Enable'])
                for t in res.test_description_detail.target_inventories:
                    inv_json = [j for j in post_json['TargetInventories']
                                if j['TemplateInventoryId'] == t.template_inventory_id][0]
                    it.assertEqual(t.id_, inv_json['InventoryId'])

                for p in res.test_description_detail.test_runner.params:
                    param_json = [j for j in post_json['TestRunner']['Params']
                                  if j['TestRunnerParamTemplateId'] == p.test_runner_param_template_id][0]
                    it.assertEqual(p.value, param_json['Value'])

                it.assertEqual(res.test_description_detail.creation_datetime, before_change_td.creation_datetime)
                it.assertNotEqual(res.test_description_detail.update_datetime, before_change_td.update_datetime)
                it.assertEqual(res.test_description_detail.star, before_change_td.star)

        @it.should('should edit test description.')
        def test():
            post_json = {
                "Name": "Neuron Coverage2",
                "QualityDimensionID": 5,
                "QualityMeasurements": [
                    {"Id": 1, "Value": "70", "RelationalOperatorId": 1, "Enable": False}
                ],
                "TargetInventories": [
                    {"Id": 1, "InventoryId": 3, "TemplateInventoryId": 3},
                    {"Id": 2, "InventoryId": 4, "TemplateInventoryId": 4}
                ],
                "TestRunner": {
                    "Id": 1,
                    "Params": [
                        {"TestRunnerParamTemplateId": 1, "Value": "0.6"},
                        {"TestRunnerParamTemplateId": 2, "Value": "0.4"},
                        {"TestRunnerParamTemplateId": 3, "Value": "1.0"}
                    ]
                }
            }
            req = PutTestDescriptionsReqSchema().load(post_json)

            with app.app_context():
                res = TestDescriptionService().put_test_descriptions(organizer_id='dep-a', ml_component_id=1,
                                                                     testdescription_id=1, req=req)
                it.assertEqual(res.result.code, 'T42000')

        @it.should('should be value_target true if QualityMeasurements is Exists.')
        def test():
            post_json = {
                "Name": "Neuron Coverage2",
                "QualityDimensionID": 1,
                "QualityMeasurements": [
                    {"Id": 1, "Value": "70", "RelationalOperatorId": 1, "Enable": False}
                ],
                "TargetInventories": [
                    {"Id": 1, "InventoryId": 3, "TemplateInventoryId": 3},
                    {"Id": 2, "InventoryId": 4, "TemplateInventoryId": 4}
                ],
                "TestRunner": {
                    "Id": 1,
                    "Params": [
                        {"TestRunnerParamTemplateId": 1, "Value": "0.6"},
                        {"TestRunnerParamTemplateId": 2, "Value": "0.4"},
                        {"TestRunnerParamTemplateId": 3, "Value": "1.0"}
                    ]
                }
            }
            req = PutTestDescriptionsReqSchema().load(post_json)

            with app.app_context():
                from qai_testbed_backend.entities.test_description import TestDescriptionMapper
                td_id = 1
                res = TestDescriptionService().put_test_descriptions(organizer_id='dep-a', ml_component_id=1,
                                                                     testdescription_id=td_id, req=req)
                it.assertEqual(res.result.code, 'T42000')
                it.assertTrue(TestDescriptionMapper.query.get(td_id).value_target)

        @it.should('should be value_target false if QualityMeasurements is not Exists.')
        def test():
            post_json = {
                "Name": "Neuron Coverage2",
                "QualityDimensionID": 5,
                "QualityMeasurements": [],
                "TargetInventories": [
                    {"Id": 1, "InventoryId": 3, "TemplateInventoryId": 3},
                    {"Id": 2, "InventoryId": 4, "TemplateInventoryId": 4}
                ],
                "TestRunner": {
                    "Id": 1,
                    "Params": [
                        {"TestRunnerParamTemplateId": 1, "Value": "0.6"},
                        {"TestRunnerParamTemplateId": 2, "Value": "0.4"},
                        {"TestRunnerParamTemplateId": 3, "Value": "1.0"}
                    ]
                }
            }
            req = PutTestDescriptionsReqSchema().load(post_json)

            with app.app_context():
                from qai_testbed_backend.entities.test_description import TestDescriptionMapper
                td_id = 1
                res = TestDescriptionService().put_test_descriptions(organizer_id='dep-a', ml_component_id=1,
                                                                     testdescription_id=td_id, req=req)
                it.assertEqual(res.result.code, 'T42000')
                it.assertFalse(TestDescriptionMapper.query.get(td_id).value_target)

        @it.should('should be an error if the TestRunnerParamTemplate does not exist.')
        def test():
            post_json = {
                "Name": "Neuron Coverage",
                "QualityDimensionID": 5,
                "ParentID": 1,
                "QualityMeasurements": [],
                "TargetInventories": [
                    {"Id": 1, "InventoryId": 1, "TemplateInventoryId": 1},
                    {"Id": 2, "InventoryId": 2, "TemplateInventoryId": 2}
                ],
                "TestRunner": {
                    "Id": 1,
                    "Params": [
                        # 存在しないTestRunnerParamTemplateId
                        {"TestRunnerParamTemplateId": 991, "Value": "0.5"},
                        {"TestRunnerParamTemplateId": 992, "Value": "0.3"},
                        {"TestRunnerParamTemplateId": 993, "Value": "1.0"}
                    ]
                }
            }
            req = AppendTestDescriptionReqSchema().load(post_json)
            
            with app.app_context():
                from qai_testbed_backend.entities.test_description import TestDescriptionMapper
                try:
                    res = TestDescriptionService().append_test_description(organizer_id='dep-a', ml_component_id=1, req=req)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'T94000')

        @it.should('should be an error if the parameter value is non-numeric.')
        def test():
            post_json = {
                "Name": "Neuron Coverage",
                "QualityDimensionID": 5,
                "ParentID": 1,
                "QualityMeasurements": [],
                "TargetInventories": [
                    {"Id": 1, "InventoryId": 1, "TemplateInventoryId": 1},
                    {"Id": 2, "InventoryId": 2, "TemplateInventoryId": 2}
                ],
                "TestRunner": {
                    "Id": 1,
                    "Params": [
                        {"TestRunnerParamTemplateId": 1, "Value": "0.5"},
                        {"TestRunnerParamTemplateId": 2, "Value": "0.3"},
                        # 数値型のパラメータ値にアルファベットを入力
                        {"TestRunnerParamTemplateId": 3, "Value": "abc"}
                    ]
                }
            }
            req = AppendTestDescriptionReqSchema().load(post_json)
            
            with app.app_context():
                from qai_testbed_backend.entities.test_description import TestDescriptionMapper
                try:
                    res = TestDescriptionService().append_test_description(organizer_id='dep-a', ml_component_id=1, req=req)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'T94001')

        @it.should('should an error if the parameter value exceeds the maximum float type.')
        def test():
            post_json = {
                "Name": "Neuron Coverage",
                "QualityDimensionID": 5,
                "ParentID": 1,
                "QualityMeasurements": [],
                "TargetInventories": [
                    {"Id": 1, "InventoryId": 1, "TemplateInventoryId": 1},
                    {"Id": 2, "InventoryId": 2, "TemplateInventoryId": 2}
                ],
                "TestRunner": {
                    "Id": 1,
                    "Params": [
                        {"TestRunnerParamTemplateId": 1, "Value": "0.5"},
                        {"TestRunnerParamTemplateId": 2, "Value": "0.3"},
                        # float型の最大3.402823e+38を超える入力値
                        {"TestRunnerParamTemplateId": 3, "Value": "3.402823e+39"}
                    ]
                }
            }
            req = AppendTestDescriptionReqSchema().load(post_json)
            
            with app.app_context():
                from qai_testbed_backend.entities.test_description import TestDescriptionMapper
                try:
                    res = TestDescriptionService().append_test_description(organizer_id='dep-a', ml_component_id=1, req=req)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'T94001')

        @it.should('should result in an error if the parameter value is greater than the max_valu.')
        def test():
            post_json = {
                "Name": "Neuron Coverage",
                "QualityDimensionID": 5,
                "ParentID": 1,
                "QualityMeasurements": [],
                "TargetInventories": [
                    {"Id": 1, "InventoryId": 1, "TemplateInventoryId": 1},
                    {"Id": 2, "InventoryId": 2, "TemplateInventoryId": 2}
                ],
                "TestRunner": {
                    "Id": 1,
                    "Params": [
                        {"TestRunnerParamTemplateId": 1, "Value": "0.5"},
                        {"TestRunnerParamTemplateId": 2, "Value": "0.3"},
                        #max_valu=1.0より大きいエラー値
                        {"TestRunnerParamTemplateId": 3, "Value": "1.1"}
                    ]
                }
            }
            req = AppendTestDescriptionReqSchema().load(post_json)
            
            with app.app_context():
                from qai_testbed_backend.entities.test_description import TestDescriptionMapper
                try:
                    res = TestDescriptionService().append_test_description(organizer_id='dep-a', ml_component_id=1, req=req)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'T94001')

        @it.should('Should result in an error if the parameter value is less than the min_value.')
        def test():
            post_json = {
                "Name": "Neuron Coverage",
                "QualityDimensionID": 5,
                "ParentID": 1,
                "QualityMeasurements": [],
                "TargetInventories": [
                    {"Id": 1, "InventoryId": 1, "TemplateInventoryId": 1},
                    {"Id": 2, "InventoryId": 2, "TemplateInventoryId": 2}
                ],
                "TestRunner": {
                    "Id": 1,
                    "Params": [
                        #min_value=0.0より小さいエラー値
                        {"TestRunnerParamTemplateId": 1, "Value": "-0.5"},
                        {"TestRunnerParamTemplateId": 2, "Value": "0.3"},
                        {"TestRunnerParamTemplateId": 3, "Value": "1.0"}
                    ]
                }
            }
            req = AppendTestDescriptionReqSchema().load(post_json)
            
            with app.app_context():
                from qai_testbed_backend.entities.test_description import TestDescriptionMapper
                try:
                    res = TestDescriptionService().append_test_description(organizer_id='dep-a', ml_component_id=1, req=req)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'T94001')

        @it.should('should be an error if the QualityMeasurement does not exist.')
        def test():
            post_json = {
                "Name": "Neuron Coverage2",
                "QualityDimensionID": 1,
                "QualityMeasurements": [
                    # 存在しないQualityMeasurementId
                    {"Id": 99, "Value": "70", "RelationalOperatorId": 1, "Enable": True}
                ],
                "TargetInventories": [
                    {"Id": 1, "InventoryId": 3, "TemplateInventoryId": 3},
                    {"Id": 2, "InventoryId": 4, "TemplateInventoryId": 4}
                ],
                "TestRunner": {
                    "Id": 1,
                    "Params": [
                        {"TestRunnerParamTemplateId": 1, "Value": "0.6"},
                        {"TestRunnerParamTemplateId": 2, "Value": "0.4"},
                        {"TestRunnerParamTemplateId": 3, "Value": "1.0"}
                    ]
                }
            }
            req = AppendTestDescriptionReqSchema().load(post_json)
            
            with app.app_context():
                from qai_testbed_backend.entities.test_description import TestDescriptionMapper
                try:
                    res = TestDescriptionService().append_test_description(organizer_id='dep-a', ml_component_id=1, req=req)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'TA4000')

        @it.should('should be an error if the measurement value is non-numeric.')
        def test():
            post_json = {
                "Name": "Neuron Coverage2",
                "QualityDimensionID": 1,
                "QualityMeasurements": [
                    # 数値型のMeasurement値にアルファベットを入力
                    {"Id": 1, "Value": "abc", "RelationalOperatorId": 1, "Enable": True}
                ],
                "TargetInventories": [
                    {"Id": 1, "InventoryId": 3, "TemplateInventoryId": 3},
                    {"Id": 2, "InventoryId": 4, "TemplateInventoryId": 4}
                ],
                "TestRunner": {
                    "Id": 1,
                    "Params": [
                        {"TestRunnerParamTemplateId": 1, "Value": "0.6"},
                        {"TestRunnerParamTemplateId": 2, "Value": "0.4"},
                        {"TestRunnerParamTemplateId": 3, "Value": "1.0"}
                    ]
                }
            }
            req = AppendTestDescriptionReqSchema().load(post_json)
            
            with app.app_context():
                from qai_testbed_backend.entities.test_description import TestDescriptionMapper
                try:
                    res = TestDescriptionService().append_test_description(organizer_id='dep-a', ml_component_id=1, req=req)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'TA4001')

        @it.should('should an error if the measurement value exceeds the maximum float type.')
        def test():
            post_json = {
                "Name": "Neuron Coverage2",
                "QualityDimensionID": 1,
                "QualityMeasurements": [
                    # float型の最大3.402823e+38を超える入力値
                    {"Id": 1, "Value": "3.402823e+39", "RelationalOperatorId": 1, "Enable": True}
                ],
                "TargetInventories": [
                    {"Id": 1, "InventoryId": 3, "TemplateInventoryId": 3},
                    {"Id": 2, "InventoryId": 4, "TemplateInventoryId": 4}
                ],
                "TestRunner": {
                    "Id": 1,
                    "Params": [
                        {"TestRunnerParamTemplateId": 1, "Value": "0.6"},
                        {"TestRunnerParamTemplateId": 2, "Value": "0.4"},
                        {"TestRunnerParamTemplateId": 3, "Value": "1.0"}
                    ]
                }
            }
            req = AppendTestDescriptionReqSchema().load(post_json)
            
            with app.app_context():
                from qai_testbed_backend.entities.test_description import TestDescriptionMapper
                try:
                    res = TestDescriptionService().append_test_description(organizer_id='dep-a', ml_component_id=1, req=req)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'TA4001')

        @it.should('should result in an error if the measurement value is greater than the max_valu.')
        def test():
            post_json = {
                "Name": "Neuron Coverage2",
                "QualityDimensionID": 1,
                "QualityMeasurements": [
                    #max_valu=100より大きいエラー値
                    {"Id": 1, "Value": "101.0", "RelationalOperatorId": 1, "Enable": True}
                ],
                "TargetInventories": [
                    {"Id": 1, "InventoryId": 3, "TemplateInventoryId": 3},
                    {"Id": 2, "InventoryId": 4, "TemplateInventoryId": 4}
                ],
                "TestRunner": {
                    "Id": 1,
                    "Params": [
                        {"TestRunnerParamTemplateId": 1, "Value": "0.6"},
                        {"TestRunnerParamTemplateId": 2, "Value": "0.4"},
                        {"TestRunnerParamTemplateId": 3, "Value": "1.0"}
                    ]
                }
            }
            req = AppendTestDescriptionReqSchema().load(post_json)
            
            with app.app_context():
                from qai_testbed_backend.entities.test_description import TestDescriptionMapper
                try:
                    res = TestDescriptionService().append_test_description(organizer_id='dep-a', ml_component_id=1, req=req)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'TA4001')

        @it.should('Should result in an error if the measurement value is less than the min_value.')
        def test():
            post_json = {
                "Name": "Neuron Coverage2",
                "QualityDimensionID": 1,
                "QualityMeasurements": [
                    #min_value=0.0より小さいエラー値
                    {"Id": 1, "Value": "-1.0", "RelationalOperatorId": 1, "Enable": True}
                ],
                "TargetInventories": [
                    {"Id": 1, "InventoryId": 3, "TemplateInventoryId": 3},
                    {"Id": 2, "InventoryId": 4, "TemplateInventoryId": 4}
                ],
                "TestRunner": {
                    "Id": 1,
                    "Params": [
                        {"TestRunnerParamTemplateId": 1, "Value": "0.6"},
                        {"TestRunnerParamTemplateId": 2, "Value": "0.4"},
                        {"TestRunnerParamTemplateId": 3, "Value": "1.0"}
                    ]
                }
            }
            req = AppendTestDescriptionReqSchema().load(post_json)
            
            with app.app_context():
                from qai_testbed_backend.entities.test_description import TestDescriptionMapper
                try:
                    res = TestDescriptionService().append_test_description(organizer_id='dep-a', ml_component_id=1, req=req)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'TA4001')

        @it.should('Organization is not Exists. should return T44002.')
        def test():
            post_json = {
                "Name": "Neuron Coverage2",
                "QualityDimensionID": 5,
                "QualityMeasurements": [],
                "TargetInventories": [],
                "TestRunner": {
                    "Id": 1,
                    "Params": []
                }
            }
            req = PutTestDescriptionsReqSchema().load(post_json)

            with app.app_context():
                from qai_testbed_backend.entities.test_description import TestDescriptionMapper
                td_id = 1
                try:
                    res = TestDescriptionService().put_test_descriptions(organizer_id='dep-hoge', ml_component_id=1,
                                                                         testdescription_id=td_id, req=req)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'T44002')

        @it.should('Organization is not Exists. should return T24001.')
        def test():
            post_json = {
                "Name": "Neuron Coverage2",
                "QualityDimensionID": 1,
                "QualityMeasurements": [],
                "TargetInventories": [],
                "TestRunner": {
                    "Id": 1,
                    "Params": []
                }
            }
            req = AppendTestDescriptionReqSchema().load(post_json)
            
            with app.app_context():
                from qai_testbed_backend.entities.test_description import TestDescriptionMapper
                try:
                    res = TestDescriptionService().append_test_description(organizer_id='dep-hoge', ml_component_id=1, req=req)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'T24001')

    with it.having('POST /<organizer_id>/ml_components/<ml_component_id>/testDescriptions/<testdescription_id>/star'):
        @it.should('should return T62000.')
        def test():
            with app.app_context():
                res = TestDescriptionService().set_star(organizer_id='dep-a', ml_component_id=1, test_description_id=3)
                it.assertEqual(res.code, 'T62000')

        @it.should('should set star.')
        def test():
            with app.app_context():
                td_id = _add_dummy_td()
                res = TestDescriptionService().get(organizer_id='dep-a', ml_component_id=1, testdescription_id=td_id)
                it.assertFalse(res.test_description_detail.star)

                TestDescriptionService().set_star(organizer_id='dep-a', ml_component_id=1, test_description_id=td_id)

                res = TestDescriptionService().get(organizer_id='dep-a', ml_component_id=1, testdescription_id=td_id)
                it.assertTrue(res.test_description_detail.star)

        @it.should('should return T64000 if TD not found.')
        def test():
            with app.app_context():
                try:
                    TestDescriptionService().set_star(organizer_id='dep-a', ml_component_id=1,
                                                      test_description_id=999  # not found id
                                                      )
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'T64000')

        @it.should('should return T65000 if TD was deleted.')
        def test():
            with app.app_context():
                td_id = _add_dummy_td()
                TestDescriptionService().delete_test_description(organizer_id='dep-a', ml_component_id=1,
                                                                 testdescription_id=td_id)
                try:
                    TestDescriptionService().set_star(organizer_id='dep-a', ml_component_id=1,
                                                      test_description_id=td_id)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'T65000')

        @it.should('should return T64001 if Organization is not Exists.')
        def test():
            with app.app_context():
                td_id = _add_dummy_td()
                try:
                    TestDescriptionService().set_star(organizer_id='dep-hoge', ml_component_id=1,
                                                      test_description_id=td_id)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'T64001')

    with it.having('POST /<organizer_id>/ml_components/<ml_component_id>/testDescriptions/<testdescription_id>/unstar'):
        @it.should('should return T72000.')
        def test():
            with app.app_context():
                res = TestDescriptionService().set_unstar(organizer_id='dep-a', ml_component_id=1, test_description_id=3)
                it.assertEqual(res.code, 'T72000')

        @it.should('should set unstar.')
        def test():
            with app.app_context():
                td_id = _add_dummy_td()
                res = TestDescriptionService().get(organizer_id='dep-a', ml_component_id=1, testdescription_id=td_id)
                it.assertFalse(res.test_description_detail.star)

                TestDescriptionService().set_star(organizer_id='dep-a', ml_component_id=1, test_description_id=td_id)

                res = TestDescriptionService().get(organizer_id='dep-a', ml_component_id=1, testdescription_id=td_id)
                it.assertTrue(res.test_description_detail.star)

                TestDescriptionService().set_unstar(organizer_id='dep-a', ml_component_id=1, test_description_id=td_id)

                res = TestDescriptionService().get(organizer_id='dep-a', ml_component_id=1, testdescription_id=td_id)
                it.assertFalse(res.test_description_detail.star)

        @it.should('should return T74000 if TD not found.')
        def test():
            with app.app_context():
                try:
                    TestDescriptionService().set_unstar(organizer_id='dep-a', ml_component_id=1,
                                                        test_description_id=999  # not found id
                                                        )
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'T74000')

        @it.should('should return T75000 if TD was deleted.')
        def test():
            with app.app_context():
                td_id = _add_dummy_td()
                TestDescriptionService().delete_test_description(organizer_id='dep-a', ml_component_id=1,
                                                                 testdescription_id=td_id)
                try:
                    TestDescriptionService().set_unstar(organizer_id='dep-a', ml_component_id=1,
                                                        test_description_id=td_id)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'T75000')

        @it.should('should return T74001 if Organization is not Exists.')
        def test():
            with app.app_context():
                try:
                    TestDescriptionService().set_unstar(organizer_id='dep-hoge', ml_component_id=1,
                                                        test_description_id=999)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'T74001')

    with it.having('GET /<organizer_id>/ml_components/<ml_component_id>/testDescriptions/<testdescription_id>/'
                   'ancestors'):
        @it.should('should return T82000.')
        def test():
            with app.app_context():
                res = TestDescriptionService().get_ancestor(organizer_id='dep-a',
                                                            ml_component_id=1,
                                                            test_description_id=1)
                it.assertEqual(res.result.code, 'T82000')

        @it.should('should return ancestors.')
        def test():
            with app.app_context():
                td_id_1 = _add_dummy_td(parent_id=-1)
                td_id_2 = _add_dummy_td(parent_id=td_id_1)
                td_id_2_2 = _add_dummy_td(parent_id=td_id_1)
                td_id_3 = _add_dummy_td(parent_id=td_id_2)
                td_id_3_2 = _add_dummy_td(parent_id=td_id_2_2)
                td_id_4 = _add_dummy_td(parent_id=td_id_3)

                res = TestDescriptionService().get_ancestor(organizer_id='dep-a',
                                                            ml_component_id=1,
                                                            test_description_id=td_id_4)
                it.assertEqual(len(res.test_descriptions), 4)
                it.assertEqual([td.id_ for td in res.test_descriptions], [td_id_1, td_id_2, td_id_3, td_id_4])

                res = TestDescriptionService().get_ancestor(organizer_id='dep-a',
                                                            ml_component_id=1,
                                                            test_description_id=td_id_3_2)
                it.assertEqual(len(res.test_descriptions), 3)
                it.assertEqual([td.id_ for td in res.test_descriptions], [td_id_1, td_id_2_2, td_id_3_2])

                res = TestDescriptionService().get_ancestor(organizer_id='dep-a',
                                                            ml_component_id=1,
                                                            test_description_id=td_id_1)
                it.assertEqual(len(res.test_descriptions), 1)
                it.assertEqual([td.id_ for td in res.test_descriptions], [td_id_1])

        @it.should('should return T84000 if TD not found.')
        def test():
            with app.app_context():
                try:
                    TestDescriptionService().get_ancestor(organizer_id='dep-a', ml_component_id=1,
                                                          test_description_id=999  # not found id
                                                         )
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'T84000')

        @it.should('should return T85000 if TD was deleted.')
        def test():
            with app.app_context():
                td_id = _add_dummy_td()
                TestDescriptionService().delete_test_description(organizer_id='dep-a', ml_component_id=1,
                                                                 testdescription_id=td_id)
                try:
                    TestDescriptionService().get_ancestor(organizer_id='dep-a', ml_component_id=1,
                                                          test_description_id=td_id)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'T85000')

        @it.should('should return T84001 if Organization is not Exists.')
        def test():
            with app.app_context():
                try:
                    TestDescriptionService().get_ancestor(organizer_id='dep-hoge', ml_component_id=1,
                                                          test_description_id=999)
                    it.fail()
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'T84001')

    with it.having('GET /testRunners/<testRunnerId>/usingTD/'):
        @it.should('should return A03000.')
        def test():
            with app.app_context():
                res = TestDescriptionService().get_using(test_runner_id=1)
                it.assertEqual(res.result.code, 'A03000')
                it.assertGreaterEqual(len(res.using_Test_Descriptions), 1)

                res = TestDescriptionService().get_using(test_runner_id=2)
                it.assertEqual(res.result.code, 'A03000')
                it.assertGreaterEqual(len(res.using_Test_Descriptions), 1)

                res = TestDescriptionService().get_using(test_runner_id=3)
                it.assertEqual(res.result.code, 'A03000')
                it.assertGreaterEqual(len(res.using_Test_Descriptions), 1)

                # 検索結果が0件でもエラーにならない
                res = TestDescriptionService().get_using(test_runner_id=99)
                it.assertEqual(res.result.code, 'A03000')
                it.assertEqual(len(res.using_Test_Descriptions), 0)
                
it.createTests(globals())

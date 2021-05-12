# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from nose2.tools import such
import tempfile
from pathlib import Path

from . import app
from qai_testbed_backend.usecases.ml_component import MLComponentService
from qai_testbed_backend.usecases.ml_framework import MLFrameworkService
from qai_testbed_backend.usecases.test_description import TestDescriptionService
from qai_testbed_backend.usecases.inventory import InventoryService
from qai_testbed_backend.controllers.dto.ml_component import PostMLComponentReq
from qai_testbed_backend.controllers.dto.inventory import AppendInventoryReq
from qai_testbed_backend.controllers.dto.test_description import AppendTestDescriptionReqSchema
from qai_testbed_backend.across.exception import QAIException, QAINotFoundException


with such.A('MLComponents') as it:

    with it.having('GET /MLComponents'):
        @it.should('should return P12000.')
        def test():
            with app.app_context():
                response = MLComponentService().get_ml_component_list(organizer_id='dep-a')
                it.assertEqual(response.result.code, 'P12000')

        @it.should('should return MLComponent schema.')
        def test():
            with app.app_context():
                response = MLComponentService().get_ml_component_list(organizer_id='dep-a')
                it.assertGreaterEqual(len(response.ml_components), 3)

                for c in response.ml_components:
                    it.assertTrue(type(c.id_) == int)
                    it.assertNotEqual(c.id_, 0)
                    it.assertTrue(type(c.name) == str)
                    it.assertNotEqual(c.name, '')
                    it.assertTrue(type(c.description) == str)
                    it.assertNotEqual(c.description, '')
                    it.assertTrue(type(c.problem_domain) == str)
                    it.assertNotEqual(c.problem_domain, '')
                    it.assertTrue(type(c.ml_framework_name) == str)
                    it.assertNotEqual(c.ml_framework_name, '')

    with it.having('POST /MLComponents'):
        @it.should('should return P22000.')
        def test():
            with app.app_context():
                frameworks = MLFrameworkService().get().ml_frameworks
                req = PostMLComponentReq(name='Fashion Classifier',
                                         description='Fashion image classification',
                                         problem_domain='ImageClassification',
                                         ml_framework_id=frameworks[0].id)
                response = MLComponentService().post(organizer_id='dep-a', req=req)
                it.assertEqual(response.result.code, 'P22000')

        @it.should('should return P24000 if org_id is not found.')
        def test():
            with app.app_context():
                frameworks = MLFrameworkService().get().ml_frameworks
                req = PostMLComponentReq(name='Fashion Classifier',
                                         description='Fashion image classification',
                                         problem_domain='ImageClassification',
                                         ml_framework_id=frameworks[0].id)
                try:
                    MLComponentService().post(organizer_id='dep-hoge', req=req)
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'P24000')

        @it.should('should add MLComponent.')
        def test():
            with app.app_context():
                frameworks = MLFrameworkService().get().ml_frameworks
                req = PostMLComponentReq(name='Test Classifier',
                                         description='Test image classification',
                                         problem_domain='TestClassification',
                                         ml_framework_id=frameworks[0].id)
                response = MLComponentService().get_ml_component_list(organizer_id='dep-a')
                before_len = len(response.ml_components)

                response = MLComponentService().post(organizer_id='dep-a', req=req)
                it.assertEqual(response.result.code, 'P22000')
                add_ml_component_id = response.ml_component_id

                response = MLComponentService().get_ml_component_list(organizer_id='dep-a')
                add_ml_component = [c for c in response.ml_components if c.id_ == add_ml_component_id][0]
                after_len = len(response.ml_components)

                it.assertEqual(before_len+1, after_len)
                it.assertEqual(req.name, add_ml_component.name)
                it.assertEqual(req.description, add_ml_component.description)
                it.assertEqual(req.problem_domain, add_ml_component.problem_domain)
                it.assertEqual(frameworks[0].name, add_ml_component.ml_framework_name)

    with it.having('DELETE /MLComponents'):

        delete_ml_component_id = -1

        @it.should('should return P32000.')
        def test():
            with app.app_context():
                global delete_ml_component_id

                # MLComponent作成
                frameworks = MLFrameworkService().get().ml_frameworks
                req = PostMLComponentReq(name='削除テスト用',
                                         description='Test image classification',
                                         problem_domain='TestClassification',
                                         ml_framework_id=frameworks[0].id)
                response = MLComponentService().post(organizer_id='dep-a', req=req)
                delete_ml_component_id = response.ml_component_id

                # インベントリ追加
                with tempfile.TemporaryDirectory() as dir_name:
                    file_name1 = str(Path(dir_name) / 'test1.csv')
                    with open(file_name1, "w") as f:
                        f.write('test1,test2')
                    file_name2 = str(Path(dir_name) / 'test2.csv')
                    with open(file_name2, "w") as f:
                        f.write('test3,test4')
                    req = AppendInventoryReq(name='Testdata99',
                                             type_id=1,
                                             file_system_id=2,
                                             file_path=file_name1,
                                             description='テスト99用のデータ',
                                             formats=['csv', 'zip'],
                                             schema='http://sample.com/datafotmat/testdata2')
                    InventoryService().append_inventory(organizer_id='dep-a',
                                                        ml_component_id=delete_ml_component_id, req=req)

                    req = AppendInventoryReq(name='Testdata100',
                                             type_id=1,
                                             file_system_id=2,
                                             file_path=file_name2,
                                             description='テスト99用のデータ',
                                             formats=['csv', 'zip'],
                                             schema='http://sample.com/datafotmat/testdata2')
                    InventoryService().append_inventory(organizer_id='dep-a',
                                                        ml_component_id=delete_ml_component_id, req=req)

                response = InventoryService().get_inventories(organizer_id='dep-a',
                                                              ml_component_id=delete_ml_component_id)

                # TD追加
                post_json = {
                    "Name": "Neuron Coverage",
                    "QualityDimensionID": 5,
                    "QualityMeasurements": [
                        {"Id": 1, "Value": "60", "RelationalOperatorId": 1, "Enable": True}
                    ],
                    "TargetInventories": [
                        {"Id": 1, "InventoryId": response.inventories[0].id_, "TemplateInventoryId": 1},
                        {"Id": 2, "InventoryId": response.inventories[1].id_, "TemplateInventoryId": 2}
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
                TestDescriptionService().append_test_description(organizer_id='dep-a',
                                                                 ml_component_id=delete_ml_component_id, req=req)

                # インベントリの存在確認( inventories > 0 )
                response = InventoryService().get_inventories(organizer_id='dep-a',
                                                              ml_component_id=delete_ml_component_id)
                it.assertGreater(len(response.inventories), 0)
                # テストディスクリプションの存在確認( test_descriptions > 0 )
                response = TestDescriptionService().get_list(organizer_id='dep-a',
                                                             ml_component_id=delete_ml_component_id)
                it.assertGreater(len(response.test.test_descriptions), 0)
                # 削除
                response = MLComponentService().delete_ml_component(organizer_id='dep-a',
                                                                    ml_component_id=delete_ml_component_id)
                it.assertEqual(response.result.code, 'P32000')
                # インベントリの削除確認( inventories = 0 )
                response = InventoryService().get_inventories(organizer_id='dep-a',
                                                              ml_component_id=delete_ml_component_id)
                it.assertEqual(len(response.inventories), 0)
                # テストディスクリプションの削除確認( test_descriptions = 0 )
                response = TestDescriptionService().get_list(organizer_id='dep-a',
                                                             ml_component_id=delete_ml_component_id)
                it.assertEqual(len(response.test.test_descriptions), 0)

        @it.should('should return MLComponents that is not delete.')
        def test():
            with app.app_context():
                response = MLComponentService().get_ml_component_list(organizer_id='dep-a')
                it.assertGreaterEqual(len(response.ml_components), 2)

                for c in response.ml_components:
                    it.assertTrue(type(c.id_) == int)
                    it.assertNotEqual(c.id_, 0)
                    it.assertTrue(type(c.name) == str)
                    it.assertNotEqual(c.name, '')
                    it.assertTrue(type(c.description) == str)
                    it.assertNotEqual(c.description, '')
                    it.assertTrue(type(c.problem_domain) == str)
                    it.assertNotEqual(c.problem_domain, '')
                    it.assertTrue(type(c.ml_framework_name) == str)
                    it.assertNotEqual(c.ml_framework_name, '')

        @it.should('should return P34000.(not found ml_component)')
        def test():
            with app.app_context():
                try:
                    response = MLComponentService().delete_ml_component(organizer_id='dep-b', ml_component_id=1)
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'P34000')

        @it.should('should return P34001.(ml_component has already been deleted)')
        def test():
            global delete_ml_component_id
            with app.app_context():
                try:
                    response = MLComponentService().delete_ml_component(organizer_id='dep-a',
                                                                        ml_component_id=delete_ml_component_id)
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'P34001')

it.createTests(globals())

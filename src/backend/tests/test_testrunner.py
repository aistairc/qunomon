# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import tempfile
from pathlib import Path
import shutil
from nose2.tools import such

from qai_testbed_backend.controllers.dto.inventory import AppendInventoryReq
from qai_testbed_backend.controllers.dto.ml_component import PostMLComponentReq
from qai_testbed_backend.usecases.inventory import InventoryService
from qai_testbed_backend.usecases.ml_component import MLComponentService
from qai_testbed_backend.usecases.ml_framework import MLFrameworkService
from . import app
from qai_testbed_backend.usecases.testrunner import TestRunnerService
from qai_testbed_backend.usecases.test_description import TestDescriptionService
from qai_testbed_backend.controllers.dto.testrunner import PostTestRunnerReq
from qai_testbed_backend.controllers.dto.test_description import AppendTestDescriptionReqSchema
from qai_testbed_backend.across.exception import QAIException, QAINotFoundException, QAIInvalidRequestException


with such.A('TestRunners') as it:

    def _add_dummy_td(organizer_id='dep-a', ml_component_id=1) -> int:
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

        req = AppendTestDescriptionReqSchema().load(post_json)
        TestDescriptionService().append_test_description(organizer_id=organizer_id, ml_component_id=ml_component_id, req=req)

        res = TestDescriptionService().get_list(organizer_id=organizer_id, ml_component_id=ml_component_id)
        return res.test.test_descriptions[-1].id_

    with it.having('GET /testRunners'):
        @it.should('should return I52000.')
        def test():
            with app.app_context():
                response = TestRunnerService().get_test_runners()
                it.assertEqual(response.result.code, 'I52000')

        @it.should('should return TestRunners.')
        def test():
            with app.app_context():
                response = TestRunnerService().get_test_runners()

                for t in response.test_runners:
                    it.assertTrue(type(t.id_) is int)
                    it.assertNotEqual(t.id_, 0)
                    it.assertTrue(type(t.name) is str)
                    it.assertNotEqual(t.name, '')
                    it.assertTrue(type(t.quality_dimension_id) is int)
                    it.assertNotEqual(t.quality_dimension_id, 0)
                    it.assertTrue(type(t.description) is str)
                    it.assertTrue(type(t.author) is str)
                    it.assertTrue(type(t.version) is str)
                    it.assertTrue(type(t.quality) is str)
                    it.assertNotEqual(t.quality, '')
                    it.assertTrue(type(t.landing_page) is str)
                    it.assertNotEqual(t.landing_page, '')
                    for r in t.reference:
                        it.assertTrue(type(r.reference) is str)
                        it.assertNotEqual(r.reference, '')
                    for p in t.params:
                        it.assertTrue(type(p.id_) is int)
                        it.assertNotEqual(p.id_, 0)
                        it.assertTrue(type(p.name) is str)
                        it.assertNotEqual(p.name, '')
                        it.assertTrue(type(p.type_) is str)
                        it.assertNotEqual(p.type_, '')
                        it.assertTrue(type(p.description) is str)
                        it.assertNotEqual(p.description, '')
                        it.assertTrue(type(p.default_value) is str)
                    for tit in t.test_inventory_templates:
                        it.assertTrue(type(tit.id_) is int)
                        it.assertNotEqual(tit.id_, 0)
                        it.assertTrue(type(tit.name) is str)
                        it.assertNotEqual(tit.name, '')
                        it.assertTrue(type(tit.type_.id_) is int)
                        it.assertNotEqual(tit.type_.id_, 0)
                        it.assertTrue(type(tit.type_.name) is str)
                        it.assertNotEqual(tit.type_.name, '')
                        it.assertTrue(type(tit.description) is str)
                        for f in tit.formats:
                            it.assertTrue(type(f.id) is int)
                            it.assertNotEqual(f.id, 0)
                            it.assertTrue(type(f.type) is str)
                            it.assertNotEqual(f.type, '')
                            it.assertTrue(type(f.format) is str)
                            it.assertNotEqual(f.format, '')
                        it.assertTrue(type(tit.schema) is str)
                    for rm in t.report.measures:
                        it.assertTrue(type(rm.id_) is int)
                        it.assertNotEqual(rm.id_, 0)
                        it.assertTrue(type(rm.name) is str)
                        it.assertNotEqual(rm.name, '')
                        it.assertTrue(type(rm.type_) is str)
                        it.assertNotEqual(rm.type_, '')
                        it.assertTrue(type(rm.description) is str)
                        it.assertNotEqual(rm.description, '')
                        it.assertTrue(type(rm.structure) is str)
                        it.assertNotEqual(rm.structure, '')
                    for rr in t.report.resources:
                        it.assertTrue(type(rr.id_) is int)
                        it.assertNotEqual(rr.id_, 0)
                        it.assertTrue(type(rr.name) is str)
                        it.assertNotEqual(rr.name, '')
                        it.assertTrue(type(rr.type_) is str)
                        it.assertNotEqual(rr.type_, '')
                        it.assertTrue(type(rr.description) is str)
                    for d in t.downloads:
                        it.assertTrue(type(d.id_) is int)
                        it.assertNotEqual(d.id_, 0)
                        it.assertTrue(type(d.name) is str)
                        it.assertNotEqual(d.name, '')
                        it.assertTrue(type(d.description) is str)

    with it.having('POST /testRunners'):
        @it.should('should return R14000 if not found test.')
        def test():
            req = PostTestRunnerReq(command='Async', test_description_ids=[1])
            with app.app_context():
                try:
                    _ = TestRunnerService().post(organizer_id='dep-a', ml_component_id=999, request=req)
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'R14000')

        @it.should('should return R14001 if not found test_description.')
        def test():
            req = PostTestRunnerReq(command='Async', test_description_ids=[999])
            with app.app_context():
                try:
                    _ = TestRunnerService().post(organizer_id='dep-a', ml_component_id=1, request=req)
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'R14001')

        @it.should('should return R14001 if test_description had deleted.')
        def test():
            with app.app_context():
                td_id = _add_dummy_td()
                req = PostTestRunnerReq(command='Async', test_description_ids=[td_id])
                # td削除
                TestDescriptionService().delete_test_description(organizer_id='dep-a', ml_component_id=1,
                                                                 testdescription_id=td_id)

                try:
                    _ = TestRunnerService().post(organizer_id='dep-a', ml_component_id=1, request=req)
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'R14001')

        @it.should('should return R14001 if test_description had executed.')
        def test():
            with app.app_context():
                from qai_testbed_backend.entities.test_description import TestDescriptionMapper
                td_id = _add_dummy_td()
                req = PostTestRunnerReq(command='Async', test_description_ids=[td_id])
                # 実行済みを設定
                td = TestDescriptionMapper.query.get(td_id)
                td.run_id = 1
                td.run.result = 'OK'

                try:
                    _ = TestRunnerService().post(organizer_id='dep-a', ml_component_id=1, request=req)
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'R14001')


        @it.should('should return R14001 if test_description had deleted when all td specific.')
        def test():
            with app.app_context():

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

                res = TestDescriptionService().get_list(organizer_id='dep-a',
                                                        ml_component_id=delete_ml_component_id)
                td_id = res.test.test_descriptions[-1].id_

                # td削除
                TestDescriptionService().delete_test_description(organizer_id='dep-a', ml_component_id=1,
                                                                 testdescription_id=td_id)

                req = PostTestRunnerReq(command='Async', test_description_ids=[])

                try:
                    _ = TestRunnerService().post(organizer_id='dep-a', ml_component_id=delete_ml_component_id,
                                                 request=req)
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'R14001')

        @it.should('should return R14003 if asset file changed.')
        def test():
            with app.app_context():
                from qai_testbed_backend.entities.test_description import TestDescriptionMapper
                td_id = _add_dummy_td()
                td = TestDescriptionMapper.query.get(td_id)
                org_file_path = td.inventories[0].inventory.file_path
                bk_file_path = org_file_path+'.bk'

                shutil.copy2(org_file_path, bk_file_path)

                with open(str(org_file_path), mode='w') as f:
                    f.write('change, 123')

                req = PostTestRunnerReq(command='Async', test_description_ids=[td_id])
                try:
                    _ = TestRunnerService().post(organizer_id='dep-a', ml_component_id=1, request=req)
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'R14003')
                finally:
                    shutil.move(bk_file_path, org_file_path)

        @it.should('should return R14002 if asset file not exists.')
        def test():
            with app.app_context():
                from qai_testbed_backend.entities.test_description import TestDescriptionMapper
                td_id = _add_dummy_td()
                td = TestDescriptionMapper.query.get(td_id)
                org_file_path = td.inventories[0].inventory.file_path
                bk_file_path = org_file_path+'.bk'

                shutil.move(org_file_path, bk_file_path)

                req = PostTestRunnerReq(command='Async', test_description_ids=[td_id])
                try:
                    _ = TestRunnerService().post(organizer_id='dep-a', ml_component_id=1, request=req)
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'R14002')
                finally:
                    shutil.move(bk_file_path, org_file_path)

it.createTests(globals())

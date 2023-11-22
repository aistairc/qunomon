# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from nose2.tools import such
from pathlib import Path

from . import app
from datetime import datetime
from qai_testbed_backend.usecases.ml_component import MLComponentService
from qai_testbed_backend.usecases.ml_framework import MLFrameworkService
from qai_testbed_backend.usecases.test_description import TestDescriptionService
from qai_testbed_backend.usecases.inventory import InventoryService
from qai_testbed_backend.controllers.dto.inventory import AppendInventoryReq
from qai_testbed_backend.controllers.dto.test_description import AppendTestDescriptionReqSchema
from qai_testbed_backend.controllers.dto.ml_component import PostMLComponentReq
from qai_testbed_backend.usecases.guideline_schema_file import GuidelineSchemaFileService
from qai_testbed_backend.across.exception import QAIException, QAINotFoundException, QAIBadRequestException
from qai_testbed_backend.entities.guideline import GuidelineMapper
from qai_testbed_backend.entities.scope import ScopeMapper
from qai_testbed_backend.entities.quality_dimension import QualityDimensionMapper
import flask
import io
import tempfile

import json

with such.A('guidelineSchemaFile') as it:

    # テスト実行時に1回実行
    @it.has_setup
    def setup():
        it.guideline_json = None
        with open('./test_res/guideline.json', encoding='utf-8') as f:
            it.guideline_json = json.load(f)

    with it.having('POST /guidelines/guideline_schema_file'):
        @it.should('should return G25000.')
        def test():
            with app.app_context():
                response = GuidelineSchemaFileService().post(guideline_schema_json=it.guideline_json)
                it.assertEqual(response.result.code, 'G25000')

        @it.should('should return G25400.(guideline existed)')
        def test():
            with app.app_context():
                try:
                    response = GuidelineSchemaFileService().post(guideline_schema_json=it.guideline_json)
                except QAIException as e:
                    it.assertTrue(type(e) is QAIBadRequestException)
                    it.assertEqual(e.result_code, 'G25400')

    with it.having('GET /guidelines/<guideline_id>/guideline_schema_file'):
        @it.should('should return G26000.')
        def test():
            with app.app_context():
                guideline = GuidelineMapper.query. \
                    filter(GuidelineMapper.delete_flag.is_(False)). \
                    filter(GuidelineMapper.name == "機械学習品質マネジメントガイドライン2.1.0").first()
                response = GuidelineSchemaFileService().get(guideline_id=guideline.id)
                it.assertEqual(response.result.code, 'G26000')

        @it.should('should return G26404.(Not found guideline)')
        def test():
            with app.app_context():
                try:
                    response = GuidelineSchemaFileService().get(guideline_id=999)
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'G26404')

    with it.having('PUT /guidelines/<guideline_id>/guideline_schema_file'):
        @it.should('should return G27000.')
        def test():
            with app.test_request_context(data={'guideline_schema': (io.open("./test_res/guideline_update.json", mode="rb"))}):
                guideline = GuidelineMapper.query. \
                    filter(GuidelineMapper.delete_flag.is_(False)). \
                    filter(GuidelineMapper.name == "機械学習品質マネジメントガイドライン2.1.0").first()
                response = GuidelineSchemaFileService().put(guideline_id=guideline.id, request=flask.request)
                it.assertEqual(response.result.code, 'G27000')

        @it.should('should return G27404.(Not found guideline_schema_file)')
        def test():
            with app.test_request_context(data={'guideline_schema': (io.open("./test_res/guideline_update.json", mode="rb"))}):
                try:
                    response = GuidelineSchemaFileService().put(guideline_id=999, request=flask.request)
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'G27404')

    with it.having('DELETE /guidelines/<guideline_id>/guideline_schema_file'):
        @it.should('should return G28000.')
        def test():
            with app.app_context():
                guideline = GuidelineMapper.query. \
                    filter(GuidelineMapper.delete_flag.is_(False)). \
                    filter(GuidelineMapper.name == "機械学習品質マネジメントガイドライン2.1.0").first()
                response = GuidelineSchemaFileService().delete(guideline_id=guideline.id)
                it.assertEqual(response.result.code, 'G28000')

        @it.should('should return G28404.(Not found guideline)')
        def test():
            with app.app_context():
                try:
                    response = GuidelineSchemaFileService().delete(guideline_id=999)
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'G28404')

    with it.having('GET /guidelines/<guideline_id>/guideline_schema_file/edit_check'):
        @it.should('should return G29000.')
        def test():
            guideline_id = 0
            with app.app_context():
                response = GuidelineSchemaFileService().post(guideline_schema_json=it.guideline_json)

            # ワーニングを出すためダミーのMLComponent、TestDescriptionを登録
            with app.app_context():
                scope_mapper = ScopeMapper.query. \
                    filter(ScopeMapper.name == 'スコープ1'). \
                    filter(ScopeMapper.delete_flag == False).first()
                frameworks = MLFrameworkService().get().ml_frameworks
                qd_mapper = QualityDimensionMapper.query. \
                    filter(QualityDimensionMapper.delete_flag == False). \
                    filter(QualityDimensionMapper.json_id == 'INT0').first()
                
                guideline_id = scope_mapper.guideline_id

                # MLComponent追加
                req = PostMLComponentReq(name='Fashion Classifier',
                                         description='Fashion image classification',
                                         problem_domain='ImageClassification',
                                         ml_framework_id=frameworks[0].id,
                                         guideline_id=guideline_id,
                                         scope_id=scope_mapper.id,
                                         guideline_reason='This guideline fits the project',
                                         scope_reason='This scope fits the project')
                response = MLComponentService().post(organizer_id='dep-a', req=req)
                tmp_ml_component_id = response.ml_component_id

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
                                             file_path=file_name1,
                                             description='テスト99用のデータ',
                                             formats=['csv'])
                    InventoryService().append_inventory(organizer_id='dep-a',
                                                        ml_component_id=tmp_ml_component_id, req=req)

                    req = AppendInventoryReq(name='Testdata100',
                                             type_id=1,
                                             file_path=file_name2,
                                             description='テスト99用のデータ',
                                             formats=['csv'])
                    InventoryService().append_inventory(organizer_id='dep-a',
                                                        ml_component_id=tmp_ml_component_id, req=req)

                response = InventoryService().get_inventories(organizer_id='dep-a',
                                                              ml_component_id=tmp_ml_component_id)

                # TD追加
                post_json = {
                    "Name": "Neuron Coverage",
                    "QualityDimensionID": qd_mapper.id,
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
                                                                 ml_component_id=tmp_ml_component_id, req=req)

            # ワーニングは、MLComponentのscopeで1件、TestDescriptionのQDで１件
            with app.test_request_context(data={'guideline_schema': (io.open("./test_res/guideline_update.json", mode="rb"))}):
                response = GuidelineSchemaFileService().edit_check(guideline_id=guideline_id, request=flask.request)
                it.assertEqual(response.result.code, 'G29000')
                it.assertFalse(response.check_result)
                it.assertEqual(len(response.warning_message), 2)

            # MLComponentを削除して、ワーニングを出さない
            with app.app_context():
                response = MLComponentService().delete_ml_component(organizer_id='dep-a',
                                                                    ml_component_id=tmp_ml_component_id)
            with app.test_request_context(data={'guideline_schema': (io.open("./test_res/guideline_update.json", mode="rb"))}):
                response = GuidelineSchemaFileService().edit_check(guideline_id=guideline_id, request=flask.request)
                it.assertEqual(response.result.code, 'G29000')
                it.assertTrue(response.check_result)
                it.assertEqual(len(response.warning_message), 0)

        @it.should('should return G29404.(Not found guideline)')
        def test():
            with app.test_request_context(data={'guideline_schema': (io.open("./test_res/guideline_update.json", mode="rb"))}):
                try:
                    response = GuidelineSchemaFileService().edit_check(guideline_id=999, request=flask.request)
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'G29404')

    with it.having('GET /guidelines/<guideline_id>/guideline_schema_file/delete_check'):
        @it.should('should return G30000.')
        def test():
            # edit_checkと同じガイドラインに対してチェックする
            with app.app_context():
                # ワーニングを出すためダミーのMLComponent、TestDescriptionを登録
                scope_mapper = ScopeMapper.query. \
                    filter(ScopeMapper.name == 'スコープ1'). \
                    filter(ScopeMapper.delete_flag == False).first()
                frameworks = MLFrameworkService().get().ml_frameworks
                qd_mapper = QualityDimensionMapper.query. \
                    filter(QualityDimensionMapper.delete_flag == False). \
                    filter(QualityDimensionMapper.json_id == 'INT0').first()

                # MLComponent追加
                req = PostMLComponentReq(name='Fashion Classifier',
                                         description='Fashion image classification',
                                         problem_domain='ImageClassification',
                                         ml_framework_id=frameworks[0].id,
                                         guideline_id=scope_mapper.guideline_id,
                                         scope_id=scope_mapper.id,
                                         guideline_reason='This guideline fits the project',
                                         scope_reason='This scope fits the project')
                response = MLComponentService().post(organizer_id='dep-a', req=req)
                tmp_ml_component_id = response.ml_component_id

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
                                             file_path=file_name1,
                                             description='テスト99用のデータ',
                                             formats=['csv'])
                    InventoryService().append_inventory(organizer_id='dep-a',
                                                        ml_component_id=tmp_ml_component_id, req=req)

                    req = AppendInventoryReq(name='Testdata100',
                                             type_id=1,
                                             file_path=file_name2,
                                             description='テスト99用のデータ',
                                             formats=['csv'])
                    InventoryService().append_inventory(organizer_id='dep-a',
                                                        ml_component_id=tmp_ml_component_id, req=req)

                response = InventoryService().get_inventories(organizer_id='dep-a',
                                                              ml_component_id=tmp_ml_component_id)

                # TD追加
                post_json = {
                    "Name": "Neuron Coverage",
                    "QualityDimensionID": qd_mapper.id,
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
                                                                 ml_component_id=tmp_ml_component_id, req=req)

                # ワーニングは、MLComponentのscopeで1件、TestDescriptionのQDで１件
                response = GuidelineSchemaFileService().delete_check(guideline_id=scope_mapper.guideline_id)
                it.assertEqual(response.result.code, 'G30000')
                it.assertFalse(response.check_result)
                it.assertEqual(len(response.warning_message), 2)

                # MLComponentを削除して、ワーニングを出さない
                response = MLComponentService().delete_ml_component(organizer_id='dep-a',
                                                                    ml_component_id=tmp_ml_component_id)
                response = GuidelineSchemaFileService().delete_check(guideline_id=scope_mapper.guideline_id)
                it.assertEqual(response.result.code, 'G30000')
                it.assertTrue(response.check_result)
                it.assertEqual(len(response.warning_message), 0)

        @it.should('should return G30404.(Not found guideline)')
        def test():
            with app.app_context():
                try:
                    response = GuidelineSchemaFileService().delete_check(guideline_id=999)
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'G30404')

it.createTests(globals())

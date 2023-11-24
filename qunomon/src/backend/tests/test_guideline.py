# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from datetime import datetime
from nose2.tools import such

from . import app
from qai_testbed_backend.usecases.guideline import GuidelineService
from qai_testbed_backend.controllers.dto.guideline import PutGuidelineReq
from qai_testbed_backend.across.exception import QAIException, QAINotFoundException, QAIInvalidRequestException

from qai_testbed_backend.gateways.extensions import sql_db


with such.A('Guidelines') as it:

    with it.having('GET /guidelines'):
        @it.should('should return G21000.')
        def test():
            with app.app_context():
                response = GuidelineService().get_guideline()
                it.assertEqual(response.result.code, 'G21000')

        @it.should('should return Guidelines.')
        def test():
            with app.app_context():
                response = GuidelineService().get_guideline()
                it.assertGreaterEqual(len(response.guidelines), 2)

                for f in response.guidelines:
                    it.assertTrue(type(f.id_) is int)
                    it.assertTrue(type(f.name) is str)
                    it.assertTrue(type(f.description) is str)
                    it.assertTrue(type(f.creator) is str)
                    it.assertTrue(type(f.publisher) is str)
                    it.assertTrue(type(f.identifier) is str)
                    it.assertTrue(type(f.publish_datetime) is datetime)
                    it.assertTrue(type(f.creation_datetime) is datetime)

    with it.having('PUT /guidelines'):
        @it.should('should return G24000.')
        def test():
            with app.app_context():
                req = PutGuidelineReq(description='Guideline_01',
                                      creator='Guideline_01_Members',
                                      publisher='AIST',
                                      identifier='https://www.digiarc.aist.go.jp/publication/aiqm/AIQM-Guideline-2.1.0.pdf',
                                      publish_datetime="2021-04-01 01:23:45",
                                      aithub_delete_flag=True
                )
                response = GuidelineService().edit_guideline(req, 1)
                it.assertEqual(response.result.code, 'G24000')

    with it.having('DELETE /guideline/<guideline_id>'):
        delete_guideline_id = -1
        @it.should('should return G23000.')
        def test():
            with app.app_context():
                global delete_guideline_id
                # 削除用ダミーデータ
                from qai_testbed_backend.entities.guideline import GuidelineMapper
                from qai_testbed_backend.entities.scope import ScopeMapper
                from qai_testbed_backend.entities.quality_dimension import QualityDimensionMapper
                from qai_testbed_backend.entities.scope_quality_dimension import ScopeQualityDimensionMapper
                guideline = GuidelineMapper(name='test1',
                                            description='test1',
                                            creator='test1',
                                            publisher='test1',
                                            identifier='test1',
                                            publish_datetime=datetime.strptime("2021-04-01 01:23:45", '%Y-%m-%d %H:%M:%S'),
                                            creation_datetime=datetime.strptime("2021-04-01 01:23:45", '%Y-%m-%d %H:%M:%S'))
                sql_db.session.add(guideline)
                sql_db.session.flush()

                delete_guideline_id = guideline.id

                scope = ScopeMapper(guideline_id=delete_guideline_id,
                                    name='test1',
                                    creation_datetime=datetime.strptime("2021-04-01 01:23:45", '%Y-%m-%d %H:%M:%S'))
                sql_db.session.add(scope)
                sql_db.session.flush()

                qd = QualityDimensionMapper(guideline_id=delete_guideline_id,
                                            name='test1',
                                            description='test1',
                                            url='test1',
                                            creation_datetime=datetime.strptime("2021-04-01 01:23:45", '%Y-%m-%d %H:%M:%S'))
                sql_db.session.add(qd)
                sql_db.session.flush()

                sqd = ScopeQualityDimensionMapper(guideline_id=delete_guideline_id,
                                                  scope_id=scope.id,
                                                  quality_dimension_id=qd.id,
                                                  creation_datetime=datetime.strptime("2021-04-01 01:23:45", '%Y-%m-%d %H:%M:%S'))
                sql_db.session.add(sqd)
                sql_db.session.commit()

                # ダミー登録後は３つ
                response = GuidelineService().get_guideline()
                it.assertGreaterEqual(len(response.guidelines), 3)

                # 削除
                response = GuidelineService().delete(guideline.id)
                it.assertEqual(response.result.code, 'G23000')

                # ダミー削除後は２つ
                response = GuidelineService().get_guideline()
                it.assertGreaterEqual(len(response.guidelines), 2)

        @it.should('should return G23404.(not found guideline)')
        def test():
            with app.app_context():
                try:
                    response = GuidelineService().delete(999)
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'G23404')

        @it.should('should return G23404.(guideline has already been deleted)')
        def test():
            global delete_guideline_id
            with app.app_context():
                try:
                    response = GuidelineService().delete(delete_guideline_id)
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'G23404')

        @it.should('should return G23403.(guideline is already registered in MlComponent)')
        def test():
            with app.app_context():
                try:
                    # ガイドライン1は登録済み
                    response = GuidelineService().delete(1)
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'G23403')


it.createTests(globals())

# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from nose2.tools import such

from . import app
from qai_testbed_backend.usecases.ml_component import MLComponentService
from qai_testbed_backend.usecases.ml_framework import MLFrameworkService
from qai_testbed_backend.controllers.dto.ml_component import PostMLComponentReq
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

it.createTests(globals())

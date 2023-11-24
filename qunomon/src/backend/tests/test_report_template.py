# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from nose2.tools import such

from . import app
from datetime import datetime
from qai_testbed_backend.usecases.report_template import ReportTemplateService
from qai_testbed_backend.across.exception import QAIException, QAINotFoundException, QAIInvalidRequestException
import flask
import io
import os

with such.A('ReportTemplate') as it:

    with it.having('GET /reportTemplates'):
        @it.should('should return R01000.')
        def test():
            with app.app_context():
                response = ReportTemplateService().get()
                it.assertEqual(response.result.code, 'R01000')
                it.assertGreaterEqual(len(response.report_templates), 1)
                for f in response.report_templates:
                    it.assertTrue(type(f.id_) is int)
                    it.assertTrue(type(f.name) is str)
                    it.assertTrue(type(f.guideline_id) is int)
                    it.assertTrue(type(f.creation_datetime) is datetime)
                    it.assertTrue(type(f.update_datetime) is datetime)

    with it.having('POST /reportTemplates'):
        @it.should('should return R02000.')
        def test():
            with app.test_request_context(data={'Name': 'test_name',
                                                'GidelineId': '1',
                                                'File': (io.open("./test_res/report_template_test_with_jinja2_code.zip", mode="rb"))}):
                response = ReportTemplateService().post(flask.request)
                it.assertEqual(response.result.code, 'R02000')

        @it.should('should return R02001.(template_name is empty)')
        def test():
            with app.test_request_context(data={'Name': '',
                                                'GidelineId': '1',
                                                'File': (io.open("./test_res/report_template_test_with_jinja2_code.zip", mode="rb"))}):
                try:
                    response = ReportTemplateService().post(flask.request)
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'R02001')

        @it.should('should return R02002.(GidelineId is empty)')
        def test():
            with app.test_request_context(data={'Name': 'test_name',
                                                'GidelineId': '',
                                                'File': (io.open("./test_res/report_template_test_with_jinja2_code.zip", mode="rb"))}):
                try:
                    response = ReportTemplateService().post(flask.request)
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'R02002')

        @it.should('should return R02003.(not found base_report_format.html in zip)')
        def test():
            with app.test_request_context(data={'Name': 'test_name',
                                                'GidelineId': '1',
                                                'File': (io.open("./test_res/report_template_test_with_jinja2_code_err_base_html.zip", mode="rb"))}):
                try:
                    response = ReportTemplateService().post(flask.request)
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'R02003')

        @it.should('should return R02004.(not found base_report.css in zip)')
        def test():
            with app.test_request_context(data={'Name': 'test_name',
                                                'GidelineId': '1',
                                                'File': (io.open("./test_res/report_template_test_with_jinja2_code_err_base_css.zip", mode="rb"))}):
                try:
                    response = ReportTemplateService().post(flask.request)
                except QAIException as e:
                    it.assertTrue(type(e) is QAIInvalidRequestException)
                    it.assertEqual(e.result_code, 'R02004')

        @it.should('should return R02005.(not found guideline)')
        def test():
            with app.test_request_context(data={'Name': 'test_name',
                                                'GidelineId': '99',
                                                'File': (io.open("./test_res/report_template_test_with_jinja2_code.zip", mode="rb"))}):
                try:
                    response = ReportTemplateService().post(flask.request)
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'R02005')
     
    with it.having('POST /reportTemplates/generate'):
        @it.should('should return R03000.')
        def test():
            with app.app_context():
                response = ReportTemplateService().post_generate(guideline_id=1)
                it.assertEqual(response.mime_type, 'application/zip')

        @it.should('Guideline is not found. should return R03001.')
        def test():
            with app.app_context():
                try:
                    response = ReportTemplateService().post_generate(guideline_id=99)
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'R03001')

        @it.should('QualityDimension is not found. should return R03002.')
        def test():
            with app.app_context():
                try:
                    # ガイドラインID=2は品質特性が無い想定
                    response = ReportTemplateService().post_generate(guideline_id=2)
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'R03002')

    with it.having('GET /reportTemplates/id/zip'):
        @it.should('should return R03000.')
        def test():
            with app.app_context():
                response = ReportTemplateService().get_zip(report_template_id=1)
                it.assertEqual(response.mime_type, 'application/zip')

        @it.should('not found ReportTemplate in DB. should return R04001.')
        def test():
            with app.app_context():
                try:
                    response = ReportTemplateService().get_zip(report_template_id=99)
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'R04001')

        @it.should('not found ReportTemplate in directory. should return R04002.')
        def test():
            with app.app_context():
                try:
                    # ディレクトリを一旦リネームしておく
                    os.rename('./report/templates/1', './report/templates/1_backup')
                    response = ReportTemplateService().get_zip(report_template_id=1)
                except QAIException as e:
                    # ディレクトリ名を元に戻す
                    os.rename('./report/templates/1_backup', './report/templates/1')
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'R04002')

it.createTests(globals())

# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from qlib.utils.logging import get_logger, log

from ..dto import ResultSchema, Result

from ..dto.report_template import GetReportTemplateResSchema, PostReportTemplateResSchema, PostReportTemplateGenerateReqSchema
from ...usecases.report_template import ReportTemplateService
from ...across.exception import QAIException


logger = get_logger()


class ReportTemplateAPI(Resource):

    def __init__(self):
        # TODO 要DI
        self.service = ReportTemplateService()

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def get(self):
        try:
            res = self.service.get()
            return GetReportTemplateResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='R01999', message='internal server error: {}'.format(e))), 500

    @jwt_required()
    @log(logger)
    def post(self):
        try:
            res = self.service.post(request)
            return PostReportTemplateResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='R02999', message='internal server error: {}'.format(e))), 500


class ReportTemplateGenerateAPI(Resource):

    def __init__(self):
        # TODO 要DI
        self.service = ReportTemplateService()

    @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def post(self):
        json_input = request.get_json()
        try:
            req = PostReportTemplateGenerateReqSchema().load(json_input)
        except ValidationError as e:
            logger.exception('Raise Exception: %s', e)
            result = Result(code='R03900', message='ValidationError: {}'.format(e))
            return ResultSchema().dump(result), 400

        try:
            res = self.service.post_generate(req.guideline_id)
            return res
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='R03999', message='internal server error: {}'.format(e))), 500


class ReportTemplateZipAPI(Resource):

    def __init__(self):
        # TODO 要DI
        self.service = ReportTemplateService()

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def get(self, id: str):
        try:
            res = self.service.get_zip(int(id))
            return res
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='R04999', message='internal server error: {}'.format(e))), 500

# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from injector import inject
from qlib.utils.logging import get_logger, log

from ...across.exception import QAIException
from ..dto.testrunner import PostTestRunnerReqSchema, PostTestRunnerResSchema, ResultSchema, Result, \
    GetTestRunnerStatusResSchema, PostReportGeneratorReqSchema, PostReportGeneratorResSchema, GetTestRunnerResSchema
from ...usecases.testrunner import TestRunnerService, TestRunnerStatusService, ReportGeneratorService
from ...usecases.ait_manifest import AITManifestService


logger = get_logger()


class TestRunnerListAPI(Resource):

    @inject
    def __init__(self, service: TestRunnerService):
        self.service = service

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def get(self):
        try:
            res = self.service.get_test_runners()
            return GetTestRunnerResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except ValueError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='I50000', message='bad request: {}'.format(e))), 422
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='I59999', message='invalid path request: {}'.format(e))), 500


class TestRunnerAPI(Resource):

    @inject
    def __init__(self, service: TestRunnerService):
        self.service = service

    @log(logger)
    def post(self, organizer_id: str, ml_component_id: int):

        # リクエストパース
        # TODO いずれはデコレータに分離
        json_input = request.get_json()
        try:
            req = PostTestRunnerReqSchema().load(json_input)
        except TypeError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='R18000', message='TypeError: {}'.format(e))), 400
        except ValidationError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='R18001', message='ValidationError: {}'.format(e))), 400
        except ValueError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='R10000', message='Bad Request: {}'.format(e))), 422
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='R19999', message='internal server error: {}'.format(e))), 500

        try:
            res = self.service.post(organizer_id, ml_component_id, req)
            return PostTestRunnerResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='R19999', message='internal server error: {}'.format(e))), 500


class AITManifestAPI(Resource):

    @inject
    def __init__(self, service: AITManifestService):
        self.service = service

    @log(logger)
    def post(self):
        try:
            res = self.service.post(request)
            return ResultSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='M19999', message='internal server error: {}'.format(e))), 500


class TestRunnerStatusAPI(Resource):

    @inject
    def __init__(self, service: TestRunnerStatusService):
        self.service = service

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def get(self, organizer_id: str, ml_component_id: int):

        try:
            res = self.service.get(organizer_id, ml_component_id)
            return GetTestRunnerStatusResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='R29999', message='internal server error: {}'.format(e))), 500


class ReportGeneratorAPI(Resource):

    @inject
    def __init__(self, service: ReportGeneratorService):
        self.service = service

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def post(self, organizer_id: str, ml_component_id: str):

        # リクエストパース
        # TODO いずれはデコレータに分離
        json_input = request.get_json()
        try:
            req = PostReportGeneratorReqSchema().load(json_input)
        except ValidationError as e:
            logger.exception('Raise Exception: %s', e)
            result = Result(code='D18000', message='ValidationError: {}'.format(e))
            return ResultSchema().dump(result), 400

        try:
            res = self.service.post(organizer_id, int(ml_component_id), req)
            return PostReportGeneratorResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except TypeError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='D18001', message='TypeError: {}'.format(e))), 400
        except ValidationError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='D18002', message='ValidationError: {}'.format(e))), 400
        except ValueError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='D10000', message='Bad Request: {}'.format(e))), 422
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='D19999', message='internal server error: {}'.format(e))), 500

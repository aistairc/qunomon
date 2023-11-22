# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from injector import inject
from qlib.utils.logging import get_logger, log

from ...across.exception import QAIException
from ..dto.testrunner import PostTestRunnerReqSchema, PostTestRunnerResSchema, ResultSchema, Result, \
    GetTestRunnerStatusResSchema, PostReportGeneratorReqSchema, PostReportGeneratorResSchema
from ..dto.ait_manifest import GetTestRunnerResSchema, PostAITManifestResSchema
from ...usecases.testrunner import TestRunnerService, TestRunnerStatusService, ReportGeneratorService
from ...usecases.ait_manifest import AITManifestService


logger = get_logger()


class TestRunnerCoreAPI(Resource):

    @inject
    def __init__(self, service: TestRunnerService):
        self.service = service

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


class TestRunnerAPI(TestRunnerCoreAPI):

    @inject
    def __init__(self, service: TestRunnerService):
        self.service = service

    # csfrトークンチェックなし
    @log(logger)
    def post(self, organizer_id: str, ml_component_id: int):    
        # スーパークラスのpostを呼び出す
        res = super().post(organizer_id, ml_component_id)
        return res


class TestRunnerFrontAPI(TestRunnerCoreAPI):

    @inject
    def __init__(self, service: TestRunnerService):
        self.service = service

    # csfrトークンチェックあり
    @jwt_required
    @log(logger)
    def post(self, organizer_id: str, ml_component_id: int):
        # スーパークラスのpostを呼び出す
        res = super().post(organizer_id, ml_component_id)
        return res


class AITManifestCoreAPI(Resource):

    @inject
    def __init__(self, service: AITManifestService):
        self.service = service

    def post(self):
        try:
            res = self.service.post(request)
            return PostAITManifestResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except TypeError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='A01400', message='TypeError: {}'.format(e))), 400
        except ValidationError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='A01400', message='ValidationError: {}'.format(e))), 400
        except ValueError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='A01400', message='Bad Request: {}'.format(e))), 422
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='M19999', message='internal server error: {}'.format(e))), 500


class AITManifestAPI(AITManifestCoreAPI):

    @inject
    def __init__(self, service: AITManifestService):
        self.service = service

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def get(self):
        try:
            res = self.service.get()
            return GetTestRunnerResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='A09999', message='invalid path request: {}'.format(e))), 500

    # csfrトークンチェックなし
    @log(logger)
    def post(self):
        # スーパークラスのpostを呼び出す
        res = super().post()
        return res


class AITManifestFrontAPI(AITManifestCoreAPI):

    @inject
    def __init__(self, service: AITManifestService):
        self.service = service

    # csfrトークンチェックあり
    @jwt_required
    @log(logger)
    def post(self):
        # スーパークラスのpostを呼び出す
        res = super().post()
        return res


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


class ReportGeneratorCoreAPI(Resource):

    @inject
    def __init__(self, service: ReportGeneratorService):
        self.service = service

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


class ReportGeneratorAPI(ReportGeneratorCoreAPI):

    @inject
    def __init__(self, service: ReportGeneratorService):
        self.service = service

    # csfrトークンチェックなし 
    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def post(self, organizer_id: str, ml_component_id: str):
        # スーパークラスのpostを呼び出す
        res = super().post(organizer_id, ml_component_id)
        return res



class ReportGeneratorFrontAPI(ReportGeneratorCoreAPI):

    @inject
    def __init__(self, service: ReportGeneratorService):
        self.service = service

    # csfrトークンチェックあり
    @jwt_required
    @log(logger)
    def post(self, organizer_id: str, ml_component_id: str):
        # スーパークラスのpostを呼び出す
        res = super().post(organizer_id, ml_component_id)
        return res


class AITManifestDetailAPI(Resource):
    def __init__(self):
        # TODO 要DI
        self.service = AITManifestService()

    # @jwt_required()
    @jwt_required
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def delete(self, test_runner_id: str):
        try:
            res = self.service.delete(int(test_runner_id))
            return ResultSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except ValueError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='A02422', message='bad request: {}'.format(e))), 422
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='A02999', message='internal server error: {}'.format(e))), 500

# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from injector import inject
from qlib.utils.logging import get_logger, log

from ..dto import ResultSchema
from ..dto.test_description import GetTestDescriptionsResSchema, GetTestDescriptionDetailResSchema, \
    DeleteTestDescriptionsResSchema, PutTestDescriptionsReqSchema, Result, PutTestDescriptionsResSchema, \
    AppendTestDescriptionResSchema, AppendTestDescriptionReqSchema, GetTestDescriptionAncestorsResSchema, \
    GetUsingTestDescriptionsResSchema
from ...usecases.test_description import TestDescriptionService
from ...across.exception import QAIException


logger = get_logger()


class TestDescriptionCoreAPI(Resource):

    @inject
    def __init__(self, service: TestDescriptionService):
        self.service = service

    def post(self, organizer_id: str, ml_component_id: str):
        try:
            json_input = request.get_json()
            req = AppendTestDescriptionReqSchema().load(json_input)
            res = self.service.append_test_description(organizer_id, int(ml_component_id), req)
            return AppendTestDescriptionResSchema().dump(res), 200

        except TypeError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='T28000', message='TypeError: {}'.format(e))), 400
        except ValidationError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='T28001', message='ValidationError: {}'.format(e))), 400
        except ValueError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='T20000', message='Bad Request: {}'.format(e))), 422
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='T29999', message='internal server error: {}'.format(e))), 500


class TestDescriptionAPI(TestDescriptionCoreAPI):

    @inject
    def __init__(self, service: TestDescriptionService):
        self.service = service

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def get(self, organizer_id: str, ml_component_id: str):
        try:
            res = self.service.get_list(organizer_id, int(ml_component_id))
            return GetTestDescriptionsResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except ValueError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='T10000', message='Bad Request: {}'.format(e))), 422
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='T19999', message='internal server error: {}'.format(e))), 500

    # csfrトークンチェックなし
    @log(logger)
    def post(self, organizer_id: str, ml_component_id: str):    
        # スーパークラスのpostを呼び出す
        res = super().post(organizer_id, ml_component_id)
        return res


class TestDescriptionFrontAPI(TestDescriptionCoreAPI):

    @inject
    def __init__(self, service: TestDescriptionService):
        self.service = service

    # csfrトークンチェックあり
    @jwt_required()
    @log(logger)
    def post(self, organizer_id: str, ml_component_id: str):
        # スーパークラスのpostを呼び出す
        res = super().post(organizer_id, ml_component_id)
        return res

class TestDescriptionDetailAPI(Resource):

    @inject
    def __init__(self, service: TestDescriptionService):
        self.service = service

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def get(self, organizer_id: str, ml_component_id: str, testdescription_id: str):
        try:
            res = self.service.get(organizer_id, int(ml_component_id), int(testdescription_id))
            return GetTestDescriptionDetailResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except ValueError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='T30000', message='Bad Request: {}'.format(e))), 422
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='T39999', message='internal server error: {}'.format(e))), 500

    @jwt_required()
    @log(logger)
    def delete(self, organizer_id: str, ml_component_id: str, testdescription_id: str):
        try:
            res = self.service.delete_test_description(organizer_id, int(ml_component_id), int(testdescription_id))
            return DeleteTestDescriptionsResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except ValueError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='T50000', message='Bad Request: {}'.format(e))), 422
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='T59999', message='internal server error: {}'.format(e))), 500

    @jwt_required()
    @log(logger)
    def put(self, organizer_id: str, ml_component_id: str, testdescription_id: str):
        try:
            json_input = request.get_json()
            req = PutTestDescriptionsReqSchema().load(json_input)
            res = self.service.put_test_descriptions(organizer_id, int(ml_component_id), int(testdescription_id), req)
            return PutTestDescriptionsResSchema().dump(res), 200

        except TypeError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='T48000', message='TypeError: {}'.format(e))), 400
        except ValidationError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='T48001', message='ValidationError: {}'.format(e))), 400
        except ValueError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='T40000', message='Bad Request: {}'.format(e))), 422
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='T49999', message='internal server error: {}'.format(e))), 500


class TestDescriptionStarAPI(Resource):

    @inject
    def __init__(self, service: TestDescriptionService):
        self.service = service

    @jwt_required()
    @log(logger)
    def post(self, organizer_id: str, ml_component_id: str, test_description_id: str):
        try:
            res = self.service.set_star(organizer_id, int(ml_component_id), int(test_description_id))
            return ResultSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='T69999', message='internal server error: {}'.format(e))), 500


class TestDescriptionUnstarAPI(Resource):

    @inject
    def __init__(self, service: TestDescriptionService):
        self.service = service

    @jwt_required()
    @log(logger)
    def post(self, organizer_id: str, ml_component_id: str, test_description_id: str):
        try:
            res = self.service.set_unstar(organizer_id, int(ml_component_id), int(test_description_id))
            return ResultSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='T79999', message='internal server error: {}'.format(e))), 500


class TestDescriptionAncestorAPI(Resource):

    @inject
    def __init__(self, service: TestDescriptionService):
        self.service = service

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def get(self, organizer_id: str, ml_component_id: str, test_description_id: str):
        try:
            res = self.service.get_ancestor(organizer_id, int(ml_component_id), int(test_description_id))
            return GetTestDescriptionAncestorsResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='T89999', message='internal server error: {}'.format(e))), 500


class TestDescriptionUsingAPI(Resource):

    @inject
    def __init__(self, service: TestDescriptionService):
        self.service = service

    # TODO 要変換アノテーション
    @log(logger)
    def get(self, test_runner_id: str):
        try:
            res = self.service.get_using(int(test_runner_id))
            return GetUsingTestDescriptionsResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='A03999', message='internal server error: {}'.format(e))), 500
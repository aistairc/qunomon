# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from qlib.utils.logging import get_logger, log

from ..dto import ResultSchema, Result
from ..dto.guideline import GetGuidelinesResSchema, \
                            DeleteGuidelineResSchema, PutGuidelineReqSchema, PutGuidelineResSchema
from ...usecases.guideline import GuidelineService
from ...across.exception import QAIException


logger = get_logger()


class GuidelineAPI(Resource):

    def __init__(self):
        # TODO 要DI
        self.service = GuidelineService()

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def get(self):
        try:
            res = self.service.get_guideline()
            return GetGuidelinesResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='G21999', message='internal server error: {}'.format(e))), 500


class GuidelineDetailAPI(Resource):

    def __init__(self):
        # TODO 要DI
        self.service = GuidelineService()

    # TODO 要変換アノテーション
    @jwt_required
    @log(logger)
    def delete(self, guideline_id: str):
        try:
            res = self.service.delete(int(guideline_id))
            return DeleteGuidelineResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='G23999', message='internal server error: {}'.format(e))), 500

    @jwt_required
    @log(logger)
    def put(self, guideline_id: str):
        json_input = request.get_json()
        try:
            req = PutGuidelineReqSchema().load(json_input)
        except TypeError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='G24400', message='TypeError: {}'.format(e))), 400
        except ValidationError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='G24400', message='ValidationError: {}'.format(e))), 400
        except ValueError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='G24400', message='ValueError: {}'.format(e))), 400
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='G24999', message='internal server error: {}'.format(e))), 500

        try:
            res = self.service.edit_guideline(req, int(guideline_id))
            return PutGuidelineResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='G24999', message='internal server error: {}'.format(e))), 500
# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from flask_restful import Resource
from flask import request
from injector import inject
from marshmallow import ValidationError
from qlib.utils.logging import get_logger, log

from ..dto import ResultSchema, Result
from ..dto.ml_component import GetMLComponentSchemaResSchema, PostMLComponentReqSchema, PostMLComponentResSchema
from ...usecases.ml_component import MLComponentService
from ...across.exception import QAIException, QAINotFoundException


logger = get_logger()


class MLComponentAPI(Resource):

    @inject
    def __init__(self, service: MLComponentService):
        self.service = service

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def get(self, organizer_id: str):
        try:
            res = self.service.get_ml_component_list(organizer_id)
            return GetMLComponentSchemaResSchema().dump(res), 200
        except QAINotFoundException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except ValueError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='P10000', message='bad request: {}'.format(e))), 422
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='P19999', message='internal server error: {}'.format(e))), 500

    @log(logger)
    def post(self, organizer_id: str):

        # リクエストパース
        # TODO いずれはデコレータに分離
        json_input = request.get_json()
        try:
            req = PostMLComponentReqSchema().load(json_input)
        except TypeError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='P28000', message='TypeError: {}'.format(e))), 400
        except ValidationError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='P28000', message='ValidationError: {}'.format(e))), 400
        except ValueError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='P28000', message='ValueError: {}'.format(e))), 400
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='P29999', message='internal server error: {}'.format(e))), 500

        try:
            res = self.service.post(organizer_id, req)
            return PostMLComponentResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='P29999', message='internal server error: {}'.format(e))), 500

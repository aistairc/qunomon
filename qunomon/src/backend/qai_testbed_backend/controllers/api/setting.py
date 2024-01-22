# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from qlib.utils.logging import get_logger, log
from marshmallow import ValidationError

from ..dto import ResultSchema, Result
from ..dto.setting import GetSettingResSchema, PutSettingReqSchema, PutSettingResSchema
from ...usecases.setting import SettingService
from ...across.exception import QAIException


logger = get_logger()


class SettingDetailAPI(Resource):

    def __init__(self):
        # TODO 要DI
        self.service = SettingService()

    # TODO 要変換アノテーション
    @log(logger)
    def get(self, key: str):
        try:
            res = self.service.get(key)
            return GetSettingResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='V09999', message='internal server error: {}'.format(e))), 500

    @jwt_required()
    @log(logger)
    def put(self, key: str):

        # リクエストパース
        # TODO いずれはデコレータに分離
        json_input = request.get_json()
        try:
            req = PutSettingReqSchema().load(json_input)
        except TypeError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='V10400', message='TypeError: {}'.format(e))), 400
        except ValidationError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='V10400', message='ValidationError: {}'.format(e))), 400
        except ValueError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='V10400', message='ValueError: {}'.format(e))), 400
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='V19999', message='internal server error: {}'.format(e))), 500

        try:
            res = self.service.put(key, req)
            return PutSettingResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='V19999', message='internal server error: {}'.format(e))), 500

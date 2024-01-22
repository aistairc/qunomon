# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.

from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from qlib.utils.logging import get_logger, log

from ..dto import ResultSchema, Result
from ..dto.login import PostLoginResSchema
from ...usecases.login import LoginService
from ...across.exception import QAIException


logger = get_logger()


class LoginAPI(Resource):

    def __init__(self):
        # TODO 要DI
        self.service = LoginService()

    @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def post(self):
        try:
            res = self.service.post(request.get_json(force=True))
            return PostLoginResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='L01999', message='internal server error: {}'.format(e))), 500

    def get(self):
        try:
            # CSRFトークンを取得する
            res = self.service.get()
            return res
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='L09999', message='internal server error: {}'.format(e))), 500

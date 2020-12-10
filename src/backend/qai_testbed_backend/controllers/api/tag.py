# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from flask import request
from flask_restful import Resource

from ..dto import ResultSchema, Result
from ..dto.tag import GetTagsResSchema
from ...usecases.tag import TagService
from ...across.exception import QAIException


class TagAPI(Resource):

    def __init__(self):
        # TODO 要DI
        self.service = TagService()

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    def get(self):
        try:
            res = self.service.get()
            return GetTagsResSchema().dump(res), 200
        except QAIException as e:
            return ResultSchema().dump(e.to_result()), e.status_code
        except ValueError as e:
            return ResultSchema().dump(Result(code='I60000', message='Bad Request: {}'.format(e))), 422
        except Exception as e:
            return ResultSchema().dump(Result(code='I69999', message='internal server error: {}'.format(e))), 500
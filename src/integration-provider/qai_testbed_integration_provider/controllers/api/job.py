# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from injector import inject

from ...across.exception import QAIException
from ..dto import Result, ResultSchema
from ..dto.job import PostJobReqSchema, PostJobResSchema
from ...usecases.job import JobService


class JobAPI(Resource):

    @inject
    def __init__(self, job_service: JobService):
        self.service = job_service

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    def post(self, organizer_id: str, ml_component_id: str):

        # リクエストパース
        # TODO いずれはデコレータに分離
        json_input = request.get_json()
        try:
            req = PostJobReqSchema().load(json_input)
        except ValidationError as err:
            result = Result(code='R10000', message='ValidationError')
            return ResultSchema().dump(result), 422

        try:
            res = self.service.post(organizer_id, int(ml_component_id), req)
        except QAIException as e:
            return ResultSchema().dump(e.to_result()), e.status_code
        return PostJobResSchema().dump(res), 200

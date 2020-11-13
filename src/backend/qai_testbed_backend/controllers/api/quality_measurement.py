# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from ...across.exception import QAIException
from ...usecases.quality_measurement import QualityMeasurementService
from ...usecases.relational_operator import RelationalOperatorService
from ..dto.quality_measurement import GetQualityMeasurementTemplateResSchema
from ..dto.relational_operator import GetRelationalOperatorResSchema
from ..dto import Result, ResultSchema


class QualityMeasurementAPI(Resource):

    def __init__(self):
        # TODO 要DI
        self.service = QualityMeasurementService()

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    def get(self):
        try:
            res = self.service.get_quality_measurement()
            return GetQualityMeasurementTemplateResSchema().dump(res), 200
        except QAIException as e:
            return ResultSchema().dump(e.to_result()), e.status_code
        except ValueError as e:
            return ResultSchema().dump(Result(code='Q20000', message='bad request: {}'.format(e))), 422
        except Exception as e:
            return ResultSchema().dump(Result(code='Q29999', message='invalid path request: {}'.format(e))), 500

    def post(self):
        return ResultSchema().dump(Result(code='Q29999', message='Not allow call API')), 500
        # try:
        #     json_input = request.get_json()
        #     req = PostMeasurementTemplateReqSchema().load(json_input)
        #     res = self.service.add_quality_measurement(req)
        #     return PostQualityMeasurementTemplateResSchema().dump(res), 200
        # except TypeError as e:
        #     return ResultSchema().dump(Result(code='Q28000', message='TypeError: {}'.format(e))), 400
        # except ValidationError as e:
        #     return ResultSchema().dump(Result(code='Q28001', message='ValidationError: {}'.format(e))), 400
        # except ValueError as e:
        #     return ResultSchema().dump(Result(code='Q20000', message='Bad Request: {}'.format(e))), 422
        # except QAIException as e:
        #     return ResultSchema().dump(e.to_result()), e.status_code
        # except Exception as e:
        #     return ResultSchema().dump(Result(code='Q29999', message='internal server error: {}'.format(e))), 500


class RelationalOperatorAPI(Resource):

    def __init__(self):
        # TODO 要DI
        self.service = RelationalOperatorService()

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    def get(self):
        try:
            res = self.service.get()
            return GetRelationalOperatorResSchema().dump(res), 200
        except QAIException as e:
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            return ResultSchema().dump(Result(code='Q39999', message='invalid path request: {}'.format(e))), 500

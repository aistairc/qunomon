# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from flask_restful import Resource
from injector import inject

from ..dto import ResultSchema, Result
from ..dto.format import GetFormatResSchema
from ...usecases.format import FormatService
from ...across.exception import QAIException


class FormatAPI(Resource):

    @inject
    def __init__(self, service: FormatService):
        self.service = service

    def get(self):
        try:
            res = self.service.get()
            return GetFormatResSchema().dump(res), 200
        except QAIException as e:
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            return ResultSchema().dump(Result(code='I69999', message='internal server error: {}'.format(e))), 500

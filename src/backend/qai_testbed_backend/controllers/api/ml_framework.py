# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from flask_restful import Resource
from injector import inject

from ..dto import ResultSchema, Result
from ..dto.ml_framework import GetMLFrameworkResSchema
from ...usecases.ml_framework import MLFrameworkService
from ...across.exception import QAIException


class MLFrameworkAPI(Resource):

    @inject
    def __init__(self, service: MLFrameworkService):
        self.service = service

    def get(self):
        try:
            res = self.service.get()
            return GetMLFrameworkResSchema().dump(res), 200
        except QAIException as e:
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            return ResultSchema().dump(Result(code='M11999', message='internal server error: {}'.format(e))), 500

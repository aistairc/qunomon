# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from flask_restful import Resource
from qlib.utils.logging import get_logger, log

from ..dto import ResultSchema, Result
from ..dto.data_type import GetDataTypesResSchema
from ...usecases.data_type import DataTypeService
from ...across.exception import QAIException


logger = get_logger()


class DataTypeAPI(Resource):

    def __init__(self):
        # TODO 要DI
        self.service = DataTypeService()

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def get(self):
        try:
            res = self.service.get_data_type()
            return GetDataTypesResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='I89999', message='internal server error: {}'.format(e))), 500

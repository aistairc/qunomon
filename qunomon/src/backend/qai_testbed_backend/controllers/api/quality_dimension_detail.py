# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.

from flask_restful import Resource
from qlib.utils.logging import get_logger, log

from ..dto import ResultSchema, Result
from ..dto.quality_dimension_detail import GetQualityDimensionDetailResSchema
from ...usecases.quality_dimension_detail import QualityDimensionDetailService
from ...across.exception import QAIException

logger = get_logger()

class QualityDimensionDetailAPI(Resource):

    def __init__(self):
        self.service = QualityDimensionDetailService()

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def get(self, guideline_name: str, qd_name: str):
        try:
            res = self.service.get_quality_dimension_detail(guideline_name, qd_name)
            return GetQualityDimensionDetailResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except ValueError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='Q02000', message='bad request: {}'.format(e))), 422
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
  
# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from flask_restful import Resource
from qlib.utils.logging import get_logger, log

from ..dto import ResultSchema, Result
from ..dto.quality_dimension import GetQualityDimensionsResSchema
from ...usecases.quality_dimension import QualityDimensionService
from ...across.exception import QAIException


logger = get_logger()


class QualityDimensionAPI(Resource):

    def __init__(self):
        # TODO 要DI
        self.service = QualityDimensionService()

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def get(self, scope_id: str):
        try:
            res = self.service.get_quality_dimension(int(scope_id))
            return GetQualityDimensionsResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except ValueError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='Q10000', message='bad request: {}'.format(e))), 422
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='Q19999', message='internal server error: {}'.format(e))), 500

class GuidelineQualityDimensionAPI(Resource):

    def __init__(self):
        # TODO 要DI
        self.service = QualityDimensionService()

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def get(self, guideline_id: int):
        try:
            res = self.service.get_guideline_quality_dimension(guideline_id)
            return GetQualityDimensionsResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except ValueError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='Q10000', message='bad request: {}'.format(e))), 422
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='Q19999', message='internal server error: {}'.format(e))), 500

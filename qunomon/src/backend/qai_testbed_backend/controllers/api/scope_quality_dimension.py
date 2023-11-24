# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from flask_restful import Resource
from qlib.utils.logging import get_logger, log

from ..dto import ResultSchema, Result
from ..dto.scope_quality_dimension import GetScopeQualityDimensionsResSchema
from ...usecases.scope_quality_dimension import ScopeQualityDimensionService
from ...across.exception import QAIException


logger = get_logger()
 

class GuidelineScopeQualityDimensionsAPI(Resource):
    
    def __init__(self):
        # TODO 要DI
        self.service = ScopeQualityDimensionService()

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def get(self, guideline_id: int):
        try:
            res = self.service.get_guideline_scope_quality_dimensions(guideline_id)
            return GetScopeQualityDimensionsResSchema().dump(res), 200

        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='S02500', message='internal server error: {}'.format(e))), 500

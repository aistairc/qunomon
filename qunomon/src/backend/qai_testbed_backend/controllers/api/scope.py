# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from flask_restful import Resource
from qlib.utils.logging import get_logger, log

from ..dto import ResultSchema, Result
from ..dto.scope import GetScopesResSchema
from ...usecases.scope import ScopeService
from ...across.exception import QAIException


logger = get_logger()


class ScopeAPI(Resource):

    def __init__(self):
        # TODO 要DI
        self.service = ScopeService()

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def get(self):
        try:
            res = self.service.get()
            return GetScopesResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='S00500', message='internal server error: {}'.format(e))), 500


class GuidelineScopeAPI(Resource):

    def __init__(self):
        # TODO 要DI
        self.service = ScopeService()

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def get(self, guideline_id: int):
        try:
            res = self.service.get_guideline_scopes(guideline_id)
            return GetScopesResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='S01500', message='internal server error: {}'.format(e))), 500

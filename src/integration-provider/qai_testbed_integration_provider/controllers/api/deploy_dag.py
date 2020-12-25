# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.

from flask import request
from flask_restful import Resource
from injector import inject
from qlib.utils.logging import get_logger, log

from ...usecases.deploy_dag import DeployDAGService
from ..dto import ResultSchema, Result
from ...across.exception import QAIException


logger = get_logger()


class DeployDAGAPI(Resource):

    @inject
    def __init__(self, service: DeployDAGService):
        self.service = service

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def post(self):
        try:
            res = self.service.post(request)
            return ResultSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='D99999', message='internal server error: {}'.format(e))), 500


class DeployDAGAsyncAPI(Resource):

    @inject
    def __init__(self, service: DeployDAGService):
        self.service = service

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def post(self):
        try:
            res = self.service.post(request, is_async_build=True)
            return ResultSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='D99999', message='internal server error: {}'.format(e))), 500

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def get(self):
        res = self.service.get_async()
        return ResultSchema().dump(res), 200


class DeployDAGNonBuildAPI(Resource):

    @inject
    def __init__(self, service: DeployDAGService):
        self.service = service

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def post(self):
        try:
            res = self.service.post(request, is_build=False)
            return ResultSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='D99999', message='internal server error: {}'.format(e))), 500

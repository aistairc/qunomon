# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.

from flask import request
from flask_restful import Resource
from injector import inject
from qlib.utils.logging import get_logger, log

from ...usecases.deploy_dag import DeployDAGService
from ..dto import ResultSchema, Result
from ...across.exception import QAIException


logger = get_logger()


class DeployDAGAsyncAPI(Resource):

    @inject
    def __init__(self, service: DeployDAGService):
        self.service = service

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def get(self):
        res = self.service.get_async()
        return ResultSchema().dump(res), 200

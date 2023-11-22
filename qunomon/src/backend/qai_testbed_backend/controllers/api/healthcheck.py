# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.

from flask_restful import Resource
from qlib.utils.logging import get_logger, log

from ..dto.healthcheck import GetHealtcheckResSchema
from ...usecases.healthcheck import HealthcheckService


logger = get_logger()


class HealthCheckAPI(Resource):

    def __init__(self):
        # TODO 要DI
        self.service = HealthcheckService()

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def get(self):
        res = self.service.get()
        return GetHealtcheckResSchema().dump(res), 200

# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from injector import inject
from qlib.utils.logging import get_logger, log

from ...across.exception import QAIException
from ..dto import Result, ResultSchema
from ..dto.run import PostNotifyCompleteRunResSchema
from ...usecases.run import NotifyRunCompeteService


logger = get_logger()


class NotifyRunCompeteAPI(Resource):

    @inject
    def __init__(self, notify_run_compete_service: NotifyRunCompeteService):
        self.service = notify_run_compete_service

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def post(self, organizer_id: str, ml_component_id: str, job_id: str, run_id: str):

        try:
            res = self.service.post(organizer_id, int(ml_component_id), int(job_id), int(run_id))
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return PostNotifyCompleteRunResSchema().dump(e.to_result()), e.status_code
        return PostNotifyCompleteRunResSchema().dump(res), 200

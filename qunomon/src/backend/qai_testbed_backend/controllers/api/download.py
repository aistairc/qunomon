# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.

from flask_restful import Resource
from qlib.utils.logging import get_logger, log

from ...usecases.download import DownloadService
from ..dto import ResultSchema, Result
from ...across.exception import QAIException


logger = get_logger()


class DownloadAPI(Resource):

    def __init__(self):
        # TODO 要DI
        self.service = DownloadService()

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def get(self, id_: str):
        try:
            res = self.service.get(int(id_))
            return res
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='D19999', message='internal server error: {}'.format(e))), 500

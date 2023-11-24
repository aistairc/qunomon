# Copyright © 2022 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from qlib.utils.logging import get_logger, log

from ..dto import ResultSchema, Result
from ..dto.ait_local import GetAITLocalListResSchema, PostAITLocalListResSchema
from ...across.exception import QAIException

from ...usecases.ait_local import AITLocalService


logger = get_logger()


class AITLocalAPI(Resource):

    def __init__(self):
        self.service = AITLocalService()

    @log(logger)
    def get(self):
        try:
            res = self.service.get_ait_local_list()
            return GetAITLocalListResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='AL0999', message='invalid path request: {}'.format(e))), 500

    @jwt_required
    @log(logger)
    def post(self):
        try:
            res = self.service.post_ait_local_list()
            status_code = '200'
            if res.result.code == 'AL1400':
                status_code = '400'
            return PostAITLocalListResSchema().dump(res), status_code
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='AL1999', message='invalid path request: {}'.format(e))), 500

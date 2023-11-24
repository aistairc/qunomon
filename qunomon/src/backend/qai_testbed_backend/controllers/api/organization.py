# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from flask_restful import Resource
from qlib.utils.logging import get_logger, log

from ..dto import ResultSchema, Result
from ..dto.organization import GetOrganizersResSchema
from ...usecases.organization import OrganizerService
from ...across.exception import QAIException


logger = get_logger()


class OrganizerAPI(Resource):

    def __init__(self):
        # TODO 要DI
        self.service = OrganizerService()

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def get(self):
        try:
            res = self.service.get_organizer_list()
            # TODO 組織関連の実装は保留とするため、一旦正常処理をコメントアウトし、ダミーのエラーを返すことにする
            # return GetOrganizersResSchema().dump(res), 200
            return ResultSchema().dump(Result(code='O99999', message='Not implemented API: GET /organizers')), 400
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='O09999', message='internal server error: {}'.format(e))), 500

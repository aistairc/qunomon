# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from flask_restful import Resource
from qlib.utils.logging import get_logger, log

from ..dto import ResultSchema, Result
from ..dto.role import GetRolesResSchema
from ...usecases.role import RoleService
from ...across.exception import QAIException


logger = get_logger()


class RoleAPI(Resource):

    def __init__(self):
        # TODO 要DI
        self.service = RoleService()

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def get(self):
        try:
            res = self.service.get_role()
            # TODO ロール関連の実装は保留とするため、一旦正常処理をコメントアウトし、ダミーのエラーを返すことにする
            # return GetRolesResSchema().dump(res), 200
            return ResultSchema().dump(Result(code='U99999', message='Not implemented API: GET /roles')), 400
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='U19999', message='internal server error: {}'.format(e))), 500

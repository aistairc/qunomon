# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import requests
import datetime

from sqlalchemy.exc import SQLAlchemyError
from requests.exceptions import RequestException
from qlib.utils.logging import get_logger, log

from ..controllers.dto import Result
from ..controllers.dto.scope import GetScopesRes
from ..entities.scope import ScopeMapper
from ..across.exception import QAINotFoundException

logger = get_logger()


class ScopeService:
    @log(logger)
    def get(self) -> GetScopesRes:

        scope_mapper = ScopeMapper.query. \
            filter(ScopeMapper.delete_flag == False).all()

        if scope_mapper is None or len(scope_mapper) == 0:
            raise QAINotFoundException(result_code='S00404',
                                       result_msg='Not found Scope')

        return GetScopesRes(
            result=Result(code='S00000', message="get list success."),
            scopes=[d.to_dto() for d in scope_mapper]
        )

    @log(logger)
    def get_guideline_scopes(self, guideline_id: int):

        scope_mapper = ScopeMapper.query. \
            filter(ScopeMapper.guideline_id == guideline_id). \
            filter(ScopeMapper.delete_flag == False).all()

        return GetScopesRes(
            result=Result(code='S01000', message="get list success."),
            scopes=[d.to_dto() for d in scope_mapper]
        )
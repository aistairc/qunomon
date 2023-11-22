# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from qlib.utils.logging import get_logger, log

from ..controllers.dto import Result
from ..controllers.dto.user import GetUsersRes
from ..entities.user import UserMapper


logger = get_logger()


class UserService:
    @log(logger)
    def get_user(self) -> GetUsersRes:
        users = UserMapper.query.all()

        return GetUsersRes(
            result=Result(code='U01000', message="get list success."),
            users=[u.to_dto() for u in users]
        )

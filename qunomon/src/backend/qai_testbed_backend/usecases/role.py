# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from qlib.utils.logging import get_logger, log

from ..controllers.dto import Result
from ..controllers.dto.role import GetRolesRes
from ..entities.role import RoleMapper


logger = get_logger()


class RoleService:
    @log(logger)
    def get_role(self) -> GetRolesRes:
        roles = RoleMapper.query.all()

        return GetRolesRes(
            result=Result(code='U12000', message="get list success."),
            roles=[d.to_dto() for d in roles]
        )

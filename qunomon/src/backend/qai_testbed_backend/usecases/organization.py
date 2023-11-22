# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from qlib.utils.logging import get_logger, log

from ..controllers.dto import Result
from ..controllers.dto.organization import GetOrganizersRes
from ..entities.organization import OrganizationMapper

logger = get_logger()


class OrganizerService:
    @log(logger)
    def get_organizer_list(self) -> GetOrganizersRes:
        organizers = OrganizationMapper.query.filter(OrganizationMapper.delete_flag == False).all()

        return GetOrganizersRes(
            result=Result(code='O01000', message="get list success."),
            organizers=[d.to_dto() for d in organizers]
        )

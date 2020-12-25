# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from qlib.utils.logging import get_logger, log

from ..controllers.dto.healthcheck import GetHealtcheckRes


logger = get_logger()


class HealthcheckService:
    @log(logger)
    def get(self) -> GetHealtcheckRes:
        return GetHealtcheckRes(code=0, message='alive.')

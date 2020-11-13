# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from ..controllers.dto.healthcheck import GetHealtcheckRes


class HealthcheckService:
    def get(self) -> GetHealtcheckRes:
        return GetHealtcheckRes(code=0, message='alive.')

# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from qlib.utils.logging import get_logger, log

from ..controllers.dto import Result
from ..controllers.dto.setting import GetSettingsRes, PutSettingReq, PutSettingRes
from ..entities.setting import SettingMapper
from ..across.exception import QAINotFoundException
from ..gateways.extensions import sql_db


logger = get_logger()


class SettingService:
    @log(logger)

    def get(self, key: str) -> GetSettingsRes:
        setting = SettingMapper.query. \
                filter(SettingMapper.key == key).first()

        if setting is None:
            raise QAINotFoundException('V00404', 'not found setting')

        return GetSettingsRes(
            result=Result(code='V00000', message="get setting success."),
            value=setting.value
        )

    def put(self, key: str, req: PutSettingReq) -> PutSettingRes:
        setting = SettingMapper.query. \
                filter(SettingMapper.key == key).first()

        if setting is None:
            raise QAINotFoundException('V10404', 'not found setting')

        setting.value = req.value
        sql_db.session.commit()

        return PutSettingRes(
            result=Result(code='V10000', message="put setting success."),
            value=setting.value
        )

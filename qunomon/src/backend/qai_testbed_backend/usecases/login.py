# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from flask import make_response
from warnings import catch_warnings
import requests
from qlib.utils.logging import get_logger, log

from ..controllers.dto import Result
from ..controllers.dto.login import UserInfo, PostLoginRes
from ..entities.setting import SettingMapper
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import random
from flask_jwt_extended import (create_access_token, set_access_cookies)

logger = get_logger()


class LoginService:
    @log(logger)
    def post(self, request) -> PostLoginRes:

        # TODO 認証機能
        account_id = request['AccountId']
        password = request['Password']

        return PostLoginRes(
            result=Result(code='L01000', message="Login Success."),
            userInfo=UserInfo(user_id=0,
                              user_name='',
                              organizer_id=0,
                              organizer_name='')
        )

    def get(self) -> Result:
        response = make_response()
        # アクセストークンの生成
        access_token = create_access_token(identity=random.random())
        set_access_cookies(response, access_token)
        return response

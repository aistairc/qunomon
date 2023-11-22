# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from marshmallow import fields

from . import Result, ResultSchema, BaseSchema

class UserInfo:
    def __init__(
        self,
        user_id: int,
        user_name: str,
        organizer_id: int,
        organizer_name: str
    ) -> None:
        self.user_id = user_id
        self.user_name = user_name
        self.organizer_id = organizer_id
        self.organizer_name = organizer_name


class UserInfoSchema(BaseSchema):
    __model__ = UserInfo
    user_id = fields.Int(data_key='UserId')
    user_name = fields.Str(data_key='UserName')
    organizer_id = fields.Int(data_key='OrganizerId')
    organizer_name = fields.Str(data_key='OrganizerName')


class PostLoginRes:
    def __init__(self, result: Result, userInfo: UserInfo = None) -> None:
        self.result = result
        if userInfo is not None:
           self.userInfo = userInfo


class PostLoginResSchema(BaseSchema):
    __model__ = PostLoginRes
    result = fields.Nested(ResultSchema, data_key='Result')
    userInfo = fields.Nested(UserInfoSchema, data_key='UserInfo')

# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import datetime
from typing import List
from marshmallow import fields

from . import Result, ResultSchema, BaseSchema
from .user_role_ml_component import UserRoleMlComponent, UserRoleMlComponentSchema


class User:
    def __init__(self, id_: int, account_id: str, user_name: str, password_hash: str,
                 delete_flag: bool, creation_datetime: datetime, update_datetime: datetime,
                 organizer_id: str, user_role_ml_components: List[UserRoleMlComponent]) -> None:
        self.id_ = id_
        self.account_id = account_id
        self.user_name = user_name
        self.password_hash = password_hash
        self.delete_flag = delete_flag
        self.creation_datetime = creation_datetime
        self.update_datetime = update_datetime
        self.organizer_id = organizer_id
        self.user_role_ml_components = user_role_ml_components


class GetUsersRes:
    def __init__(self, result: Result, users: List[User]) -> None:
        self.result = result
        self.users = users


class UserSchema(BaseSchema):
    __model__ = User
    id_ = fields.Int(data_key='Id')
    account_id = fields.Str(data_key='AccountId')
    user_name = fields.Str(data_key='UserName')
    password_hash = fields.Str(data_key='PasswordHash')
    creation_datetime = fields.Str(data_key='CreationDatetime')
    update_datetime = fields.Str(data_key='UpdateDatetime')
    organizer_id = fields.Str(data_key='OrganizerId')
    user_role_ml_components = fields.Nested(UserRoleMlComponentSchema, data_key='Roles', many=True)


class GetUsersResSchema(BaseSchema):
    __model__ = GetUsersRes
    result = fields.Nested(ResultSchema, data_key='Result')
    users = fields.Nested(UserSchema, data_key='Users', many=True)

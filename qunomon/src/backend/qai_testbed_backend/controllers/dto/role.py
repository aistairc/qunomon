# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List
from marshmallow import fields

from . import Result, ResultSchema, BaseSchema


class Role:
    def __init__(self, id_: int, name: str) -> None:
        self.id_ = id_
        self.name = name


class GetRolesRes:
    def __init__(self, result: Result, roles: List[Role]) -> None:
        self.result = result
        self.roles = roles


class RoleSchema(BaseSchema):
    __model__ = Role
    id_ = fields.Int(data_key='Id')
    name = fields.Str(data_key='Name')


class GetRolesResSchema(BaseSchema):
    __model__ = GetRolesRes
    result = fields.Nested(ResultSchema, data_key='Result')
    roles = fields.Nested(RoleSchema, data_key='Roles', many=True)

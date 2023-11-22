# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List
from marshmallow import fields

from . import Result, ResultSchema, BaseSchema


class UserRoleMlComponent:
    def __init__(self, id_: int, role: str, target_ml_component_id: int) -> None:
        self.id_ = id_
        self.role = role
        self.target_ml_component_id = target_ml_component_id


class UserRoleMlComponentSchema(BaseSchema):
    __model__ = UserRoleMlComponent
    id_ = fields.Int(data_key='Id')
    role = fields.Str(data_key='Role')
    target_ml_component_id = fields.Int(data_key='TargetMlComponentId')

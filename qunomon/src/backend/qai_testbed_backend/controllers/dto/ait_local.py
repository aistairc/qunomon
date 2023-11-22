# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List
from marshmallow import fields

from . import Result, ResultSchema, BaseSchema


class AITLocal:
    def __init__(
        self, 
        id_: int, 
        name: str, 
        version: str, 
        description: str,
        create_user_account: str,
        create_user_name: str,
        install_status: str
    ) -> None:
        self.id_ = id_
        self.name = name
        self.version = version
        self.description = description
        self.create_user_account = create_user_account
        self.create_user_name = create_user_name
        self.install_status = install_status


class AITLocalSchema(BaseSchema):
    __model__ = AITLocal
    id_ = fields.Int(data_key='Id', required=True)
    name = fields.Str(data_key='Name', required=True)
    version = fields.Str(data_key='Version', required=True)
    description = fields.Str(data_key='Description', required=True)
    create_user_account = fields.Str(data_key='CreateUserAccount', required=False)
    create_user_name = fields.Str(data_key='CreateUserName', required=False)
    install_status = fields.Str(data_key='Status', required=True)


class GetAITLocalListRes:
    def __init__(self, result: Result, ait_Local_list: List[AITLocal]) -> None:
        self.result = result
        self.ait_Local_list = ait_Local_list


class GetAITLocalListResSchema(BaseSchema):
    __model__ = GetAITLocalListRes
    result = fields.Nested(ResultSchema, data_key='Result')
    ait_Local_list = fields.Nested(AITLocalSchema, data_key='AITLocalList', many=True)


class ValidationOutputRes:
    def __init__(self, location: str, detail: str) -> None:
        self.location = location
        self.detail = detail


class ValidationOutputResSchema(BaseSchema):
    __model__ = ValidationOutputRes
    location = fields.Str(data_key='location')
    detail = fields.Str(data_key='detail')


class PostAITLocalListRes:
    def __init__(self, result: Result,
                 validation_outputs: List[ValidationOutputRes] = None) -> None:
        self.result = result
        if validation_outputs is not None:
            self.validation_outputs = validation_outputs


class PostAITLocalListResSchema(BaseSchema):
    __model__ = PostAITLocalListRes
    result = fields.Nested(ResultSchema, data_key='Result')
    validation_outputs = fields.Nested(
        ValidationOutputResSchema, data_key='ValidationOutput', many=True)

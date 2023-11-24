# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List
from marshmallow import fields

from . import Result, ResultSchema, BaseSchema


class Setting:
    def __init__(self, key: str, value: str) -> None:
        self.key = key
        self.value = value


class SettingSchema(BaseSchema):
    __model__ = Setting
    key = fields.Int(data_key='Key')
    value = fields.Str(data_key='Value')


class GetSettingsRes:
    def __init__(self, result: Result, value: str) -> None:
        self.result = result
        self.value = value


class GetSettingResSchema(BaseSchema):
    __model__ = GetSettingsRes
    result = fields.Nested(ResultSchema, data_key='Result')
    value = fields.Str(data_key='Value')


class PutSettingReq:
    def __init__(self, value: str) -> None:
        self.value = value


class PutSettingReqSchema(BaseSchema):
    __model__ = PutSettingReq
    value = fields.Str(data_key='Value')


class PutSettingRes:
    def __init__(self, result: Result, value: str) -> None:
        self.result = result
        self.value = value


class PutSettingResSchema(BaseSchema):
    __model__ = PutSettingRes
    result = fields.Nested(ResultSchema, data_key='Result')
    value = fields.Str(data_key='Value')

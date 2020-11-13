# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List
from marshmallow import fields

from . import Result, ResultSchema, BaseSchema


class Format:
    def __init__(self, id_: int, type_: str, format_: str) -> None:
        self.id = id_
        self.format = format_
        self.type = type_


class GetFormatRes:
    def __init__(self, result: Result, formats: List[Format]) -> None:
        self.result = result
        self.formats = formats


class FormatSchema(BaseSchema):
    __model__ = Format
    id = fields.Int(data_key='Id', required=True)
    type = fields.Str(data_key='Type', required=True)
    format = fields.Str(data_key='Format', required=True)


class GetFormatResSchema(BaseSchema):
    __model__ = GetFormatRes
    result = fields.Nested(ResultSchema, data_key='Result')
    formats = fields.Nested(FormatSchema, data_key='Formats', many=True)

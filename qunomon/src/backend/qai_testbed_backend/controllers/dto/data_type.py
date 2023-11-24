# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List
from marshmallow import fields

from . import Result, ResultSchema, BaseSchema


class DataType:
    def __init__(self, id_: int, name: str) -> None:
        self.id_ = id_
        self.name = name


class GetDataTypesRes:
    def __init__(self, result: Result, data_types: List[DataType]) -> None:
        self.result = result
        self.data_types = data_types


class DataTypeSchema(BaseSchema):
    __model__ = DataType
    id_ = fields.Int(data_key='Id')
    name = fields.Str(data_key='Name')


class GetDataTypesResSchema(BaseSchema):
    __model__ = GetDataTypesRes
    result = fields.Nested(ResultSchema, data_key='Result')
    data_types = fields.Nested(DataTypeSchema, data_key='DataTypes', many=True)

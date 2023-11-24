# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List
from marshmallow import fields

from . import Result, ResultSchema, BaseSchema


class MLFramework:
    def __init__(self, id_: int, name: str) -> None:
        self.id = id_
        self.name = name


class GetMLFrameworkRes:
    def __init__(self, result: Result, ml_frameworks: List[MLFramework]) -> None:
        self.result = result
        self.ml_frameworks = ml_frameworks


class MLFrameworkSchema(BaseSchema):
    __model__ = MLFramework
    id = fields.Int(data_key='Id', required=True)
    name = fields.Str(data_key='Name', required=True)


class GetMLFrameworkResSchema(BaseSchema):
    __model__ = GetMLFrameworkRes
    result = fields.Nested(ResultSchema, data_key='Result')
    ml_frameworks = fields.Nested(MLFrameworkSchema, data_key='MLFrameworks', many=True)

# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List
from marshmallow import fields

from . import Result, ResultSchema, BaseSchema


class Structure:
    def __init__(self, id_: int, structure: str) -> None:
        self.id_ = id_
        self.structure = structure


class GetStructureRes:
    def __init__(self, result: Result, structures: List[Structure]) -> None:
        self.result = result
        self.structures = structures


class StructureSchema(BaseSchema):
    __model__ = Structure
    id_ = fields.Int(data_key='Id', required=True)
    structure = fields.Str(data_key='Structure', required=True)


class GetStructureResSchema(BaseSchema):
    __model__ = GetStructureRes
    result = fields.Nested(ResultSchema, data_key='Result')
    structures = fields.Nested(StructureSchema, data_key='Structures', many=True)

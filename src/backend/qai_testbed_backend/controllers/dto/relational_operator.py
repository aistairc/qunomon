# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List
from marshmallow import fields
from . import Result, ResultSchema, BaseSchema


class RelationalOperator:
    def __init__(self, id_: int, expression: str, description: str) -> None:
        self.id_ = id_
        self.expression = expression
        self.description = description


class GetRelationalOperatorRes:
    def __init__(self, result: Result, relational_operators: List[RelationalOperator]) -> None:
        self.result = result
        self.relational_operators = relational_operators


class RelationalOperatorSchema(BaseSchema):
    __model__ = RelationalOperator
    id_ = fields.Int(data_key='Id', required=True)
    expression = fields.Str(data_key='Expression', required=True)
    description = fields.Str(data_key='Description', required=True)


class GetRelationalOperatorResSchema(BaseSchema):
    __model__ = GetRelationalOperatorRes
    result = fields.Nested(ResultSchema, data_key='Result')
    relational_operators = fields.Nested(RelationalOperatorSchema, data_key='RelationalOperator', many=True)

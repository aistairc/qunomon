# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List
from marshmallow import fields

from . import Result, ResultSchema, BaseSchema


class TestRunnerReference:
    def __init__(self, id_: int, reference: str) -> None:
        self.id_ = id_
        self.reference = reference


class TestRunnerReferenceRes:
    def __init__(self, result: Result, references: List[TestRunnerReference]) -> None:
        self.result = result
        self.references = references


class TestRunnerReferenceSchema(BaseSchema):
    __model__ = TestRunnerReference
    id_ = fields.Int(data_key='Id', required=True)
    reference = fields.Str(data_key='Reference', required=True)


class TestRunnerReferenceResSchema(BaseSchema):
    __model__ = TestRunnerReferenceRes
    result = fields.Nested(ResultSchema, data_key='Result')
    reference = fields.Nested(TestRunnerReferenceSchema, data_key='TestRunnerReference', many=True)

# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List
from marshmallow import fields

from . import Result, ResultSchema, BaseSchema


class TestRunnerReference:
    def __init__(self, id_: int, bib_info: str, additional_info: str = None, url_: str = None) -> None:
        self.id_ = id_
        self.bib_info = bib_info
        self.additional_info = additional_info
        self.url_ = url_


class TestRunnerReferenceRes:
    def __init__(self, result: Result, references: List[TestRunnerReference]) -> None:
        self.result = result
        self.references = references


class TestRunnerReferenceSchema(BaseSchema):
    __model__ = TestRunnerReference
    id_ = fields.Int(data_key='Id', required=True)
    bib_info = fields.Str(data_key='Bib_info', required=True)
    additional_info = fields.Str(data_key='Additional_info', required=False)
    url_ = fields.Str(data_key='Url', required=False)


class TestRunnerReferenceResSchema(BaseSchema):
    __model__ = TestRunnerReferenceRes
    result = fields.Nested(ResultSchema, data_key='Result')
    reference = fields.Nested(TestRunnerReferenceSchema, data_key='TestRunnerReference', many=True)

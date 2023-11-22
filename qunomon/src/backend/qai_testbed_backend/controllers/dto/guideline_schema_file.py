# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from marshmallow import fields
from typing import List

from . import Result, ResultSchema, BaseSchema


class GetGuidelineSchemaFileRes:
    def __init__(self, result: Result, guideline_schema_file: dict = None) -> None:
        self.result = result
        if guideline_schema_file is not None:
            self.guideline_schema_file = guideline_schema_file


class GetGuidelineSchemaFileResSchema(BaseSchema):
    __model__ = GetGuidelineSchemaFileRes
    result = fields.Nested(ResultSchema, data_key='Result')
    guideline_schema_file = fields.Dict(data_key='GuidelineSchemaFile')


class PostGuidelineSchemaFileRes:
    def __init__(self, result: Result, guideline_schema_file_id: int = None) -> None:
        self.result = result
        if guideline_schema_file_id is not None:
            self.guideline_schema_file_id = guideline_schema_file_id


class PostGuidelineSchemaFileResSchema(BaseSchema):
    __model__ = PostGuidelineSchemaFileRes
    result = fields.Nested(ResultSchema, data_key='Result')
    guideline_schema_file_id = fields.Integer(data_key='GuidelineSchemaFileId')


class PutGuidelineSchemaFileRes:
    def __init__(self, result: Result, guideline_schema_file_id: int = None) -> None:
        self.result = result
        if guideline_schema_file_id is not None:
            self.guideline_schema_file_id = guideline_schema_file_id


class PutGuidelineSchemaFileResSchema(BaseSchema):
    __model__ = PutGuidelineSchemaFileRes
    result = fields.Nested(ResultSchema, data_key='Result')
    guideline_schema_file_id = fields.Integer(data_key='GuidelineSchemaFileId')


class DeleteGuidelineSchemaFileRes:
    def __init__(self, result: Result) -> None:
        self.result = result


class DeleteGuidelineSchemaFileResSchema(BaseSchema):
    __model__ = DeleteGuidelineSchemaFileRes
    result = fields.Nested(ResultSchema, data_key='Result')


class CheckGuidelineSchemaFileRes:
    def __init__(self, result: Result, check_result: bool, warning_message: List[str] = None) -> None:
        self.result = result
        self.check_result = check_result
        if warning_message is not None:
            self.warning_message = warning_message


class CheckGuidelineSchemaFileResSchema(BaseSchema):
    __model__ = CheckGuidelineSchemaFileRes
    result = fields.Nested(ResultSchema, data_key='Result')
    check_result = fields.Boolean(data_key='CheckResult')
    warning_message = fields.List(fields.String(), data_key='WarningMessage', required=False)


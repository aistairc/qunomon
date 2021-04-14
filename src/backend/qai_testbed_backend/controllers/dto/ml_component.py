# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List
from marshmallow import fields

from . import Result, ResultSchema, BaseSchema


class MLComponent:
    def __init__(self, name: str, description: str, problem_domain: str, ml_framework_name: str, delete_flag: bool, id_: int = None)\
            -> None:
        self.id_ = id_
        self.name = name
        self.description = description
        self.problem_domain = problem_domain
        self.ml_framework_name = ml_framework_name
        self.delete_flag = delete_flag


class GetMLComponentRes:
    def __init__(self, result: Result, ml_components: List[MLComponent]) -> None:
        self.result = result
        self.ml_components = ml_components


class MLComponentSchema(BaseSchema):
    __model__ = MLComponent
    id_ = fields.Int(data_key='Id')
    name = fields.Str(data_key='Name')
    description = fields.Str(data_key='Description')
    problem_domain = fields.Str(data_key='ProblemDomain')
    ml_framework_name = fields.Str(data_key='MLFrameworkName')


class GetMLComponentSchemaResSchema(BaseSchema):
    __model__ = GetMLComponentRes
    result = fields.Nested(ResultSchema, data_key='Result')
    ml_components = fields.Nested(MLComponentSchema, data_key='MLComponents', many=True)


class MLComponentReq:
    def __init__(self, organizer_id_: str):
        self.organizer_id_ = organizer_id_


class PostMLComponentReq:
    def __init__(self, name: str, description: str, problem_domain: str, ml_framework_id: id) -> None:
        self.name = name
        self.description = description
        self.problem_domain = problem_domain
        self.ml_framework_id = ml_framework_id


class PostMLComponentReqSchema(BaseSchema):
    __model__ = PostMLComponentReq
    name = fields.Str(data_key='Name')
    description = fields.Str(data_key='Description')
    problem_domain = fields.Str(data_key='ProblemDomain')
    ml_framework_id = fields.Int(data_key='MLFrameworkId')


class PostMLComponentRes:
    def __init__(self, result: Result, ml_component_id: int) -> None:
        self.result = result
        self.ml_component_id = ml_component_id


class PostMLComponentResSchema(BaseSchema):
    __model__ = PostMLComponentRes
    result = fields.Nested(ResultSchema, data_key='Result')
    ml_component_id = fields.Integer(data_key='MLComponentId')

class DeleteMLComponentRes:
    def __init__(self, result: Result) -> None:
        self.result = result

class DeleteMLComponentResSchema(BaseSchema):
    __model__ = DeleteMLComponentRes
    result = fields.Nested(ResultSchema, data_key='Result')
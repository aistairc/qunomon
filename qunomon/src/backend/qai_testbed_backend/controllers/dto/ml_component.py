# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List
from marshmallow import fields

from . import Result, ResultSchema, BaseSchema


class MLComponent:
    def __init__(self, name: str, description: str, problem_domain: str, ml_framework_name: str, guideline_name: str, scope_name: str,
                 scope_id: str, delete_flag: bool, guideline_reason: str = None, scope_reason: str = None, report_opinion: str = None, id_: int = None)\
            -> None:
        self.id_ = id_
        self.name = name
        self.description = description
        self.problem_domain = problem_domain
        self.ml_framework_name = ml_framework_name
        self.delete_flag = delete_flag
        self.guideline_name = guideline_name
        self.scope_name = scope_name
        self.scope_id = scope_id
        self.guideline_reason = guideline_reason
        self.scope_reason = scope_reason
        self.report_opinion = report_opinion


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
    guideline_name = fields.Str(data_key='GuidelineName')
    scope_name = fields.Str(data_key='ScopeName')
    scope_id = fields.Str(data_key='ScopeId')
    guideline_reason = fields.Str(data_key='GuidelineReason')
    scope_reason = fields.Str(data_key='ScopeReason')
    report_opinion = fields.Str(data_key='ReportOpinion')


class GetMLComponentSchemaResSchema(BaseSchema):
    __model__ = GetMLComponentRes
    result = fields.Nested(ResultSchema, data_key='Result')
    ml_components = fields.Nested(MLComponentSchema, data_key='MLComponents', many=True)


class PostMLComponentReq:
    def __init__(self, name: str, description: str, problem_domain: str, ml_framework_id: id, guideline_id: id, scope_id: id,
                 guideline_reason: str = None, scope_reason: str = None) -> None:
        self.name = name
        self.description = description
        self.problem_domain = problem_domain
        self.ml_framework_id = ml_framework_id
        self.guideline_id = guideline_id
        self.scope_id = scope_id
        self.guideline_reason = guideline_reason
        self.scope_reason = scope_reason


class PostMLComponentReqSchema(BaseSchema):
    __model__ = PostMLComponentReq
    name = fields.Str(data_key='Name')
    description = fields.Str(data_key='Description')
    problem_domain = fields.Str(data_key='ProblemDomain')
    ml_framework_id = fields.Int(data_key='MLFrameworkId')
    guideline_id = fields.Int(data_key='GuidelineId')
    scope_id = fields.Int(data_key='ScopeId')
    guideline_reason = fields.Str(data_key='GuidelineReason', allow_none=True)
    scope_reason = fields.Str(data_key='ScopeReason', allow_none=True)


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


class PutMLComponentReq:
    def __init__(self, name: str, description: str, problem_domain: str, ml_framework_id: id, guideline_id: id, scope_id: id,
                 guideline_reason: str = None, scope_reason: str = None) -> None:
        self.name = name
        self.description = description
        self.problem_domain = problem_domain
        self.ml_framework_id = ml_framework_id
        self.guideline_id = guideline_id
        self.scope_id = scope_id
        self.guideline_reason = guideline_reason
        self.scope_reason = scope_reason


class PutMLComponentReqSchema(BaseSchema):
    __model__ = PutMLComponentReq
    name = fields.Str(data_key='Name')
    description = fields.Str(data_key='Description')
    problem_domain = fields.Str(data_key='ProblemDomain')
    ml_framework_id = fields.Int(data_key='MLFrameworkId')
    guideline_id = fields.Int(data_key='GuidelineId')
    scope_id = fields.Int(data_key='ScopeId')
    guideline_reason = fields.Str(data_key='GuidelineReason', allow_none=True)
    scope_reason = fields.Str(data_key='ScopeReason', allow_none=True)


class PutMLComponentRes:
    def __init__(self, result: Result, ml_component_id: int) -> None:
        self.result = result
        self.ml_component_id = ml_component_id


class PutMLComponentResSchema(BaseSchema):
    __model__ = PutMLComponentRes
    result = fields.Nested(ResultSchema, data_key='Result')
    ml_component_id = fields.Integer(data_key='MLComponentId')


class PutReportOpinionReq:
    def __init__(self, report_opinion: str = None) -> None:
        self.report_opinion = report_opinion


class PutReportOpinionReqSchema(BaseSchema):
    __model__ = PutReportOpinionReq
    report_opinion = fields.Str(data_key='ReportOpinion')


class PutReportOpinionRes:
    def __init__(self, result: Result, ml_component_id: int) -> None:
        self.result = result
        self.ml_component_id = ml_component_id


class PutReportOpinionResSchema(BaseSchema):
    __model__ = PutReportOpinionRes
    result = fields.Nested(ResultSchema, data_key='Result')
    ml_component_id = fields.Integer(data_key='MLComponentId')


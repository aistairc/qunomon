# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from marshmallow import fields
from typing import List

from . import Result, ResultSchema, BaseSchema


class ReportTemplate:
    def __init__(self, id_: int, name: str, guideline_id: int, creation_datetime: str, update_datetime: str) -> None:
        self.id_ = id_
        self.name = name
        self.guideline_id = guideline_id
        self.creation_datetime = creation_datetime
        self.update_datetime = update_datetime


class GetReportTemplatesRes:
    def __init__(self, result: Result, report_templates: List[ReportTemplate]) -> None:
        self.result = result
        self.report_templates = report_templates


class ReportTemplateSchema(BaseSchema):
    __model__ = ReportTemplate
    id_ = fields.Int(data_key='Id')
    name = fields.Str(data_key='Name')
    guideline_id = fields.Int(data_key='GuidelineId')
    creation_datetime = fields.Str(data_key='CreationDatetime')
    update_datetime = fields.Str(data_key='UpdateDatetime')


class GetReportTemplateResSchema(BaseSchema):
    __model__ = GetReportTemplatesRes
    result = fields.Nested(ResultSchema, data_key='Result')
    report_templates = fields.Nested(ReportTemplateSchema, data_key='ReportTemplates', many=True)


class PostReportTemplateReq:
    def __init__(self, id_: int, guideline_id: str, name: str) -> None:
        self.id_ = id_
        self.guideline_id = guideline_id
        self.name = name


class PostReportTemplateReqSchema(BaseSchema):
    __model__ = PostReportTemplateReq
    id_ = fields.Int(data_key='Id')
    guideline_id = fields.Str(data_key='GuidelineId')
    name = fields.Str(data_key='Name')


class PostReportTemplateRes:
    def __init__(self, result: Result, report_template_id: int) -> None:
        self.result = result
        self.report_template_id = report_template_id


class PostReportTemplateResSchema(BaseSchema):
    __model__ = PostReportTemplateRes
    result = fields.Nested(ResultSchema, data_key='Result')
    report_template_id = fields.Integer(data_key='ReportTemplateId')


class PostReportTemplateGenerateReq:
    def __init__(self, guideline_id: str) -> None:
        self.guideline_id = guideline_id


class PostReportTemplateGenerateReqSchema(BaseSchema):
    __model__ = PostReportTemplateGenerateReq
    guideline_id = fields.Str(data_key='GuidelineId')

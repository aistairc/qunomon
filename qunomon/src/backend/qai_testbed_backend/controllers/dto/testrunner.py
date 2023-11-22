# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import datetime
from marshmallow import fields, post_dump
from typing import List

from . import Result, ResultSchema, BaseSchema


class PostTestRunnerReq:
    def __init__(self, command: str, test_description_ids: []) -> None:
        self.command = command
        self.test_description_ids = test_description_ids


class PostTestRunnerReqSchema(BaseSchema):
    __model__ = PostTestRunnerReq
    command = fields.Str(data_key='Command', required=True)
    test_description_ids = fields.List(fields.Int, data_key='TestDescriptionIds', required=True)


class Job:
    def __init__(self, id_: str, start_datetime: datetime) -> None:
        self.id_ = id_
        self.start_datetime = start_datetime


class PostTestRunnerRes:
    def __init__(self, result: Result, job: Job) -> None:
        self.result = result
        self.job = job


class JobSchema(BaseSchema):
    __model__ = Job
    id_ = fields.Str(data_key='Id')
    start_datetime = fields.Str(data_key='StartDateTime')


class PostTestRunnerResSchema(BaseSchema):
    __model__ = PostTestRunnerRes
    result = fields.Nested(ResultSchema, data_key='Result')
    job = fields.Nested(JobSchema, data_key='Job')


class RunStatus:
    def __init__(self, id_: int, status: str, test_description_id: int, result: str, result_detail: str) -> None:
        self.id_ = id_
        self.status = status
        self.test_description_id = test_description_id
        self.result = result
        self.result_detail = result_detail


class JobStatus:
    def __init__(self, id_: int, status: str, result: str, result_detail: str) -> None:
        self.id_ = id_
        self.status = status
        self.result = result
        self.result_detail = result_detail


class GetTestRunnerStatusRes:
    def __init__(self, result: Result, job_status: JobStatus, run_statuses: [RunStatus]) -> None:
        self.result = result
        self.job_status = job_status
        self.run_statuses = run_statuses


class RunStatusSchema(BaseSchema):
    __model__ = RunStatus
    id_ = fields.Int(data_key='Id')
    status = fields.Str(data_key='Status')
    test_description_id = fields.Int(data_key='TestDescriptionID')
    result = fields.Str(data_key='Result')
    result_detail = fields.Str(data_key='ResultDetail')


class JobStatusSchema(BaseSchema):
    __model__ = JobStatus
    id_ = fields.Int(data_key='Id', required=True)
    status = fields.Str(data_key='Status', required=True)
    result = fields.Str(data_key='Result', required=True)
    result_detail = fields.Str(data_key='ResultDetail', required=True)


class GetTestRunnerStatusResSchema(BaseSchema):
    __model__ = GetTestRunnerStatusRes
    result = fields.Nested(ResultSchema, data_key='Result')
    job_status = fields.Nested(JobStatusSchema, data_key='Job', required=True)
    run_statuses = fields.Nested(RunStatusSchema, data_key='Runs', many=True)


class GraphParam:
    def __init__(self, id_: int, report_required: bool, report_index: int = 0, report_name: str = '') -> None:
        self.id_ = id_
        self.report_required = report_required
        self.report_index = report_index
        self.report_name = report_name


class PostReportGeneratorReq:
    def __init__(self, command: str, destination: [], params=None) -> None:
        self.command = command
        self.destination = destination
        self.params = params


class GraphsTemplate:
    def __init__(self, opinion: str = '', graphs: List[GraphParam] = [], target_report_template_id: int = None) -> None:
        self.opinion = opinion
        self.graphs = graphs
        self.target_report_template_id = target_report_template_id


class GraphParamSchema(BaseSchema):
    __model__ = GraphParam
    id_ = fields.Int(data_key='GraphId')
    report_required = fields.Boolean(data_key='ReportRequired')
    report_index = fields.Int(data_key='ReportIndex', required=False)
    report_name = fields.Str(data_key='ReportName', required=False)


class GraphsTemplateSchema(BaseSchema):
    __model__ = GraphsTemplate
    opinion = fields.Str(data_key='Opinion', required=False)
    graphs = fields.Nested(GraphParamSchema, data_key='Graphs', many=True, required=False)
    target_report_template_id = fields.Int(data_key='TargetReportTemplateId', required=False)


class PostReportGeneratorReqSchema(BaseSchema):
    __model__ = PostReportGeneratorReq
    command = fields.Str(data_key='Command')
    destination = fields.List(fields.Str, data_key='Destination')
    params = fields.Nested(GraphsTemplateSchema, data_key='Params')


class PostReportGeneratorRes:
    def __init__(self, result: Result, out_params: {}) -> None:
        self.result = result
        self.out_params = out_params


class PostReportGeneratorResSchema(BaseSchema):
    __model__ = PostReportGeneratorRes
    result = fields.Nested(ResultSchema, data_key='Result')
    out_params = fields.Dict(keys=fields.Str, values=fields.Str, data_key='OutParams')

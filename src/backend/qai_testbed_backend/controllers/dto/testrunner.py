# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import datetime
from marshmallow import fields, post_dump
from typing import List, Optional

from . import Result, ResultSchema, BaseSchema
from .format import Format, FormatSchema
from .data_type import DataType, DataTypeSchema
from .downloadable_template import DownloadableTemplate, DownloadableTemplateSchema


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
    def __init__(self, opinion: str, graphs: List[GraphParam]) -> None:
        self.opinion = opinion
        self.graphs = graphs


class GraphParamSchema(BaseSchema):
    __model__ = GraphParam
    id_ = fields.Int(data_key='GraphId')
    report_required = fields.Boolean(data_key='ReportRequired')
    report_index = fields.Int(data_key='ReportIndex', required=False)
    report_name = fields.Str(data_key='ReportName', required=False)


class GraphsTemplateSchema(BaseSchema):
    __model__ = GraphsTemplate
    opinion = fields.Str(data_key='Opinion')
    graphs = fields.Nested(GraphParamSchema, data_key='Graphs', many=True)


class PostReportGeneratorReqSchema(BaseSchema):
    __model__ = PostReportGeneratorReq
    command = fields.Str(data_key='Command')
    destination = fields.List(fields.Str, data_key='Destination')
    params = fields.Nested(GraphsTemplateSchema, data_key='Params')


class PostReportGeneratorRes:
    def __init__(self, result: Result, out_params: {}) -> None:
        self.result = result
        self.out_params = out_params


class ParamTemplate:
    def __init__(self, type_: str, description: str, default_value: str = None, id_: Optional[int] = None,
                 name: Optional[str] = None, test_runner_param_template_id: Optional[int] = None) -> None:
        self.id_ = id_
        self.name = name
        self.type_ = type_
        self.test_runner_param_template_id = test_runner_param_template_id
        self.description = description
        self.default_value = default_value


class PostReportGeneratorResSchema(BaseSchema):
    __model__ = PostReportGeneratorRes
    result = fields.Nested(ResultSchema, data_key='Result')
    out_params = fields.Dict(keys=fields.Str, values=fields.Str, data_key='OutParams')


class TestInventoryTemplate:
    def __init__(self, id_: int, name: str, type_: DataType, description: str, formats: List[Format],
                 schema: str = None) -> None:
        self.id_ = id_
        self.name = name
        self.type_ = type_
        self.description = description
        self.formats = formats
        self.schema = schema


class TestRunnerTemplate:
    def __init__(self, id_: int, quality_dimension_id: int, name: str, description: str,
                 author: str, version: str, quality: str, landing_page: str, reference: List[str],
                 params: List[ParamTemplate],
                 test_inventory_templates: List[TestInventoryTemplate],
                 report, downloads: List[DownloadableTemplate], email: str = None) -> None:
        self.id_ = id_
        self.quality_dimension_id = quality_dimension_id
        self.name = name
        self.description = description
        self.author = author
        self.email = email
        self.version = version
        self.quality = quality
        self.landing_page = landing_page
        self.reference = reference
        self.params = params
        self.test_inventory_templates = test_inventory_templates
        self.report = report
        self.downloads = downloads


class GetTestRunnerRes:
    def __init__(self, result: Result, test_runners: List[TestRunnerTemplate]) -> None:
        self.result = result
        self.test_runners = test_runners


class ParamTemplateSchema(BaseSchema):
    __model__ = ParamTemplate
    id_ = fields.Int(data_key='Id', required=True)
    name = fields.Str(data_key='Name', required=True)
    type_ = fields.Str(data_key='Type', required=True)
    description = fields.Str(data_key='Description', required=True)
    default_value = fields.Str(data_key='DefaultVal', required=True)

    @post_dump
    def remove_skip_values(self, data, **_):
        return {
            key: value for key, value in data.items()
            if (key != 'DefaultVal') or (value is not None)
        }


class TargetInventoryTemplateSchema(BaseSchema):
    __model__ = TestInventoryTemplate
    id_ = fields.Int(data_key='Id', required=True)
    name = fields.Str(data_key='Name', required=True)
    type_ = fields.Nested(DataTypeSchema, data_key='DataType', required=True)
    description = fields.Str(data_key='Description', required=True)
    formats = fields.Nested(FormatSchema, data_key='Formats', many=True)
    schema = fields.Str(data_key='Schema', required=False)

    @post_dump
    def remove_skip_values(self, data, **_):
        return {
            key: value for key, value in data.items()
            if (key != 'Schema') or (value is not None)
        }


class Measure:
    def __init__(self, id_: int, name: str, type_: str, description: str, min_value:float, max_value:float, structure: str) -> None:
        self.id_ = id_
        self.name = name
        self.type_ = type_
        self.description = description
        self.min_value = min_value
        self.max_value = max_value
        self.structure = structure


class MeasureSchema(BaseSchema):
    __model__ = Measure
    id_ = fields.Int(data_key='Id', required=True)
    name = fields.Str(data_key='Name', required=True)
    type_ = fields.Str(data_key='Type', required=True)
    description = fields.Str(data_key='Description', required=True)
    min_value = fields.Str(data_key='Min', required=False)
    max_value = fields.Str(data_key='Max', required=False)
    structure = fields.Str(data_key='Structure', required=True)


class Resource:
    def __init__(self, id_: int, name: str, type_: str, description: str) -> None:
        self.id_ = id_
        self.name = name
        self.type_ = type_
        self.description = description


class ResourceSchema(BaseSchema):
    __model__ = Resource
    id_ = fields.Int(data_key='Id', required=True)
    name = fields.Str(data_key='Name', required=True)
    type_ = fields.Str(data_key='Type', required=True)
    description = fields.Str(data_key='Description', required=True)


class Report:
    def __init__(self, measures: List[Measure], resources: List[Resource]) -> None:
        self.measures = measures
        self.resources = resources


class ReportSchema(BaseSchema):
    __model__ = Report
    measures = fields.Nested(MeasureSchema, data_key='Measures', many=True)
    resources = fields.Nested(ResourceSchema, data_key='Resources', many=True)


class TestRunnersTemplateSchema(BaseSchema):
    __model__ = TestRunnerTemplate
    id_ = fields.Int(data_key='Id', required=True)
    quality_dimension_id = fields.Int(data_key='QualityDimensionId', required=True)
    name = fields.Str(data_key='Name', required=True)
    description = fields.Str(data_key='Description', required=True)
    author = fields.Str(data_key='Author', required=True)
    email = fields.Str(data_key='Email', required=False)
    version = fields.Str(data_key='Version', required=True)
    quality = fields.Str(data_key='Quality', required=True)
    landing_page = fields.Str(data_key='LandingPage', required=True)
    reference = fields.List(fields.Str, data_key='Reference', required=True)
    params = fields.Nested(ParamTemplateSchema, data_key='ParamTemplates', many=True)
    test_inventory_templates = fields.Nested(TargetInventoryTemplateSchema, data_key='TargetInventories', many=True)
    report = fields.Nested(ReportSchema, data_key='Report', many=False)
    downloads = fields.Nested(DownloadableTemplateSchema, data_key='Downloads', many=True)

    @post_dump
    def remove_skip_values(self, data, **_):
        return {
            key: value for key, value in data.items()
            if (key != 'Email') or (value is not None)
        }


class GetTestRunnerResSchema(BaseSchema):
    __model__ = GetTestRunnerRes
    result = fields.Nested(ResultSchema, data_key='Result')
    test_runners = fields.Nested(TestRunnersTemplateSchema, data_key='TestRunners', many=True)

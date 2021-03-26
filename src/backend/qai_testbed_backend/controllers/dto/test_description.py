# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import datetime
from typing import List, Optional
from marshmallow import fields, post_dump

from . import Result, ResultSchema, BaseSchema
from .downloadable_data import DownloadableData, DownloadableDataSchema


class DataType:
    def __init__(self, id_: int, name: str) -> None:
        self.id_ = id_
        self.name = name


class Inventory:
    def __init__(self, id_: int, name: str, type_: DataType, description: str, template_inventory_id: int) -> None:
        self.id_ = id_
        self.name = name
        self.type_ = type_
        self.description = description
        self.template_inventory_id = template_inventory_id


class TestDescription:
    def __init__(self, id_: int, name: str, status: str, result: str, result_detail: str, creation_datetime: datetime,
                 opinion: str,
                 delete_flag: bool, target_inventories: List[Inventory],
                 update_datetime: datetime, star: bool,
                 parent_id: Optional[int] = None,
                 test_runner_id: Optional[int] = None) -> None:
        self.id_ = id_
        self.name = name
        self.status = status
        self.result = result
        self.result_detail = result_detail
        self.creation_datetime = creation_datetime
        self.opinion = opinion
        self.delete_flag = delete_flag
        self.parent_id = parent_id
        self.target_inventories = target_inventories
        self.update_datetime = update_datetime
        self.star = star
        self.test_runner_id = test_runner_id


class Test:
    def __init__(self, id_: int, status: str, result: str, result_detail: str,
                 test_descriptions: List[TestDescription]) -> None:
        self.id_ = id_
        self.status = status
        self.result = result
        self.result_detail = result_detail
        self.test_descriptions = test_descriptions


class GetTestDescriptionsRes:
    def __init__(self, result: Result, test: Test) -> None:
        self.result = result
        self.test = test


class QualityDimension:
    def __init__(self, id_: int, name: str) -> None:
        self.id_ = id_
        self.name = name


class QualityMeasurement:
    def __init__(self, id_: int, enable: bool, name: Optional[str] = None,
                 description: Optional[str] = None, structure: Optional[str] = None,
                 value: Optional[str] = None, relational_operator_id: Optional[int] = None,) -> None:
        self.id_ = id_
        self.name = name
        self.description = description
        self.structure = structure
        self.value = value
        self.relational_operator_id = relational_operator_id
        self.enable = enable


class QualityMeasurementForReport:
    def __init__(self, id_: int, enable: bool, name: Optional[str] = None,
                 description: Optional[str] = None,structure: Optional[str] = None,
                 value: Optional[str] = None, relational_operator: Optional[str] = None,) -> None:
        self.id_ = id_
        self.name = name
        self.description = description
        self.structure = structure
        self.value = value
        self.relational_operator = relational_operator
        self.enable = enable


class PutInventory:
    def __init__(self, id_: int, inventory_id: int, template_inventory_id: int) -> None:
        self.id_ = id_
        self.inventory_id = inventory_id
        self.template_inventory_id = template_inventory_id


class TestRunnerParam:
    def __init__(self, value: str, id_: Optional[int] = None,
                 name: Optional[str] = None, test_runner_param_template_id: Optional[int] = None) -> None:
        self.id_ = id_
        self.name = name
        self.value = value
        self.test_runner_param_template_id = test_runner_param_template_id


class TestRunner:
    def __init__(self, id_: int, params: List[TestRunnerParam], description: str = None, author: str = None,
                 version: str = None, quality: str = None, landing_page: str = None, email: Optional[str] = None,
                 name: Optional[str] = None) -> None:
        self.id_ = id_
        self.name = name
        self.description = description
        self.author = author
        self.email = email
        self.version = version
        self.quality = quality
        self.landing_page = landing_page
        self.params = params


class Graph:
    def __init__(self, id_: int, name: str, description: str, report_required: bool, graph_type: str,
                 report_index: int, report_name: str, graph: str, file_name: str) -> None:
        self.id_ = id_
        self.name = name
        self.description = description
        self.report_required = report_required
        self.graph_type = graph_type
        self.report_index = report_index
        self.report_name = report_name
        self.graph = graph
        self.file_name = file_name


class TestDescriptionResult:
    def __init__(self, summary: str, detail: str, log_file: str, graphs: List[Graph],
                 downloads: List[DownloadableData], cpu_brand: str, cpu_arch: str,
                 cpu_clocks: str, cpu_cores: str, memory_capacity: str) -> None:
        self.summary = summary
        self.detail = detail
        self.log_file = log_file
        self.graphs = graphs
        self.downloads = downloads
        self.cpu_brand = cpu_brand
        self.cpu_arch = cpu_arch
        self.cpu_clocks = cpu_clocks
        self.cpu_cores = cpu_cores
        self.memory_capacity = memory_capacity


class TestDescriptionDetail:
    def __init__(self, id_: int, name: str, status: str, quality_dimension: QualityDimension, opinion: str,
                 delete_flag: bool,
                 quality_measurements: List[QualityMeasurement],
                 target_inventories: List[Inventory],
                 test_runner: TestRunner,
                 test_description_result: TestDescriptionResult,
                 creation_datetime: datetime,
                 update_datetime: datetime,
                 star: bool,
                 parent_id: Optional[int]) -> None:
        self.id_ = id_
        self.name = name
        self.status = status
        self.quality_dimension = quality_dimension
        self.opinion = opinion
        self.delete_flag = delete_flag
        self.quality_measurements = quality_measurements
        self.target_inventories = target_inventories
        self.test_runner = test_runner
        self.test_description_result = test_description_result
        self.parent_id = parent_id
        self.creation_datetime = creation_datetime
        self.update_datetime = update_datetime
        self.star = star


class TestDescriptionForReport:
    def __init__(self, id_: int, name: str, quality_dimension: QualityDimension, opinion: str,
                 value_target: bool,
                 quality_measurements: List[QualityMeasurementForReport],
                 target_inventories: List[Inventory],
                 test_runner: TestRunner,
                 test_description_result: TestDescriptionResult) -> None:
        self.id_ = id_
        self.name = name
        self.quality_dimension = quality_dimension
        self.opinion = opinion
        self.value_target = value_target
        self.quality_measurements = quality_measurements
        self.target_inventories = target_inventories
        self.test_runner = test_runner
        self.test_description_result = test_description_result


class GetTestDescriptionDetailRes:
    def __init__(self, result: Result,
                 test_description_detail: TestDescriptionDetail) -> None:
        self.result = result
        self.test_description_detail = test_description_detail


class DeleteTestDescriptionRes:
    def __init__(self, result: Result) -> None:
        self.result = result


class PutTestDescriptionRes:
    def __init__(self, result: Result, test_description: TestDescription) -> None:
        self.result = result
        self.test_description = test_description


class AppendTestDescriptionRes:
    def __init__(self, result: Result) -> None:
        self.result = result


class DataTypeSchema(BaseSchema):
    __model__ = DataType
    id_ = fields.Int(data_key='Id')
    name = fields.Str(data_key='Name')


class InventorySchema(BaseSchema):
    __model__ = Inventory
    id_ = fields.Int(data_key='Id')
    name = fields.Str(data_key='Name')
    type_ = fields.Nested(DataTypeSchema, data_key='DataType')
    description = fields.Str(data_key='Description')
    template_inventory_id = fields.Int(data_key='TemplateInventoryId')


class TestDescriptionSchema(BaseSchema):
    __model__ = TestDescription
    id_ = fields.Int(data_key='Id')
    parent_id = fields.Int(data_key='ParentID')
    name = fields.Str(data_key='Name')
    result = fields.Str(data_key='Result')
    result_detail = fields.Str(data_key='ResultDetail')
    creation_datetime = fields.DateTime(data_key='CreationDatetime')
    update_datetime = fields.DateTime(data_key='UpdateDatetime')
    target_inventories = fields.Nested(InventorySchema, data_key='TargetInventories', many=True)
    opinion = fields.Str(data_key='Opinion')
    star = fields.Bool(data_key='Star')
    test_runner_id = fields.Int(data_key='TestRunnerId')

    @post_dump
    def remove_skip_values(self, data, **_):
        return {
            key: value for key, value in data.items()
            if (key != 'ParentID') or (value is not None)
        }


class TestSchema(BaseSchema):
    __model__ = Test
    id_ = fields.Int(data_key='Id')
    status = fields.Str(data_key='Status')
    result = fields.Str(data_key='Result')
    result_detail = fields.Str(data_key='ResultDetail')
    test_descriptions = fields.Nested(TestDescriptionSchema, data_key='TestDescriptions', many=True)


class GetTestDescriptionsResSchema(BaseSchema):
    __model__ = GetTestDescriptionsRes
    result = fields.Nested(ResultSchema, data_key='Result')
    test = fields.Nested(TestSchema, data_key='Test')


class QualityDimensionSchema(BaseSchema):
    __model__ = QualityDimension
    id_ = fields.Int(data_key='Id')
    name = fields.Str(data_key='Name')


class QualityMeasurementSchema(BaseSchema):
    __model__ = QualityMeasurement
    id_ = fields.Int(data_key='Id')
    name = fields.Str(data_key='Name', required=False)
    value = fields.Str(data_key='Value', required=False)
    description = fields.Str(data_key='Description', required=False)
    structure = fields.Str(data_key='Structure', required=False)
    relational_operator_id = fields.Int(data_key='RelationalOperatorId', required=False)
    enable = fields.Bool(data_key='Enable')


class QualityMeasurementForReportSchema(BaseSchema):
    __model__ = QualityMeasurementForReport
    id_ = fields.Int(data_key='Id')
    name = fields.Str(data_key='Name', required=False)
    value = fields.Str(data_key='Value', required=False)
    description = fields.Str(data_key='Description', required=False)
    structure = fields.Str(data_key='Structure', required=False)
    relational_operator = fields.Str(data_key='RelationalOperator', required=False)
    enable = fields.Bool(data_key='Enable')


class PutInventorySchema(BaseSchema):
    __model__ = PutInventory
    id_ = fields.Int(data_key='Id')
    inventory_id = fields.Int(data_key='InventoryId')
    template_inventory_id = fields.Int(data_key='TemplateInventoryId')


class TestRunnerParamSchema(BaseSchema):
    __model__ = TestRunnerParam
    id_ = fields.Int(data_key='Id', required=False)
    name = fields.Str(data_key='Name', required=False)
    value = fields.Str(data_key='Value')
    min_value = fields.Float(data_key='Min', required=False)
    max_value = fields.Float(data_key='Max', required=False)
    test_runner_param_template_id = fields.Int(data_key='TestRunnerParamTemplateId', required=False)


class TestRunnerSchema(BaseSchema):
    __model__ = TestRunner
    id_ = fields.Int(data_key='Id')
    name = fields.Str(data_key='Name', required=False)
    description = fields.Str(data_key='Description', required=False)
    author = fields.Str(data_key='Author', required=False)
    email = fields.Str(data_key='Email', required=False)
    version = fields.Str(data_key='Version', required=False)
    quality = fields.Str(data_key='Quality', required=False)
    landing_page = fields.Str(data_key='LandingPage', required=False)
    params = fields.Nested(TestRunnerParamSchema, data_key='Params', many=True)


class GraphSchema(BaseSchema):
    __model__ = Graph
    id_ = fields.Int(data_key='Id')
    name = fields.Str(data_key='Name')
    file_name = fields.Str(data_key='FileName')
    graph_type = fields.Str(data_key='GraphType')
    description = fields.Str(data_key='Description')
    report_required = fields.Boolean(data_key='ReportRequired')
    report_index = fields.Int(data_key='ReportIndex')
    report_name = fields.Str(data_key='ReportName')
    graph = fields.Str(data_key='Graph')


class TestDescriptionResultSchema(BaseSchema):
    __model__ = TestDescriptionResult
    summary = fields.Str(data_key='Summary')
    detail = fields.Str(data_key='Detail')
    log_file = fields.Str(data_key='LogFile')
    graphs = fields.Nested(GraphSchema, data_key='Graphs', many=True)
    downloads = fields.Nested(DownloadableDataSchema, data_key='Downloads', many=True)
    creation_datetime = fields.DateTime(data_key='CreationDatetime')
    update_datetime = fields.DateTime(data_key='UpdateDatetime')

    @post_dump
    def remove_skip_values(self, data, **_):
        return {
            key: value for key, value in data.items()
            if (key != 'Downloads') or (value is not None)
        }


class TestDescriptionDetailSchema(BaseSchema):
    __model__ = TestDescriptionDetail
    id_ = fields.Int(data_key='Id')
    name = fields.Str(data_key='Name')
    quality_dimension = fields.Nested(QualityDimensionSchema, data_key='QualityDimension')
    opinion = fields.Str(data_key='Opinion')
    quality_measurements = fields.Nested(QualityMeasurementSchema, data_key='QualityMeasurements', many=True)
    target_inventories = fields.Nested(InventorySchema, data_key='TargetInventories', many=True)
    test_runner = fields.Nested(TestRunnerSchema, data_key='TestRunner')
    test_description_result = fields.Nested(TestDescriptionResultSchema, data_key='TestDescriptionResult')
    parent_id = fields.Int(data_key='ParentID')
    star = fields.Bool(data_key='Star')

    @post_dump
    def remove_skip_values(self, data, **_):
        return {
            key: value for key, value in data.items()
            if (key != 'ParentID') or (value is not None)
        }


class TestDescriptionForReportSchema(BaseSchema):
    __model__ = TestDescriptionForReport
    id_ = fields.Int(data_key='Id')
    name = fields.Str(data_key='Name')
    quality_dimension = fields.Nested(QualityDimensionSchema, data_key='QualityDimension')
    opinion = fields.Str(data_key='Opinion')
    quality_measurements = fields.Nested(QualityMeasurementForReportSchema, data_key='QualityMeasurements', many=True)
    target_inventories = fields.Nested(InventorySchema, data_key='TargetInventories', many=True)
    test_runner = fields.Nested(TestRunnerSchema, data_key='TestRunner')
    test_description_result = fields.Nested(TestDescriptionResultSchema, data_key='TestDescriptionResult')
    value_target = fields.Str(data_key='ValueTarget')


class GetTestDescriptionDetailResSchema(BaseSchema):
    __model__ = GetTestDescriptionsRes
    result = fields.Nested(ResultSchema, data_key='Result')
    test_description_detail = fields.Nested(TestDescriptionDetailSchema, data_key='TestDescriptionDetail')


class GetTestDescriptionForReportResSchema(BaseSchema):
    __model__ = GetTestDescriptionsRes
    result = fields.Nested(ResultSchema, data_key='Result')
    test_description_detail = fields.Nested(TestDescriptionForReportSchema, data_key='TestDescriptionDetail')


class DeleteTestDescriptionsResSchema(BaseSchema):
    __model__ = DeleteTestDescriptionRes
    result = fields.Nested(ResultSchema, data_key='Result')


class PutTestDescriptionsResSchema(BaseSchema):
    __model__ = PutTestDescriptionRes
    result = fields.Nested(ResultSchema, data_key='Result')


class PutTestDescriptionsReq:
    def __init__(self, name: str, quality_dimension_id: int, quality_measurements: List[QualityMeasurement],
                 target_inventories: List[PutInventory], test_runner: TestRunner) -> None:
        self.name = name
        self.quality_dimension_id = quality_dimension_id
        self.quality_measurements = quality_measurements
        self.target_inventories = target_inventories
        self.test_runner = test_runner


class PutTestDescriptionsReqSchema(BaseSchema):
    __model__ = PutTestDescriptionsReq
    name = fields.Str(data_key='Name', required=True)
    quality_dimension_id = fields.Int(data_key='QualityDimensionID', required=True)
    quality_measurements = fields.Nested(QualityMeasurementSchema, data_key='QualityMeasurements',
                                         many=True, required=True)
    target_inventories = fields.Nested(PutInventorySchema, data_key='TargetInventories', many=True, required=True)
    test_runner = fields.Nested(TestRunnerSchema, data_key='TestRunner', required=True)


class AppendTestDescriptionResSchema(BaseSchema):
    __model__ = AppendTestDescriptionRes
    result = fields.Nested(ResultSchema, data_key='Result')


class AppendTestDescriptionReq:
    def __init__(self, name: str, quality_dimension_id: int, quality_measurements: List[QualityMeasurement],
                 target_inventories: List[PutInventory], test_runner: TestRunner,
                 parent_id: Optional[int] = None) -> None:
        self.name = name
        self.quality_dimension_id = quality_dimension_id
        self.quality_measurements = quality_measurements
        self.target_inventories = target_inventories
        self.test_runner = test_runner
        self.parent_id = parent_id


class AppendTestDescriptionReqSchema(BaseSchema):
    __model__ = AppendTestDescriptionReq
    name = fields.Str(data_key='Name', required=True)
    quality_dimension_id = fields.Int(data_key='QualityDimensionID', required=True)
    parent_id = fields.Int(data_key='ParentID', required=False)
    quality_measurements = fields.Nested(QualityMeasurementSchema, data_key='QualityMeasurements',
                                         many=True, required=True)
    target_inventories = fields.Nested(PutInventorySchema, data_key='TargetInventories', many=True, required=True)
    test_runner = fields.Nested(TestRunnerSchema, data_key='TestRunner', required=True)


class GetTestDescriptionAncestorsRes:
    def __init__(self, result: Result, test_descriptions: List[TestDescription]) -> None:
        self.result = result
        self.test_descriptions = test_descriptions


class GetTestDescriptionAncestorsResSchema(BaseSchema):
    __model__ = GetTestDescriptionAncestorsRes
    result = fields.Nested(ResultSchema, data_key='Result')
    test_descriptions = fields.Nested(TestDescriptionSchema, data_key='TestDescriptions', many=True)

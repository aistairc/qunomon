# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import datetime
from typing import List
from marshmallow import Schema, fields

from . import Result, ResultSchema


class TestDescription:
    def __init__(self, id_: int, name: str, result: str, creation_datetime: datetime) -> None:
        self.id = id_
        self.name = name
        self.result = result
        self.creation_datetime = creation_datetime


class Test:
    def __init__(self, id_: int, status: str, result: str, test_descriptions: List[TestDescription]) -> None:
        self.id = id_
        self.status = status
        self.result = result
        self.test_descriptions = test_descriptions


class GetTestDescriptionsRes:
    def __init__(self, result: Result, test: Test) -> None:
        self.result = result
        self.test = test


class QualityDimension:
    def __init__(self, id_: int, name: str) -> None:
        self.id = id_
        self.name = name


class Operand:
    def __init__(self, id_: int, name: str, value: float, unit: str) -> None:
        self.id = id_
        self.name = name
        self.value = value
        self.unit = unit


class QualityMeasurement:
    def __init__(self, id_: int, name: str, operands: List[Operand]) -> None:
        self.id = id_
        self.name = name
        self.operands = operands


class Inventory:
    def __init__(self, id_: int, name: str) -> None:
        self.id = id_
        self.name = name


class TestRunnerParam:
    def __init__(self, id_: int, name: str, value: str) -> None:
        self.id = id_
        self.name = name
        self.value = value


class TestRunner:
    def __init__(self, id_: int, name: str, params: List[TestRunnerParam]) -> None:
        self.id = id_
        self.name = name
        self.params = params


class Graph:
    def __init__(self, id_: int, graph_type: str, graph: str) -> None:
        self.id = id_
        self.graph_type = graph_type
        self.graph = graph


class TestDescriptionResult:
    def __init__(self, summary: str, detail: str, graphs: List[Graph]) -> None:
        self.summary = summary
        self.detail = detail
        self.graphs = graphs


class TestDescriptionDetail:
    def __init__(self, id_: int, name: str, quality_dimension: QualityDimension, opinion: str,
                 quality_measurement: QualityMeasurement,
                 target_inventories: List[Inventory],
                 test_runner: TestRunner,
                 test_description_result: TestDescriptionResult) -> None:
        self.id = id_
        self.name = name
        self.quality_dimension = quality_dimension
        self.opinion = opinion
        self.quality_measurement = quality_measurement
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


class TestDescriptionSchema(Schema):
    id = fields.Int(data_key='Id')
    name = fields.Str(data_key='Name')
    result = fields.Str(data_key='Result')
    creation_datetime = fields.DateTime(data_key='CreationDatetime')

    class Meta:
        ordered = True


class TestSchema(Schema):
    id = fields.Int(data_key='Id')
    status = fields.Str(data_key='Status')
    result = fields.Str(data_key='Result')
    test_descriptions = fields.Nested(TestDescriptionSchema, data_key='TestDescriptions', many=True)

    class Meta:
        ordered = True


class GetTestDescriptionsResSchema(Schema):
    result = fields.Nested(ResultSchema, data_key='Result')
    test = fields.Nested(TestSchema, data_key='Test')

    class Meta:
        ordered = True


class QualityDimensionSchema(Schema):
    id = fields.Int(data_key='Id')
    name = fields.Str(data_key='Name')

    class Meta:
        ordered = True


class OperandSchema(Schema):
    id = fields.Int(data_key='Id')
    name = fields.Str(data_key='Name')
    value = fields.Number(data_key='Value')
    unit = fields.Str(data_key='Unit')

    class Meta:
        ordered = True


class QualityMeasurementSchema(Schema):
    id = fields.Int(data_key='Id')
    name = fields.Str(data_key='Name')
    operands = fields.Nested(OperandSchema, data_key='Operands', many=True)

    class Meta:
        ordered = True


class InventorySchema(Schema):
    id = fields.Int(data_key='Id')
    name = fields.Str(data_key='Name')

    class Meta:
        ordered = True


class TestRunnerParamSchema(Schema):
    id = fields.Int(data_key='Id')
    name = fields.Str(data_key='Name')
    value = fields.Str(data_key='Value')

    class Meta:
        ordered = True


class TestRunnerSchema(Schema):
    id = fields.Int(data_key='Id')
    name = fields.Str(data_key='Name')
    params = fields.Nested(TestRunnerParamSchema, data_key='Params', many=True)

    class Meta:
        ordered = True


class GraphSchema(Schema):
    id = fields.Int(data_key='Id')
    graph_type = fields.Str(data_key='GraphType')
    graph = fields.Str(data_key='Graph')

    class Meta:
        ordered = True


class TestDescriptionResultSchema(Schema):
    summary = fields.Str(data_key='Summary')
    detail = fields.Str(data_key='Detail')
    graphs = fields.Nested(GraphSchema, data_key='Graphs', many=True)

    class Meta:
        ordered = True


class TestDescriptionDetailSchema(Schema):
    id = fields.Int(data_key='Id')
    name = fields.Str(data_key='Name')
    quality_dimension = fields.Nested(QualityDimensionSchema, data_key='QualityDimension')
    opinion = fields.Str(data_key='Opinion')
    quality_measurement = fields.Nested(QualityMeasurementSchema, data_key='QualityMeasurement')
    target_inventories = fields.Nested(InventorySchema, data_key='TargetInventories', many=True)
    test_runner = fields.Nested(TestRunnerSchema, data_key='TestRunner')
    test_description_result = fields.Nested(TestDescriptionResultSchema, data_key='TestDescriptionResult')

    class Meta:
        ordered = True


class GetTestDescriptionDetailResSchema(Schema):
    result = fields.Nested(ResultSchema, data_key='Result')
    test_description_detail = fields.Nested(TestDescriptionDetailSchema, data_key='TestDescriptionDetail')

    class Meta:
        ordered = True


class DeleteTestDescriptionsResSchema(Schema):
    result = fields.Nested(ResultSchema, data_key='Result')

    class Meta:
        ordered = True


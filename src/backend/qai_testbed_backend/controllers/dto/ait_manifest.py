# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List
from marshmallow import fields

from . import BaseSchema


class Download:
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description


class DownloadSchema(BaseSchema):
    __model__ = Download
    name = fields.Str(data_key='name', required=True)
    description = fields.Str(data_key='description', required=True)


class Parameter:
    def __init__(self, name: str, type_: str, description: str, default_value: str = None, 
                 min_value: float = None, max_value: float = None) -> None:
        self.name = name
        self.type = type_
        self.description = description
        self.default_value = default_value
        self.min_value = min_value
        self.max_value = max_value


class ParameterSchema(BaseSchema):
    __model__ = Parameter
    name = fields.Str(data_key='name', required=True)
    type_ = fields.Str(data_key='type', required=True)
    description = fields.Str(data_key='description', required=True)
    default_value = fields.Str(data_key='default_val', required=False)
    min_value = fields.Float(data_key='min', required=False)
    max_value = fields.Float(data_key='max', required=False)


class Inventory:
    def __init__(self, name: str, type_: str, description: str, format_: List[str], schema: str = None) -> None:
        self.name = name
        self.type = type_
        self.description = description
        self.format = format_
        self.schema = schema


class InventorySchema(BaseSchema):
    __model__ = Inventory
    name = fields.Str(data_key='name', required=True)
    type_ = fields.Str(data_key='type', required=True)
    description = fields.Str(data_key='description', required=True)
    format_ = fields.List(fields.String(), data_key='format', required=True)
    schema = fields.Str(data_key='schema', required=False)


class ReportMeasure:
    def __init__(self, name: str, description: str, type_: str, 
                 structure: str, min_value: float = None, max_value: float = None) -> None:
        self.name = name
        self.description = description
        self.type = type_
        self.min_value = min_value
        self.max_value = max_value
        self.structure = structure


class ReportMeasureSchema(BaseSchema):
    __model__ = ReportMeasure
    name = fields.Str(data_key='name', required=True)
    description = fields.Str(data_key='description', required=True)
    type_ = fields.Str(data_key='type', required=True)
    min_value = fields.Float(data_key='min', required=False)
    max_value = fields.Float(data_key='max', required=False)
    structure = fields.Str(data_key='structure', required=True)


class ReportResource:
    def __init__(self, name: str, type_: str, description: str) -> None:
        self.name = name
        self.type = type_
        self.description = description


class ReportResourceSchema(BaseSchema):
    __model__ = ReportResource
    name = fields.Str(data_key='name', required=True)
    type_ = fields.Str(data_key='type', required=True)
    description = fields.Str(data_key='description', required=True)


class Report:
    def __init__(self, measures: List[ReportMeasure], resources: List[ReportResource]) -> None:
        self.measures = measures
        self.resources = resources


class ReportSchema(BaseSchema):
    __model__ = Report
    measures = fields.Nested(ReportMeasureSchema, data_key='measures', many=True, required=True)
    resources = fields.Nested(ReportResourceSchema, data_key='resources', many=True, required=True)


class AITManifest:
    def __init__(self, name: str, description: str, author: str, email: str, version: str, quality: str,
                 reference, inventories: List[Inventory], parameters: List[Parameter],
                 report: Report, downloads: List[Download]) -> None:
        self.name = name
        self.description = description
        self.author = author
        self.email = email
        self.version = version
        self.quality = quality
        self.reference = reference
        self.inventories = inventories
        self.parameters = parameters
        self.report = report
        self.downloads = downloads


class AITManifestSchema(BaseSchema):
    __model__ = AITManifest
    name = fields.Str(data_key='name', required=True)
    description = fields.Str(data_key='description', required=True)
    author = fields.Str(data_key='author', required=True)
    email = fields.Str(data_key='email', required=False)
    version = fields.Str(data_key='version', required=True)
    quality = fields.Str(data_key='quality', required=True)
    reference = fields.Raw(data_key='reference', required=False)
    inventories = fields.Nested(InventorySchema, data_key='inventories', many=True, required=True)
    parameters = fields.Nested(ParameterSchema, data_key='parameters', many=True, required=True)
    report = fields.Nested(ReportSchema, data_key='report', many=False, required=True)
    downloads = fields.Nested(DownloadSchema, data_key='downloads', many=True, required=True)

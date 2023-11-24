# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List
from marshmallow import fields

from . import Result, ResultSchema, BaseSchema


class OperandTemplate:
    def __init__(self, name: str, unit: str, description: str, type_: str, id_: int = 0) -> None:
        self.id_ = id_
        self.name = name
        self.unit = unit
        self.description = description
        self.type_ = type_


class QualityMeasurementTemplate:
    def __init__(self, name: str, structure: str, description: str,
                 type_: str, id_: int = 0, min_value: float = None, max_value: float = None) -> None:
        self.id_ = id_
        self.name = name
        self.structure = structure
        self.description = description
        self.type = type_
        self.min_value = min_value
        self.max_value = max_value


class GetQualityMeasurementTemplateRes:
    def __init__(self, result: Result, quality_measurements: List[QualityMeasurementTemplate]) -> None:
        self.result = result
        self.quality_measurements = quality_measurements


# class PostQualityMeasurementTemplateRes:
#     def __init__(self, result: Result) -> None:
#         self.result = result
#
#
# class PostQualityMeasurementTemplateReq(QualityMeasurementTemplate):
#     def __init__(self, name: str, version: str, description: str, quality_dimension_id: int,
#                  operand_templates: List[OperandTemplate]) -> None:
#         super().__init__(name=name,
#                          version=version,
#                          description=description,
#                          quality_dimension_id=quality_dimension_id,
#                          operand_templates=operand_templates)


class OperandTemplateSchema(BaseSchema):
    __model__ = OperandTemplate
    id = fields.Int(data_key='OperandTemplateId', required=False)
    name = fields.Str(data_key='Name', required=True)
    unit = fields.Str(data_key='Unit', required=True)


class QualityMeasurementTemplateSchema(BaseSchema):
    __model__ = QualityMeasurementTemplate
    id_ = fields.Int(data_key='Id', required=False)
    name = fields.Str(data_key='Name', required=True)
    description = fields.Str(data_key='Description', required=True)
    structure = fields.Str(data_key='Structure', required=True)    
    type = fields.Str(data_key='Type', required=True)
    min_value = fields.Float(data_key='Min', required=False)
    max_value = fields.Float(data_key='Max', required=False)


class GetQualityMeasurementTemplateResSchema(BaseSchema):
    __model__ = GetQualityMeasurementTemplateRes
    result = fields.Nested(ResultSchema, data_key='Result')
    quality_measurements = fields.Nested(QualityMeasurementTemplateSchema, data_key='QualityMeasurements', many=True)

#
# class PostMeasurementTemplateReqSchema(QualityMeasurementTemplateSchema):
#     __model__ = PostQualityMeasurementTemplateReq
#
#
# class PostQualityMeasurementTemplateResSchema(BaseSchema):
#     __model__ = PostQualityMeasurementTemplateRes
#     result = fields.Nested(ResultSchema, data_key='Result')

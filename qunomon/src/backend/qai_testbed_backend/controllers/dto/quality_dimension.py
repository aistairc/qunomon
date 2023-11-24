# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import datetime
from typing import List
from marshmallow import fields

from . import Result, ResultSchema, BaseSchema
from .quality_dimension_level import QualityDimensionLevel, QualityDimensionLevelSchema


class QualityDimension:
    def __init__(self, id_: int, aithub_quality_dimension_id: int, json_id: str, guideline_id: int, name: str, description: str, 
                 sub_dimensions: str, quality_dimension_levels: List[QualityDimensionLevel], url: str,
                 creation_datetime: datetime, update_datetime: datetime) -> None:
        self.id_ = id_
        self.aithub_quality_dimension_id = aithub_quality_dimension_id
        self.guideline_id = guideline_id
        self.json_id = json_id
        self.name = name
        self.description = description
        self.sub_dimensions = sub_dimensions
        self.quality_dimension_levels = quality_dimension_levels
        self.url = url
        self.creation_datetime = creation_datetime
        self.update_datetime = update_datetime


class QualityDimensions:
    def __init__(self, quality_dimensions: List[QualityDimension]) -> None:
        self.qualityDimensions = quality_dimensions


class GetQualityDimensionsRes:
    def __init__(self, result: Result, quality_dimensions: QualityDimensions) -> None:
        self.result = result
        self.quality_dimensions = quality_dimensions


class QualityDimensionSchema(BaseSchema):
    __model__ = QualityDimension
    id_ = fields.Int(data_key='Id')
    aithub_quality_dimension_id = fields.Int(data_key='AithubQualityDimensionId')
    guideline_id = fields.Int(data_key='GuidelineId')
    json_id = fields.Str(data_key='JsonId')
    name = fields.Str(data_key='Name')
    description = fields.Str(data_key='Description')
    sub_dimensions =  fields.Str(data_key='SubDimensions')
    quality_dimension_levels = fields.Nested(QualityDimensionLevelSchema, data_key='QualityDimensionLevels', many=True)
    url = fields.Str(data_key='Url')
    creation_datetime = fields.Str(data_key='CreationDatetime')
    update_datetime = fields.Str(data_key='UpdateDatetime')


class GetQualityDimensionsResSchema(BaseSchema):
    __model__ = GetQualityDimensionsRes
    result = fields.Nested(ResultSchema, data_key='Result')
    quality_dimensions = fields.Nested(QualityDimensionSchema, data_key='QualityDimensions', many=True)

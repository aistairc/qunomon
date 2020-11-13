# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List
from marshmallow import fields

from . import Result, ResultSchema, BaseSchema


class QualityDimension:
    def __init__(self, id_: int, name: str) -> None:
        self.id_ = id_
        self.name = name


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
    name = fields.Str(data_key='Name')


class GetQualityDimensionsResSchema(BaseSchema):
    __model__ = GetQualityDimensionsRes
    result = fields.Nested(ResultSchema, data_key='Result')
    quality_dimensions = fields.Nested(QualityDimensionSchema, data_key='QualityDimensions', many=True)

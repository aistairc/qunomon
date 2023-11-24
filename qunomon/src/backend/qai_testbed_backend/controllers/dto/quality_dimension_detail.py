# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.

from marshmallow import fields

from . import Result, ResultSchema, BaseSchema
from .quality_dimension import QualityDimension, QualityDimensionSchema

class GetQualityDimensionDetailRes:
    def __init__(self, result: Result, quality_dimension: QualityDimension = None) -> None:
        self.result = result
        self.quality_dimension = quality_dimension

class GetQualityDimensionDetailResSchema(BaseSchema):
    __model__ = GetQualityDimensionDetailRes
    result = fields.Nested(ResultSchema, data_key='Result')
    quality_dimension = fields.Nested(QualityDimensionSchema, data_key='QualityDimension')
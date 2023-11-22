# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from marshmallow import fields

from . import Result, ResultSchema, BaseSchema


class ScopeQualityDimension:
    def __init__(
        self,
        id: int,
        guideline_id: int,
        scope_id: int,
        quality_dimension_id: int,
        creation_datetime: str
    ) -> None:
        self.id = id
        self.guideline_id = guideline_id
        self.scope_id = scope_id
        self.quality_dimension_id = quality_dimension_id
        self.creation_datetime = creation_datetime


class GetScopeQualityDimensionsRes:
    def __init__(self, result: Result, scopeQualityDimension: ScopeQualityDimension) -> None:
        self.result = result
        self.scopeQualityDimension = scopeQualityDimension


class ScopeQualityDimensionSchema(BaseSchema):
    __model__ = ScopeQualityDimension
    id = fields.Int(data_key='Id')
    guideline_id = fields.Int(data_key='GuidelineId')
    scope_id = fields.Int(data_key='ScopeId')
    quality_dimension_id = fields.Int(data_key='QualityDimensionId')
    creation_datetime = fields.Str(data_key='CreationDatetime')


class GetScopeQualityDimensionsResSchema(BaseSchema):
    __model__ = GetScopeQualityDimensionsRes
    result = fields.Nested(ResultSchema, data_key='Result')
    scopeQualityDimension = fields.Nested(ScopeQualityDimensionSchema, data_key='ScopeQualityDimensions', many=True)

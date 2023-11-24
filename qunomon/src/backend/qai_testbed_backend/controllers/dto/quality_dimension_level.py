# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from marshmallow import fields

from . import BaseSchema


class QualityDimensionLevel:
    def __init__(
        self,
        id: int,
        quality_dimension_level_id: str,
        name: str,
        description: str,
        level: float,
        creation_datetime: str,
        update_datetime: str
    ) -> None:
        self.id = id
        self.quality_dimension_level_id = quality_dimension_level_id
        self.name = name
        self.description = description
        self.level = level
        self.creation_datetime = creation_datetime
        self.update_datetime = update_datetime


class QualityDimensionLevelSchema(BaseSchema):
    __model__ = QualityDimensionLevel
    id = fields.Int(data_key='Id')
    quality_dimension_level_id = fields.Str(data_key='QualityDimensionLevelId')
    name = fields.Str(data_key='Name')
    description = fields.Str(data_key='Description')
    level = fields.Float(data_key='Level')
    creation_datetime = fields.Str(data_key='CreationDatetime')
    update_datetime = fields.Str(data_key='UpdateDatetime')


# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import datetime
import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db
from ..controllers.dto.quality_dimension_level import QualityDimensionLevel


class QualityDimensionLevelMapper(sql_db.Model):
    __tablename__ = 'M_Quality_Dimension_Level'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    quality_dimension_level_id = sa.Column(sa.String, nullable=False)
    name = sa.Column(sa.String, nullable=True)
    description = sa.Column(sa.String, nullable=False)
    level = sa.Column(sa.Float, nullable=False)
    quality_dimension_id = sa.Column(sa.Integer, sa.ForeignKey('M_Quality_Dimension.id'))
    creation_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    update_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    delete_flag = sa.Column(sa.Boolean, unique=False, default=False)

    @hybrid_method
    def to_dto(self) -> QualityDimensionLevel:
        return QualityDimensionLevel(
            id=self.id,
            quality_dimension_level_id=self.quality_dimension_level_id,
            name=self.name,
            description=self.description,
            level=self.level,
            creation_datetime=self.creation_datetime,
            update_datetime=self.update_datetime
        )
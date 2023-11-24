# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import datetime
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db
from ..controllers.dto.scope_quality_dimension import ScopeQualityDimension


class ScopeQualityDimensionMapper(sql_db.Model):
    __tablename__ = 'M_Scope_QualityDimension'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    guideline_id = sa.Column(sa.Integer, sa.ForeignKey('M_Guideline.id'))
    scope_id = sa.Column(sa.Integer, sa.ForeignKey('M_Scope.id'))
    quality_dimension_id = sa.Column(sa.Integer, sa.ForeignKey('M_Quality_Dimension.id'))
    creation_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    update_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    delete_flag = sa.Column(sa.Boolean, unique=False, default=False)

    guideline = relationship('GuidelineMapper')
    scope = relationship('ScopeMapper')
    quality_dimension = relationship('QualityDimensionMapper')

    @hybrid_method
    def to_dto(self) -> ScopeQualityDimension:
        return ScopeQualityDimension(
            id=self.id,
            guideline_id=self.guideline_id,
            scope_id=self.scope_id,
            quality_dimension_id=self.quality_dimension_id,
            creation_datetime=self.creation_datetime
        )
# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import datetime
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from ..gateways.extensions import sql_db


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

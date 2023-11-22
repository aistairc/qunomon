# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db
# from ..controllers.dto.quality_dimension import QualityDimension


class QualityDimensionMapper(sql_db.Model):

    __tablename__ = 'M_Quality_Dimension'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    aithub_quality_dimension_id = sa.Column(sa.Integer, nullable=True)
    guideline_id = sa.Column(sa.Integer, sa.ForeignKey('M_Guideline.id'))
    json_id = sa.Column(sa.String, nullable=True)
    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String)
    sub_dimensions = sa.Column(sa.String, nullable=True)
    url = sa.Column(sa.String)
    creation_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    update_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    delete_flag = sa.Column(sa.Boolean, unique=False, default=False)

    guideline = relationship('GuidelineMapper')
    quality_dimension_level = relationship('QualityDimensionLevelMapper')

    # @hybrid_method
    # def to_dto(self) -> QualityDimension:
    #     return QualityDimension(
    #         id_=self.id,
    #         name=self.name
    #     )

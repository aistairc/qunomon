# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db
from ..controllers.dto.quality_dimension import QualityDimension


class QualityDimensionMapper(sql_db.Model):

    __tablename__ = 'M_Quality_Dimension'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)

    @hybrid_method
    def to_dto(self) -> QualityDimension:
        return QualityDimension(
            id_=self.id,
            name=self.name
        )

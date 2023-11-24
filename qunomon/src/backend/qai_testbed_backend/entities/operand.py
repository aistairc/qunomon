# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from ..gateways.extensions import sql_db


class OperandMapper(sql_db.Model):

    __tablename__ = 'T_Operand'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    value = sa.Column(sa.String, nullable=False)
    enable = sa.Column(sa.Boolean, unique=False, default=True)

    quality_measurement_id = sa.Column(sa.Integer, sa.ForeignKey('M_Quality_Measurement.id'))
    test_description_id = sa.Column(sa.Integer, sa.ForeignKey('T_TestDescription.id'))
    relational_operator_id = sa.Column(sa.Integer, sa.ForeignKey('M_RelationalOperator.id'))

    quality_measurement = relationship('QualityMeasurementMapper')

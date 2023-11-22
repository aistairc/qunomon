# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from .operand import OperandMapper
from ..gateways.extensions import sql_db


class QualityMeasurementMapper(sql_db.Model):

    __tablename__ = 'M_Quality_Measurement'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=False)
    type = sa.Column(sa.String, nullable=False)

    structure_id = sa.Column(sa.Integer, sa.ForeignKey('M_Structure.id'))
    test_runner_id = sa.Column(sa.Integer, sa.ForeignKey('M_TestRunner.id'))

    structure = relationship('StructureMapper')

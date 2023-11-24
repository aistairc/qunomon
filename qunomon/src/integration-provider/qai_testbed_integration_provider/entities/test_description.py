# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import datetime
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db


class TestDescriptionMapper(sql_db.Model):

    __tablename__ = 'T_TestDescription'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    creation_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    update_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    opinion = sa.Column(sa.String, nullable=False)
    delete_flag = sa.Column(sa.Boolean, unique=False, default=False)
    value_target = sa.Column(sa.Boolean, unique=False)
    star = sa.Column(sa.Boolean, default=False)

    test_id = sa.Column(sa.Integer, sa.ForeignKey('T_Test.id'))
    quality_dimension_id = sa.Column(sa.Integer, sa.ForeignKey('M_Quality_Dimension.id'))
    test_runner_id = sa.Column(sa.Integer, sa.ForeignKey('M_TestRunner.id'))
    parent_id = sa.Column(sa.Integer, sa.ForeignKey('T_TestDescription.id'), nullable=True)
    run_id = sa.Column(sa.Integer, sa.ForeignKey('T_Run.id'), nullable=True)

    quality_dimension = relationship('QualityDimensionMapper')
    inventories = relationship('InventoryTDMapper')
    operands = relationship('OperandMapper')
    test_runner = relationship('TestRunnerMapper')
    test_runner_params = relationship('TestRunnerParamMapper')
    parent = relationship("TestDescriptionMapper", remote_side=[id])
    run = relationship('RunMapper')

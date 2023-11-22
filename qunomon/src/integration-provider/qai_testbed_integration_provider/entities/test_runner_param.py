# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from ..gateways.extensions import sql_db


class TestRunnerParamMapper(sql_db.Model):

    __tablename__ = 'T_TestRunnerParam'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    value = sa.Column(sa.String, nullable=True)

    test_runner_param_template_id = sa.Column(sa.Integer, sa.ForeignKey('M_TestRunnerParamTemplate.id_'))
    test_description_id = sa.Column(sa.Integer, sa.ForeignKey('T_TestDescription.id'))

    test_runner_param_template = relationship('TestRunnerParamTemplateMapper')

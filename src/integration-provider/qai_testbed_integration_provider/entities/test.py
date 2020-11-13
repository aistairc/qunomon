# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.

import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db
from ..controllers.dto.test_description import Test


class TestMapper(sql_db.Model):

    __tablename__ = 'T_Test'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    report_url = sa.Column(sa.String, nullable=True)

    job_id = sa.Column(sa.Integer, sa.ForeignKey('T_Job.id'), nullable=True)
    ml_component_id = sa.Column(sa.Integer, sa.ForeignKey('M_MLComponent.id'))

    job = relationship('JobMapper')
    test_descriptions = relationship('TestDescriptionMapper', backref='test')


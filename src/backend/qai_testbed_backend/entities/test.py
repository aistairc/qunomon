# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.

import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db
from ..controllers.dto.test_description import Test
from ..entities.test_description import TestDescriptionMapper


class TestMapper(sql_db.Model):

    __tablename__ = 'T_Test'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    report_url = sa.Column(sa.String, nullable=True)

    job_id = sa.Column(sa.Integer, sa.ForeignKey('T_Job.id'), nullable=True)
    ml_component_id = sa.Column(sa.Integer, sa.ForeignKey('M_MLComponent.id'))

    job = relationship('JobMapper')
    test_descriptions = relationship('TestDescriptionMapper', backref='test')

    @hybrid_method
    def to_dto(self, test_descriptions: [TestDescriptionMapper] = None) -> Test:
        if self.job_id is None:
            return Test(
                id_=self.id,
                status='NA',
                result='NA',
                result_detail='NA',
                test_descriptions=[mapper.to_dto() for mapper in test_descriptions]
            )
        else:
            return Test(
                id_=self.id,
                status=self.job.status,
                result=self.job.result,
                result_detail=self.job.result_detail,
                test_descriptions=[mapper.to_dto() for mapper in test_descriptions]
            )

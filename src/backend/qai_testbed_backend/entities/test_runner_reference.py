# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db
from ..controllers.dto.test_runner_reference import TestRunnerReference


class TestRunnerReferenceMapper(sql_db.Model):

    __tablename__ = 'M_TestRunnerReference'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    reference = sa.Column(sa.String, nullable=False)

    test_runner_id = sa.Column(sa.Integer, sa.ForeignKey('M_TestRunner.id'))

    @hybrid_method
    def to_dto(self) -> TestRunnerReference:
        return TestRunnerReference(
            id_=self.id,
            reference=self.reference
        )

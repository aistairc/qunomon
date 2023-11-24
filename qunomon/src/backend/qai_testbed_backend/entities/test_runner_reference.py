# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db
from ..controllers.dto.test_runner_reference import TestRunnerReference


class TestRunnerReferenceMapper(sql_db.Model):

    __tablename__ = 'M_TestRunnerReference'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    bib_info = sa.Column(sa.String, nullable=False)
    additional_info = sa.Column(sa.String, nullable=True)
    url_ = sa.Column(sa.String, nullable=True)

    test_runner_id = sa.Column(sa.Integer, sa.ForeignKey('M_TestRunner.id'))

    @hybrid_method
    def to_dto(self) -> TestRunnerReference:
        return TestRunnerReference(
            id_=self.id,
            bib_info=self.bib_info,
            additional_info=self.additional_info,
            url_=self.url_
        )

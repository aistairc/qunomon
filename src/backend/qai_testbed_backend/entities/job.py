# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import datetime
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db
from ..controllers.dto.testrunner import JobStatus


class JobMapper(sql_db.Model):

    __tablename__ = 'T_Job'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    status = sa.Column(sa.String, nullable=False)
    result = sa.Column(sa.String, nullable=False)
    result_detail = sa.Column(sa.String, nullable=False)
    creation_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    test_id = sa.Column(sa.Integer, nullable=True)

    runs = relationship('RunMapper')

    @hybrid_method
    def to_dto(self) -> JobStatus:
        return JobStatus(
            id_=self.id,
            status=self.status,
            result=self.result,
            result_detail=self.result_detail
        )

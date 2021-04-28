# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import datetime
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db
from ..controllers.dto.testrunner import RunStatus
from ..controllers.dto.test_description import TestDescriptionResult, Graph
from ..controllers.dto.downloadable_data import DownloadableData


class RunMapper(sql_db.Model):

    __tablename__ = 'T_Run'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    status = sa.Column(sa.String, nullable=False)
    result = sa.Column(sa.String, nullable=True)
    result_detail = sa.Column(sa.String, nullable=True)
    cpu_brand = sa.Column(sa.String, nullable=True)
    cpu_arch = sa.Column(sa.String, nullable=True)
    cpu_clocks = sa.Column(sa.String, nullable=True)
    cpu_cores = sa.Column(sa.String, nullable=True)
    memory_capacity = sa.Column(sa.String, nullable=True)
    launch_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    done_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    execution_date = sa.Column(sa.String)
    ait_output_file = sa.Column(sa.String, nullable=True)
    log_file = sa.Column(sa.String, nullable=True)
    test_description_id = sa.Column(sa.Integer, nullable=True)
    error_code = sa.Column(sa.String, nullable=True)

    job_id = sa.Column(sa.Integer, sa.ForeignKey('T_Job.id'))
    
    job = relationship('JobMapper')
    graphs = relationship('GraphMapper', order_by="GraphMapper.id")
    download_data = relationship('DownloadableDataMapper', order_by="DownloadableDataMapper.id")

    @hybrid_method
    def to_dto(self) -> RunStatus:
        return RunStatus(
            id_=self.id,
            status=self.status,
            result=self.result,
            result_detail=self.result_detail,
            test_description_id=self.test_description_id
        )

    @hybrid_method
    def to_dto_result(self) -> TestDescriptionResult:
        return TestDescriptionResult(
            summary=self.result,
            detail=self.result_detail,
            error_code=self.error_code,
            log_file=self.log_file,
            graphs=[g.to_dto() for g in self.graphs],
            downloads=[d.to_dto() for d in self.download_data],
            cpu_brand=self.cpu_brand,
            cpu_arch=self.cpu_arch,
            cpu_clocks=self.cpu_clocks,
            cpu_cores=self.cpu_cores,
            memory_capacity=self.memory_capacity
        )

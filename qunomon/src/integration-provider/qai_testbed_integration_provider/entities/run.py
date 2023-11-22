# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import datetime
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db
from ..controllers.dto.test_description import TestDescription, TestDescriptionDetail


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
    run_measures = relationship('RunMeasureMapper')

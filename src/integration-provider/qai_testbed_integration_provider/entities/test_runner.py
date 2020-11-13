# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from ..gateways.extensions import sql_db


class TestRunnerMapper(sql_db.Model):

    __tablename__ = 'M_TestRunner'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    # dag_name = sa.Column(sa.String, unique=True)
    description = sa.Column(sa.String, nullable=True)
    author = sa.Column(sa.String, nullable=True)
    email = sa.Column(sa.String, nullable=True)
    version = sa.Column(sa.String, nullable=True)
    quality = sa.Column(sa.String, nullable=False)
    landing_page = sa.Column(sa.String, nullable=False)

    quality_measurements = relationship('QualityMeasurementMapper')
    test_runner_param_templates = relationship('TestRunnerParamTemplateMapper')
    test_inventory_templates = relationship('TestInventoryTemplateMapper')
    test_runner_reference = relationship('TestRunnerReferenceMapper')
    downloadable_template = relationship('DownloadableTemplateMapper')
    graph_templates = relationship('GraphTemplateMapper')

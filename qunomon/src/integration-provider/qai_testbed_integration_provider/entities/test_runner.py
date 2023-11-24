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
    source_repository = sa.Column(sa.String, nullable=True)
    create_user_account = sa.Column(sa.String, nullable=True)
    create_user_name = sa.Column(sa.String, nullable=True)
    version = sa.Column(sa.String, nullable=True)
    quality = sa.Column(sa.String, nullable=False)
    keywords = sa.Column(sa.String, nullable=True)
    licenses = sa.Column(sa.String, nullable=True)
    landing_page = sa.Column(sa.String, nullable=False)
    install_mode = sa.Column(sa.String, nullable=True)
    install_status = sa.Column(sa.String, nullable=True)
    delete_flag = sa.Column(sa.Boolean, unique=False, default=False)

    quality_measurements = relationship('QualityMeasurementMapper')
    test_runner_param_templates = relationship('TestRunnerParamTemplateMapper')
    test_inventory_templates = relationship('TestInventoryTemplateMapper')
    test_runner_references = relationship('TestRunnerReferenceMapper')
    downloadable_template = relationship('DownloadableTemplateMapper')
    graph_templates = relationship('GraphTemplateMapper')

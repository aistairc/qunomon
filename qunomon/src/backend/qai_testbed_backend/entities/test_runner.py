# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db
from ..controllers.dto.test_description import TestRunner, TestRunnerParam
from ..controllers.dto.ait_manifest import TestRunnerTemplate, Report
from .test_runner_param import TestRunnerParamMapper


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

    @hybrid_method
    def to_dto(self, param_mappers: List[TestRunnerParamMapper]) -> TestRunner:
        return TestRunner(
            id_=self.id,
            name=self.name,
            description=self.description,
            source_repository=self.source_repository,
            create_user_account=self.create_user_account,
            create_user_name=self.create_user_name,
            version=self.version,
            quality=self.quality,
            keywords=self.keywords,
            licenses=self.licenses,
            landing_page=self.landing_page,
            install_mode=self.install_mode,
            install_status=self.install_status,
            params=[TestRunnerParam(id_=p.id, 
                                    name=p.test_runner_param_template.name, 
                                    value=p.value,
                                    test_runner_param_template_id=p.test_runner_param_template.id_)
                    for p in param_mappers]
        )

    @hybrid_method
    def to_template_dto(self) -> TestRunnerTemplate:
        return TestRunnerTemplate(
            id_=self.id,
            name=self.name,
            description=self.description,
            source_repository=self.source_repository,
            create_user_account=self.create_user_account,
            create_user_name=self.create_user_name,
            version=self.version,
            quality=self.quality,
            keywords=self.keywords,
            licenses=self.licenses,
            landing_page=self.landing_page,
            install_mode=self.install_mode,
            install_status=self.install_status,
            references=[r.to_dto() for r in self.test_runner_references],
            params=[p.to_dto() for p in self.test_runner_param_templates],
            test_inventory_templates=[t.to_dto() for t in self.test_inventory_templates],
            report=Report(
                measures=[t.to_measure_dto() for t in self.quality_measurements],
                resources=[t.to_dto() for t in self.graph_templates]
            ),
            downloads=[d.to_dto() for d in self.downloadable_template],
        )

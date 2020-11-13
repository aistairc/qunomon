# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db
from ..controllers.dto.test_description import TestRunner, TestRunnerParam
from .test_runner_param import TestRunnerParamMapper
from ..controllers.dto.testrunner import TestRunnerTemplate, Report
from .quality_dimension import QualityDimensionMapper

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

    @hybrid_method
    def to_dto(self, param_mappers: List[TestRunnerParamMapper]) -> TestRunner:
        return TestRunner(
            id_=self.id,
            name=self.name,
            description=self.description,
            author=self.author,
            email=self.email,
            version=self.version,
            quality=self.quality,
            landing_page=self.landing_page,
            params=[TestRunnerParam(id_=p.id, name=p.test_runner_param_template.name, value=p.value,
                                    test_runner_param_template_id=p.test_runner_param_template.id_)
                    for p in param_mappers]
        )

    @hybrid_method
    def to_template_dto(self) -> TestRunnerTemplate:
        #  TODO:QualityMeasurementsが存在しないAITに対する暫定対応
        if len(self.quality_measurements) == 0:
            tmp_quality_dimension_id = QualityDimensionMapper.query.first().id
        else:
            tmp_quality_dimension_id = self.quality_measurements[0].quality_dimension_id
        return TestRunnerTemplate(
            id_=self.id,
            name=self.name,
            quality_dimension_id=tmp_quality_dimension_id,
            description=self.description,
            author=self.author,
            version=self.version,
            quality=self.quality,
            landing_page=self.landing_page,
            reference=[t.reference for t in self.test_runner_reference],
            params=[p.to_dto() for p in self.test_runner_param_templates],
            test_inventory_templates=[t.to_dto() for t in self.test_inventory_templates],
            report=Report(
                measures=[t.to_measure_dto() for t in self.quality_measurements],
                resources=[t.to_dto() for t in self.graph_templates]
            ),
            downloads=[d.to_dto() for d in self.downloadable_template],
        )

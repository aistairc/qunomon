# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_method

from .operand import OperandMapper
from ..gateways.extensions import sql_db
from ..controllers.dto.test_description import QualityMeasurement, QualityMeasurementForReport
from ..controllers.dto.quality_measurement import QualityMeasurementTemplate
from ..controllers.dto.testrunner import Measure
from ..entities.relational_operator import RelationalOperatorMapper

class QualityMeasurementMapper(sql_db.Model):

    __tablename__ = 'M_Quality_Measurement'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=False)
    type = sa.Column(sa.String, nullable=False)
    min_value = sa.Column(sa.Float, nullable=True)
    max_value = sa.Column(sa.Float, nullable=True)

    structure_id = sa.Column(sa.Integer, sa.ForeignKey('M_Structure.id'))
    quality_dimension_id = sa.Column(sa.Integer, sa.ForeignKey('M_Quality_Dimension.id'))
    test_runner_id = sa.Column(sa.Integer, sa.ForeignKey('M_TestRunner.id'))

    structure = relationship('StructureMapper')

    @hybrid_method
    def to_dto(self, operand_mapper: OperandMapper) -> QualityMeasurement:
        return QualityMeasurement(
            id_=self.id,
            name=self.name,
            description=self.description,
            structure=self.structure.structure,
            value=operand_mapper.value,
            relational_operator_id=operand_mapper.relational_operator_id,
            enable=operand_mapper.enable
        )

    @hybrid_method
    def to_dto_report(self, operand_mapper: OperandMapper) -> QualityMeasurementForReport:
        ro = RelationalOperatorMapper.query.get(operand_mapper.relational_operator_id)
        return QualityMeasurementForReport(
            id_=self.id,
            name=self.name,
            description=self.description,
            structure=self.structure.structure,
            value=operand_mapper.value,
            relational_operator=ro.expression,
            enable=operand_mapper.enable
        )

    @hybrid_method
    def to_template_dto(self) -> QualityMeasurementTemplate:
        return QualityMeasurementTemplate(
            id_=self.id,
            name=self.name,
            type_=self.type,
            description=self.description,
            quality_dimension_id=self.quality_dimension_id,
            structure=self.structure.structure
        )

    @hybrid_method
    def to_measure_dto(self) -> Measure:
        return Measure(
            id_=self.id,
            name=self.name,
            type_=self.type,
            description=self.description,
            min_value=self.min_value,
            max_value=self.max_value,
            structure=self.structure.structure
        )

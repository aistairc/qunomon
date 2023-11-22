# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import datetime
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db
from ..controllers.dto.test_description import TestDescription, TestDescriptionDetail, TestDescriptionForReport, UsingTestDescription


class TestDescriptionMapper(sql_db.Model):

    __tablename__ = 'T_TestDescription'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    creation_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    update_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    opinion = sa.Column(sa.String, nullable=False)
    delete_flag = sa.Column(sa.Boolean, unique=False, default=False)
    value_target = sa.Column(sa.Boolean, unique=False)
    star = sa.Column(sa.Boolean, default=False)

    test_id = sa.Column(sa.Integer, sa.ForeignKey('T_Test.id'))
    quality_dimension_id = sa.Column(sa.Integer, sa.ForeignKey('M_Quality_Dimension.id'))
    test_runner_id = sa.Column(sa.Integer, sa.ForeignKey('M_TestRunner.id'))
    parent_id = sa.Column(sa.Integer, sa.ForeignKey('T_TestDescription.id'), nullable=True)
    run_id = sa.Column(sa.Integer, sa.ForeignKey('T_Run.id'), nullable=True)

    quality_dimension = relationship('QualityDimensionMapper')
    inventories = relationship('InventoryTDMapper')
    operands = relationship('OperandMapper')
    test_runner = relationship('TestRunnerMapper')
    test_runner_params = relationship('TestRunnerParamMapper')
    parent = relationship("TestDescriptionMapper", remote_side=[id])
    run = relationship('RunMapper')

    @hybrid_method
    def to_dto(self) -> TestDescription:
        status = 'NA'
        result = 'NA'
        result_detail = 'NA'
        if self.run_id is not None:
            status = self.run.status
            result = self.run.result
            result_detail = self.run.result_detail
        return TestDescription(
            id_=self.id,
            name=self.name,
            status=status,
            result=result,
            result_detail=result_detail,
            creation_datetime=self.creation_datetime,
            update_datetime=self.update_datetime,
            opinion=self.opinion,
            delete_flag=self.delete_flag,
            parent_id=self.parent_id,
            target_inventories=[i.inventory.to_dto(i.template_inventory.id_, i.template_inventory.name) for i in self.inventories],
            star=self.star,
            test_runner_id=self.test_runner_id
        )

    @hybrid_method
    def to_dto_detail(self) -> TestDescriptionDetail:
        status = 'NA'
        td_result = None
        if self.run_id is not None:
            status = self.run.status
            td_result = self.run.to_dto_result()
        quality_measurements = []
        for o in self.operands:
            q_m = o.quality_measurement
            run_measure_value = ''
            if self.run is not None and self.run.run_measures is not None:
                for r_m in self.run.run_measures:
                    if q_m.name == r_m.measure_name:
                        if run_measure_value == '':
                            run_measure_value = str(r_m.measure_value)
                        else:
                            run_measure_value = run_measure_value + ' , '  + str(r_m.measure_value)
            quality_measurements.append(q_m.to_dto(operand_mapper=o, run_measure_value=run_measure_value))
        return TestDescriptionDetail(
            id_=self.id,
            name=self.name,
            status=status,
            quality_dimension=self.quality_dimension.to_dto(),
            opinion=self.opinion,
            delete_flag=self.delete_flag,
            quality_measurements=quality_measurements,
            target_inventories=[i.inventory.to_dto(i.template_inventory.id_, i.template_inventory.name) for i in self.inventories],
            test_runner=self.test_runner.to_dto(self.test_runner_params),
            test_description_result=td_result,
            creation_datetime=self.creation_datetime,
            update_datetime=self.update_datetime,
            parent_id=self.parent_id,
            star=self.star
        )

    @hybrid_method
    def to_dto_report(self) -> TestDescriptionForReport:
        td_result = None
        if self.run_id is not None:
            td_result = self.run.to_dto_result()
        return TestDescriptionForReport(
            id_=self.id,
            name=self.name,
            quality_dimension=self.quality_dimension.to_dto(),
            opinion=self.opinion,
            value_target=self.value_target,
            quality_measurements=[o.quality_measurement.to_dto_report(operand_mapper=o) for o in self.operands],
            target_inventories=[i.inventory.to_dto(i.template_inventory.id_, i.template_inventory.name) for i in self.inventories],
            test_runner=self.test_runner.to_dto(self.test_runner_params),
            test_description_result=td_result,
        )

    @hybrid_method
    def to_dto_useing(self) -> UsingTestDescription:
        return UsingTestDescription(
            test_description_id = self.id,
            test_runner_id=self.test_runner_id,
            ml_component_id = self.test.ml_component_id
        )

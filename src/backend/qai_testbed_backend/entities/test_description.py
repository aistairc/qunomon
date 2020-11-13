# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import datetime
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db
from ..controllers.dto.test_description import TestDescription, TestDescriptionDetail, TestDescriptionForReport


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
            target_inventories=[i.inventory.to_dto(i.template_inventory.id_) for i in self.inventories],
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
        return TestDescriptionDetail(
            id_=self.id,
            name=self.name,
            status=status,
            quality_dimension=self.quality_dimension.to_dto(),
            opinion=self.opinion,
            delete_flag=self.delete_flag,
            quality_measurements=[o.quality_measurement.to_dto(operand_mapper=o) for o in self.operands],
            target_inventories=[i.inventory.to_dto(i.template_inventory.id_) for i in self.inventories],
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
            target_inventories=[i.inventory.to_dto(i.template_inventory.id_) for i in self.inventories],
            test_runner=self.test_runner.to_dto(self.test_runner_params),
            test_description_result=td_result,
        )

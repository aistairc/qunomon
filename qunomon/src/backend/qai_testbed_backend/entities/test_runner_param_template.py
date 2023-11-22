# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa

from ..gateways.extensions import sql_db
from sqlalchemy.ext.hybrid import hybrid_method
from ..controllers.dto.ait_manifest import ParamTemplate


class TestRunnerParamTemplateMapper(sql_db.Model):

    __tablename__ = 'M_TestRunnerParamTemplate'

    id_ = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    value_type = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=False)
    default_value = sa.Column(sa.String, nullable=True)
    min_value = sa.Column(sa.Float, nullable=True)
    max_value = sa.Column(sa.Float, nullable=True)
    depends_on_parameter = sa.Column(sa.String, nullable=True)

    test_runner_id = sa.Column(sa.Integer, sa.ForeignKey('M_TestRunner.id'))

    @hybrid_method
    def to_dto(self) -> ParamTemplate:
        return ParamTemplate(
            id_=self.id_,
            name=self.name,
            type_=self.value_type,
            description=self.description,
            default_value=self.default_value,
            min_value=self.min_value,
            max_value=self.max_value,
            depends_on_parameter=self.depends_on_parameter
        )

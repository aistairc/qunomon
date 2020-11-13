# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db
from ..controllers.dto.relational_operator import RelationalOperator
from sqlalchemy.orm import relationship


class RelationalOperatorMapper(sql_db.Model):

    __tablename__ = 'M_RelationalOperator'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    expression = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=False)

    # operand = relationship('T_Operand')

    @hybrid_method
    def to_dto(self) -> RelationalOperator:
        return RelationalOperator(
            id_=self.id,
            expression=self.expression,
            description=self.description
        )

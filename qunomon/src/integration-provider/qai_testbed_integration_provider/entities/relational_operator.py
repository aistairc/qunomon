# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa

from ..gateways.extensions import sql_db
from sqlalchemy.orm import relationship


class RelationalOperatorMapper(sql_db.Model):

    __tablename__ = 'M_RelationalOperator'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    expression = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=False)

    # operand = relationship('T_Operand')

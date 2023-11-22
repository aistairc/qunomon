# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db
from ..controllers.dto.format import Format


class FormatMapper(sql_db.Model):

    __tablename__ = 'M_Format'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    format_ = sa.Column(sa.String, unique=True)

    @hybrid_method
    def to_dto(self) -> Format:
        return Format(
            id_=self.id,
            format_=self.format_
        )
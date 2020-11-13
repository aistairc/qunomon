# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db
from ..controllers.dto.format import Format
from sqlalchemy.orm import relationship


class FormatMapper(sql_db.Model):

    __tablename__ = 'M_Format'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    format_ = sa.Column(sa.String, unique=True)

    resource_type_id = sa.Column(sa.Integer, sa.ForeignKey('M_ResourceType.id'))

    resource_type = relationship('ResourceTypeMapper')

    @hybrid_method
    def to_dto(self) -> Format:
        return Format(
            id_=self.id,
            type_=self.resource_type.type,
            format_=self.format_
        )
# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db
from ..controllers.dto.tag import Tag


class TagMapper(sql_db.Model):

    __tablename__ = 'M_Tag'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    type = sa.Column(sa.String, nullable=False)

    @hybrid_method
    def to_dto(self) -> Tag:
        return Tag(
            id_=self.id,
            name=self.name
        )
# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db
from ..controllers.dto.structure import Structure
from sqlalchemy.orm import relationship


class StructureMapper(sql_db.Model):

    __tablename__ = 'M_Structure'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    structure = sa.Column(sa.String, unique=True)

    @hybrid_method
    def to_dto(self) -> Structure:
        return Structure(
            id_=self.id,
            structure=self.structure
        )
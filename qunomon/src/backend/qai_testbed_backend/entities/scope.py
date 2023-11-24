# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import datetime
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db
from ..controllers.dto.scope import Scope


class ScopeMapper(sql_db.Model):
    __tablename__ = 'M_Scope'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    aithub_scope_id = sa.Column(sa.Integer, nullable=True)
    guideline_id = sa.Column(sa.Integer, sa.ForeignKey('M_Guideline.id'))
    name = sa.Column(sa.String, nullable=False)
    creation_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    update_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    delete_flag = sa.Column(sa.Boolean, unique=False, default=False)

    guideline = relationship('GuidelineMapper')

    @hybrid_method
    def to_dto(self) -> Scope:
        return Scope(
            id_=self.id,
            aithub_scope_id=self.aithub_scope_id,
            guideline_id=self.guideline_id,
            name=self.name,
            creation_datetime=self.creation_datetime,
            update_datetime=self.update_datetime
        )

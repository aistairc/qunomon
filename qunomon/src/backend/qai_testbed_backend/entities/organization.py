# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db
from ..controllers.dto.organization import Organizer


class OrganizationMapper(sql_db.Model):

    __tablename__ = 'M_Organization'

    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    organizer_id = sa.Column(sa.String, nullable=False, unique=True)
    name = sa.Column(sa.String, nullable=False)
    creation_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    update_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    delete_flag = sa.Column(sa.Boolean, default=False)

    ml_components = relationship('MLComponentMapper', backref='organization')

    @hybrid_method
    def to_dto(self) -> Organizer:
        return Organizer(
            id_=self.id,
            organizer_id=self.organizer_id,
            name=self.name,
            creation_datetime=self.creation_datetime,
            update_datetime=self.update_datetime,
            delete_flag=self.delete_flag,
        )

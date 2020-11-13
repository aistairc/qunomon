# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from ..gateways.extensions import sql_db


class OrganizationMapper(sql_db.Model):

    __tablename__ = 'M_Organization'

    id = sa.Column(sa.String, primary_key=True, nullable=False)
    name = sa.Column(sa.String, nullable=False)

    ml_components = relationship('MLComponentMapper', backref='organization')

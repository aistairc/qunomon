# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db


class UserMapper(sql_db.Model):
    __tablename__ = 'M_User'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    account_id = sa.Column(sa.String, nullable=False, unique=True)
    user_name = sa.Column(sa.String, nullable=False)
    password_hash = sa.Column(sa.String, nullable=False)
    delete_flag = sa.Column(sa.Boolean, default=False)
    creation_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    update_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)

    org_id = sa.Column(sa.Integer, sa.ForeignKey('M_Organization.id'))

    organization = relationship('OrganizationMapper')
    user_role_ml_components = relationship('UserRoleMLComponentMapper')

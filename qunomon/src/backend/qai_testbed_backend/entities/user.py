# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db
from ..controllers.dto.user import User


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

    @hybrid_method
    def to_dto(self) -> User:
        return User(
            id_=self.id,
            account_id=self.account_id,
            user_name=self.user_name,
            password_hash=self.password_hash,
            delete_flag=self.delete_flag,
            creation_datetime=self.creation_datetime,
            update_datetime=self.update_datetime,
            organizer_id=self.organization.organizer_id,
            user_role_ml_components=[mapper.to_dto() for mapper in self.user_role_ml_components]
        )

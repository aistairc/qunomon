# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db


class UserRoleMLComponentMapper(sql_db.Model):

    __tablename__ = 'M_User_Role_MLComponent'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    user_id = sa.Column(sa.Integer, sa.ForeignKey('M_User.id'))
    role_id = sa.Column(sa.Integer, sa.ForeignKey('M_Role.id'))
    ml_component_id = sa.Column(sa.Integer, sa.ForeignKey('M_MLComponent.id'))

    role = relationship('RoleMapper')

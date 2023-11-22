# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa

from ..gateways.extensions import sql_db


class MLFrameworkMapper(sql_db.Model):

    __tablename__ = 'M_MLFrameworkMapper'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, unique=True)

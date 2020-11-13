# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa

from ..gateways.extensions import sql_db


class SettingMapper(sql_db.Model):

    __tablename__ = 'M_Setting'

    key = sa.Column(sa.String, primary_key=True, nullable=False)
    value = sa.Column(sa.String, nullable=True)

# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa

from ..gateways.extensions import sql_db


class DownloadMapper(sql_db.Model):

    __tablename__ = 'T_Download'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    path = sa.Column(sa.String, nullable=False)

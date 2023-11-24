# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import datetime
import sqlalchemy as sa

from ..gateways.extensions import sql_db


class GuidelineMapper(sql_db.Model):
    __tablename__ = 'M_Guideline'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    aithub_guideline_id = sa.Column(sa.Integer, nullable=True)
    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=True)
    creator = sa.Column(sa.String, nullable=True)
    publisher = sa.Column(sa.String, nullable=True)
    identifier = sa.Column(sa.String, nullable=True)
    publish_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    creation_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    update_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    delete_flag = sa.Column(sa.Boolean, unique=False, default=False)

# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa
import datetime

from ..gateways.extensions import sql_db


class ReportTemplateMapper(sql_db.Model):

    __tablename__ = 'M_ReportTemplate'

    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    name = sa.Column(sa.String, nullable=False)
    creation_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    update_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)

    guideline_id = sa.Column(sa.Integer, sa.ForeignKey('M_Guideline.id'))


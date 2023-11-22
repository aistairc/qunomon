# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import datetime
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from ..gateways.extensions import sql_db


class GuidelineSchemaFileMapper(sql_db.Model):
    __tablename__ = 'M_Guideline_Schema_File'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    guideline_id = sa.Column(sa.Integer, sa.ForeignKey('M_Guideline.id'))
    name = sa.Column(sa.String, nullable=False)
    guideline_schema_file = sa.Column(sa.JSON, nullable=False)
    creation_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    update_datetime = sa.Column(sa.DateTime, nullable=True)
    delete_flag = sa.Column(sa.Boolean, unique=False, default=False)

    guideline = relationship('GuidelineMapper')

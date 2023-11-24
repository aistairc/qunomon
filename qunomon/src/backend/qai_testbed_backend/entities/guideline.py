# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import datetime
import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db
from ..controllers.dto.guideline import Guideline


class GuidelineMapper(sql_db.Model):
    __tablename__ = 'M_Guideline'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    aithub_guideline_id = sa.Column(sa.Integer, nullable=True)
    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=True)
    creator = sa.Column(sa.String, nullable=True)
    publisher = sa.Column(sa.String, nullable=True)
    identifier = sa.Column(sa.String, nullable=True)
    publish_datetime = sa.Column(sa.DateTime, nullable=True)
    aithub_delete_flag = sa.Column(sa.Boolean, unique=False, default=False)
    creation_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    update_datetime = sa.Column(sa.DateTime, nullable=True)
    delete_flag = sa.Column(sa.Boolean, unique=False, default=False)

    @hybrid_method
    def to_dto(self) -> Guideline:
        return Guideline(
            id_=self.id,
            aithub_guideline_id=self.aithub_guideline_id,
            name=self.name,
            description=self.description,
            creator=self.creator,
            publisher=self.publisher,
            identifier=self.identifier,
            publish_datetime=self.publish_datetime,
            aithub_delete_flag=self.aithub_delete_flag,
            creation_datetime=self.creation_datetime,
            update_datetime=self.update_datetime
        )

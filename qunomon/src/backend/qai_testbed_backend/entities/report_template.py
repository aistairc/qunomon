# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa
import datetime

from sqlalchemy.ext.hybrid import hybrid_method
from ..gateways.extensions import sql_db
from ..controllers.dto.report_template import ReportTemplate


class ReportTemplateMapper(sql_db.Model):

    __tablename__ = 'M_ReportTemplate'

    id = sa.Column(sa.Integer, primary_key=True, nullable=False)
    name = sa.Column(sa.String, nullable=False)
    creation_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    update_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)

    guideline_id = sa.Column(sa.Integer, sa.ForeignKey('M_Guideline.id'))

    @hybrid_method
    def to_dto(self) -> ReportTemplate:
        return ReportTemplate(
            id_=self.id,
            name=self.name,
            guideline_id=self.guideline_id,
            creation_datetime=self.creation_datetime,
            update_datetime=self.update_datetime
        )

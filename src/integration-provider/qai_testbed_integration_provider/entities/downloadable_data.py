# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from ..gateways.extensions import sql_db


class DownloadableDataMapper(sql_db.Model):

    __tablename__ = 'T_Downloadable_Data'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    download_address = sa.Column(sa.String, nullable=False)

    run_id = sa.Column(sa.Integer, sa.ForeignKey('T_Run.id'))
    downloadable_template_id = sa.Column(sa.Integer, sa.ForeignKey('M_Downloadable_Template.id'))
    download_id = sa.Column(sa.Integer, sa.ForeignKey('T_Download.id'))

    download_template = relationship('DownloadableTemplateMapper')

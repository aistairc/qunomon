# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from ..gateways.extensions import sql_db


class GraphMapper(sql_db.Model):

    __tablename__ = 'T_Graph'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    report_required = sa.Column(sa.Boolean, nullable=False)
    graph_address = sa.Column(sa.String, nullable=False)
    report_index = sa.Column(sa.Integer, nullable=False)
    report_name = sa.Column(sa.String, nullable=False)

    graph_template_id = sa.Column(sa.Integer, sa.ForeignKey('M_GraphTemplate.id'))
    run_id = sa.Column(sa.Integer, sa.ForeignKey('T_Run.id'))
    download_id = sa.Column(sa.Integer, sa.ForeignKey('T_Download.id'))

    graph_template = relationship('GraphTemplateMapper')
    download = relationship('DownloadMapper')

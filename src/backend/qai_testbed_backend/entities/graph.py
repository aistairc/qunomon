# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db
from ..controllers.dto.test_description import Graph


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

    @hybrid_method
    def to_dto(self) -> Graph:
        return Graph(
            id_=self.id,
            name=self.graph_template.name,
            description=self.graph_template.description,
            report_required=self.report_required,
            graph_type=self.graph_template.resource_type.type,
            report_index=self.report_index,
            report_name=self.report_name,
            graph=self.graph_address)

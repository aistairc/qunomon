# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from ..gateways.extensions import sql_db


class GraphTemplateMapper(sql_db.Model):

    __tablename__ = 'M_GraphTemplate'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=True)

    test_runner_id = sa.Column(sa.Integer, sa.ForeignKey('M_TestRunner.id'))
    resource_type_id = sa.Column(sa.Integer, sa.ForeignKey('M_ResourceType.id'))

    resource_type = relationship('ResourceTypeMapper')

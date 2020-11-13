# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from ..gateways.extensions import sql_db


class MLComponentMapper(sql_db.Model):

    __tablename__ = 'M_MLComponent'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=False)
    problem_domain = sa.Column(sa.String, nullable=False)

    org_id = sa.Column(sa.String, sa.ForeignKey('M_Organization.id'))
    ml_framework_id = sa.Column(sa.Integer, sa.ForeignKey('M_MLFrameworkMapper.id'))

    test = relationship('TestMapper', backref='ml_component')
    ml_framework = relationship('MLFrameworkMapper')

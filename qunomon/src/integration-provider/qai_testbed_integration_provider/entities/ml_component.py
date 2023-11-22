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
    guideline_reason = sa.Column(sa.String, nullable=True)
    scope_reason = sa.Column(sa.String, nullable=True)
    report_opinion = sa.Column(sa.String, nullable=True)
    delete_flag = sa.Column(sa.Boolean, unique=False, default=False)

    org_id = sa.Column(sa.Integer, sa.ForeignKey('M_Organization.id'))
    ml_framework_id = sa.Column(sa.Integer, sa.ForeignKey('M_MLFrameworkMapper.id'))
    guideline_id = sa.Column(sa.Integer, sa.ForeignKey('M_Guideline.id'))
    scope_id = sa.Column(sa.Integer, sa.ForeignKey('M_Scope.id'))

    test = relationship('TestMapper', backref='ml_component')
    ml_framework = relationship('MLFrameworkMapper')
    guideline = relationship('GuidelineMapper')
    scope = relationship('ScopeMapper')

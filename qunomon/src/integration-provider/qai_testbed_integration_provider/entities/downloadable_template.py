# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa

from ..gateways.extensions import sql_db


class DownloadableTemplateMapper(sql_db.Model):

    __tablename__ = 'M_Downloadable_Template'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=True)

    test_runner_id = sa.Column(sa.Integer, sa.ForeignKey('M_TestRunner.id'))

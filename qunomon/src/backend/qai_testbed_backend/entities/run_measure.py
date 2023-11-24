# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa

from ..gateways.extensions import sql_db


class RunMeasureMapper(sql_db.Model):

    __tablename__ = 'T_RunMeasure'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    measure_name = sa.Column(sa.String, nullable=False)
    measure_value = sa.Column(sa.Float, nullable=False)

    run_id = sa.Column(sa.Integer, sa.ForeignKey('T_Run.id'), nullable=False)

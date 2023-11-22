# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa

from ..gateways.extensions import sql_db


class TestInventoryTemplateAdditionalInfoMapper(sql_db.Model):

    __tablename__ = 'M_TestInventoryTemplate_Additional_Info'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    key = sa.Column(sa.String, nullable=False)
    value = sa.Column(sa.String, nullable=True)

    inventory_template_id = sa.Column(sa.Integer, sa.ForeignKey('M_TestInventoryTemplate.id_'))

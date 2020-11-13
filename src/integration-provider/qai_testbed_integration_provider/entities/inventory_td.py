# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from ..gateways.extensions import sql_db


class InventoryTDMapper(sql_db.Model):

    __tablename__ = 'T_Inventory_TestDescription'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    inventory_id = sa.Column(sa.Integer, sa.ForeignKey('M_Inventory.id'))
    template_inventory_id = sa.Column(sa.Integer, sa.ForeignKey('M_TestInventoryTemplate.id_'))
    test_description_id = sa.Column(sa.Integer, sa.ForeignKey('T_TestDescription.id'))

    inventory = relationship('InventoryMapper')
    template_inventory = relationship('TestInventoryTemplateMapper')

# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa

from ..gateways.extensions import sql_db
from sqlalchemy.orm import relationship


class TestInventoryTemplateFormatMapper(sql_db.Model):

    __tablename__ = 'M_TestInventoryTemplate_Format'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    inventory_template_id = sa.Column(sa.Integer, sa.ForeignKey('M_TestInventoryTemplate.id_'))
    format_id = sa.Column(sa.Integer, sa.ForeignKey('M_Format.id'))

    format = relationship('FormatMapper')

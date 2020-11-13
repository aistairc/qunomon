# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa

from ..gateways.extensions import sql_db
from sqlalchemy.orm import relationship


class TestInventoryTemplateMapper(sql_db.Model):

    __tablename__ = 'M_TestInventoryTemplate'

    id_ = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=True)
    schema = sa.Column(sa.String, nullable=True)

    test_runner_id = sa.Column(sa.Integer, sa.ForeignKey('M_TestRunner.id'))
    type_id = sa.Column(sa.Integer, sa.ForeignKey('M_DataType.id'))

    test_inventory_template_tags = relationship('TestInventoryTemplateTagMapper')
    format_ = relationship('TestInventoryTemplateFormatMapper')
    dataType = relationship('DataTypeMapper')


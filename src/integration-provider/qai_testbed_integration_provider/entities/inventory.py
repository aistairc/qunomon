# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import datetime
import sqlalchemy as sa
from sqlalchemy.orm import relationship

from ..gateways.extensions import sql_db


class InventoryMapper(sql_db.Model):

    __tablename__ = 'M_Inventory'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    file_path = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=True)
    delete_flag = sa.Column(sa.Boolean, unique=False, default=False)
    schema = sa.Column(sa.String, nullable=True)
    creation_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    update_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    file_hash_sha256 = sa.Column(sa.String, nullable=False)

    ml_component_id = sa.Column(sa.Integer, sa.ForeignKey('M_MLComponent.id'))
    type_id = sa.Column(sa.Integer, sa.ForeignKey('M_DataType.id'))
    file_system_id = sa.Column(sa.Integer, sa.ForeignKey('M_FileSystem.id'))

    inventory_format = relationship('InventoryFormatMapper')
    data_type = relationship('DataTypeMapper')
    file_system = relationship('FileSystemMapper')

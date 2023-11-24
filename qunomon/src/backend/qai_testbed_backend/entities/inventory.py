# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import datetime
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db
from ..controllers.dto.test_description import Inventory
from ..controllers.dto.inventory import InventoryDetail


class InventoryMapper(sql_db.Model):

    __tablename__ = 'M_Inventory'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    file_path = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=True)
    delete_flag = sa.Column(sa.Boolean, unique=False, default=False)
    creation_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    update_datetime = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
    file_hash_sha256 = sa.Column(sa.String, nullable=False)

    ml_component_id = sa.Column(sa.Integer, sa.ForeignKey('M_MLComponent.id'))
    type_id = sa.Column(sa.Integer, sa.ForeignKey('M_DataType.id'))
    file_system_id = sa.Column(sa.Integer, sa.ForeignKey('M_FileSystem.id'))

    inventory_format = relationship('InventoryFormatMapper')
    data_type = relationship('DataTypeMapper')
    file_system = relationship('FileSystemMapper')

    @hybrid_method
    def to_dto(self, template_inventory_id: int, template_inventory_name: str) -> Inventory:
        return Inventory(
            id_=self.id,
            name=self.name,
            type_=self.data_type.to_dto(),
            description=self.description,
            file_path=self.file_path,
            template_inventory_id=template_inventory_id,
            template_inventory_name=template_inventory_name
        )

    @hybrid_method
    def to_dto_detail(self) -> InventoryDetail:
        return InventoryDetail(
            id_=self.id,
            name=self.name,
            type_=self.data_type.to_dto(),
            file_path=self.file_path,
            description=self.description,
            formats=[i.format.to_dto() for i in self.inventory_format],
            creation_datetime=self.creation_datetime,
            update_datetime=self.update_datetime,
        )

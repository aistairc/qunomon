# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db
from ..controllers.dto.ait_manifest import TestInventoryTemplateCompatiblePackage


class TestInventoryTemplateCompatiblePackageMapper(sql_db.Model):

    __tablename__ = 'M_TestInventoryTemplate_Compatible_Package'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    version = sa.Column(sa.String, nullable=True)
    additional_info = sa.Column(sa.String, nullable=True)

    inventory_template_id = sa.Column(sa.Integer, sa.ForeignKey('M_TestInventoryTemplate.id_'))

    @hybrid_method
    def to_dto(self) -> TestInventoryTemplateCompatiblePackage:
        return TestInventoryTemplateCompatiblePackage(
            id_=self.id,
            name=self.name,
            version=self.version,
            additional_info=self.additional_info
        )

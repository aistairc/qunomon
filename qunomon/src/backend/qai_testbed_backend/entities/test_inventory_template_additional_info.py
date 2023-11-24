# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_method

from ..gateways.extensions import sql_db
from ..controllers.dto.ait_manifest import TestInventoryTemplateAdditionalInfo


class TestInventoryTemplateAdditionalInfoMapper(sql_db.Model):

    __tablename__ = 'M_TestInventoryTemplate_Additional_Info'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    key = sa.Column(sa.String, nullable=False)
    value = sa.Column(sa.String, nullable=True)

    inventory_template_id = sa.Column(sa.Integer, sa.ForeignKey('M_TestInventoryTemplate.id_'))

    @hybrid_method
    def to_dto(self) -> TestInventoryTemplateAdditionalInfo:
        return TestInventoryTemplateAdditionalInfo(
            id_=self.id,
            key=self.key,
            value=self.value
        )

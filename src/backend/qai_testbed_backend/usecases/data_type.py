# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from ..controllers.dto import Result
from ..controllers.dto.data_type import GetDataTypesRes
from ..entities.data_type import DataTypeMapper


class DataTypeService:
    def get_data_type(self) -> GetDataTypesRes:
        data_types = DataTypeMapper.query.all()

        return GetDataTypesRes(
            result=Result(code='I82000', message="get list success."),
            data_types=[d.to_dto() for d in data_types]
        )

# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from qlib.utils.logging import get_logger, log

from ..controllers.dto import Result
from ..controllers.dto.data_type import GetDataTypesRes
from ..entities.data_type import DataTypeMapper


logger = get_logger()


class DataTypeService:
    @log(logger)
    def get_data_type(self) -> GetDataTypesRes:
        data_types = DataTypeMapper.query.all()

        return GetDataTypesRes(
            result=Result(code='I82000', message="get list success."),
            data_types=[d.to_dto() for d in data_types]
        )

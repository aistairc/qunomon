# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from sqlalchemy.exc import SQLAlchemyError
from qlib.utils.logging import get_logger, log

from ..controllers.dto import Result
from ..entities.ml_framework import MLFrameworkMapper
from ..across.exception import QAIInvalidRequestException
from ..controllers.dto.ml_framework import GetMLFrameworkRes


logger = get_logger()


class MLFrameworkService:

    @log(logger)
    def get(self):
        try:
            ml_frameworks = MLFrameworkMapper.query.all()

            return GetMLFrameworkRes(
                result=Result(code='M11000', message="Success."),
                ml_frameworks=[f.to_dto() for f in ml_frameworks]
            )
        except SQLAlchemyError as e:
            raise QAIInvalidRequestException('M11999', 'database error: {}'.format(e))

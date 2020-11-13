# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from sqlalchemy.exc import SQLAlchemyError

from ..controllers.dto import Result
from ..entities.format import FormatMapper
from ..across.exception import QAINotFoundException, QAIException, QAIInvalidRequestException, \
    QAIInternalServerException
from ..controllers.dto.format import GetFormatRes


class FormatService:

    def get(self):
        try:
            formats = FormatMapper.query.all()

            if formats is None:
                raise QAINotFoundException(result_code='I74000', result_msg='not found format')
            return GetFormatRes(
                result=Result(code='I72000', message="Success."),
                formats=[t.to_dto() for t in formats]
            )
        except QAIException as e:
            raise e
        except SQLAlchemyError as e:
            raise QAIInvalidRequestException('I79000', 'database error: {}'.format(e))
        except Exception as e:
            raise QAIInternalServerException(result_code='I79999', result_msg='internal server error: {}'.format(e))

# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from qlib.utils.logging import get_logger, log

from ..controllers.dto import Result
from ..entities.relational_operator import RelationalOperatorMapper
from ..across.exception import QAINotFoundException, QAIException, QAIInvalidRequestException, \
    QAIInternalServerException
from ..controllers.dto.relational_operator import GetRelationalOperatorRes
from sqlalchemy.exc import SQLAlchemyError


logger = get_logger()


class RelationalOperatorService:

    @log(logger)
    def get(self):
        try:
            relational_operators = RelationalOperatorMapper.query.all()

            if relational_operators is None:
                raise QAINotFoundException(result_code='Q34000', result_msg='not found relational operator')
            return GetRelationalOperatorRes(
                result=Result(code='Q32000', message="Success."),
                relational_operators=[r.to_dto() for r in relational_operators]
            )

        except QAIException as e:
            raise e
        except SQLAlchemyError as e:
            raise QAIInvalidRequestException('Q39000', 'database error: {}'.format(e))
        except Exception as e:
            raise QAIInternalServerException(result_code='Q39999', result_msg='internal server error: {}'.format(e))

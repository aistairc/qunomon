# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from ..controllers.dto import Result
from ..entities.tag import TagMapper
from ..across.exception import QAINotFoundException, QAIException, QAIInvalidRequestException, \
    QAIInternalServerException
from ..controllers.dto.tag import GetTagsRes
from ..gateways.extensions import sql_db
from sqlalchemy.exc import SQLAlchemyError


class TagService:

    def get(self):
        try:
            tags = TagMapper.query.all()

            if tags is None:
                raise QAINotFoundException(result_code='I64000', result_msg='not found tag')
            return GetTagsRes(
                result=Result(code='I62000', message="Success."),
                tags=[t.to_dto() for t in tags]
            )

        except QAIException as e:
            raise e
        except SQLAlchemyError as e:
            raise QAIInvalidRequestException('I69000', 'database error: {}'.format(e))
        except Exception as e:
            raise QAIInternalServerException(result_code='I69999', result_msg='internal server error: {}'.format(e))

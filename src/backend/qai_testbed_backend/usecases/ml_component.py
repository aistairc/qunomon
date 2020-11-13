# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from sqlalchemy.exc import SQLAlchemyError

from ..controllers.dto import Result
from ..controllers.dto.ml_component import GetMLComponentRes, PostMLComponentReq, PostMLComponentRes
from ..entities.organization import OrganizationMapper
from ..entities.ml_component import MLComponentMapper
from ..entities.test import TestMapper
from ..across.exception import QAINotFoundException, QAIInvalidRequestException, QAIInternalServerException
from ..gateways.extensions import sql_db


class MLComponentService:
    def get_ml_component_list(self, organizer_id: str) -> GetMLComponentRes:
        org = OrganizationMapper.query.get(organizer_id)
        if org is None:
            raise QAINotFoundException('P14000', 'not found organizer')

        ml_components = MLComponentMapper.query\
            .filter(MLComponentMapper.org_id == organizer_id).all()

        return GetMLComponentRes(
            result=Result(code='P12000', message="get list success."),
            ml_components=[m.to_dto() for m in ml_components]
        )

    def post(self, organizer_id: str, req: PostMLComponentReq) -> PostMLComponentRes:
        org = OrganizationMapper.query.get(organizer_id)
        if org is None:
            raise QAINotFoundException('P24000', 'not found organizer')

        try:
            ml_component_mapper = MLComponentMapper(name=req.name,
                                                    description=req.description,
                                                    problem_domain=req.problem_domain,
                                                    ml_framework_id=req.ml_framework_id,
                                                    org_id=org.id)
            sql_db.session.add(ml_component_mapper)
            sql_db.session.flush()

            test = TestMapper(ml_component_id=ml_component_mapper.id)
            sql_db.session.add(test)

            sql_db.session.commit()
        except SQLAlchemyError as e:
            sql_db.session.rollback()
            raise QAIInvalidRequestException('P29999', 'database error: {}'.format(e))
        except Exception as e:
            sql_db.session.rollback()
            raise QAIInternalServerException('P29999', 'internal server error: {}'.format(e))

        return PostMLComponentRes(
            result=Result(code='P22000', message="add ml-component success."),
            ml_component_id=ml_component_mapper.id
        )

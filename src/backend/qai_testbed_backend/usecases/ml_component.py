# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from sqlalchemy.exc import SQLAlchemyError
from qlib.utils.logging import get_logger, log

from ..controllers.dto import Result
from ..controllers.dto.ml_component import GetMLComponentRes, PostMLComponentReq, PostMLComponentRes, DeleteMLComponentRes
from ..entities.organization import OrganizationMapper
from ..entities.ml_component import MLComponentMapper
from ..entities.test import TestMapper
from ..across.exception import QAINotFoundException, QAIInvalidRequestException, QAIInternalServerException, QAIException
from ..gateways.extensions import sql_db

from ..entities.test_description import TestDescriptionMapper
from ..entities.inventory import InventoryMapper

logger = get_logger()


class MLComponentService:
    @log(logger)
    def get_ml_component_list(self, organizer_id: str) -> GetMLComponentRes:
        org = OrganizationMapper.query.get(organizer_id)
        if org is None:
            raise QAINotFoundException('P14000', 'not found organizer')

        ml_components = MLComponentMapper.query\
            .filter(MLComponentMapper.org_id == organizer_id)\
            .filter(MLComponentMapper.delete_flag == False).all()
        
        return GetMLComponentRes(
            result=Result(code='P12000', message="get list success."),
            ml_components=[m.to_dto() for m in ml_components]
        )

    @log(logger)
    def post(self, organizer_id: str, req: PostMLComponentReq) -> PostMLComponentRes:
        org = OrganizationMapper.query.get(organizer_id)
        if org is None:
            raise QAINotFoundException('P24000', 'not found organizer')

        try:
            ml_component_mapper = MLComponentMapper(name=req.name,
                                                    description=req.description,
                                                    problem_domain=req.problem_domain,
                                                    ml_framework_id=req.ml_framework_id,
                                                    org_id=org.id,
                                                    delete_flag=False)
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

    @log(logger)
    def delete_ml_component(self, organizer_id: str, ml_component_id: int) -> DeleteMLComponentRes:
        try:
            ml_component = MLComponentMapper.query. \
                filter(MLComponentMapper.id == ml_component_id). \
                filter(MLComponentMapper.org_id == organizer_id).first()

            if ml_component is None:
                raise QAINotFoundException('P34000', 'not found ml_component')

            if ml_component.delete_flag is True:
                raise QAINotFoundException('P34001', 'ml_component has already been deleted')

            ml_component.delete_flag = True

            # 関連するTesDescriptionを削除する
            test = TestMapper.query. \
                filter(TestMapper.ml_component_id == ml_component_id). \
                filter(MLComponentMapper.org_id == organizer_id). \
                first()
            
            if test is not None:
                test_descriptions = TestDescriptionMapper.query. \
                    filter(TestDescriptionMapper.test_id == test.id). \
                    filter(TestDescriptionMapper.delete_flag == False). \
                    all()
            
                for t_d in test_descriptions:
                    t_d.delete_flag = True

            # 関連するInventoryを削除する
            inventories = InventoryMapper.query. \
                filter(InventoryMapper.ml_component_id == ml_component_id). \
                filter(MLComponentMapper.org_id == organizer_id). \
                all()

            for inv in inventories:
                inv.delete_flag = True

            sql_db.session.commit()

        except QAIException as e:
            sql_db.session.rollback()
            raise e
        except SQLAlchemyError as e:
            sql_db.session.rollback()
            raise QAIInvalidRequestException('P39000', 'database error: {}'.format(e))
        except Exception as e:
            sql_db.session.rollback()
            raise QAIInternalServerException(result_code='P39999', result_msg='internal server error: {}'.format(e))

        return DeleteMLComponentRes(
            result=Result(code='P32000', message="delete success.")
        )

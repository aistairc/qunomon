# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import requests
import datetime

from sqlalchemy.exc import SQLAlchemyError
from requests.exceptions import RequestException
from qlib.utils.logging import get_logger, log

from ..controllers.dto import Result
from ..controllers.dto.guideline import GetGuidelinesRes, DeleteGuidelineRes, \
                                        PutGuidelineReq, PutGuidelineRes
from ..entities.guideline import GuidelineMapper
from ..entities.ml_component import MLComponentMapper
from ..entities.quality_dimension import QualityDimensionMapper
from ..entities.quality_dimension_level import QualityDimensionLevelMapper
from ..entities.setting import SettingMapper
from ..entities.scope import ScopeMapper
from ..entities.scope_quality_dimension import ScopeQualityDimensionMapper
from ..across.exception import QAINotFoundException, QAIInternalServerException, QAIInvalidRequestException, QAIException
from ..gateways.extensions import sql_db
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logger = get_logger()


class GuidelineService:
    @log(logger)
    def get_guideline(self) -> GetGuidelinesRes:

        guidelines = GuidelineMapper.query. \
            filter(GuidelineMapper.delete_flag == False).all()

        return GetGuidelinesRes(
            result=Result(code='G21000', message="get list success."),
            guidelines=[d.to_dto() for d in guidelines]
        )


    def delete(self, guideline_id: int) -> DeleteGuidelineRes:
        try:
            guideline = GuidelineMapper.query. \
                filter(GuidelineMapper.id == guideline_id).first()

            if guideline is None:
                raise QAINotFoundException('G23404', 'not found guideline')

            if guideline.delete_flag is True:
                raise QAINotFoundException('G23404', 'guideline has already been deleted')

            # ガイドラインがMlComponentに登録済みの場合は削除不可
            ml_component = MLComponentMapper.query. \
                filter(MLComponentMapper.guideline_id == guideline_id). \
                filter(MLComponentMapper.delete_flag == False).all()
            if len(ml_component) > 0:
                raise QAIInvalidRequestException('G23403', 'guideline is already registered in MlComponent.')

            # guideline削除
            guideline.update_datetime = datetime.datetime.utcnow()
            guideline.delete_flag = True
            sql_db.session.flush()

            # scopes削除
            scopes = ScopeMapper.query. \
                filter(ScopeMapper.guideline_id == guideline_id).all()
            for scope in scopes:
                scope.update_datetime = datetime.datetime.utcnow()
                scope.delete_flag = True
            sql_db.session.flush()

            # quality_dimensions削除
            qds = QualityDimensionMapper.query. \
                filter(QualityDimensionMapper.guideline_id == guideline_id).all()
            for qd in qds:
                qd.update_datetime = datetime.datetime.utcnow()
                qd.delete_flag = True
            sql_db.session.flush()

            # scopes_quality_dimensions削除
            sqds = ScopeQualityDimensionMapper.query. \
                filter(ScopeQualityDimensionMapper.guideline_id == guideline_id).all()
            for sqd in sqds:
                sqd.update_datetime = datetime.datetime.utcnow()
                sqd.delete_flag = True
            sql_db.session.commit()

        except QAIException as e:
            sql_db.session.rollback()
            raise e
        except SQLAlchemyError as e:
            sql_db.session.rollback()
            raise QAIInvalidRequestException(result_code='G23999', result_msg='database error: {}'.format(e))
        except Exception as e:
            sql_db.session.rollback()
            raise QAIInternalServerException(result_code='G23999', result_msg='internal server error: {}'.format(e))

        return DeleteGuidelineRes(
            result=Result(code='G23000', message="delete success.")
        )

    def edit_guideline(self, req: PutGuidelineReq, guideline_id: int) -> PutGuidelineRes:
        try:
            guideline = GuidelineMapper.query. \
                filter(GuidelineMapper.id == guideline_id).first()

            if guideline is None:
                raise QAINotFoundException('G24404', 'not found guideline')

            if guideline.delete_flag is True:
                raise QAINotFoundException('G24404', 'guideline has already been deleted')

            if req.description is not None :
                guideline.description = req.description

            if req.creator is not None :
                guideline.creator = req.creator

            if req.publisher is not None :
                guideline.publisher = req.publisher
            
            if req.identifier is not None :
                guideline.identifier = req.identifier

            if req.publish_datetime is not None :
                guideline.publish_datetime = datetime.datetime.strptime(req.publish_datetime, '%Y-%m-%d %H:%M:%S')
            
            if req.aithub_delete_flag is not None :
                guideline.aithub_delete_flag = bool(req.aithub_delete_flag)
            
            # guideline.update_datetime = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            guideline.update_datetime = datetime.datetime.utcnow()

            sql_db.session.commit()

        except QAIException as e:
            sql_db.session.rollback()
            raise e
        except SQLAlchemyError as e:
            sql_db.session.rollback()
            raise QAIInvalidRequestException(result_code='G24999', result_msg='database error: {}'.format(e))
        except Exception as e:
            sql_db.session.rollback()
            raise QAIInternalServerException(result_code='G24999', result_msg='internal server error: {}'.format(e))

        return PutGuidelineRes(
            result=Result(code='G24000', message="update success.")
        )
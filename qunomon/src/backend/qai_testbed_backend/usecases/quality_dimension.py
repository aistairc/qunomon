# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import requests
import datetime

from pathlib import Path
from sqlalchemy.exc import SQLAlchemyError
from requests.exceptions import RequestException
from qlib.utils.logging import get_logger, log

from ..controllers.dto import Result
from ..controllers.dto.quality_dimension import GetQualityDimensionsRes
from ..entities.quality_dimension import QualityDimensionMapper
from ..entities.scope_quality_dimension import ScopeQualityDimensionMapper


logger = get_logger()


class QualityDimensionService:
    @log(logger)
    def get_quality_dimension(self, scope_id: int) -> GetQualityDimensionsRes:

        quality_dimensions = QualityDimensionMapper.query. \
            join(ScopeQualityDimensionMapper, ScopeQualityDimensionMapper.quality_dimension_id == QualityDimensionMapper.id). \
            filter(QualityDimensionMapper.delete_flag == False). \
            filter(ScopeQualityDimensionMapper.scope_id == scope_id).all()

        return GetQualityDimensionsRes(
            result=Result(code='Q00000', message="get list success."),
            quality_dimensions=[q.to_dto() for q in quality_dimensions]
        )

    @log(logger)
    def get_guideline_quality_dimension(self, guideline_id: int) -> GetQualityDimensionsRes:

        quality_dimensions = QualityDimensionMapper.query. \
            filter(QualityDimensionMapper.delete_flag == False). \
            filter(QualityDimensionMapper.guideline_id == guideline_id).all()

        return GetQualityDimensionsRes(
            result=Result(code='Q01000', message="get list success."),
            quality_dimensions=[q.to_dto() for q in quality_dimensions]
        )
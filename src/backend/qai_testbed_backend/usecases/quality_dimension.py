# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from qlib.utils.logging import get_logger, log

from ..controllers.dto import Result
from ..controllers.dto.quality_dimension import GetQualityDimensionsRes, QualityDimensions
from ..entities.quality_dimension import QualityDimensionMapper
from ..across.exception import QAINotFoundException


logger = get_logger()


class QualityDimensionService:
    @log(logger)
    def get_quality_dimension(self) -> GetQualityDimensionsRes:
        quality_dimensions = QualityDimensionMapper.query.all()

        if quality_dimensions is None:
            raise QAINotFoundException('Q14000', 'not found quality property')

        return GetQualityDimensionsRes(
            result=Result(code='Q12000', message="get list success."),
            quality_dimensions=[q.to_dto() for q in quality_dimensions]
        )

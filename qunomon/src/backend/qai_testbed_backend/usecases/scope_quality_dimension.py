# Copyright © 2022 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
# from qlib.utils.logging import get_logger, log
from qlib.utils.logging import get_logger, log

from ..controllers.dto import Result
from ..entities.scope_quality_dimension import ScopeQualityDimensionMapper
from ..controllers.dto.scope_quality_dimension import GetScopeQualityDimensionsRes


logger = get_logger()


class ScopeQualityDimensionService:

    @log(logger)
    def get_guideline_scope_quality_dimensions(self, guideline_id: int):

        guideline_scope_qd_list = ScopeQualityDimensionMapper.query \
                            .filter(ScopeQualityDimensionMapper.guideline_id == guideline_id) \
                            .filter(ScopeQualityDimensionMapper.delete_flag.is_(False)) \
                            .all()

        return GetScopeQualityDimensionsRes(
            result=Result(code='S02000', message='Success.'),
            scopeQualityDimension=[sqd.to_dto() for sqd in guideline_scope_qd_list]
        )



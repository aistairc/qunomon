# Copyright © 2022 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.

from qlib.utils.logging import get_logger, log

from ..controllers.dto import Result
from ..controllers.dto.quality_dimension_detail import GetQualityDimensionDetailRes
from ..entities.guideline import GuidelineMapper
from ..entities.quality_dimension import QualityDimensionMapper
from ..across.exception import QAINotFoundException


logger = get_logger()


class QualityDimensionDetailService:

    @log(logger)
    def get_quality_dimension_detail(self, guideline_name: str, qd_name: str):

        # QDテーブルからデータ取得
        quality_dimension = QualityDimensionMapper.query.\
            join(GuidelineMapper, GuidelineMapper.id == QualityDimensionMapper.guideline_id).\
            filter(QualityDimensionMapper.name == qd_name).\
            filter(GuidelineMapper.name == guideline_name).first()

        # 品質特性が存在しないまたは削除されている場合エラー
        if quality_dimension is None or quality_dimension.delete_flag:
            raise QAINotFoundException('Q02404', 'not found quality dimension.')

        return GetQualityDimensionDetailRes(
            result=Result(code='Q02000', message='Success.'),
            quality_dimension=quality_dimension.to_dto()
        )


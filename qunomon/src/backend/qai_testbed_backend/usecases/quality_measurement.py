# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from datetime import datetime, timedelta, timezone
from requests import post, get
from qlib.utils.logging import get_logger, log

from ..across.exception import QAINotFoundException, QAIBadRequestException, QAIException, QAIInternalServerException
from ..controllers.dto import Result
from ..controllers.dto.quality_measurement import GetQualityMeasurementTemplateRes
from ..entities.quality_measurement import QualityMeasurementMapper
from ..entities.quality_dimension import QualityDimensionMapper
from ..gateways.extensions import sql_db


logger = get_logger()


class QualityMeasurementService:
    def __init__(self):
        pass

    @log(logger)
    def get_quality_measurement(self) -> GetQualityMeasurementTemplateRes:
        quality_measurements = QualityMeasurementMapper.query.all()  # organizer_id, ml_component_idに関わらずすべて取得
        if quality_measurements is None:
            raise QAINotFoundException('Q24000', 'not found quality_measurements')

        return GetQualityMeasurementTemplateRes(
            result=Result(code='Q22000', message="get quality_measurement success."),
            quality_measurements=[m.to_template_dto() for m in quality_measurements]
        )
    #
    # def add_quality_measurement(self, req: PostQualityMeasurementTemplateReq) -> PostQualityMeasurementTemplateRes:
    #
    #     # 同一measurementチェック
    #     same_measure = QualityMeasurementMapper.query.\
    #         filter(QualityMeasurementMapper.name == req.name).\
    #         filter(QualityMeasurementMapper.version == req.version).first()
    #     if same_measure is not None:
    #         raise QAIBadRequestException(result_code='Q23010', result_msg='invalid request. '
    #                                                                       'Same Name and Version exists.')
    #
    #     # quality_dimension_id 整合性チェック
    #     quality_prop = QualityDimensionMapper.query.get(req.quality_dimension_id)
    #     if quality_prop is None:
    #         raise QAIBadRequestException(result_code='Q23010', result_msg='invalid request. '
    #                                                                       'QualityDimensionId is not found.')
    #     try:
    #         quality_measurement = QualityMeasurementMapper(name=req.name,
    #                                         version=req.version,
    #                                         description=req.description,
    #                                         quality_dimension_id=req.quality_dimension_id)
    #         sql_db.session.add(quality_measurement)
    #         sql_db.session.flush()
    #
    #         ope_temps = []
    #         for operand_req in req.operand_templates:
    #             operand = OperandTemplateMapper(name=operand_req.name,
    #                                             unit=operand_req.unit,
    #                                             quality_measurement_id=quality_measurement.id)
    #             ope_temps.append(operand)
    #         sql_db.session.add_all(ope_temps)
    #
    #         sql_db.session.commit()
    #
    #         return PostQualityMeasurementTemplateRes(
    #             result=Result(code='Q23000', message="add quality_measurement success.")
    #         )
    #     except QAIException as e:
    #         sql_db.session.rollback()
    #         raise e
    #     except Exception as e:
    #         sql_db.session.rollback()
    #         raise QAIInternalServerException(result_code='Q49999', result_msg='internal server error: {}'.format(e))

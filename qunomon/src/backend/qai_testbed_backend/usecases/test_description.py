# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import Optional
from qlib.utils.logging import get_logger, log

from ..controllers.dto import Result
from ..controllers.dto.test_description import GetTestDescriptionsRes, GetTestDescriptionDetailRes,\
    DeleteTestDescriptionRes, PutTestDescriptionRes, PutTestDescriptionsReq, AppendTestDescriptionRes,\
    AppendTestDescriptionReq, GetTestDescriptionAncestorsRes, GetUsingTestDescriptionsRes
from ..entities.test import TestMapper
from ..entities.ml_component import MLComponentMapper
from ..entities.test_description import TestDescriptionMapper
from ..entities.operand import OperandMapper
from ..entities.quality_measurement import QualityMeasurementMapper
from ..entities.inventory_td import InventoryTDMapper
from ..entities.organization import OrganizationMapper
from ..entities.test_runner_param import TestRunnerParamMapper
from ..entities.test_runner_param_template import TestRunnerParamTemplateMapper
from ..across.exception import QAIException, QAINotFoundException, QAIInternalServerException,\
    QAIInvalidRequestException
from ..across.utils import is_num
from ..gateways.extensions import sql_db
from sqlalchemy.exc import SQLAlchemyError
import datetime


logger = get_logger()


class TestDescriptionService:

    def __init__(self):
        # TODO 要DI
        pass

    @log(logger)
    def get(self, organizer_id: str, ml_component_id: int, testdescription_id: int) -> GetTestDescriptionDetailRes:

        org = OrganizationMapper.query.filter(OrganizationMapper.organizer_id == organizer_id).first()
        if org is None:
            raise QAINotFoundException(result_code='I34002', result_msg=f'organizer_id:{organizer_id} is not found')
        try:
            td = TestDescriptionMapper.query. \
                                       filter(TestMapper.ml_component_id == ml_component_id).\
                                       filter(MLComponentMapper.org_id == org.id).\
                                       filter(TestDescriptionMapper.id == testdescription_id).first()
            if td is None:
                raise QAINotFoundException(result_code='T34000', result_msg='not found test description')

            # delete_flagがTrueのTDであれば、エラーを返す。
            if td.delete_flag is True:
                raise QAINotFoundException(result_code='T34001', result_msg='test description has already been deleted')

            return GetTestDescriptionDetailRes(result=Result(code='T32000', message="get detail success."),
                                               test_description_detail=td.to_dto_detail())
        except QAIException as e:
            raise e
        except SQLAlchemyError as e:
            raise QAIInvalidRequestException('T39000', 'database error: {}'.format(e))
        except Exception as e:
            raise QAIInternalServerException(result_code='T39999', result_msg='internal server error: {}'.format(e))

    @log(logger)
    def get_list(self, organizer_id: str, ml_component_id: int) -> GetTestDescriptionsRes:

        org = OrganizationMapper.query.filter(OrganizationMapper.organizer_id == organizer_id).first()
        if org is None:
            raise QAINotFoundException(result_code='T14001', result_msg=f'organizer_id:{organizer_id} is not found')
        try:
            test = TestMapper.query.\
                              filter(TestMapper.ml_component_id == ml_component_id).\
                              filter(MLComponentMapper.org_id == org.id).first()
            if test is None:
                raise QAINotFoundException(result_code='T14000', result_msg='not found test descriptions')
            # delete_flagがTrueのTDを除外したTestDescriptionMapperを作る
            mapper = TestDescriptionMapper.query. \
                filter(TestDescriptionMapper.test_id == test.id). \
                filter(TestDescriptionMapper.delete_flag == False). \
                all()

            return GetTestDescriptionsRes(
                result=Result(code='T12000', message="get list success."),
                test=test.to_dto(mapper)
            )
        except QAIException as e:
            raise e
        except SQLAlchemyError as e:
            raise QAIInvalidRequestException('T19000', 'database error: {}'.format(e))
        except Exception as e:
            raise QAIInternalServerException(result_code='T19999', result_msg='internal server error: {}'.format(e))

    @log(logger)
    def delete_test_description(self, organizer_id: str, ml_component_id: int,
                                testdescription_id: int) -> DeleteTestDescriptionRes:

        org = OrganizationMapper.query.filter(OrganizationMapper.organizer_id == organizer_id).first()
        if org is None:
            raise QAINotFoundException(result_code='T54002', result_msg=f'organizer_id:{organizer_id} is not found')
        try:
            test_description = TestDescriptionMapper.query. \
                filter(TestMapper.ml_component_id == ml_component_id). \
                filter(MLComponentMapper.org_id == org.id). \
                filter(TestDescriptionMapper.id == testdescription_id).first()

            if test_description is None:
                raise QAINotFoundException('T54000', 'not found test descriptions')

            if test_description.delete_flag is True:
                raise QAINotFoundException('T54001', 'test description has already been deleted')

            # 子供がいる場合、子供のdelete_flagもTrueに変更する
            self._delete_children_td(org.id, ml_component_id, test_description.id)

            test_description.delete_flag = True
            sql_db.session.commit()
            return DeleteTestDescriptionRes(
                result=Result(code='T52000', message="delete success.")
            )
        except QAIException as e:
            sql_db.session.rollback()
            raise e
        except SQLAlchemyError as e:
            sql_db.session.rollback()
            raise QAIInvalidRequestException('T59000', 'database error: {}'.format(e))
        except Exception as e:
            sql_db.session.rollback()
            raise QAIInternalServerException(result_code='T59999', result_msg='internal server error: {}'.format(e))

    def _delete_children_td(self, organizer_id: int, ml_component_id: int, parent_td_id: Optional[int]):
        td_children = TestDescriptionMapper.query. \
            filter(TestMapper.ml_component_id == ml_component_id). \
            filter(MLComponentMapper.org_id == organizer_id). \
            filter(TestDescriptionMapper.parent_id == parent_td_id).all()
        for td_child in td_children:
            self._delete_children_td(organizer_id, ml_component_id, td_child.id)
            td_child.delete_flag = True

    @log(logger)
    def put_test_descriptions(self, organizer_id: str, ml_component_id: int,
                              testdescription_id: int, req: PutTestDescriptionsReq) -> PutTestDescriptionRes:

        org = OrganizationMapper.query.filter(OrganizationMapper.organizer_id == organizer_id).first()
        if org is None:
            raise QAINotFoundException(result_code='T44002', result_msg=f'organizer_id:{organizer_id} is not found')
        try:
            test_description = TestDescriptionMapper.query. \
                filter(TestDescriptionMapper.id == testdescription_id). \
                filter(TestMapper.ml_component_id == ml_component_id). \
                filter(MLComponentMapper.org_id == org.id).first()
            if test_description is None:
                raise QAINotFoundException(result_code='T44000', result_msg='not found test descriptions')

            # delete_flagがTrueのTDであれば、エラーを返す。
            if test_description.delete_flag is True:
                raise QAINotFoundException(result_code='T44001', result_msg='test description has already been deleted')

            test_description.name = req.name
            test_description.quality_dimension_id = req.quality_dimension_id
            test_description.test_runner_id = req.test_runner.id_
            test_description.update_datetime = datetime.datetime.utcnow()

            InventoryTDMapper().query.\
                filter(InventoryTDMapper.test_description_id == test_description.id).delete()
            OperandMapper().query.\
                filter(OperandMapper.test_description_id == test_description.id).delete()
            TestRunnerParamMapper().query.\
                filter(TestRunnerParamMapper.test_description_id == test_description.id).delete()

            self._add_operands(req, test_description)
            self._add_inventories(req, test_description)
            self._add_test_runner_params(req, test_description)
            self._update_value_target(req, test_description)

            sql_db.session.commit()

            return PutTestDescriptionRes(
                result=Result(code='T42000', message="put success."),
                test_description=test_description
            )
        except QAIException as e:
            sql_db.session.rollback()
            raise e
        except Exception as e:
            sql_db.session.rollback()
            raise QAIInternalServerException(result_code='T49999', result_msg='internal server error: {}'.format(e))

    @log(logger)
    def append_test_description(self, organizer_id: str, ml_component_id: int,
                                req: AppendTestDescriptionReq) -> AppendTestDescriptionRes:

        org = OrganizationMapper.query.filter(OrganizationMapper.organizer_id == organizer_id).first()
        if org is None:
            raise QAINotFoundException(result_code='T24001', result_msg=f'organizer_id:{organizer_id} is not found')
        try:
            test_description = TestDescriptionMapper()
            test = TestMapper.query. \
                filter(TestMapper.ml_component_id == ml_component_id). \
                filter(MLComponentMapper.org_id == org.id).first()
            test_description.name = req.name
            test_description.opinion = ''
            test_description.delete_flag = False

            if req.parent_id is not None:
                parent_td = TestDescriptionMapper.query.get(req.parent_id)
                if parent_td is None:
                    raise QAINotFoundException('T24000', 'not found parent test description')
                if parent_td.delete_flag:
                    raise QAINotFoundException('T24000', 'parent test description has deleted')
                test_description.parent_id = req.parent_id

            test_description.test_id = test.id
            test_description.quality_dimension_id = req.quality_dimension_id
            test_description.test_runner_id = req.test_runner.id_
            sql_db.session.add(test_description)
            sql_db.session.flush()

            self._add_operands(req, test_description)
            self._add_inventories(req, test_description)
            self._add_test_runner_params(req, test_description)
            self._update_value_target(req, test_description)

            sql_db.session.commit()

            return AppendTestDescriptionRes(
                result=Result(code='T22000', message="append test description success.")
            )
        except QAIException as e:
            sql_db.session.rollback()
            raise e
        except SQLAlchemyError as e:
            sql_db.session.rollback()
            raise QAIInvalidRequestException('T29000', 'database error: {}'.format(e))
        except Exception as e:
            sql_db.session.rollback()
            raise QAIInternalServerException(result_code='T29999', result_msg='internal server error: {}'.format(e))

    def _add_test_runner_params(self, req, test_description):
        try:
            test_runner_params = []
            for test_runner_param_req in req.test_runner.params:
                # パラメータのminとmaxを取得する
                param_temp = TestRunnerParamTemplateMapper.query.get(test_runner_param_req.test_runner_param_template_id)
                if param_temp is None:
                    raise QAINotFoundException(result_code='T94000', result_msg='not found TestRunnerParamTemplate')
                # 空白・NULL以外の場合
                if (test_runner_param_req.value is not None) and (len(test_runner_param_req.value) > 0):
                    # min < 入力値 < maxのチェック
                    if param_temp.value_type == "int" or param_temp.value_type == "float":
                        # 入力値が数値か判定
                        if is_num(test_runner_param_req.value):
                            if param_temp.min_value is not None:
                                if param_temp.min_value > float(test_runner_param_req.value):
                                    raise QAIInvalidRequestException('T94001', f'parameter value({test_runner_param_req.value}) < min_val({param_temp.min_value})')

                            if param_temp.max_value is not None:
                                if param_temp.max_value < float(test_runner_param_req.value):
                                    raise QAIInvalidRequestException('T94001', f'parameter value({test_runner_param_req.value}) > max_val({param_temp.max_value})')
                        else:
                            raise QAIInvalidRequestException('T94001',  f'parameter value({test_runner_param_req.value}) is invalid')

                test_runner_param = TestRunnerParamMapper()
                test_runner_param.value = test_runner_param_req.value
                test_runner_param.test_description_id = test_description.id
                # TODO test_runner_param_template_idが紐づいているテストランナーのものかチェック
                test_runner_param.test_runner_param_template_id = test_runner_param_req.test_runner_param_template_id
                test_runner_params.append(test_runner_param)
            sql_db.session.add_all(test_runner_params)

        except QAIException as e:
            sql_db.session.rollback()
            raise e
        except SQLAlchemyError as e:
            sql_db.session.rollback()
            raise QAIInvalidRequestException('T99000', 'database error: {}'.format(e))
        except Exception as e:
            sql_db.session.rollback()
            raise QAIInternalServerException(result_code='T99999', result_msg='internal server error: {}'.format(e))

    def _add_inventories(self, req, test_description):
        inventories = []
        for inventory_req in req.target_inventories:
            inventory = InventoryTDMapper()
            inventory.inventory_id = inventory_req.inventory_id
            inventory.test_description_id = test_description.id
            # TODO template_inventory_idが紐づいているテストランナーのものかチェック
            inventory.template_inventory_id = inventory_req.template_inventory_id
            inventories.append(inventory)
        sql_db.session.add_all(inventories)

    def _add_operands(self, req, test_description):
        try:
            operands = []
            for measurement_req in req.quality_measurements:
                # クライテリアの入力があった場合
                if measurement_req.enable:
                    # クライテリアのminとmaxを取得する
                    quality_measurement = QualityMeasurementMapper.query.get(measurement_req.id_)
                    if quality_measurement is None:
                        raise QAINotFoundException(result_code='TA4000', result_msg='not found QualityMeasurement')
                    # min < 入力値 < maxのチェック
                    if quality_measurement.type == "int" or quality_measurement.type == "float":
                        # 入力値が数値か判定
                        if is_num(measurement_req.value):
                            if quality_measurement.min_value is not None:
                                if quality_measurement.min_value > float(measurement_req.value):
                                    raise QAIInvalidRequestException('TA4001', f'measurement value({measurement_req.value}) < min_val({quality_measurement.min_value})')

                            if quality_measurement.max_value is not None:
                                if quality_measurement.max_value < float(measurement_req.value):
                                    raise QAIInvalidRequestException('TA4001', f'measurement value({measurement_req.value}) > max_val({quality_measurement.max_value})')
                        else:
                            raise QAIInvalidRequestException('TA4001',  f'measurement value({measurement_req.value}) is invalid')

                operand = OperandMapper()
                operand.quality_measurement_id = measurement_req.id_
                operand.value = measurement_req.value
                operand.test_description_id = test_description.id
                operand.relational_operator_id = measurement_req.relational_operator_id
                operand.enable = measurement_req.enable
                operands.append(operand)
            sql_db.session.add_all(operands)

        except QAIException as e:
            sql_db.session.rollback()
            raise e
        except SQLAlchemyError as e:
            sql_db.session.rollback()
            raise QAIInvalidRequestException('TA9000', 'database error: {}'.format(e))
        except Exception as e:
            sql_db.session.rollback()
            raise QAIInternalServerException(result_code='TA9999', result_msg='internal server error: {}'.format(e))

    def _update_value_target(self, req, test_description):
        """quality_measurementsが存在する場合、レポートへの指標値出力フラグを有効にする"""
        if (req.quality_measurements is None) or (len(req.quality_measurements) == 0):
            test_description.value_target = False
        else:
            test_description.value_target = True

    @log(logger)
    def set_star(self, organizer_id: str, ml_component_id: int, test_description_id: int) -> Result:

        org = OrganizationMapper.query.filter(OrganizationMapper.organizer_id == organizer_id).first()
        if org is None:
            raise QAINotFoundException(result_code='T64001', result_msg=f'organizer_id:{organizer_id} is not found')
        try:
            td = TestDescriptionMapper.query. \
                                       filter(TestMapper.ml_component_id == ml_component_id).\
                                       filter(MLComponentMapper.org_id == org.id).\
                                       filter(TestDescriptionMapper.id == test_description_id).first()
            if td is None:
                raise QAINotFoundException(result_code='T64000', result_msg='not found test description')

            # delete_flagがTrueのTDであれば、エラーを返す。
            if td.delete_flag is True:
                raise QAIInvalidRequestException(result_code='T65000',
                                                 result_msg='test description has already been deleted')

            td.star = True
            sql_db.session.commit()

            return Result(code='T62000', message='set star success.')

        except QAIException as e:
            sql_db.session.rollback()
            raise e
        except SQLAlchemyError as e:
            sql_db.session.rollback()
            raise QAIInvalidRequestException('T69999', 'database error: {}'.format(e))

    @log(logger)
    def set_unstar(self, organizer_id: str, ml_component_id: int, test_description_id: int) -> Result:

        org = OrganizationMapper.query.filter(OrganizationMapper.organizer_id == organizer_id).first()
        if org is None:
            raise QAINotFoundException(result_code='T74001', result_msg=f'organizer_id:{organizer_id} is not found')
        try:
            td = TestDescriptionMapper.query. \
                                       filter(TestMapper.ml_component_id == ml_component_id).\
                                       filter(MLComponentMapper.org_id == org.id).\
                                       filter(TestDescriptionMapper.id == test_description_id).first()
            if td is None:
                raise QAINotFoundException(result_code='T74000', result_msg='not found test description')

            # delete_flagがTrueのTDであれば、エラーを返す。
            if td.delete_flag is True:
                raise QAIInvalidRequestException(result_code='T75000',
                                                 result_msg='test description has already been deleted')

            td.star = False
            sql_db.session.commit()

            return Result(code='T72000', message='set star success.')

        except QAIException as e:
            sql_db.session.rollback()
            raise e
        except SQLAlchemyError as e:
            sql_db.session.rollback()
            raise QAIInvalidRequestException('T79999', 'database error: {}'.format(e))

    @log(logger)
    def get_ancestor(self, organizer_id: str, ml_component_id: int, test_description_id: int)\
            -> GetTestDescriptionAncestorsRes:

        org = OrganizationMapper.query.filter(OrganizationMapper.organizer_id == organizer_id).first()
        if org is None:
            raise QAINotFoundException(result_code='T84001', result_msg=f'organizer_id:{organizer_id} is not found')
        try:
            td = TestDescriptionMapper.query. \
                                       filter(TestMapper.ml_component_id == ml_component_id).\
                                       filter(MLComponentMapper.org_id == org.id).\
                                       filter(TestDescriptionMapper.id == test_description_id).first()
            if td is None:
                raise QAINotFoundException(result_code='T84000', result_msg='not found test description')

            # delete_flagがTrueのTDであれば、エラーを返す。
            if td.delete_flag is True:
                raise QAIInvalidRequestException(result_code='T85000',
                                                 result_msg='test description has already been deleted')

            test_descriptions = []

            next_td = td
            while next_td is not None:
                test_descriptions.append(next_td)
                next_td = TestDescriptionMapper.query. \
                    filter(TestMapper.ml_component_id == ml_component_id). \
                    filter(MLComponentMapper.org_id == org.id). \
                    filter(TestDescriptionMapper.id == next_td.parent_id). \
                    filter(TestDescriptionMapper.delete_flag == False).first()

            test_descriptions.reverse()

            return GetTestDescriptionAncestorsRes(result=Result(code='T82000', message="get detail success."),
                                                  test_descriptions=[td.to_dto() for td in test_descriptions])
        except QAIException as e:
            raise e
        except SQLAlchemyError as e:
            raise QAIInvalidRequestException('T89000', 'database error: {}'.format(e))

    @log(logger)
    def get_using(self, test_runner_id: int) -> GetUsingTestDescriptionsRes:

        try:
            td_list  = TestDescriptionMapper.query.\
                          filter(TestDescriptionMapper.test_runner_id == test_runner_id).\
                          filter(TestDescriptionMapper.delete_flag == False).all()

            return GetUsingTestDescriptionsRes(
                result=Result(code='A03000', message="command invoke success."),
                using_Test_Descriptions=[t.to_dto_useing() for t in td_list ]
            )
        except QAIException as e:
            raise e
        except SQLAlchemyError as e:
            raise QAIInvalidRequestException('A03900', 'database error: {}'.format(e))
        except Exception as e:
            raise QAIInternalServerException(result_code='A03999', result_msg='internal server error: {}'.format(e))

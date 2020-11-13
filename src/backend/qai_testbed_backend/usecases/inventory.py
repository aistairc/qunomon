# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import datetime
from typing import List
from sqlalchemy.exc import IntegrityError
import re

from ..controllers.dto import Result
from ..controllers.dto.inventory import GetInventoriesRes, DeleteInventoryRes, AppendInventoryReq,\
    AppendInventoryRes, PutInventoryReq, PutInventoryRes
from ..controllers.dto.format import Format
from ..entities.inventory import InventoryMapper
from ..entities.inventory_td import InventoryTDMapper
from ..entities.test_description import TestDescriptionMapper
from ..entities.organization import OrganizationMapper
from ..entities.ml_component import MLComponentMapper
from ..entities.format import FormatMapper
from ..entities.inventory_format import InventoryFormatMapper
from ..entities.file_system import FileSystemMapper
from ..across.exception import QAIException, \
    QAINotFoundException, QAIInvalidRequestException, QAIInternalServerException
from ..gateways.extensions import sql_db
from sqlalchemy.exc import SQLAlchemyError


class InventoryService:

    def get_inventories(self, organizer_id: str, ml_component_id: int) -> GetInventoriesRes:

        if OrganizationMapper.query.get(organizer_id) is None:
            raise QAINotFoundException(result_code='I14000', result_msg=f'organizer_id:{organizer_id} is not found')

        if MLComponentMapper.query.get(ml_component_id) is None:
            raise QAINotFoundException(result_code='I14000',
                                       result_msg=f'ml_component_id:{ml_component_id} is not found')

        inventories = InventoryMapper.query. \
            filter(InventoryMapper.ml_component_id == ml_component_id). \
            filter(MLComponentMapper.org_id == organizer_id). \
            filter(InventoryMapper.delete_flag == False)

        return GetInventoriesRes(
            result=Result(code='I12000', message="get list success."),
            inventories=[i.to_dto_detail() for i in inventories]
        )

    def delete_inventory(self, organizer_id: str, ml_component_id: int,
                         inventory_id: int) -> DeleteInventoryRes:
        inventory = InventoryMapper.query. \
            filter(InventoryMapper.ml_component_id == ml_component_id). \
            filter(MLComponentMapper.org_id == organizer_id). \
            filter(InventoryMapper.id == inventory_id).first()

        if inventory is None:
            raise QAINotFoundException('I44000', 'not found inventory')

        if inventory.delete_flag is True:
            raise QAINotFoundException('I44001', 'inventory has already been deleted')

        # 未削除のTDに利用されているInventoryは削除できないようにチェックする
        inv_tds = InventoryTDMapper.query. \
            filter(InventoryTDMapper.inventory_id == inventory_id).all()
        if inv_tds is not None:
            for inv_td in inv_tds:
                td = TestDescriptionMapper.query. \
                    filter(TestDescriptionMapper.id == inv_td.test_description_id).first()
                if td is not None and td.delete_flag is False:
                    raise QAINotFoundException('I45000',
                                               'this inventory cannot delete because it\'s referenced by'
                                               ' \'' + td.name + '\'')

        try:
            inventory.delete_flag = True
            sql_db.session.commit()
        except SQLAlchemyError as e:
            sql_db.session.rollback()
            raise QAIInvalidRequestException('I49000', 'database error: {}'.format(e))

        except Exception as e:
            sql_db.session.rollback()
            raise QAIInternalServerException(result_code='I49999', result_msg='internal server error: {}'.format(e))

        return DeleteInventoryRes(
            result=Result(code='I42000', message='delete success.')
        )

    def append_inventory(self, organizer_id: str, ml_component_id: int,
                         req: AppendInventoryReq) -> AppendInventoryRes:
        inventory = InventoryMapper()

        if not self._check_file_path(req.file_system_id, req.file_path):
            raise QAIInvalidRequestException('I24001', 'inventory file path is invalid.')

        try:
            inventory.name = req.name
            inventory.type_id = req.type_id
            inventory.file_system_id = req.file_system_id
            inventory.file_path = req.file_path
            inventory.description = req.description
            inventory.schema = req.schema
            inventory.delete_flag = False
            inventory.ml_component_id = ml_component_id
            sql_db.session.add(inventory)
            sql_db.session.flush()

            inventory_format_list = self.create_inventory_format_list(inventory.id, req.formats)
            sql_db.session.add_all(inventory_format_list)
            sql_db.session.commit()
            return AppendInventoryRes(
                result=Result(code='I22000', message="append Inventory success.")
            )
        except IntegrityError as e:
            print(e)
            sql_db.session.rollback()
            raise QAINotFoundException(result_code='I24000', result_msg='not found ml_component')
        except QAIException:
            raise
        except Exception as e:
            print('Exception: {}'.format(e))
            raise QAIInternalServerException(result_code='I29999', result_msg='internal server error')

    @staticmethod
    def create_inventory_format_list(inventory_id: int, formats: List[Format]) -> List[InventoryFormatMapper]:
        inventory_format_list = []
        for format_ in formats:
            format_mapper = FormatMapper.query.filter(FormatMapper.format_ == format_).first()
            if format_mapper is None:
                raise QAIInvalidRequestException(result_code='I20000', result_msg=f'Formats:[{format_}] is not found.')

            inventory_format = InventoryFormatMapper(inventory_id=inventory_id, format_id=format_mapper.id)
            inventory_format_list.append(inventory_format)
        return inventory_format_list

    def put_inventory(self, organizer_id: str, ml_component_id: int,
                      inventory_id: int, req: PutInventoryReq) -> PutInventoryRes:

        inventory = InventoryMapper.query. \
            filter(InventoryMapper.ml_component_id == ml_component_id). \
            filter(MLComponentMapper.org_id == organizer_id). \
            filter(InventoryMapper.id == inventory_id).first()

        if inventory is None:
            raise QAINotFoundException('I34000', 'not found inventory')

        if inventory.delete_flag is True:
            raise QAINotFoundException('I34001', 'inventory has already been deleted')

        if not self._check_file_path(req.file_system_id, req.file_path):
            raise QAIInvalidRequestException('I34002', 'inventory file path is invalid.')

        try:
            inventory.name = req.name
            inventory.type_id = req.type_id
            inventory.file_system_id = req.file_system_id
            inventory.file_path = req.file_path
            inventory.description = req.description
            inventory.schema = req.schema
            inventory.update_datetime = datetime.datetime.utcnow()
            sql_db.session.flush()

            InventoryFormatMapper.query. \
                filter(InventoryFormatMapper.inventory_id == inventory_id).delete()

            inventory_format_list = self.create_inventory_format_list(inventory.id, req.formats)
            sql_db.session.add_all(inventory_format_list)
            sql_db.session.commit()

            return PutInventoryRes(
                result=Result(code='I32000', message="put success.")
            )
        except SQLAlchemyError as e:
            sql_db.session.rollback()
            raise QAIInvalidRequestException('I39000', 'database error: {}'.format(e))
        except Exception as e:
            sql_db.session.rollback()
            raise QAIInternalServerException(result_code='I39999', result_msg='internal server error: {}'.format(e))

    @staticmethod
    def _check_file_path(file_system_id, file_path) -> bool:
        file_system = FileSystemMapper.query.get(file_system_id)

        if file_system is None:
            return False

        if file_system.name == 'WINDOWS_FILE':
            if re.search('^[A-Z]:', file_path.upper()) is None:
                return False

            if len(file_path) > 259:
                return False

            return True
        elif file_system.name == 'UNIX_FILE_SYSTEM':
            if not file_path.startswith('/'):
                return False

            if len(file_path) > 1023:
                return False

            for item in file_path.split('/'):
                if len(item) > 255:
                    return False

            return True
        else:
            return False

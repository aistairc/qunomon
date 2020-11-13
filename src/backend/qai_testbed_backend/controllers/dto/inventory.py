# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List
from marshmallow import post_dump, fields

from . import Result, ResultSchema, BaseSchema
from .format import Format, FormatSchema


class DataType:
    def __init__(self, id_: int, name: str) -> None:
        self.id_ = id_
        self.name = name


class FileSystem:
    def __init__(self, id_: int, name: str) -> None:
        self.id_ = id_
        self.name = name


class InventoryDetail:
    def __init__(self, id_: int, name: str, type_: DataType, file_system: FileSystem, file_path: str, description: str,
                 formats: List[Format], schema: str, creation_datetime: str, update_datetime: str) -> None:
        self.id_ = id_
        self.name = name
        self.type = type_
        self.file_system = file_system
        self.file_path = file_path
        self.description = description
        self.formats = formats
        self.schema = schema
        self.creation_datetime = creation_datetime
        self.update_datetime = update_datetime


class GetInventoriesRes:
    def __init__(self, result: Result, inventories: List[InventoryDetail]) -> None:
        self.result = result
        self.inventories = inventories


class DeleteInventoryRes:
    def __init__(self, result: Result) -> None:
        self.result = result


class AppendInventoryRes:
    def __init__(self, result: Result) -> None:
        self.result = result


class PutInventoryRes:
    def __init__(self, result: Result) -> None:
        self.result = result


class AppendInventoryReq:
    def __init__(self, name: str, type_id: int, file_system_id: int, file_path: str, description: str,
                 formats: List[str], schema: str = None) -> None:
        self.name = name
        self.type_id = type_id
        self.file_system_id = file_system_id
        self.file_path = file_path
        self.description = description
        self.formats = formats
        self.schema = schema


class PutInventoryReq:
    def __init__(self, name: str, type_id: int, file_system_id: int, file_path: str, description: str,
                 formats: List[str], schema: str = None) -> None:
        self.name = name
        self.type_id = type_id
        self.file_system_id = file_system_id
        self.file_path = file_path
        self.description = description
        self.formats = formats
        self.schema = schema


class DataTypeSchema(BaseSchema):
    __model__ = DataType
    id_ = fields.Int(data_key='Id')
    name = fields.Str(data_key='Name')


class FileSystemSchema(BaseSchema):
    __model__ = FileSystem
    id_ = fields.Int(data_key='Id')
    name = fields.Str(data_key='Name')


class InventoryDetailSchema(BaseSchema):
    __model__ = InventoryDetail
    id_ = fields.Int(data_key='Id')
    name = fields.Str(data_key='Name')
    type = fields.Nested(DataTypeSchema, data_key='DataType')
    file_system = fields.Nested(FileSystemSchema, data_key='FileSystem')
    file_path = fields.Str(data_key='FilePath')
    description = fields.Str(data_key='Description')
    formats = fields.Nested(FormatSchema, data_key='Formats', many=True)
    schema = fields.Str(data_key='Schema')
    creation_datetime = fields.Str(data_key='CreationDatetime')
    update_datetime = fields.Str(data_key='UpdateDatetime')

    @post_dump
    def remove_skip_values(self, data, **_):
        return {
            key: value for key, value in data.items()
            if (key != 'Schema') or (value is not None)
        }


class GetInventoriesResSchema(BaseSchema):
    __model__ = GetInventoriesRes
    result = fields.Nested(ResultSchema, data_key='Result')
    inventories = fields.Nested(InventoryDetailSchema, data_key='Inventories', many=True)


class DeleteInventoryResSchema(BaseSchema):
    __model__ = DeleteInventoryRes
    result = fields.Nested(ResultSchema, data_key='Result')


class AppendInventoryResSchema(BaseSchema):
    __model__ = AppendInventoryRes
    result = fields.Nested(ResultSchema, data='Result')


class PutInventoryResSchema(BaseSchema):
    __model__ = PutInventoryRes
    result = fields.Nested(ResultSchema, data='Result')


class AppendInventoryReqSchema(BaseSchema):
    __model__ = AppendInventoryReq
    name = fields.Str(data_key='Name', required=True)
    type_id = fields.Int(data_key='TypeId', required=True)
    file_system_id = fields.Int(data_key='FileSystemId', required=True)
    file_path = fields.Str(data_key='FilePath', required=True)
    description = fields.Str(data_key='Description')
    formats = fields.List(fields.Str, data_key='Formats', required=True)
    schema = fields.Str(data_key='Schema', required=False)


class PutInventoryReqSchema(BaseSchema):
    __model__ = PutInventoryReq
    name = fields.Str(data_key='Name', required=True)
    type_id = fields.Int(data_key='TypeId', required=True)
    file_system_id = fields.Int(data_key='FileSystemId', required=True)
    file_path = fields.Str(data_key='FilePath', required=True)
    description = fields.Str(data_key='Description')
    formats = fields.List(fields.Str, data_key='Formats', required=True)
    schema = fields.Str(data_key='Schema', required=False)

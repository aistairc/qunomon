# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List
from marshmallow import fields

from . import Result, ResultSchema, BaseSchema


class FileSystem:
    def __init__(self, id_: int, name: str) -> None:
        self.id_ = id_
        self.name = name


class GetFileSystemsRes:
    def __init__(self, result: Result, file_systems: List[FileSystem]) -> None:
        self.result = result
        self.file_systems = file_systems


class FileSystemSchema(BaseSchema):
    __model__ = FileSystem
    id_ = fields.Int(data_key='Id')
    name = fields.Str(data_key='Name')


class GetFileSystemsResSchema(BaseSchema):
    __model__ = GetFileSystemsRes
    result = fields.Nested(ResultSchema, data_key='Result')
    file_systems = fields.Nested(FileSystemSchema, data_key='FileSystems', many=True)

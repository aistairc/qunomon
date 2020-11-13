# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List
from marshmallow import fields

from . import Result, ResultSchema, BaseSchema


class DownloadableData:
    def __init__(self, id_: int, name: str, description: str, download_url: str) -> None:
        self.id_ = id_
        self.name = name
        self.description = description
        self.download_url = download_url


class DownloadableDataSchema(BaseSchema):
    __model__ = DownloadableData
    id_ = fields.Int(data_key='Id', required=True)
    name = fields.Str(data_key='Name', required=True)
    description = fields.Str(data_key='Description', required=True)
    download_url = fields.Str(data_key='DownloadURL', required=True)

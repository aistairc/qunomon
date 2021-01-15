# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List
from marshmallow import fields

from . import Result, ResultSchema, BaseSchema


class DownloadableTemplate:
    def __init__(self, id_: int, name: str, description: str) -> None:
        self.id_ = id_
        self.name = name
        self.description = description


class GetDownloadableTemplateRes:
    def __init__(self, result: Result, downloadable_data: List[DownloadableTemplate]) -> None:
        self.result = result
        self.downloadable_Data = downloadable_data


class DownloadableTemplateSchema(BaseSchema):
    __model__ = DownloadableTemplate
    id_ = fields.Int(data_key='Id', required=True)
    name = fields.Str(data_key='Name', required=True)
    description = fields.Str(data_key='Description', required=True)


class GetDownloadableTemplateResSchema(BaseSchema):
    __model__ = GetDownloadableTemplateRes
    result = fields.Nested(ResultSchema, data_key='Result')
    downloadable_data = fields.Nested(DownloadableTemplateSchema, data_key='Structure', many=True)

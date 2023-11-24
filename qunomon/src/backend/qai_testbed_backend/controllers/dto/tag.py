# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List, Optional
from marshmallow import fields, post_dump

from . import Result, ResultSchema, BaseSchema


class Tag:
    def __init__(self, id_: int, name: str) -> None:
        self.id_ = id_
        self.name = name


class GetTagsRes:
    def __init__(self, result: Result, tags: List[Tag]) -> None:
        self.result = result
        self.tags = tags


class TagSchema(BaseSchema):
    __model__ = Tag
    id_ = fields.Int(data_key='Id')
    name = fields.Str(data_key='Name')


class GetTagsResSchema(BaseSchema):
    __model__ = GetTagsRes
    result = fields.Nested(ResultSchema, data_key='Result')
    tags = fields.Nested(TagSchema, data_key='Tags', many=True)

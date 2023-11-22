# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List
from marshmallow import fields

from . import Result, ResultSchema, BaseSchema


class Guideline:
    def __init__(self, id_: int, aithub_guideline_id: int, name: str, description: str, creator: str, publisher: str, identifier: str,
                 publish_datetime: str, aithub_delete_flag: bool, creation_datetime: str, update_datetime: str) -> None:
        self.id_ = id_
        self.aithub_guideline_id = aithub_guideline_id
        self.name = name
        self.description = description
        self.creator = creator
        self.publisher = publisher
        self.identifier = identifier
        self.publish_datetime = publish_datetime
        self.aithub_delete_flag = aithub_delete_flag
        self.creation_datetime = creation_datetime
        self.update_datetime = update_datetime


class GetGuidelinesRes:
    def __init__(self, result: Result, guidelines: List[Guideline]) -> None:
        self.result = result
        self.guidelines = guidelines


class GuidelineSchema(BaseSchema):
    __model__ = Guideline
    id_ = fields.Int(data_key='Id')
    aithub_guideline_id = fields.Int(data_key='AithubGuidelineId')
    name = fields.Str(data_key='Name')
    description = fields.Str(data_key='Description')
    creator = fields.Str(data_key='Creator')
    publisher = fields.Str(data_key='Publisher')
    identifier = fields.Str(data_key='Identifier')
    publish_datetime = fields.Str(data_key='PublishDatetime')
    aithub_delete_flag = fields.Boolean(data_key='AIThubDeleteFlag')
    creation_datetime = fields.Str(data_key='CreationDatetime')
    update_datetime = fields.Str(data_key='UpdateDatetime')


class GetGuidelinesResSchema(BaseSchema):
    __model__ = GetGuidelinesRes
    result = fields.Nested(ResultSchema, data_key='Result')
    guidelines = fields.Nested(GuidelineSchema, data_key='Guidelines', many=True)


class DeleteGuidelineRes:
    def __init__(self, result: Result) -> None:
        self.result = result


class DeleteGuidelineResSchema(BaseSchema):
    __model__ = DeleteGuidelineRes
    result = fields.Nested(ResultSchema, data_key='Result')


class PutGuidelineReq:
    def __init__(self, description: str = None, creator: str = None, publisher: str = None, identifier: str = None,
                  publish_datetime: str = None, aithub_delete_flag: bool = False) -> None:
        self.description = description
        self.creator = creator
        self.publisher = publisher
        self.identifier = identifier
        self.publish_datetime = publish_datetime
        self.aithub_delete_flag = aithub_delete_flag


class PutGuidelineReqSchema(BaseSchema):
    __model__ = PutGuidelineReq
    description = fields.Str(data_key='Description', required=False)
    creator = fields.Str(data_key='Creator', required=False)
    publisher = fields.Str(data_key='Publisher', required=False)
    identifier = fields.Str(data_key='Identifier', required=False)
    publish_datetime = fields.Str(data_key='PublishDatetime', required=False)
    aithub_delete_flag = fields.Boolean(data_key='AIThubDeleteFlag', required=True)


class PutGuidelineRes:
    def __init__(self, result: Result) -> None:
        self.result = result


class PutGuidelineResSchema(BaseSchema):
    __model__ = PutGuidelineRes
    result = fields.Nested(ResultSchema, data_key='Result')


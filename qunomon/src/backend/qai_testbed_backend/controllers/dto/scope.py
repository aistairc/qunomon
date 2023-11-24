# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List
from marshmallow import fields

from . import Result, ResultSchema, BaseSchema


class Scope:
    def __init__(self, id_: int, aithub_scope_id: int, guideline_id: int, name: str, creation_datetime: str, update_datetime: str) -> None:
        self.id_ = id_
        self.aithub_scope_id = aithub_scope_id
        self.guideline_id = guideline_id
        self.name = name
        self.creation_datetime = creation_datetime
        self.update_datetime = update_datetime


class GetScopesRes:
    def __init__(self, result: Result, scopes: List[Scope]) -> None:
        self.result = result
        self.scopes = scopes


class ScopeSchema(BaseSchema):
    __model__ = Scope
    id_ = fields.Int(data_key='Id')
    aithub_scope_id = fields.Int(data_key='AithubScopeId')
    guideline_id = fields.Int(data_key='GuidelineId')
    name = fields.Str(data_key='Name')
    creation_datetime = fields.Str(data_key='CreationDatetime')
    update_datetime = fields.Str(data_key='UpdateDatetime')


class GetScopesResSchema(BaseSchema):
    __model__ = GetScopesRes
    result = fields.Nested(ResultSchema, data_key='Result')
    scopes = fields.Nested(ScopeSchema, data_key='Scopes', many=True)

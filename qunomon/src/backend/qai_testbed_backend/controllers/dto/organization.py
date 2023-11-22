# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List
from marshmallow import fields

from . import Result, ResultSchema, BaseSchema


class Organizer:
    def __init__(self, id_: int, organizer_id: str, name: str, creation_datetime: str, update_datetime: str, delete_flag: bool) -> None:
        self.id_ = id_
        self.organizer_id = organizer_id
        self.name = name
        self.creation_datetime = creation_datetime
        self.update_datetime = update_datetime
        self.delete_flag = delete_flag


class GetOrganizersRes:
    def __init__(self, result: Result, organizers: List[Organizer]) -> None:
        self.result = result
        self.organizers = organizers


class OrganizerSchema(BaseSchema):
    __model__ = Organizer
    id_ = fields.Int(data_key='Id')
    organizer_id = fields.Str(data_key='OrganizerId')
    name = fields.Str(data_key='Name')
    creation_datetime = fields.Str(data_key='CreationDatetime')
    update_datetime = fields.Str(data_key='UpdateDatetime')


class GetOrganizersResSchema(BaseSchema):
    __model__ = GetOrganizersRes
    result = fields.Nested(ResultSchema, data_key='Result')
    organizers = fields.Nested(OrganizerSchema, data_key='Organizers', many=True)

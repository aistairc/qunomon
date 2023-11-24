# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.

from marshmallow import Schema, fields, post_load


class BaseSchema(Schema):
    __model__ = None

    @post_load
    def to_dto(self, data, **_):
        return self.__model__(**data)

    class Meta:
        ordered = True


class Result:
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message


class ResultSchema(BaseSchema):
    __model__ = Result
    code = fields.Str(data_key='Code')
    message = fields.Str(data_key='Message')

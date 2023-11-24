# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from marshmallow import Schema, fields, post_load

from . import Result, ResultSchema


class PostNotifyCompleteRunRes:
    def __init__(self, result: Result) -> None:
        self.result = result


class PostNotifyCompleteRunResSchema(Schema):
    result = fields.Nested(ResultSchema, data_key='Result')

    class Meta:
        ordered = True

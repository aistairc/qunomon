# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import datetime
from marshmallow import Schema, fields, post_load

from . import Result, ResultSchema


class PostJobReq:
    def __init__(self, test_description_ids: []) -> None:
        self.test_description_ids = test_description_ids


class PostJobReqSchema(Schema):
    test_description_ids = fields.List(fields.Integer(), data_key='TestDescriptionIds', required=True, many=True)

    @post_load
    def to_dto(self, data, **_):
        return PostJobReq(**data)


class PostJobRes:
    def __init__(self, result: Result, job_id: int) -> None:
        self.result = result
        self.job_id = job_id


class PostJobResSchema(Schema):
    result = fields.Nested(ResultSchema, data_key='Result')
    job_id = fields.Int(data_key='JobId', required=True)

    class Meta:
        ordered = True

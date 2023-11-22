# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from marshmallow import fields
from . import BaseSchema


class GetHealtcheckRes:
    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message


class GetHealtcheckResSchema(BaseSchema):
    __model__ = GetHealtcheckRes
    code = fields.Integer(data_key='Code')
    message = fields.Str(data_key='Message')

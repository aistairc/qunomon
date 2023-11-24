# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
# !/usr/bin/env python3.6
# coding=utf-8
import bson
import re
from urllib.parse import urlparse


def is_a_valid_object_id(object_id):
    """Verify if the value is valid as an object id.
    :object_id: a string object
    :returns: True or False

    """
    return bson.objectid.ObjectId.is_valid(object_id)


def is_num(input_str: str):
    """入力文字列が数値ならTrue、非数値ならfalseを返す.
    :input_str: 入力文字列
    :returns: True or False
    """
    # 純粋な数値なら[-.0-9]の正規表現だけでOKだが、
    # 指数の+123e10などもOKにする
    p = re.compile('[-+.a-zA-Z0-9]+')
    # 上記の正規表現に合致するか判定（全角文字はFalseにする）
    if p.fullmatch(input_str):
        try:
            # floatで型変換できれば数値型
            float(input_str)
        except ValueError:
            return False
        else:
            return True
    else:
        return False

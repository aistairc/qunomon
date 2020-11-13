# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
# !/usr/bin/env python3.6
# coding=utf-8
import bson
from urllib.parse import urlparse


def is_a_valid_object_id(object_id):
    """Verify if the value is valid as an object id.
    :object_id: a string object
    :returns: True or False

    """
    return bson.objectid.ObjectId.is_valid(object_id)


def get_last_url_element(url_str: str) -> str:
    """ URLの最終要素を取得する
    url_str：
    https://airc.aist.go.jp/aiqm/quality/internal/学習モデルの正確性
    ↓
    戻り値
    学習モデルの正確性
    """
    url = urlparse(url_str)
    return url.path.split('/')[-1]

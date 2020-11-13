# Copyright c 2019 National Institute of Advanced Industrial Science and Technology �iAIST�j. All rights reserved.
# !/usr/bin/env python3.6
# coding=utf-8

from io import StringIO

from .exception import InvalidOperationException


def get_summary_text(model):
    """
    モデルのサマリ情報を出力します。

    Outputs the summary information of the model.

    Args:
        model :
            モデル

            model
    """

    # for keras 
    with StringIO() as buf:
        # StringIOに書き込む
        model.summary(print_fn=lambda x: buf.write(x + "\n"))
        # StringIOから取得
        text = buf.getvalue()


def convert_type(type_: str, value: str) -> object:
    """
    指定された方で値を変換します。

    Converts the value to the specified one.

    Args:
        type_ (str) :
            型を指定します。
            型は以下を許容します。

            Specify the type.
            The type allows for the following

            'int'
            'float'
            'bool'
            'string'
            'str'
            'list[int]'
            'list[float]'
            'list[bool]'
            'list[string]'
            'list[str]'

        value (str) :
            値を指定します。

            Specify the value.

    Returns:
        object
    """
    type_convert_dict = {
        'int': int,
        'float': float,
        'bool':  bool,
        'string': str,
        'str': str,
        'list[int]': int,
        'list[float]': float,
        'list[bool]':  bool,
        'list[string]': str,
        'list[str]': str
    }
    type_lower = type_.lower()
    if type_lower not in type_convert_dict:
        raise InvalidOperationException(f'type:{type_lower} is not defined')
    if type_lower.startswith('list['):
        return [type_convert_dict[type_lower](v) for v in value.split(',')]
    else:
        return type_convert_dict[type_lower](value)

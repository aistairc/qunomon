# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
# !/usr/bin/env python3.6
# coding=utf-8
from functools import wraps
from pathlib import Path
from os import makedirs

from ..utils.timer import Timer
from ..common.files.ait_output import AITOutput
from .ait_path_helper import AITPathHelper


def ait_main(ait_output: AITOutput, path_helper: AITPathHelper):
    """
    mainラッパー関数
    main関数の実行時間計測、およびait_outputの出力を実施する。

    main wrapper function
    Measure the execution time of the main function and output the ait_output.

    Args:
        ait_output (ait_sdl.common.files.ait_output.AITOutput)
        path_helper (ait_sdl.develop.ait_path_helper.AITPathHelper)

    Returns:
        _decoratorの返り値

        Return value of _decorator
    """

    def _decorator(func):
        """
        デコレーターを使用する関数を引数とする

        A function that takes a function with a decorator as an argument

        Args:
            func (function)

        Returns:
            wrapperの返り値

            Return value of wrapper
        """

        # funcのメタデータを引き継ぐ
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            実際の処理を書くための関数

            Functions for writing the actual process

            Args:
                *args:
                    funcの引数

                    func argument

                 **kwargs:
                    funcの引数

                    func argument

            Returns:
                funcの返り値

                Return value of func
            """

            timer = Timer()
            timer.start_timer()

            # funcの実行
            ret = func(*args, **kwargs)

            timer.stop_timer()
            ait_output.write_output(output_file_path=path_helper.get_output_file_path(),
                                    start_dt=timer.get_start_dt(),
                                    stop_dt=timer.get_stop_dt())

            return ret
        return wrapper
    return _decorator


def measures(ait_output: AITOutput, *names: str, is_many: bool = False):
    """
    measureを追加するためのラッパー関数

    A wrapper function for adding measure

    Args:
        ait_output (ait_sdl.common.files.ait_output.AITOutput)
        names (str)
        is_many (bool)

    Returns:
        _decoratorの返り値

        Return value of _decorator
    """

    def _decorator(func):
        """
        デコレーターを使用する関数を引数とする

        A function that takes a function with a decorator as an argument

        Args:
            func (function)

        Returns:
            wrapperの返り値

            Return value of wrapper
        """

        # funcのメタデータを引き継ぐ
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            実際の処理を書くための関数

            Functions for writing the actual process

            Args:
                *args:
                    funcの引数

                    func argument

                 **kwargs:
                    funcの引数

                    func argument

            Returns:
                funcの返り値

                Return value of func
            """

            # funcの実行
            ret = func(*args, **kwargs)

            # measure追加
            if type(ret) is not tuple:
                if not is_many:
                    ait_output.add_measure(name=names[0], value=str(ret))
                else:
                    ait_output.add_measure(name=names[0], value=','.join(map(str, ret)))
            else:
                for val, name in zip(ret, names):
                    if not is_many:
                        ait_output.add_measure(name=name, value=str(val))
                    else:
                        ait_output.add_measure(name=name, value=','.join(map(str, val)))

            return ret
        return wrapper
    return _decorator


def resources(ait_output: AITOutput, path_helper: AITPathHelper, item_name: str, file_name: str = None):
    """
    resourceを追加するためのラッパー関数

    デコレータで読み込んだfile_pathを設定するため、関数の引数にはかならずfile_pathを定義すること。
    ひとつのresourceに複数ファイルを設定する場合は、list型かtuple型でパスを返却すること。
    ファイルパスを返却した場合、そのファイルパスに上書きしてait.output.jsonへ出力する。

    Wrapper function for adding resources

    In order to set the file_path read by the decorator, the function must always define the file_path as an argument.
    When multiple files are set in one resource, the path must be returned as a list type or a tuple type.
    If the file path is returned, it will overwrite the file path and output it to ait.output.json.

    Args:
        ait_output (ait_sdl.common.files.ait_output.AITOutput)
        path_helper (ait_sdl.develop.ait_path_helper.AITPathHelper)
        item_name (str)
        file_name (str)

    Returns:
        _decoratorの返り値

        Return value of _decorator
    """

    def _decorator(func):
        """
        デコレーターを使用する関数を引数とする

        A function that takes a function with a decorator as an argument

        Args:
            func (function)

        Returns:
            wrapperの返り値

            Return value of wrapper
        """

        # funcのメタデータを引き継ぐ
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            実際の処理を書くための関数

            Functions for writing the actual process

            Args:
                *args:
                    funcの引数

                    func argument

                 **kwargs:
                    funcの引数

                    func argument

            Returns:
                funcの返り値

                Return value of func
            """

            dir_path = path_helper.get_output_resource_path(item_name)
            makedirs(dir_path, exist_ok=True)
            if file_name is None:
                out_path = dir_path
            else:
                out_path = str(Path(dir_path).joinpath(file_name))
            kwargs['file_path'] = out_path

            # funcの実行
            ret = func(*args, **kwargs)

            # resource追加
            if type(ret) is list or type(ret) is tuple:
                for val in ret:
                    ait_output.add_resource(name=item_name, path=val)
            elif type(ret) is str:
                ait_output.add_resource(name=item_name, path=ret)
            else:
                ait_output.add_resource(name=item_name, path=out_path)

            return ret
        return wrapper
    return _decorator


def downloads(ait_output: AITOutput, path_helper: AITPathHelper, item_name: str, file_name: str = None):
    """
    downloadを追加するためのラッパー関数

    デコレータで読み込んだfile_pathを設定するため、関数の引数にはかならずfile_pathを定義すること。
    ひとつのdownloadに複数ファイルを設定する場合は、list型かtuple型でパスを返却すること。

    Wrapper function for adding the download

    To set the file_path loaded by the decorator, the function must define the file_path as an argument.
    If you set multiple files in one download, you must return the path as a list type or a tuple type.

    Args:
        ait_output (ait_sdl.common.files.ait_output.AITOutput)
        path_helper (ait_sdl.develop.ait_path_helper.AITPathHelper)
        item_name (str)
        file_name (str)

    Returns:
        _decoratorの返り値

        Return value of _decorator
    """

    def _decorator(func):
        """
        デコレーターを使用する関数を引数とする

        A function that takes a function with a decorator as an argument

        Args:
            func (function)

        Returns:
            wrapperの返り値

            Return value of wrapper
        """

        # funcのメタデータを引き継ぐ
        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            実際の処理を書くための関数

            Functions for writing the actual process

            Args:
                *args:
                    funcの引数

                    func argument

                 **kwargs:
                    funcの引数

                    func argument

            Returns:
                funcの返り値

                Return value of func
            """

            dir_path = path_helper.get_output_download_path(item_name)
            makedirs(dir_path, exist_ok=True)
            if file_name is None:
                out_path = dir_path
            else:
                out_path = str(Path(dir_path).joinpath(file_name))
            kwargs['file_path'] = out_path

            # funcの実行
            ret = func(*args, **kwargs)

            # resource追加
            if type(ret) is list or type(ret) is tuple:
                for val in ret:
                    ait_output.add_downloads(name=item_name, path=val)
            elif type(ret) is str:
                ait_output.add_downloads(name=item_name, path=ret)
            else:
                ait_output.add_downloads(name=item_name, path=out_path)

            return ret
        return wrapper
    return _decorator

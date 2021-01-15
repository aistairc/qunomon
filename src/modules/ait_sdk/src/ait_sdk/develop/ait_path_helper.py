# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
# !/usr/bin/env python3.6
# coding=utf-8
from typing import List
from pathlib import Path

from ..common.files.ait_input import AITInput
from ..common.files.ait_manifest import AITManifest
from ..utils.exception import InvalidOperationException
from ..utils.logging import log, get_logger


logger = get_logger()


class AITPathHelper:
    """
    aitのパス補助クラスです。

    class for ait path help.
    """

    @log(logger)
    def __init__(self, argv: List[str], ait_input: AITInput, ait_manifest: AITManifest, entry_point_dir: str):
        """
        コンストラクタ

        Constructor

        Args:
            argv (List[str]) :
                プログラムの起動引数を指定します。

                Specifies the starting argument for the program.

            ait_input (AITInput) :
                ait_inputを指定します。

                Specify ait_input.

            ait_manifest (AITManifest) :
                ait_manifestを指定します。

                Specify the ait_manifest.

            entry_point_dir (str) :
                実行フォルダパスを指定します。

                Specify the path to the executable folder.

        """

        # check args
        if len(argv) != 2:
            raise InvalidOperationException('Invalid Argument.')

        self._args_dir = argv[1]
        self._ait_input = ait_input
        self._ait_manifest = ait_manifest
        self._entry_point_dir = entry_point_dir

    @log(logger)
    def get_manifest_file_path(self) -> str:
        """
        manifest_file_pathを取得します。

        Get manifest_file_path.

        Returns:
            manifest_file_path

        """
        return str(Path(self._entry_point_dir) / 'ait.manifest.json')

    @log(logger)
    def get_input_file_path(self) -> str:
        """
        input_file_pathを取得します。

        Get input_file_path.

        Returns:
            input_file_path

        """
        return str(Path(self._args_dir) / 'ait.input.json')

    @log(logger)
    def get_output_file_path(self) -> str:
        """
        output_file_pathを取得します。

        Get output_file_path.

        Returns:
            output_file_path

        """
        return str(self._get_result_dir_path() / 'ait.output.json')

    @log(logger)
    def _get_result_dir_path(self) -> Path:
        return self._ait_input.get_mount_dir_path() / 'ip' / 'job_result' / \
               str(self._ait_input.get_job_id()) / \
               str(self._ait_input.get_run_id())

    @log(logger)
    def get_output_resource_path(self, item_name: str) -> str:
        """
        output_resource_pathを取得します。

        Get output_resource_path.

        Args:
            item_name (str) :
                項目名を指定します。

                Specify the name of the item.

        Returns:
            output_resource_path

        """
        org_path = f'/usr/local/qai/resources/{item_name}/'
        return org_path.replace('/usr/local/qai', str(self._get_result_dir_path()))

    @log(logger)
    def get_output_download_path(self, item_name: str) -> str:
        """
        output_download_pathを取得します。

        Get output_download_path.

        Args:
            item_name (str) :
                項目名を指定します。

                Specify the name of the item.

        Returns:
            output_download_path

        """
        org_path = f'/usr/local/qai/downloads/{item_name}/'
        return org_path.replace('/usr/local/qai', str(self._get_result_dir_path()))

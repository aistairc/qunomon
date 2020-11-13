# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
# !/usr/bin/env python3.6
# coding=utf-8
from typing import Dict, Optional
import json
from pathlib import Path

from .ait_manifest import AITManifest
from ...utils.logging import log, get_logger
from ...utils import convert_type

logger = get_logger()


class AITInput:
    """
    AITの入力ファイル「ait.input.json」を管理するクラスです。

    This class manages the AIT input file "ait.input.json".
    """

    def __init__(self, ait_manifest: AITManifest):
        """
        コンストラクタ

        constructor

        Args:
            ait_manifest (AITManifest) :
                ait_manifestを指定します。

                Specify the ait_manifest.
        """
        self._ait_manifest = ait_manifest
        self._input_json = None

    @log(logger)
    def read_json(self, input_json_path: str) -> None:
        """
        ait.input.jsonを読み込みます。

        Load ait.input.json.

        Args:
            input_json_path (str) :
                jsonファイルパスを指定します。

                Specify the json file path.

        """
        # read input file
        with open(input_json_path, encoding='utf-8') as f:
            self._input_json = json.load(f)

    @log(logger)
    def get_mount_dir_path(self) -> Path:
        """
        mount_dir_pathを取得します。

        Get mount_dir_path.

        Returns:
            mount_dir_path
        """
        return Path(self._input_json['testbed_mount_volume_path'])

    @log(logger)
    def get_method_params(self) -> Dict[str, str]:
        """
        method_paramsを取得します。

        Get method_params.

        Returns:
            method_params
        """
        return self._input_json['MethodParams']

    @log(logger)
    def get_method_param_value(self, name: str) -> object:
        """
        method_param_valueを取得します。

        Get method_param_value.

        Args:
            name (str) :
                method_param_valueのnameを指定します。

                Specify the name of the method_param_value.

        Returns:
            method_param_value
        """
        value = self._find_value('MethodParams', name, is_raise_error=False)
        # 値がない場合、manifestのデフォルト値を設定
        if value is None:
            value = self._ait_manifest.get_ait_parameter_default_value(name)

        # manifestのタイプに変換して返却
        return convert_type(self._ait_manifest.get_ait_parameter_type(name), value)

    @log(logger)
    def get_inventories(self) -> Dict[str, str]:
        """
        inventoriesを取得します。

        Get inventories.

        Returns:
            inventories
        """
        return self._input_json['Inventories']

    @log(logger)
    def get_inventory_path(self, name: str) -> str:
        """
        inventory_pathを取得します。

        Get inventory_path.

        Args:
            name (str) :
                inventoryのnameを指定します。

                Specify the name of the inventory.

        Returns:
            inventory_path
        """
        return self._find_value('Inventories', name)

    @log(logger)
    def get_run_id(self) -> int:
        """
        run_idを取得します。

        Get run_id.

        Returns:
            run_id
        """
        return self._input_json['run_id']

    @log(logger)
    def get_job_id(self) -> int:
        """
        job_idを取得します。

        Get job_id.

        Returns:
            job_id
        """
        return self._input_json['job_id']

    @log(logger)
    def _find_value(self, section_name: str, name: str, is_raise_error: bool = True) -> Optional[str]:
        values = [i['Value'] for i in self._input_json[section_name] if i['Name'] == name]
        if len(values) == 0:
            if is_raise_error:
                raise KeyError(f'{section_name}/{name} is not found.')
            else:
                return None
        return values[0]

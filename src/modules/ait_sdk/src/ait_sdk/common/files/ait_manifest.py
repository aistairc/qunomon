# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
# !/usr/bin/env python3.6
# coding=utf-8
from typing import List, Dict, Optional
import json

from ...utils.logging import log, get_logger


logger = get_logger()


class AITManifest:
    """
    AITを定義するファイル「ait.manifest.json」を管理するクラスです。

    This class manages the file "ait.manifest.json", which defines AIT.

    """

    def __init__(self):
        """
        コンストラクタ

        constructor
        """
        self._manifest_json = None

    @log(logger)
    def read_json(self, manifest_json_path: str) -> None:
        """
        ait.manifest.jsonを読み込みます。

        Load ait.manifest.json.

        Args:
            manifest_json_path (str) :
                jsonファイルパスを指定します。

                Specify the json file path.

        """
        # read manifest file
        with open(manifest_json_path, encoding='utf-8') as f:
            self._manifest_json = json.load(f)

    @log(logger)
    def get_ait_measures(self) -> List[Dict[str, str]]:
        """
        measuresを取得します。

        Get measures.

        Returns:
            measures
        """
        return self._manifest_json['report']['measures']

    @log(logger)
    def get_ait_resources(self) -> List[Dict[str, str]]:
        """
        resourcesを取得します。

        Get resources.

        Returns:
            resources
        """
        return self._manifest_json['report']['resources']

    @log(logger)
    def get_ait_downloads(self) -> List[Dict[str, str]]:
        """
        downloadsを取得します。

        Get downloads.

        Returns:
            downloads
        """
        return self._manifest_json['downloads']

    @log(logger)
    def get_name(self) -> str:
        """
        nameを取得します。

        Get name.

        Returns:
            name
        """
        return self._manifest_json['name']

    @log(logger)
    def get_version(self) -> str:
        """
        versionを取得します。

        Get version.

        Returns:
            version
        """
        return self._manifest_json['version']

    @log(logger)
    def get_ait_resource_path(self, name: str) -> str:
        """
        resource_pathを取得します。

        Get resource_path.

        Args:
            name (str) :
                resourceのnameを指定します。

                Specify the name of the resource.

        Returns:
            resource_path
        """
        return self._find_path(section=self._manifest_json['report']['resources'],
                               value_key='path',
                               name=name)
        
    @log(logger)
    def get_ait_download_path(self, name: str, is_raise_key_error: bool = True) -> str:
        """
        download_pathを取得します。

        Get download_path.

        Args:
            name (str) :
                downloadのnameを指定します。

                Specify the name of the download.

            is_raise_key_error (bool) :
                downloadのnameが存在しない場合にkey_errorを発生させるかどうかを指定します。

                Specifies whether key_error is raised if the download name does not exist.

        Returns:
            download_path
        """
        return self._find_path(section=self._manifest_json['downloads'],
                               value_key='path',
                               name=name,
                               is_raise_key_error=is_raise_key_error)

    @log(logger)
    def get_ait_parameter_default_value(self, name: str, is_raise_key_error: bool = True) -> str:
        """
        parameter_default_valueを取得します。

        Get parameter_default_value.

        Args:
            name (str) :
                parameterのnameを指定します。

                Specify the name of the parameter.

            is_raise_key_error (bool) :
                parameterのnameが存在しない場合にkey_errorを発生させるかどうかを指定します。

                Specifies whether key_error is raised if the parameter name does not exist.

        Returns:
            parameter_default_value
        """
        return self._find_path(section=self._manifest_json['parameters'],
                               value_key='default_val',
                               name=name,
                               is_raise_key_error=is_raise_key_error)

    @log(logger)
    def get_ait_parameter_type(self, name: str) -> str:
        """
        parameter_typeを取得します。

        Get parameter_type.

        Args:
            name (str) :
                parameterのnameを指定します。

                Specify the name of the parameter.

        Returns:
            parameter_type
        """
        return self._find_path(section=self._manifest_json['parameters'],
                               value_key='type',
                               name=name)

    @log(logger)
    def _find_path(self, section: List[Dict[str, str]], value_key: str, name: str,
                   is_raise_key_error: bool = True) -> Optional[str]:
        paths = [i[value_key] for i in section if i['name'] == name]
        if len(paths) == 0:
            if is_raise_key_error:
                raise KeyError(f'{name} is not found.')
            else:
                return None
        return paths[0]

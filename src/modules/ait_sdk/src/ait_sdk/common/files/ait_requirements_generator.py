# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
# !/usr/bin/env python3.6
# coding=utf-8

import shutil
import os
from pathlib import Path

from ...utils.logging import log, get_logger


logger = get_logger()


class AITRequirementsGenerator:
    """
    requirements.txtを出力するためのクラス。

    Class for outputting requirements.txt.
    """
    def __init__(self):
        """
        コンストラクタ

        constructor
        """
        self._req_name = 'requirements.txt'
        self._package_list = []

    @log(logger)
    def add_package(self, package_name: str, package_ver: str = '') -> None:
        """
        パッケージ情報のリストを作成する。

        Create a list of package information.

        Args:
            package_name (str) :
                インストールするパッケージ名

                Package name to be installed

            package_ver (str) :
                インストールするパッケージのバージョン（任意）

                Version of the package to be installed (optional)

        """
        if (package_ver is not None) and (len(package_ver) > 0):
            # バージョン情報あり
            self._package_list.append(package_name + '==' + package_ver)
        else:
            # バージョン情報なし
            self._package_list.append(package_name)

    @log(logger)
    def create_requirements(self, base_dir: str) -> str:
        """
        pip install パッケージ情報のリストをrequirementsファイルに出力する。

        pip install Output the list of package information to the requirements file.

        Args:
            base_dir (str) :
                requirements.txtの保存ディレクトリ

                Requirements.txt storage directory

        Returns:
            requirementsファイル保存先フルパス

            full path to the requirements file
        """
        base_path = Path(base_dir)

        # requirements.txt作成
        requirements_txt_path = str(base_path/self._req_name)
        with open(requirements_txt_path, 'w', encoding='utf-8') as f:
            for p_name in self._package_list:
                f.write(p_name + '\n')

        return requirements_txt_path

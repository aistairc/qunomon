# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
# !/usr/bin/env python3.6
# coding=utf-8
from . import license_setting


class LicenseGenerator:
    """
    LICENSE.txtを出力するためのクラス。

    Class for outputting LICENSE.txt.
    """
    def __init__(self):
        """
        コンストラクタ

        constructor
        """

    def write(self, licence_path: str, year: str, owner: str) -> None:
        """
        LICENSE.txtを出力する。

        Output LICENSE.txt.

        Args:
            licence_path (str) :
                ライセンスファイルのパス

                License file path

            year (str) :
                著作物発行年。

                Year of Publication.

            owner (str) :
                著作権者名。

                Copyright Holder Name.

        Returns:
            無し
        """
        with open(licence_path, 'w', encoding='utf-8') as f:
            f.write(license_setting.license_template.format(year, owner))

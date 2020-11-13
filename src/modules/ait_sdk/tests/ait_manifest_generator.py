# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
# !/usr/bin/env python3.6
# coding=utf-8


import unittest
from src.ait_sdk.common.files.ait_manifest_generator import AITManifestGenerator


class TestAITManifestGenerator(unittest.TestCase):

    def test_write_output(self):
        print('++ テスト開始')
        aaa = AITManifestGenerator('./')
        aaa.set_ait_name("set_ait_name")
        aaa.set_ait_description("set_ait_description")
        aaa.set_ait_author("set_ait_author")
        aaa.set_ait_email("set_ait_email")
        aaa.set_ait_version("0.1")
        aaa.set_ait_quality("set_ait_quality")
        aaa.set_ait_reference("set_ait_reference")
        aaa.add_ait_inventories('name1', 'type1', 'description1', ['csv'], 'schema1')
        aaa.add_ait_inventories('name2', 'type2', 'description2', ['gz', 'zip'], 'schema')
        aaa.add_ait_parameters('name1', 'type1', 'description1', 'default_val1')
        aaa.add_ait_parameters('name2', 'type2', 'description2')
        aaa.add_ait_measures('name1', 'type1', 'description1', 'structure1')
        aaa.add_ait_measures('name2', 'type2', 'description2', 'structure2')
        aaa.add_ait_resources('name1', 'path1', 'type1', 'description1')
        aaa.add_ait_resources('name2', 'path2', 'type2', 'description2')
        aaa.add_ait_downloads('name1', 'path1', 'description1')
        aaa.add_ait_downloads('name2', 'path2', 'description2')
        aaa.write()
        print('++ テスト終了')


if __name__ == "__main__":
    unittest.main()

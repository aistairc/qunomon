# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
# !/usr/bin/env python3.6
# coding=utf-8


import unittest
from ait_sdk.common.files.ait_input_generator import AITInputGenerator
from ait_sdk.common.files.ait_manifest_generator import AITManifestGenerator


class TestAITInputGenerator(unittest.TestCase):

    def test_write(self):
        print('++ テスト準備')
        # あらかじめait.manifest.jsonを生成
        aaa = AITManifestGenerator('./')
        aaa.set_ait_name("set_ait_name")
        aaa.set_ait_description("set_ait_description")
        aaa.set_ait_author("set_ait_author")
        aaa.set_ait_email("set_ait_email")
        aaa.set_ait_version("0.1")
        aaa.set_ait_quality("set_ait_quality")
        aaa.set_ait_reference("set_ait_reference")
        aaa.add_ait_inventories('image_data', 'type1', 'description1', ['csv'], 'schema1')
        aaa.add_ait_inventories('model_data', 'type2', 'description2', ['gz', 'zip'], 'schema')
        aaa.add_ait_parameters('name1', 'type1', 'description1', 'default_val1')
        aaa.add_ait_parameters('name2', 'type2', 'description2')
        aaa.add_ait_measures('name1', 'type1', 'description1', 'structure1')
        aaa.add_ait_measures('name2', 'type2', 'description2', 'structure2')
        aaa.add_ait_resources('name1', 'type1', 'description1')
        aaa.add_ait_resources('name2', 'type2', 'description2')
        aaa.add_ait_downloads('name1', 'description1')
        aaa.add_ait_downloads('name2', 'description2')
        manifest_path = aaa.write()

        print('++ テスト開始')
        bbb = AITInputGenerator(manifest_path)
        bbb.add_ait_inventories('image_data', 'image/001.jpg')
        bbb.add_ait_inventories('model_data', 'model/test.h5')
        bbb.set_ait_params('name2', '123')
        bbb.write()
        print('++ テスト終了')


if __name__ == "__main__":
    unittest.main()

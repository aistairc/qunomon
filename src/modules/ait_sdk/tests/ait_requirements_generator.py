# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
# !/usr/bin/env python3.6
# coding=utf-8

import unittest
from ait_sdk.common.files.ait_requirements_generator import AITRequirementsGenerator


class TestAITRequirementsGenerator(unittest.TestCase):

    def test_create_requirements(self):
        print('++ テスト開始')
        aaa = AITRequirementsGenerator()
        aaa.add_package("aaa","1.11.111")
        aaa.add_package("bbb",'2.22.222')
        aaa.add_package("ccc",'3.33.333')
        aaa.add_package("ddd")
        aaa.add_package("eee")
        # あらかじめ"F:/test/develop"と"F:/test/deploy/container/repository"を作成しておく
        aaa.create_requirements("F:/test/develop")
        print('++ テスト終了')

if __name__ == "__main__":
    unittest.main()

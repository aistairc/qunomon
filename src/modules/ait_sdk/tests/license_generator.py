# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
# !/usr/bin/env python3.6
# coding=utf-8
import unittest
from ait_sdk.license.license_generator import LicenseGenerator

class TestLicenseGenerator(unittest.TestCase):

    def test_write(self):
        print('++ テスト開始')
        aaa = LicenseGenerator()
        aaa.write('LICENSE.txt', '2020', 'test')
        print('++ テスト終了')

if __name__ == "__main__":
    unittest.main()
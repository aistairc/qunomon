# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
# !/usr/bin/env python3.6
# coding=utf-8

import unittest

from ait_sdk.utils.logging import get_logger, log
from ait_sdk.develop.ait_base import AITBase

logger = get_logger()


@log(logger)
def log_test():
    print('test')


class TestAITBase(unittest.TestCase):

    def test_execute_invalid_param(self):
        ait_base = AITBase()
        try:
            ait_base.execute(['dummy', 'invalid_path'], __file__)
            self.fail()
        except Exception as e:
            self.assertIsNotNone(e)

    def test_log_func(self):
        log_test()


if __name__ == "__main__":
    unittest.main()

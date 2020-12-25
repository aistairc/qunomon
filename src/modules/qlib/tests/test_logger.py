# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
# !/usr/bin/env python3.6
# coding=utf-8

import unittest

from src.qlib.utils.logging import get_logger, log

logger = get_logger()


@log(logger)
def log_test():
    print('test')


class TestAITInputGenerator(unittest.TestCase):

    def test_log_func(self):
        log_test()


if __name__ == "__main__":
    unittest.main()

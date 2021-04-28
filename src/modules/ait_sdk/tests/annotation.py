# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
# !/usr/bin/env python3.6
# coding=utf-8

import unittest
from pathlib import Path
import shutil

from ait_sdk.utils.logging import get_logger
from ait_sdk.develop.annotation import ait_main
from ait_sdk.common.files.ait_input import AITInput
from ait_sdk.common.files.ait_output import AITOutput
from ait_sdk.common.files.ait_manifest import AITManifest
from ait_sdk.develop.ait_path_helper import AITPathHelper
from ait_sdk.utils.exception import InvalidOperationException

logger = get_logger()

ait_manifest = AITManifest()
ait_input = AITInput(ait_manifest)
ait_output = AITOutput(ait_manifest)
test_dir = str(Path(__file__).parent / 'annotation_test_data')
path_helper = AITPathHelper(argv=['', test_dir], ait_input=ait_input, ait_manifest=ait_manifest,
                            entry_point_dir=test_dir)
ait_input.read_json(path_helper.get_input_file_path())
ait_manifest.read_json(path_helper.get_manifest_file_path())
path_helper._get_result_dir_path().mkdir(parents=True, exist_ok=True)


class TestAITMain(unittest.TestCase):

    def setUp(self):
        self._func_name = None

    def tearDown(self):
        src_path = path_helper._get_result_dir_path() / 'ait.output.json'
        dst_path = path_helper._get_result_dir_path() / f'ait.output_{self._func_name}.json'
        shutil.move(str(src_path), str(dst_path))

    @ait_main(ait_output=ait_output, path_helper=path_helper)
    def test_value_error(self):
        self._func_name = 'test_value_error'
        raise ValueError('test_value_error')

    @ait_main(ait_output=ait_output, path_helper=path_helper)
    def test_invalid_operation_exception(self):
        self._func_name = 'test_invalid_operation_exception'
        raise InvalidOperationException('test_invalid_operation_exception')

    @ait_main(ait_output=ait_output, path_helper=path_helper)
    def test_memory_error(self):
        self._func_name = 'test_memory_error'
        raise MemoryError('test_memory_error')

    @ait_main(ait_output=ait_output, path_helper=path_helper)
    def test_divide_zero(self):
        self._func_name = 'test_divide_zero'
        a = 1 / 0


if __name__ == "__main__":
    unittest.main()

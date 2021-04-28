# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
# !/usr/bin/env python3.6
# coding=utf-8
from typing import List
import shutil
from pathlib import Path
import traceback

from ..common.files.ait_input import AITInput
from ..common.files.ait_manifest import AITManifest
from ..common.files.ait_output import AITOutput
from .ait_path_helper import AITPathHelper
from ..utils.timer import Timer
from ..utils.logging import get_logger, log, get_log_path


logger = get_logger()


class AITBase:

    @log(logger)
    def __init__(self):
        self._ait_manifest = AITManifest()
        self._ait_input = AITInput(self._ait_manifest)
        self._ait_output = AITOutput(self._ait_manifest)
        self._timer = Timer()
        self._path_helper = None

    @log(logger)
    def execute(self, argv: List[str], entry_point_dir: str) -> None:
        try:
            self._path_helper = AITPathHelper(argv, self._ait_input, self._ait_manifest, entry_point_dir)
            self._timer.start_timer()

            self.pre_process()
            self.main_process()
            self.post_process()

        except Exception as e:
            logger.error(f'Exception: {e}')
            try:
                self._timer.stop_timer()
                self._ait_output.write_output(output_file_path=self._path_helper.get_output_file_path(),
                                              start_dt=self._timer.get_start_dt(),
                                              stop_dt=self._timer.get_stop_dt(),
                                              ex=e,
                                              error_detail=traceback.format_exc())
            except Exception as e2:
                logger.error(f'Failed write ait.output.json. exception={e2}')
            raise e
        finally:
            self.clean_up()

    @log(logger)
    def pre_process(self) -> None:
        self._ait_input.read_json(self._path_helper.get_input_file_path())
        self._ait_manifest.read_json(self._path_helper.get_manifest_file_path())
        logger.info('AIT({}_{}) START.'.format(self._ait_manifest.get_name(), self._ait_manifest.get_version()))

    @log(logger)
    def main_process(self) -> None:
        pass

    @log(logger)
    def post_process(self) -> None:
        
        self._timer.stop_timer()

        Path(self._path_helper.get_output_file_path()).parent.mkdir(parents=True, exist_ok=True)

        # write output json
        self._ait_output.write_output(output_file_path=self._path_helper.get_output_file_path(),
                                      start_dt=self._timer.get_start_dt(),
                                      stop_dt=self._timer.get_stop_dt())

    def clean_up(self) -> None:
        """
        最終処理を実装する。
        ログファイルのコピー処理などの後始末をするため、logデコレーションしない。
        """
        pass

    @staticmethod
    def _move_log_file(dst_path: str) -> None:
        Path(dst_path).parent.mkdir(parents=True, exist_ok=True)
        shutil.move(get_log_path(), dst_path)

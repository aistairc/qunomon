# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
#!/usr/bin/env python3.6
# coding=utf-8

from pathlib import Path
import shutil

### ↓標準使用モジュール↓
from ait_sdk.develop.ait_base import AITBase
from ait_sdk.utils.logging import get_logger, log, get_log_path
### ↑標準使用モジュール↑


logger = get_logger()

class MyAIT(AITBase):
    
    @log(logger)
    def pre_process(self) -> None:
        """
        実装が必要な関数その1：前処理
        super().pre_process()実施後に独自処理を記載する。
        
        データ読み込みや加工などの前処理を記載する。
        """
        super().pre_process()


    @log(logger)
    def main_process(self) -> None:
        """
        実装が必要な関数その2：本処理
        super().main_process()実施後に独自処理を記載する。
        
        推論やその結果取得処理を記載する。
        """
        super().main_process()
        self._ait_output.add_measure(name='学習モデルの敵対的サンプル安定性計測2', value=str(0.99))

        item_name='acc.csv'
        file_path = self._path_helper.get_output_resource_path(item_name)
        self._copy_dummy_file(item_name, file_path)
        self._ait_output.add_resource(name=item_name, path=file_path)

        item_name='acc.png'
        file_path = self._path_helper.get_output_resource_path(item_name)
        self._copy_dummy_file(item_name, file_path)
        self._ait_output.add_resource(name=item_name, path=file_path)
        
        item_name='images.png'
        file_path = self._path_helper.get_output_resource_path(item_name)
        self._copy_dummy_file(item_name, file_path)
        self._ait_output.add_resource(name=item_name, path=file_path)
        
        item_name='Incorrect_data.csv'
        file_path = self._path_helper.get_output_resource_path(item_name)
        self._copy_dummy_file(item_name, file_path)
        self._ait_output.add_resource(name=item_name, path=file_path)
        
        item_name='log.txt'
        file_path = self._path_helper.get_output_download_path(item_name)
        self._copy_dummy_file(item_name, file_path)
        self._ait_output.add_downloads(name=item_name, path=file_path)
        
        item_name='adversarial_samples'
        item_file_name='adversarial_samples.zip'
        file_path = self._path_helper.get_output_download_path(item_name)
        self._copy_dummy_file(item_file_name, file_path)
        self._ait_output.add_downloads(name=item_name, path=file_path)

    def _copy_dummy_file(self, item_name: str, file_path: str):
        src_file = Path(__file__).parent / 'dummy_result_data' / item_name
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(str(src_file), file_path)

    @log(logger)
    def post_process(self) -> None:
        """
        実装が必要な関数その3：後処理
        super().post_process()実施後に独自処理を記載する。
        
        後始末の処理を記載する。
        """
        super().post_process()

    def clean_up(self) -> None:
        """
        最終処理を実装する。
        super().post_process()実施前に独自処理を記載する。
        ログファイルのコピー処理などの後始末をするため、logデコレーションしない。
        """
        super().clean_up()

# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.

import docker
import docker.errors
import os
from pathlib import Path
import datetime
import json

from ..entities.setting import SettingMapper
from ..entities.file_system import FileSystemMapper
from qlib.utils.logging import get_logger, log


logger = get_logger()


class FileChecker:

    IMAGE_NAME = 'file_checker:0.1'

    def __init__(self):
        # インベントリチェック結果格納フォルダの設定
        if os.name == 'nt':
            self._root_dir_path = Path(SettingMapper.query.get('mount_src_path').value) / 'inventory_check'
        else:
            self._root_dir_path = Path(SettingMapper.query.get('mount_dst_path').value) / 'inventory_check'

        # dockerクライアントの設定
        if os.name == 'nt':
            self._client = docker.from_env()
        else:  # コンテナ起動の場合ソケット指定
            self._client = docker.DockerClient(base_url='unix://var/run/docker.sock')

        # イメージがなければビルド
        self._build_image_if_need()

    def execute(self, file_path: str, file_system_id: int) -> {}:

        # チェック対象のファイルパスをフォルダパスとファイル名に分割
        file_system_mapper = FileSystemMapper.query.get(file_system_id)
        if file_system_mapper.name == 'UNIX_FILE_SYSTEM':
            splits = file_path.rsplit('/', 1)
            if len(splits) == 1:
                splits.insert(0, '/')
        else:
            splits = file_path.rsplit('\\', 1)
            splits[0] += '\\'
        input_dir = splits[0]
        input_file_name = splits[1]

        current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')

        # マウントボリューム構築
        volumes = {
            input_dir:
                {'bind': '/usr/local/qai/input', 'mode': 'rw'},
            SettingMapper.query.get('mount_src_path').value:
                {'bind': '/usr/local/qai/output', 'mode': 'rw'}
        }

        logger.debug(volumes)
        logger.debug(f'input_file_name={input_file_name} current_datetime={current_datetime}')

        self._client.containers.run(self.IMAGE_NAME, [input_file_name, current_datetime], volumes=volumes, remove=True)

        # 結果読み込み
        result_file = str(self._root_dir_path / current_datetime / 'result.json')
        with open(result_file) as f:
            result = json.load(f)

        logger.debug(result)

        return result

    def _build_image_if_need(self):
        try:
            _ = self._client.images.get(self.IMAGE_NAME)
        except docker.errors.ImageNotFound:
            # imageがない場合、build
            self._client.images.build(path='./file_checker', nocache=True, rm=False, forcerm=True,
                                      tag=self.IMAGE_NAME)

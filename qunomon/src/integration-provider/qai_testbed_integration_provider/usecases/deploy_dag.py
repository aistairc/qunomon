# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from pathlib import Path
from injector import singleton
import json
from datetime import datetime
import os
import shutil
import werkzeug
from zipfile import ZipFile
import docker
from docker.errors import ImageNotFound
from glob import glob
import asyncio
from threading import Lock, Thread
from qlib.utils.logging import get_logger, log

from ..across.exception import QAIInvalidRequestException, QAIInternalServerException
from ..controllers.dto import Result
from ..entities.setting import SettingMapper


logger = get_logger()


@singleton
class DeployDAGService:

    def __init__(self):
        # dagのルートフォルダ いずれなんかのリポジトリに移動？
        self.root_dag_dir_path = Path(__file__).parent.joinpath('../../../dag')
        if not (os.environ.get('IP_ROOT_DAG_DIR_PATH') is None):
            self.root_dag_dir_path = Path(os.environ.get('IP_ROOT_DAG_DIR_PATH'))

        # dagの一時フォルダ
        self.work_dag_dir_path = self.root_dag_dir_path.joinpath('deploy_work')
        self._clean_create_dir(self.work_dag_dir_path)

        # docker container リポジトリURL
        self.docker_repository_url = SettingMapper.query.get('docker_repository_url').value

        # 非同期ロックオブジェクト
        self._async_deploy_dag_lock = Lock()

        # 非同期実行エラー結果
        self._async_deploy_dag_err = None

    @staticmethod
    def _clean_create_dir(dir_path: Path):
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
        else:
            shutil.rmtree(str(dir_path))
            dir_path.mkdir(parents=True)

    def get_async(self) -> Result:
        if self._async_deploy_dag_lock.locked():
            return Result(code='D00011', message='Deploy running.')

        if self._async_deploy_dag_err is None:
            return Result(code='D00010', message='Deploy not running.')
        else:
            # エラー発生時はその結果を返却する
            res = self._async_deploy_dag_err
            self._async_deploy_dag_err = None
            return res

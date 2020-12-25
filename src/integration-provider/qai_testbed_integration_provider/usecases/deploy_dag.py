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

    @log(logger)
    def post(self, request, is_async_build=False, is_build=True) -> Result:

        if is_async_build and not self._async_deploy_dag_lock.acquire(blocking=False):
            return Result(code='D00001', message='Deploy already running.')

        self._deploy_dag(request, is_async_build, is_build)

        return Result(code='D00001', message='Deploy success')

    def _deploy_dag(self, request, is_async_build, is_build):
        """
        同期非同期をis_async_buildで切り分ける。
        スレッドのコンテキストが分かれると、requestが扱えなくなるため、
        requestをつかうzip保存は非同期処理前に実施する。
        """

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_dir_path = self.work_dag_dir_path.joinpath(timestamp)
            self._clean_create_dir(save_dir_path)

            # ZIP配置
            zip_path = self._save_zip(request, save_dir_path)

            if not is_async_build:
                self._deploy_dag_core(is_async_build, save_dir_path, zip_path, is_build)
            else:
                self._async_deploy_dag_err = None
                loop = asyncio.new_event_loop()
                p = Thread(target=self._thread_worker, args=(is_async_build, save_dir_path, zip_path, is_build, loop,))
                p.start()
        except Exception:
            if is_async_build:
                self._async_deploy_dag_lock.release()
            raise

    def _deploy_dag_core(self, is_async_build, save_dir_path, zip_path, is_build):
        unzip_dir_path = None
        try:
            # ZIP解凍
            unzip_dir_path = self._unzip(zip_path)

            # dag存在チェック
            dag_file = unzip_dir_path / 'dag.py'
            if not dag_file.exists():
                raise QAIInvalidRequestException(result_code='D11001',
                                                 result_msg='not found dag.py in zip.')
            # ait.manifest.json検索
            manifest_files = self._find_files(unzip_dir_path, 'ait.manifest.json')

            # ait.manifest.jsonオープン
            manifest_file = Path(manifest_files[0])
            if not manifest_file.exists():
                raise QAIInvalidRequestException(result_code='D11001',
                                                 result_msg='not found ait.manifest.json in zip.')
            with open(str(manifest_file), encoding='utf-8') as f:
                manifest_json = json.load(f)

            # ait.manifest.jsonからnameとversion取得
            if 'name' not in manifest_json or len(manifest_json['name']) == 0:
                raise QAIInvalidRequestException(result_code='D11003',
                                                 result_msg='not found name in ait.manifest.json.')
            if 'version' not in manifest_json or len(manifest_json['version']) == 0:
                raise QAIInvalidRequestException(result_code='D11003',
                                                 result_msg='not found version in ait.manifest.json.')
            docker_image_name = manifest_json['name']
            docker_image_version = manifest_json['version']

            if is_build:
                # dockerfile検索
                docker_files = self._find_files(unzip_dir_path, 'dockerfile')

                # docker build
                self._build_docker(Path(docker_files[0]).parent, docker_image_name, docker_image_version)
        except Exception as e:
            # 失敗した場合はunzip_dir_path削除
            if unzip_dir_path is not None:
                shutil.rmtree(str(unzip_dir_path))
            if not is_async_build:
                raise e
            else:
                self._async_deploy_dag_err = Result(code='D99999', message=str(e))
        finally:
            # work削除
            shutil.rmtree(str(save_dir_path))
            if is_async_build:
                self._async_deploy_dag_lock.release()

    @staticmethod
    def _find_files(unzip_dir_path: Path, file_name: str):
        files = glob(str(unzip_dir_path.joinpath(f'**/{file_name}')), recursive=True)
        if len(files) == 0:
            raise QAIInvalidRequestException(result_code='D11002', result_msg=f'not found {file_name} in zip.')
        elif len(files) > 1:
            raise QAIInvalidRequestException(result_code='D10002',
                                             result_msg=f'{file_name} must be one exists in zip.')
        return files

    def _save_zip(self, request, save_dir_path: Path) -> Path:

        if 'dag_zip' not in request.files:
            raise QAIInvalidRequestException(result_code='D10001', result_msg='uploadFile is required.')

        file = request.files['dag_zip']
        filename = file.filename
        if '' == filename:
            raise QAIInvalidRequestException(result_code='D10001', result_msg='filename must not empty.')

        if not filename.endswith('.zip'):
            raise QAIInvalidRequestException(result_code='D10001', result_msg='file extension must be zip.')

        save_filename = werkzeug.utils.secure_filename(filename)
        save_path = save_dir_path.joinpath(save_filename)
        file.save(str(save_path))

        return save_path

    def _unzip(self, zip_path: Path) -> Path:
        unzip_dir_path = self.root_dag_dir_path.joinpath(zip_path.stem)
        if unzip_dir_path.exists():
            shutil.rmtree(str(unzip_dir_path))

        with ZipFile(zip_path) as existing_zip:
            existing_zip.extractall(self.root_dag_dir_path)

        return unzip_dir_path

    def _build_docker(self, docker_dir: Path, docker_image_name: str, docker_image_version: str):

        # imageとversionをmanifestから取得
        docker_image_id = docker_image_name + ':' + docker_image_version
        docker_remote_image_name = self.docker_repository_url + '/' + docker_image_id

        if os.name == 'nt':
            client = docker.from_env()
        else:  # コンテナ起動の場合ソケット指定
            client = docker.DockerClient(base_url='unix://var/run/docker.sock')

        # 応答確認
        if client.ping() is False:
            raise QAIInternalServerException(result_code='D19999', result_msg='docker service is not available.')

        # clean
        client.images.prune()
        client.images.prune_builds()
        try:
            client.images.remove(docker_image_id, force=True)
        except ImageNotFound:
            pass  # imageが見つからない場合は正常処理として継続
        try:
            client.images.remove(docker_remote_image_name, force=True)
        except ImageNotFound:
            pass  # imageが見つからない場合は正常処理として継続

        # build
        client.images.build(path=str(docker_dir.absolute()), nocache=True, rm=True, forcerm=True,
                            tag=docker_remote_image_name)

        # push
        client.images.push(repository=docker_remote_image_name)

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

    def _thread_worker(self, is_async_build, save_dir_path, zip_path, is_build, loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._deploy_dag_core(is_async_build, save_dir_path, zip_path, is_build))

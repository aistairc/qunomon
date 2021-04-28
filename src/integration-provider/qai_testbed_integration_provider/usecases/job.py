# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import concurrent.futures
from pathlib import Path
import shutil
from injector import singleton
import requests
import json
from time import sleep
import urllib.parse
import socket
import datetime
import os
import glob
from qlib.utils.logging import get_logger, log
import docker
from docker.errors import ImageNotFound

from ..across.exception import QAIException, QAINotFoundException, QAIInternalServerException,\
    QAIInvalidRequestException
from ..controllers.dto import Result
from ..controllers.dto.job import PostJobReq, PostJobRes
from ..entities.ml_component import MLComponentMapper
from ..entities.test import TestMapper
from ..entities.test_description import TestDescriptionMapper
from ..entities.job import JobMapper
from ..entities.run import RunMapper
from ..entities.setting import SettingMapper
from ..gateways.extensions import sql_db
from sqlalchemy.exc import SQLAlchemyError


logger = get_logger()


@singleton
class JobService:

    def __init__(self):
        self._init_clean_mode = False

        self._dummy_kfp_run_id = 0
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self.mnt_src_dir = Path(SettingMapper.query.get('mount_src_path').value)
        self._init_dir(self.mnt_src_dir, self._init_clean_mode)

        self.mnt_dst_ip_dir = Path(SettingMapper.query.get('mount_dst_path').value) / 'ip'
        self.result_dir = self.mnt_dst_ip_dir / 'job_result'
        self._init_dir(self.result_dir, self._init_clean_mode)

        self.airflow_host = SettingMapper.query.get('airflow_entry_point').value
        self.testbed_mount_volume_path = Path('/usr/local/qai/mnt')

        self.airflow_mount_volume_path = Path(SettingMapper.query.get('airflow_mount_volume_path').value)

        # dagの情報取得 いずれなんかのリポジトリに移動？
        self.root_dag_dir_path = Path(__file__).parent.joinpath('../../../dag')
        if not(os.environ.get('IP_ROOT_DAG_DIR_PATH') is None):
            self.root_dag_dir_path = Path(os.environ.get('IP_ROOT_DAG_DIR_PATH'))

    @staticmethod
    def _init_dir(dir_path: Path, init_clean_mode: bool = True):
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
        elif init_clean_mode:
            shutil.rmtree(str(dir_path))
            dir_path.mkdir(parents=True)

    @log(logger)
    def post(self, organizer_id: str, ml_component_id: int, request: PostJobReq) -> PostJobRes:

        if len(request.test_description_ids) == 0:
            raise QAIInvalidRequestException(result_code='R10001', result_msg='Invalid param.')

        ml_component = MLComponentMapper.query.\
            filter(MLComponentMapper.id == ml_component_id).\
            filter(MLComponentMapper.org_id == organizer_id).first()
        if ml_component is None:
            raise QAINotFoundException(result_code='R14000', result_msg='not found test.')

        try:

            # job初期登録
            job = JobMapper(status='QUEUED', result='NA', result_detail='NA', test_id=ml_component.test[0].id)
            sql_db.session.add(job)
            sql_db.session.flush()

            job_id = job.id

            # testのjob idに設定
            test = TestMapper.query.get(job.test_id)
            test.job_id = job.id

            # runs初期登録
            runs = []
            for td_id in request.test_description_ids:
                runs.append(RunMapper(job_id=job.id, test_description_id=td_id, status='QUEUED', result='NA'))
            sql_db.session.add_all(runs)
            sql_db.session.commit()

            # td-run紐づけ
            for td_id in request.test_description_ids:
                td = TestDescriptionMapper.query.get(td_id)
                run = RunMapper.query.\
                    filter(RunMapper.job_id == job.id).\
                    filter(RunMapper.test_description_id == td_id).first()
                # tdのrun id設定
                td.run_id = run.id
            sql_db.session.commit()

            job.status = 'RUNNING'

            for td_id in request.test_description_ids:
                try:
                    self._exec_run(job, organizer_id, ml_component_id, td_id)
                    sql_db.session.commit()
                except QAIException as e:
                    self._update_error(job_id, request.test_description_ids, td_id,
                                       'result_code:{} result_msg:{}'.format(e.result_code, e.result_msg))
                    print(e)
                except Exception as e:
                    self._update_error(job_id, request.test_description_ids, td_id, str(e))
                    print(e)

        except SQLAlchemyError as e:
            print(e)
            sql_db.session.rollback()
            raise QAIInvalidRequestException(result_code='R19001', result_msg='failed db operation.')
        except QAIException as e:
            print(e)
            sql_db.session.rollback()
            raise e
        except Exception as e:
            print(e)
            sql_db.session.rollback()
            raise QAIInvalidRequestException(result_code='R19999', result_msg='unknown exception.')

        return PostJobRes(
            result=Result(code='R12000', message="job create success."),
            job_id=job.id
        )

    def _exec_run(self, job, organizer_id, ml_component_id, td_id):
        td = TestDescriptionMapper.query.get(td_id)
        dag_id = td.test_runner.name + '_' + td.test_runner.version
        dag_dir_path = self.root_dag_dir_path.joinpath(dag_id)
        if not dag_dir_path.exists():
            raise QAINotFoundException(result_code='R14001', result_msg='not found dag.')

        # ait.manifest.json存在チェック
        manifest_paths = glob.glob(str(dag_dir_path.joinpath('**/ait.manifest.json')), recursive=True)
        if len(manifest_paths) == 0:
            raise QAINotFoundException(result_code='R14002', result_msg='not found ait.manifest.json.')
        elif len(manifest_paths) > 1:
            raise QAIException(result_code='R14002', result_msg='found many ait.manifest.json.')
        # ait.manifest.json読み込み
        with open(str(manifest_paths[0]), encoding='utf-8') as f:
            manifest = json.load(f)
        # dag_idの一致チェック
        defined_dag_id = manifest['name'] + '_' + manifest['version']
        if dag_id != defined_dag_id:
            raise QAIInternalServerException(result_code='R17000', result_msg='not match dag_id.')
        # airflowにdag存在しなければ、dagをdeployする
        res = requests.get('{}/api/experimental/dags/{}/dag_runs'.format(self.airflow_host, dag_id))
        if res.status_code != 200:
            dag_py_path = dag_dir_path.joinpath('dag.py')
            mime_type = 'plain/text; charset=UTF-8'
            file_name = '{}.py'.format(dag_id)
            file_data = open(dag_py_path, 'rb').read()
            res = requests.post('{}/admin/rest_api/api?api=deploy_dag'.format(self.airflow_host, dag_id),
                                data={'force': 'on'},
                                files={'dag_file': (file_name, file_data, mime_type)})
            if res.status_code != 200:
                raise QAIInternalServerException(result_code='R17001', result_msg='failed deploy dag.')

            # DAG反映までsleep
            sleep(2)

        # pause解除
        res = requests.post('{}/admin/rest_api/api?api=unpause&dag_id={}'.
                            format(self.airflow_host, dag_id))
        if res.status_code != 200:
            raise QAIInternalServerException(result_code='R17002', result_msg='failed unpause dag.')

        # docker imageのpull
        # 本来はairflow内でpullされるはずだが、イメージ取得失敗するため、このタイミングでpullするように変更
        docker_remote_image_name = 'qunomon/' + manifest['name'] + ':' + manifest['version']
        if os.name == 'nt':
            client = docker.from_env()
        else:  # コンテナ起動の場合ソケット指定
            client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        try:
            # イメージが存在しない場合、pullする
            client.images.get(docker_remote_image_name)
        except ImageNotFound:
            try:
                client.images.pull(docker_remote_image_name)
            except ImageNotFound as ex:
                # localで作成したイメージはこのルートに入る。ログ出力して継続。
                logger.debug(f'{docker_remote_image_name} failed pull.')

        # # リフレッシュ(all)
        # res = requests.post('{}/admin/rest_api/api?api=refresh_all_dags'.format(self.airflow_host))
        # if res.status_code != 200:
        #     raise QAIInternalServerException(result_code=399, result_msg='failed refresh dag.')

        # リフレッシュ
        # res = requests.post('{}/admin/rest_api/api?api=refresh_dag&dag_id={}'.
        #                     format(self.airflow_host, dag_id))
        # if res.status_code != 200:
        #     raise QAIInternalServerException(result_code='R17002', result_msg='failed refresh dag.')

        run = RunMapper.query. \
            filter(RunMapper.job_id == job.id). \
            filter(RunMapper.test_description_id == td_id).first()
        # dag実行の引数ファイルを格納するフォルダ作成
        run_args_src_dir = self.airflow_mount_volume_path / 'ip' / 'job_args' / str(job.id) / str(run.id)
        self._init_dir(run_args_src_dir)
        # dag実行の引数ファイル作成
        input_file = run_args_src_dir / 'ait.input.json'
        self._create_input_file(input_file, td, run.id, job.id)

        # dag実行
        airflow_conf_file = run_args_src_dir / 'airflow_conf.json'
        callback_address = socket.gethostbyname(socket.gethostname())
        if not(os.environ.get('CONTAINER_FLAG') is None):
            callback_address = 'ip'
        callback_url = 'http://{}:6000/qai-ip/api/0.0.1/{}/mlComponents/{}/jobs/{}/runs/{}/notify-complete'.format(
            callback_address,
            organizer_id,
            str(ml_component_id),
            str(job.id),
            str(run.id))
        self._create_airflow_conf_file(airflow_conf_file, td, self.mnt_src_dir, run.id, job.id, callback_url)
        if os.name == 'nt':
            # windows(非コンテナ)の場合、ipでのconfigとairflowでのconfigにパスの差異がある。
            # ここで指定するのは、airflowから見たときのconfig
            dag_param = {'airflow_conf_file': self._get_posix_path_str(
                self.mnt_dst_ip_dir / 'job_args' / str(job.id) / str(run.id) / 'airflow_conf.json')}
        else:
            dag_param = {'airflow_conf_file': self._get_posix_path_str(airflow_conf_file)}
        dag_param_encoded = urllib.parse.quote(json.dumps(dag_param))
        res = requests.post('{}/admin/rest_api/api?api=trigger_dag&dag_id={}&conf={}'.
                            format(self.airflow_host, dag_id, dag_param_encoded))
        if res.status_code != 200:
            raise QAIInternalServerException(result_code='R17003', result_msg='failed run dag.')
        # execution_date反映
        res = requests.get('{}/api/experimental/dags/{}/dag_runs'.
                           format(self.airflow_host, dag_id))
        if res.status_code != 200 or res.text == '[]\n':
            raise QAIInternalServerException(result_code='R17004', result_msg='failed get runs.')
        max_run_id = max([run['id'] for run in res.json()])
        latest_execution_date = [run['execution_date'] for run in res.json() if run['id'] == max_run_id][0]
        run.execution_date = latest_execution_date
        run.status = 'RUNNING'
        run.launch_datetime = datetime.datetime.now()
        return

    def _update_error(self, job_id: int, test_description_ids: [int], td_id: int, error_msg: str):
        if job_id == -1 or td_id == -1:
            return

        run = RunMapper.query. \
            filter(RunMapper.job_id == job_id). \
            filter(RunMapper.test_description_id == td_id).first()
        run.status = 'DONE'
        run.result = 'ERR'
        run.result_detail = error_msg
        run.error_code = 'E201'
        run.done_datetime = datetime.datetime.now()
        sql_db.session.commit()

        runs = RunMapper.query.filter(RunMapper.job_id == job_id).all()

        job = JobMapper.query.get(job_id)
        job.result = 'ERR'
        if all([r.status == 'DONE' for r in runs]):
            job.status = 'DONE'
        job.result_detail = 'OK:{} NG:{} ERR:{} NA:{}'.format(
            len([r for r in runs if r.result == 'OK']),
            len([r for r in runs if r.result == 'NG']),
            len([r for r in runs if r.result == 'ERR']),
            len([r for r in runs if r.result == 'NA']))

        sql_db.session.commit()

    @staticmethod
    def _get_posix_path_str(path: Path):
        if str(path)[0] in ['/', '\\']:
            # 「/」、「\」始まりの場合は先頭に/を付与しない
            return '{}'.format(str(path).replace(':', '').replace('\\', '/'))
        else:
            return '/{}'.format(str(path).replace(':', '').replace('\\', '/'))

    def _create_airflow_conf_file(self, conf_file: Path, td: TestDescriptionMapper, args_src_dir: Path,
                                  run_id: int, job_id: int, callback_url: str):

        # input_json_dirの設定
        conf_json = {
            'input_json_dir': self._get_posix_path_str(
                self.testbed_mount_volume_path / 'ip' / 'job_args' / str(job_id) / str(run_id))
        }

        # mountsの設定
        if os.name == 'nt':
            mounts = [{"name": "mount_dir",
                       "src_path": self._get_posix_path_str(args_src_dir),  # 非コンテナの場合は、dockerホストのファイルパスのためposixパス変換
                       "dst_path": self._get_posix_path_str(self.testbed_mount_volume_path)}]
        else:
            mounts = [{"name": "mount_dir",
                       "src_path": str(args_src_dir),  # コンテナの場合は、posixパスではなく、ボリューム名のためパス変換はしない
                       "dst_path": self._get_posix_path_str(self.testbed_mount_volume_path)}]

        # inventory
        for i in td.inventories:
            name = i.template_inventory.name
            file_path = self._get_posix_path_str(i.inventory.file_path)
            last_item = file_path.split('/')[-1]
            # インベントリファイルの親フォルダをマウントする
            src_path = file_path.rstrip(last_item).rstrip('/')
            dst_path = "/usr/local/qai/inventory/{}".format(name)
            mounts.append({"name": "inv_{}".format(name),
                           "src_path": src_path,
                           "dst_path": dst_path})

        conf_json['mounts'] = mounts

        # callback_urlの設定
        conf_json['callback_url'] = callback_url

        # jsonファイルの作成
        with open(str(conf_file), 'w', encoding='utf-8') as f:
            json.dump(conf_json, f, indent=4, ensure_ascii=False)

    def _create_input_file(self, input_file: Path, td: TestDescriptionMapper, run_id: int, job_id: int):

        # run_idとjob_idの登録
        args_json = {'testbed_mount_volume_path': self._get_posix_path_str(self.testbed_mount_volume_path),
                     'run_id': run_id,
                     'job_id': job_id}

        # inventoriesの設定
        inventories = []
        for i in td.inventories:
            name = i.template_inventory.name
            # pathlibを使うと、実行OSのパス形式に依存して変換してしまうため、強制的にPOSIXにして、最終要素としてファイル名を取得
            file_name = self._get_posix_path_str(i.inventory.file_path).split('/')[-1]
            value = "/usr/local/qai/inventory/{}/{}".format(name, file_name)
            inventories.append({"Name": name, "Value": value})
        args_json['Inventories'] = inventories

        # method_paramsの設定
        method_params = []
        for p in td.test_runner_params:
            name = p.test_runner_param_template.name
            value = str(p.value)
            method_params.append({"Name": name, "Value": value})
        args_json['MethodParams'] = method_params

        with open(str(input_file), 'w', encoding='utf-8') as f:
            json.dump(args_json, f, indent=4, ensure_ascii=False)

# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
# !/usr/bin/env python3.6
# coding=utf-8
import requests
from pathlib import Path
import zipfile
from glob import glob
import pprint
import json
import time
from os import remove


class Helper:
    """
    テストのヘルパークラスです。

    Test helper class.
    """

    def __init__(self, backend_entry_point: str, ip_entry_point: str,
                 ait_dir: Path = None, ait_full_name: str = None, org_name: str = 'dep-a', ml_component_id: str = 1):
        """
        コンストラクタ

        Constructor

        Args:
            backend_entry_point (str) :
                バックエンドのエントリポイントアドレスを指定します。

                Specify the backend entry point address.

            ip_entry_point (str) :
                IPのエントリポイントアドレスを指定します。

                Specifies the entry point address of the IP.

            ait_dir (Path) :
                aitが格納されるフォルダを指定します。

                Specify the folder where the ait is stored.

            ait_full_name (str) :
                aitのバージョンまで含めた完全名を指定します。

                Specify the full name, including the version of ait.

            org_name (str) :
                組織名を指定します。

                Specifies the name of the organization.

            ml_component_id (str) :
                MLコンポーネントIDを指定します。

                Specify the ML component ID.
        """
        self._backend_entry_point = backend_entry_point
        self._ip_entry_point = ip_entry_point
        self._org_name = org_name
        self._ml_component_id = ml_component_id
        self._ait_dir = ait_dir
        self._ait_full_name = ait_full_name
        self._internal_dir = 'container'

        self._wait_animation = [
            " [*     ]",
            " [ *    ]",
            " [  *   ]",
            " [   *  ]",
            " [    * ]",
            " [     *]",
            " [    * ]",
            " [   *  ]",
            " [  *   ]",
            " [ *    ]",
        ]

    def get_bk(self, path: str, is_print_response: bool = True, is_print_json: bool = True):
        """
        バックエンドに対してGETメソッドを発行します。

        Issue a GET method to the backend.

        Args:
            path (str) :
                GETを実行するパスを指定します。

                Specify the path to execute GET.

            is_print_response (bool) :
                レスポンスをprintするか指定します。

                Specifies whether to print the response.

            is_print_json (bool) :
                レスポンスのjsonをprintするか指定します。

                Specifies whether to print the response json.

        Returns:
            response

        """
        response = requests.get(f'{self._backend_entry_point}{path}')
        if is_print_response:
            print(response)
        if is_print_json:
            pprint.pprint(response.json())
        return response

    def get_ip(self, path: str, is_print_response: bool = True, is_print_json: bool = True):
        """
        IPに対してGETメソッドを発行します。

        Issue a GET method to the IP.

        Args:
            path (str) :
                GETを実行するパスを指定します。

                Specify the path to execute GET.

            is_print_response (bool) :
                レスポンスをprintするか指定します。

                Specifies whether to print the response.

            is_print_json (bool) :
                レスポンスのjsonをprintするか指定します。

                Specifies whether to print the response json.

        Returns:
            response

        """
        response = requests.get(f'{self._ip_entry_point}{path}')
        if is_print_response:
            print(response)
        if is_print_json:
            pprint.pprint(response.json())
        return response

    def post_bk(self, path: str, data, is_print_response: bool = True, is_print_json: bool = True):
        """
        バックエンドに対してPOSTメソッドを発行します。

        Issue a POST method to the backend.

        Args:
            path (str) :
                GETを実行するパスを指定します。

                Specify the path to execute GET.

            data :
                POSTするデータを指定します。

                Specify the data to be POSTed.

            is_print_response (bool) :
                レスポンスをprintするか指定します。

                Specifies whether to print the response.

            is_print_json (bool) :
                レスポンスのjsonをprintするか指定します。

                Specifies whether to print the response json.

        Returns:
            response

        """
        response = requests.post(f'{self._backend_entry_point}{path}',
                                 json.dumps(data),
                                 headers={'Content-Type': 'application/json'})
        if is_print_response:
            print(response)
        if is_print_json:
            pprint.pprint(response.json())
        return response

    def post_ip(self, path: str, data, is_print_response: bool = True, is_print_json: bool = True):
        """
        IPに対してPOSTメソッドを発行します。

        Issue a POST method to the IP.

        Args:
            path (str) :
                GETを実行するパスを指定します。

                Specify the path to execute GET.

            data :
                POSTするデータを指定します。

                Specify the data to be POSTed.

            is_print_response (bool) :
                レスポンスをprintするか指定します。

                Specifies whether to print the response.

            is_print_json (bool) :
                レスポンスのjsonをprintするか指定します。

                Specifies whether to print the response json.

        Returns:
            response

        """
        response = requests.post(f'{self._ip_entry_point}{path}',
                                 json.dumps(data),
                                 headers={'Content-Type': 'application/json'})
        if is_print_response:
            print(response)
        if is_print_json:
            pprint.pprint(response.json())
        return response

    def upload_zip_id(self, zip_path: str):
        """
        zipファイルをアップロードします。
        これはAITをデプロイするために使用します。

        Upload the zip file.
        This will be used to deploy the AIT.

        Args:
            zip_path (str) :
                zipパスを指定します。

                Specifies the zip path.

        Returns:
            response

        """
        file_obj = open(zip_path, 'rb')
        response = requests.post(f'{self._ip_entry_point}/deploy-dag',
                                 data={"name": "dag_zip"},
                                 files={"archive": (str(Path(zip_path).name), file_obj)})
        print(response)
        pprint.pprint(response.json())
        return response

    def _create_zip(self, ait_dir: str = None, ait_full_name: str = None, is_non_build_zip: bool = False):
        zip_dir = ait_dir / 'deploy'
        zip_file = Path(__file__).parent / f'{ait_full_name}.zip'

        with zipfile.ZipFile(zip_file, 'w', compression=zipfile.ZIP_STORED) as new_zip:
            new_zip.write(str(zip_dir.joinpath('dag.py')), arcname=f'{ait_full_name}/dag.py')

            if is_non_build_zip:
                # 必要となるait.manifest.jsonのみ同梱
                new_zip.write(str(zip_dir.joinpath(self._internal_dir).joinpath('repository/ait.manifest.json')),
                              arcname=f'{ait_full_name}/{self._internal_dir}/repository/ait.manifest.json')
            else:
                # docker build をIPで実施するため、すべてのファイルを梱包
                new_zip.write(str(zip_dir.joinpath(self._internal_dir).joinpath('dockerfile')),
                              arcname=f'{ait_full_name}/{self._internal_dir}/dockerfile')

                dir_path = zip_dir.joinpath(self._internal_dir).joinpath('repository')
                files = glob(str(dir_path.joinpath('**')), recursive=True)
                for file in files:
                    file_name = Path(file).name
                    new_zip.write(file, arcname=f'{ait_full_name}/{self._internal_dir}/repository/{file_name}')
        return zip_file

    def async_build_ait(self, zip_path):
        """
        aitを非同期でビルドします。

        Build ait asynchronously.

        Args:
            zip_path (str) :
                zipパスを指定します。

                Specifies the zip path.

        Returns:
            response

        """
        zip_name = str(Path(zip_path).name)
        with open(zip_path, 'rb') as file_obj:
            response = requests.post(f'{self._ip_entry_point}/async-deploy-dag',
                                     files={"dag_zip": (zip_name, file_obj)})
        print(response)
        pprint.pprint(response.json())
        return response

    def post_manifest(self, manifest_path):
        """
        ait.manifest.jsonをバックエンドに登録します。

        Register ait.manifest.json in the backend.

        Args:
            manifest_path (str) :
                ait.manifest.jsonパスを指定します。

                Specifies the ait.manifest.json path.

        Returns:
            response

        """
        manifest_name = str(Path(manifest_path).name)
        with open(manifest_path, 'rb') as file_obj:
            response = requests.post(f'{self._backend_entry_point}/testRunners/manifest',
                                     files={"ait.manifest": (manifest_name, file_obj)})
        print(response)
        pprint.pprint(response.json())
        return response

    @staticmethod
    def _find_file(dir_path: Path, file_name: str):
        files = glob(str(dir_path.joinpath(f'**/{file_name}')), recursive=True)
        if len(files) == 0:
            raise Exception(f'not found {file_name} in zip.')
        elif len(files) > 1:
            raise Exception(f'{file_name} must be one exists in zip.')
        return files[0]

    def deploy_ait_async_and_wait(self, ait_dir=None, ait_full_name=None, need_build_container: bool = True,
                                  wait_time: float = 0.5):

        """
        aitを非同期でデプロイします。

        Deploy ait asynchronously.

        Args:
            ait_dir (Path) :
                aitが格納されるフォルダを指定します。

                Specify the folder where the ait is stored.

            ait_full_name (str) :
                aitのバージョンまで含めた完全名を指定します。

                Specify the full name, including the version of ait.

            need_build_container (bool) :
                コンテナビルドが必要かどうかを指定します。

                Specifies whether or not a container build is required.

            wait_time (float) :
                完了チェックの周期秒を指定します。

                Specifies the cycle seconds for completion check.

        """
        if ait_dir is None:
            ait_dir = self._ait_dir

        if ait_full_name is None:
            ait_full_name = self._ait_full_name

        self._deploy_ait_async(ait_dir, ait_full_name, need_build_container=need_build_container)
        self._wait_deploy_complete(wait_time=wait_time)

    def deploy_ait_non_build(self, ait_dir=None, ait_full_name=None):

        """
        aitをビルド無しでデプロイします。

        Deploy ait with no build.

        Args:
            ait_dir (Path) :
                aitが格納されるフォルダを指定します。

                Specify the folder where the ait is stored.

            ait_full_name (str) :
                aitのバージョンまで含めた完全名を指定します。

                Specify the full name, including the version of ait.

        """
        if ait_dir is None:
            ait_dir = self._ait_dir

        if ait_full_name is None:
            ait_full_name = self._ait_full_name

        # add manifest
        self.post_manifest(self._find_file(ait_dir / 'deploy' / self._internal_dir, 'ait.manifest.json'))

        # deploy
        zip_path = self._create_zip(ait_dir, ait_full_name, is_non_build_zip=True)
        zip_name = str(Path(zip_path).name)
        with open(zip_path, 'rb') as file_obj:
            response = requests.post(f'{self._ip_entry_point}/deploy-dag-non-build',
                                     files={"dag_zip": (zip_name, file_obj)})
        print(response)
        pprint.pprint(response.json())
        remove(zip_path)

    def _deploy_ait_async(self, ait_dir=None, ait_full_name=None, need_build_container: bool = True):
        # add manifest
        self.post_manifest(self._find_file(ait_dir / 'deploy' / self._internal_dir, 'ait.manifest.json'))

        # deploy
        if need_build_container:
            zip_file = self._create_zip(ait_dir, ait_full_name)
            self.async_build_ait(zip_file)
            remove(zip_file)

    def _wait_deploy_complete(self, wait_time: float = 1):
        i = 0

        while True:
            print(self._wait_animation[i % len(self._wait_animation)], end="\r")
            i += 1

            json_ = self.get_ip('/async-deploy-dag', is_print_response=False, is_print_json=False).json()
            if json_['Code'] != 'D00011':
                if json_['Code'] != 'D00010':
                    # D00010以外はエラー発生のため、コンソールに出力
                    pprint.pprint(json_)
                else:
                    print('complete')
                break
            time.sleep(wait_time)

    def _wait_run_complete(self, wait_time: float = 1):
        i = 0

        while True:
            print(self._wait_animation[i % len(self._wait_animation)], end="\r")
            i += 1

            run_status = self.get_bk(f'/{self._org_name}/mlComponents/{self._ml_component_id}/testDescriotions/run-status',
                                     is_print_response=False,
                                     is_print_json=False).json()
            if run_status['Job']['Status'] != 'RUNNING':
                pprint.pprint(run_status['Runs'])
                break
            time.sleep(wait_time)

    def post_inventory(self, name: str, type_id: int, file_system_id: int, file_pass: str, description: str,
                       formats: []) -> str:
        """
        インベントリのPOSTメソッドを発行します。

        Issue a POST method for inventory.

        Args:
            name (str) :
                名前を指定します。

                Specify a name.

            type_id :
                タイプIDを指定します。

                Specify the type ID.

            file_system_id :
                ファイルシステムIDをprintするか指定します。

                Specifies whether to print the file system ID.

            file_pass (str) :
                ファイルパスを指定します。

                Specifies the file path.

            description (str) :
                説明を指定します。

                Specify a description.

            formats :
                フォーマットを指定します。

                Specify the format.

        Returns:
            inventory_name

        """
        inventory_name = f'{self._ait_full_name}_{name}'
        self.post_bk(f'/{self._org_name}/mlComponents/{self._ml_component_id}/inventories', {
            'Name': inventory_name,
            'TypeId': type_id,
            'FileSystemId': file_system_id,
            'FilePath': file_pass,
            'Description': description,
            'Formats': formats,
        })
        return inventory_name

    def get_inventory(self, name: str):
        """
        インベントリ名を指定して、インベントリJSONを取得します。

        Inventory JSON is obtained by specifying an inventory name.

        Args:
            name (str) :
                インベントリ名前を指定します。

                Specify an inventory name.

        Returns:
            res_json

        """
        res_json = self.get_bk(f'/{self._org_name}/mlComponents/{self._ml_component_id}/inventories',
                               is_print_json=False).json()
        return [j for j in res_json['Inventories'] if j['Name'] == name][-1]

    def post_td(self, name: str, quality_dimension_id: id, quality_measurements, target_inventories, test_runner):
        """
        テストデスクリプションのPOSTメソッドを発行します。

        Issue the POST method of the test-description.

        Args:
            name (str) :
                名前を指定します。

                Specify a name.

            quality_dimension_id :
                品質ディメンションIDを指定します。

                Specifies a quality dimension ID.

            quality_measurements :
                品質指標を指定します。

                Specify a quality quality_measurements.

            target_inventories:
                対象インベントリを指定します。

                Specify the target inventory.

            test_runner:
                テストランナーを指定します。

                Specify a test runner.

        """
        self.post_bk(f'/{self._org_name}/mlComponents/{self._ml_component_id}/testDescriotions', {
            'Name': name,
            'QualityDimensionID': quality_dimension_id,
            'QualityMeasurements': quality_measurements,
            'TargetInventories': target_inventories,
            'TestRunner': test_runner
        })

    def get_td(self, name: str):
        """
        テストデスクリプション名を指定して、テストデスクリプションJSONを取得します。

        Get the test-description JSON by specifying the test-description name.

        Args:
            name (str) :
                テストデスクリプション名前を指定します。

                Specify a test-description name.

        Returns:
            res_json

        """
        res_json = self.get_bk(f'/{self._org_name}/mlComponents/{self._ml_component_id}/testDescriotions',
                               is_print_json=False).json()
        return [j for j in res_json['Test']['TestDescriptions'] if j['Name'] == name][-1]

    def post_run_and_wait(self, *td_id):
        """
        指定したテストデスクリプションIDを実行して、完了するまで待機します。

        Run the specified Test Description ID and wait for it to complete.

        Args:
            td_id :
                テストデスクリプションIDを指定します。

                Specifies the test-description ID.

        """
        wait_time = 0.5
        self.post_bk(f'/{self._org_name}/mlComponents/{self._ml_component_id}/testDescriotions/runners', {
            "Command": "AsyncStart",
            "TestDescriptionIds": list(td_id)
        })

        self._wait_run_complete(wait_time=wait_time)

    def get_td_detail(self, td_id: int):
        """
        テストデスクリプション名を指定して、テストデスクリプション詳細JSONを取得します。

        Get the test-description detail JSON by specifying the test-description name.

        Args:
            td_id :
                テストデスクリプションIDを指定します。

                Specifies the test-description ID.

        Returns:
            res_json

        """
        return self.get_bk(f'/{self._org_name}/mlComponents/{self._ml_component_id}/testDescriotions/{td_id}',
                           is_print_json=False).json()

    def post_report(self, *td_id):
        """
        指定したテストデスクリプションIDでレポートを生成します。

        Generate a report with the specified test-description ID.

        Args:
            td_id :
                テストデスクリプションIDを指定します。

                Specifies the test-description ID.

        Returns:
            res_json

        """
        return self.post_bk(f'/{self._org_name}/mlComponents/{self._ml_component_id}/testDescriotions/reportGenerator', {
            "Command": "Generate",
            "Destination": [str(t) for t in td_id]
        }).json()

    def post_ml_component(self, name: str, description: str, problem_domain: str, ml_framework_id: int = -1):
        """
        MLコンポーネントのPOSTメソッドを発行します。

        Issue the POST method of ML components.

        Args:
            name (str) :
                名前を指定します。

                Specify a name.

            description :
                説明を指定します。

                Specify a description.

            problem_domain :
                問題領域を指定します。

                Specify the problem domain.

            ml_framework_id:
                MLフレームワークIDを指定します。

                Specify the ML framework ID.

        Returns:
            res_json
        """
        if ml_framework_id == -1:
            ml_framework_id = self.get_bk('/mlFrameworks',
                                          is_print_response=False,
                                          is_print_json=False).json()['MLFrameworks'][0]['Id']

        return self.post_bk(f'/{self._org_name}/mlComponents', {
            'Name': name,
            'Description': description,
            'ProblemDomain': problem_domain,
            'MLFrameworkId': ml_framework_id
        }).json()

    def set_ml_component_id(self, ml_component_id: int):
        """
        MLコンポーネントIDを設定します。

        Set the ML component ID.

        Args:
            ml_component_id (int) :
                MLコンポーネントIDを指定します。

                Specify the ML component ID.

        """
        self._ml_component_id = ml_component_id

    def get_data_types(self):
        """
        データタイプ一覧を取得します。

        Get a list of data types.

        Returns:
            res_json
        """
        res_json = self.get_bk('/dataTypes',
                               is_print_response=False,
                               is_print_json=False).json()
        return res_json

    def get_file_systems(self):
        """
        ファイルシステム一覧を取得します。

        Get a list of file systems.

        Returns:
            res_json
        """
        res_json = self.get_bk('/fileSystems',
                               is_print_response=False,
                               is_print_json=False).json()
        return res_json

# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
# !/usr/bin/env python3.6
# coding=utf-8

import json
from pathlib import Path

from ...utils.logging import log, get_logger


logger = get_logger()


class AITInputGenerator:
    """
    ait.input.jsonを出力するためのクラス。
    set関数で各項目を入力し、write関数でjsonを出力する。
    あらかじめait.manifest.jsonを生成しておく必要がある。

    Class for outputting ait.input.json.
    You input each item with the set function and output json with the write function.
    You must generate ait.manifest.json beforehand.
    """
    def __init__(self, manifest_path: str):
        """
        コンストラクタ

        Constructor

        Args:
            manifest_path :
                ait.manifest.jsonのパス情報

                Path information in ait.manifest.json
        """
        self._mount_path = '/usr/local/qai/mnt'
        self._run_id = 1
        self._job_id = 1

        self._output_file_path = f'{self._mount_path}/ip/job_args/{self._job_id}/{self._run_id}/ait.input.json'
 
        self._ait_inventories = []
        self._ait_method_params = []

        self._ait_manifest_json = None

        # ait.manifest.jsonをロード
        with open(manifest_path, encoding='utf-8') as f:
            self._ait_manifest_json = json.load(f)
        # ait.manifest.jsonからparameters項目を取得
        if self._ait_manifest_json['parameters'] is not None:
            for param in self._ait_manifest_json['parameters']:
                # 'default_val'がNULLの場合は'0'を入れる
                if (param['default_val'] is not None) and (len(param['default_val']) > 0):
                    self._ait_method_params.append({'Name': param['name'], 'Value': param['default_val']})
                else:
                    self._ait_method_params.append({'Name': param['name'], 'Value': '0'})

    @log(logger)
    def add_ait_inventories(self, name: str, value: str) -> None:
        """
        Inventories項目を設定する。

        Set the Inventories item.

        Args:
            name (str) :
                Inventoriesの名称。ait.manifest.jsonのInventoriesの名称と同じにする必要がある。

                The name of Inventories, which should be the same as the name of Inventories in ait.manifest.json.

            value (str) :
                Inventoriesの格納場所。{AIT_ROOT}/local_qai/inventory/以下のフォルダ/ファイル名の情報。
                （例）{AIT_ROOT}/local_qai/inventory/input/test.jpgなら「input/test.jpg」

                The location of Inventories. Information on the folders/file names under {AIT_ROOT}/local_qai/inventory/.
                (e.g., "input/test.jpg" for {AIT_ROOT}/local_qai/inventory/input/test.jpg
        """
        # ait.manifest.jsonのinventories項目の中に引数nameが存在するか確認する。
        name_exist_flag = False
        if self._ait_manifest_json['inventories'] is not None:
            for inventory in self._ait_manifest_json['inventories']:
                if inventory['name'] == name:
                    name_exist_flag = True
                    break

        # 引数nameが存在しなかった場合はエラー
        if name_exist_flag is False:
            raise KeyError(f'{name} is not found in ait.manifest.json')

        value_path = '/usr/local/qai/inventory/' + value
        self._ait_inventories.append({'Name': name, 'Value': value_path})

    @log(logger)
    def set_ait_params(self, name: str, value: str) -> None:
        """
        parameters項目を設定する。

        Set the parameters item.

        Args:
            name (str) :
                parametersの名称。ait.manifest.jsonのparametersの名称と同じにする必要がある。

                The name of the parameters, which must be the same as the name of the parameters in ait.manifest.json.

            value (str) :
                parametersの値。

                The value of parameters.

        """
        # ait.manifest.jsonのparameters項目の中に引数nameが存在するか確認する。
        name_exist_flag = False
        if self._ait_manifest_json['parameters'] is not None:
            for parameter in self._ait_manifest_json['parameters']:
                if parameter['name'] == name:
                    name_exist_flag = True
                    break

        # 引数nameが存在しなかった場合はエラー
        if name_exist_flag is False:
            raise KeyError(f'{name} is not found in ait.manifest.json')

        param = [p for p in self._ait_method_params if p['Name'] == name][0]
        param['Value'] = value

    @log(logger)
    def write(self) -> str:
        """
        設定した各項目をjsonファイルに出力する。

        出力先ファイルパスは以下となる。
        /usr/local/qai/mnt/ip/job_args/[job_id]/[run_id]/ait.input.json

        Output each set item to a json file.

        The output file path is as follows.
        /usr/local/qai/mnt/ip/job_args/[job_id]/[run_id]/ait.input.json

        Returns:
            出力先ファイルパス
            Output file path

        """
        output_json = {}
        output_json['Inventories'] = self._ait_inventories
        output_json['MethodParams'] = self._ait_method_params
        output_json['testbed_mount_volume_path'] = self._mount_path
        output_json['run_id'] = self._run_id
        output_json['job_id'] = self._job_id

        # 親フォルダ作成
        Path(self._output_file_path).parent.mkdir(parents=True, exist_ok=True)

        with open(self._output_file_path, 'w', encoding='utf-8') as f:
            json.dump(output_json, f, indent=2, ensure_ascii=False)

        return self._output_file_path

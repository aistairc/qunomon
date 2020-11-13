# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
# !/usr/bin/env python3.6
# coding=utf-8
import json
from datetime import datetime
import psutil
import cpuinfo

from .ait_manifest import AITManifest
from ...utils.logging import log, get_logger


logger = get_logger()


class AITOutput:
    """
    AITが出力するファイル「ait.output.json」を管理するクラスです。

    This class manages the file "ait.output.json", which is output by AIT.
    """

    @log(logger)
    def __init__(self, ait_manifest: AITManifest):
        """
        コンストラクタ

        constructor

        Args:
            ait_manifest (AITManifest) :
                ait_manifestを指定します。

                Specify the ait_manifest.
        """
        self._ait_manifest = ait_manifest
        self._measures = []
        self._resources = []
        self._downloads = []

    @log(logger)
    def add_measure(self, name: str, value: str) -> None:
        """
        measureを追加します。

        Add measure.

        Args:
            name (str) :
                名前を指定します。

                Specify a name.

            value (str) :
                値を指定します。

                Specify a value.
        """
        self._measures.append({'Name': name, 'Value': value})

    @log(logger)
    def add_resource(self, name: str, path: str) -> None:
        """
        resourceを追加します。

        Add resource.

        Args:
            name (str) :
                名前を指定します。

                Specify a name.

            path (str) :
                パスを指定します。

                Specify a path.
        """
        self._resources.append({'Name': name, 'Path': path})

    @log(logger)
    def add_downloads(self, name: str, path: str) -> None:
        """
        downloadsを追加します。

        Add downloads.

        Args:
            name (str) :
                名前を指定します。

                Specify a name.

            path (str) :
                パスを指定します。

                Specify a path.
        """
        self._downloads.append({'Name': name, 'Path': path})

    @log(logger)
    def write_output(self, 
                     output_file_path: str,
                     start_dt: datetime,
                     stop_dt: datetime,
                     error: str = None) -> None:

        """
        ait.output.jsonを出力します。

        Output ait.output.json.

        Args:
            output_file_path (str) :
                出力先パスを指定します。

                Specify the output path.

            start_dt (datetime) :
                処理開始日時を指定します。

                Specify the date and time to start processing.

            stop_dt (datetime) :
                処理終了日時を指定します。

                Specify the date and time when the process ends.

            error (str) :
                エラー情報を指定します。

                Specify the error information.
        """
        output_json = {
            'AIT': {
                'Name': self._ait_manifest.get_name(),
                'Version': self._ait_manifest.get_version()
                },
            'ExecuteInfo': {
                'StartDateTime': start_dt.strftime('%Y-%m-%dT%H:%M:%S%z'),
                'EndDateTime': stop_dt.strftime('%Y-%m-%dT%H:%M:%S%z'),
                'MachineInfo': self._get_machine_info()
                }
            }
        
        if error is not None:
            output_json['ExecuteInfo']['Error'] = error
        else:
            if (self._measures is not None) or (self._resources is not None) or (self._downloads is not None):
                output_json['Result'] = {}
                if (self._measures is not None) and (len(self._measures) > 0):
                    output_json['Result']['Measures'] = self._measures
                if (self._resources is not None) and (len(self._resources) > 0):
                    output_json['Result']['Resources'] = self._resources
                if (self._downloads is not None) and (len(self._downloads) > 0):
                    output_json['Result']['Downloads'] = self._downloads

        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(output_json, f, indent=4, ensure_ascii=False)

    def _get_machine_info(self):
        cpu_info_dict = cpuinfo.get_cpu_info()
        machine_info = {
            'cpu_brand':  cpu_info_dict['brand_raw'],
            'cpu_arch':   cpu_info_dict['arch'],
            'cpu_clocks': cpu_info_dict['hz_advertised_friendly'],
            'cpu_cores':  str(cpu_info_dict['count']),
            'memory_capacity': str(psutil.virtual_memory().total)
        }
        return machine_info
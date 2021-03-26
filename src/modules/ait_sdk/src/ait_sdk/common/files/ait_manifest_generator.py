# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
# !/usr/bin/env python3.6
# coding=utf-8
from typing import List
import json
from pathlib import Path

from ...utils.logging import log, get_logger


logger = get_logger()


class AITManifestGenerator:
    """
    ait.manifest.jsonを出力するためのクラス。
    set関数で各項目を入力し、write関数でjsonを出力する。

    Class for outputting ait.manifest.json.
    Input each item with the set function and output json with the write function.
    """
    def __init__(self, base_dir: str):
        """
        コンストラクタ

        Constructor

        Args:
            base_dir (str) :
                ait.manifest.json出力先のフォルダを指定する

                Specify the destination folder for ait.manifest.json output

        """
        self._ait_name = ""
        self._ait_description = ""
        self._ait_author = ""
        self._ait_email = ""
        self._ait_version = ""
        self._ait_quality = ""
        self._ait_reference = ""
 
        self._ait_inventories = []
        self._ait_parameters = []
        self._ait_measures = []
        self._ait_resources = []
        self._ait_downloads = []

        self._output_file_path = f'{base_dir}/ait.manifest.json'

    @log(logger)
    def set_ait_name(self, name: str) -> None:
        """
        name項目を設定する。
        名称+バージョンで全体で一意になる必要性があります。

        名称自由に決めていただいて結構ですが、一意制約があるため以下の命名規則に沿って定義することを推奨します。

        Set the name item.
        The name + version must be unique across the whole.

        You can use any name you want, but it is recommended to define it according to the following naming conventions because of the unique restriction.

        * {prefix}_{target_problem}_{delegate_metric}_{...}
          * {prefix}
            * eval : 品質評価
            * alyz : 分析
            * misc : その他
            * dev : 開発でのみ使用
          * {target_problem}
            * 対象とする問題領域を簡潔に記載します。
          * {delegate_metric}
            * 代表的な指標値を記載します。
          * {...}
             * これ以降は自由に記載してください。

        Args:
            name (str)

        """
        self._ait_name = name

    @log(logger)
    def set_ait_description(self, description: str) -> None:
        """
        description項目を設定する。

        AIT利用者にとって選択の一助となるように、AITの算出する指標値について、
        導出式を記載することを推奨します。

        Set a description item.

        In order to help AIT users make a choice, the index values calculated by AIT should be
        It is recommended that the derivation formula be stated.

        Args:
            description (str)

        """
        self._ait_description = description

    @log(logger)
    def set_ait_author(self, author: str) -> None:
        """
        author項目を設定する。

        Set the author item.

        Args:
            author (str)

        """
        self._ait_author = author

    @log(logger)
    def set_ait_email(self, email: str) -> None:
        """
        email項目を設定する。

        Set the email field.

        Args:
            email (str)
        """
        self._ait_email = email

    @log(logger)
    def set_ait_version(self, version: str) -> None:
        """
        version項目を設定する。

        バージョンはメジャーバージョンとマイナーバージョンの組み合わせを推奨しますが、数値である必要はなく、
        それぞれが管理可能な体系としてください。

        Set the version item.

        Versions should be a combination of major and minor versions, but they do not have to be numeric.
        Each should be a manageable system.

        * {major_version}_{minor_version}

        Args:
            version (str)
        """
        self._ait_version = version

    @log(logger)
    def set_ait_quality(self, quality: str) -> None:
        """
        quality項目を設定する。
        QualityはURLで表現されます。
        上記URLから取得できるjsonデータにQualityDimensionに関する情報が記載されます。
        この機能が実装されるまでは、暫定的にURLの最終要素をQualityDimensionとして扱います。

        Set the quality item.
        Quality is expressed as a URL.
        The information about the QualityDimension is described in the json data you can get from the above URL.
        Until this feature is implemented, the final element of the URL is treated as the QualityDimension.

        Args:
            quality (str)
        """
        self._ait_quality = quality

    @log(logger)
    def set_ait_reference(self, reference: str) -> None:
        """
        reference項目を設定する。
        AITの根拠となる論文参照を記載します。

        Establish a reference item.
        Describe the paper reference as the basis for the AIT.

        Args:
            reference (str)
        """
        self._ait_reference = reference

    # inventories
    @log(logger)
    def add_ait_inventories(self, name: str, type_: str, description: str, format_: list, schema: str) -> None:
        """
        inventories項目を設定する。

        Set the inventories item.

        Args:
            name (str)
            type_ (str):
                以下いずれかの値である必要があります。

                It should be one of the following values

                    dataset
                    model
                    attribute set

            description (str)
            format_ (List)
            schema (str)

        """
        self._ait_inventories.append({'name': name, 'type': type_, 'description': description, 'format': format_,
                                      'schema': schema})

    # parameters
    @log(logger)
    def add_ait_parameters(self, name: str, type_: str, description: str, default_val: str = '', 
                           min_value: str = '', max_value: str = '') -> None:
        """
        parameters項目を設定する。

        Set the parameters item.

        Args:
            name (str)
            type_ (str):
                以下いずれかの値である必要があります。

                It should be one of the following values

                    int
                    float
                    bool
                    str

            description (str)
            default_val (str):
                任意

                Optional

            min_value (str) :
                最小値を設定します。（任意）

                Set the minimum value. (optional)

            max_value (str) :
                最大値を設定します。（任意）

                Set the maximum value. (optional)
        """
        parameter = {'name': name, 'type': type_, 'description': description, 'default_val': default_val}
        if len(min_value)>0 :
            parameter['min'] = min_value
        if len(max_value)>0 :
            parameter['max'] = max_value
        self._ait_parameters.append(parameter)

    # measures
    @log(logger)
    def add_ait_measures(self, name: str, type_: str, description: str, structure: str, min: str = '', max: str = '') -> None:
        """
        measures項目を設定する。

        Set the measures item.

        Args:
            name (str)

            type_ (str):
                以下いずれかの値である必要があります。

                It should be one of the following values

                    int
                    float
                    bool
                    str

            description (str)

            structure (str) :
                以下いずれかの値である必要があります。

                It should be one of the following values

                    single
                    sequence

            min (str) :
                最小値を設定します。（任意）

                Set the minimum value. (optional)

            max (str) :
                最大値を設定します。（任意）

                Set the maximum value. (optional)
        """
        if len(min) > 0 and len(max) > 0:
            self._ait_measures.append({'name': name, 'type': type_, 'description': description, 'structure': structure, 'min':min, 'max':max})
        elif len(min) > 0 and len(max) == 0:
            self._ait_measures.append({'name': name, 'type': type_, 'description': description, 'structure': structure, 'min':min})
        elif len(min) == 0 and len(max) > 0:
            self._ait_measures.append({'name': name, 'type': type_, 'description': description, 'structure': structure, 'max':max})
        else:
            self._ait_measures.append({'name': name, 'type': type_, 'description': description, 'structure': structure})

    # resources
    @log(logger)
    def add_ait_resources(self, name: str, type_: str, description: str) -> None:
        """
        resources項目を設定する。

        Set the resources item.

        Args:
            name (str)

            type_ (str):

                以下いずれかの値である必要があります。

                It should be one of the following values

                    text
                    picture
                    table

            description (str)
        """
        self._ait_resources.append({'name': name, 'type': type_, 'description': description})

    # downloads
    @log(logger)
    def add_ait_downloads(self, name: str, description: str) -> None:
        """
        downloads項目を設定する。

        Set the downloads item.

        Args:
            name (str)
            description (str)
        """
        self._ait_downloads.append({'name': name, 'description': description})

    @log(logger)
    def _check_required_items(self) -> None:
        """
        必須項目のチェックを実施する

        Check the required fields

        Raises:
            ValueError:
                必須項目が存在しないときに発生する

                This occurs when a required field does not exist

        """
        check_general = {'ait_name': self._ait_name,
                         'ait_description': self._ait_description,
                         'ait_author': self._ait_author,
                         'ait_version': self._ait_version,
                         'ait_quality': self._ait_quality}
        for k, v in check_general.items():
            if len(v) == 0:
                raise ValueError(f'{k} is required.')

        self._check__required_item_section('inventories', self._ait_inventories)
        self._check__required_item_section('parameters', self._ait_parameters, ['default_val'])
        self._check__required_item_section('measures', self._ait_measures, ['min', 'max'])
        self._check__required_item_section('resources', self._ait_resources)
        self._check__required_item_section('downloads', self._ait_downloads)

    @staticmethod
    def _check__required_item_section(section_name, sections, skip_items=None):
        """
        必須項目の各セクションごとのチェックを実施する
        Conduct a check for each section of the required fields

        Args:
            section_name (str)
            sections (List)
            skip_items (List)

        Raises:
            ValueError:
                必須項目が存在しないときに発生する

                This occurs when a required field does not exist

        """
        for section in sections:
            name = section['name']
            for k, v in section.items():
                if (skip_items is not None) and (k in skip_items):
                    continue
                if len(v) == 0:
                    raise ValueError(f'{section_name}[{name}]/{k} is required.')

    @log(logger)
    def write(self) -> str:
        """
        設定した各項目をjsonファイルに出力する。
        書き込む前に必須チェックを実施する。

        Output each set item to a json file.
        Before writing, perform the required checks.

        Raises:
            ValueError:
                必須項目が存在しないときに発生する

                This occurs when a required field does not exist
        
        Returns:
            出力先ファイルパス

            Output file path

        """

        self._check_required_items()

        output_json = {
            'name': self._ait_name,
            'description': self._ait_description,
            'author': self._ait_author,
            'email': self._ait_email,
            'version': self._ait_version,
            'quality': self._ait_quality,
            'reference': self._ait_reference
            }

        output_json['inventories'] = self._ait_inventories
        output_json['parameters'] = self._ait_parameters
        output_json['report'] = {}
        output_json['report']['measures'] = self._ait_measures
        output_json['report']['resources'] = self._ait_resources
        output_json['downloads'] = self._ait_downloads

        # 親フォルダ作成
        Path(self._output_file_path).parent.mkdir(parents=True, exist_ok=True)

        with open(self._output_file_path, 'w', encoding='utf-8') as f:
            json.dump(output_json, f, indent=2, ensure_ascii=False)

        return self._output_file_path

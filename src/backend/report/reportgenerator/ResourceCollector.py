import shutil
import pandas as pd
import platform

from pandas import DataFrame
from sqlalchemy import or_
import sys
import os
from pathlib import Path
import reportgenerator.Tools as tools
import json
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# base.pyのあるディレクトリの絶対パスを取得(ReportGenerator単体で実行するときにだけ必要な処理)
current_dir = Path(__file__).resolve().parent
print(current_dir)
# # モジュールのあるパスを追加(ReportGenerator単体で実行するときにだけ必要な処理)
sys.path.append(os.path.join(os.path.dirname(current_dir), '..'))

class ResourceCollector():

    def __init__(self):
        self.zero_padding = 3

    # make_directory, collect_testresult, collect_template, collect_commoninfoを一気通貫で実行する
    # これらの関数は単体で実行する機会がないため、この関数で一括実行してしまって大丈夫なはず?
    def collect(self, app_debug_flg: Flask, dbinfo: SQLAlchemy, stragehome_path: str, downloadfiles_json: str,
                work_path: str):
        print('ResourceCollector() collect() start')
        try:
            # json to dataframe
            df = pd.read_json(downloadfiles_json)
            # レポート基本情報を"report_dataset"に格納(レポートジェネレータ単体でデバッグするときは、app_debug_flgにダミーのFlaskが存在する)
            if app_debug_flg is None:
                report_dataset = self.collect_commoninfo(dbinfo, df)
            else:
                with app_debug_flg.app_context():
                    report_dataset = self.collect_commoninfo(dbinfo, df)
            # report_datasetをJSON形式で保存する
            self.output_report_dataset(work_path, report_dataset)
            # ディレクトリ構造作成
            self.make_directory(stragehome_path, df, report_dataset)
            # テスト結果を<workdir>に配置
            self.collect_testresult(stragehome_path, df)
            # テンプレートを<workdir>に配置
            self.collect_template(dbinfo, stragehome_path, downloadfiles_json)
        except Exception as e:
            print("ReportGeneratorException: {}".format(e))
            raise
        return report_dataset

    def make_directory(self, stragehome_path: str, df: DataFrame, report_dataset: dict):
        # <workdir>(初期値はdb_resouce)フォルダがないなら作成
        if not (os.path.exists(stragehome_path)):
            os.makedirs(stragehome_path)

        # <workdir>配下のフォルダも作成していく
        for qp_id in report_dataset['QualityDimension'].keys():
            for index, row in df.iterrows():
                if int(qp_id) == row['quality_props']:
                    copy_to_folder = os.path.join(
                        stragehome_path,
                        str(qp_id),
                        str(row['testDescriptionID'])
                    )
                    # なかったら作成
                    if not (os.path.exists(copy_to_folder)):
                        os.makedirs(copy_to_folder)

    # ファイルリストを解読。品質特性、ランナーIDの情報を元にディレクトリ生成
    def collect_testresult(self, stragehome_path: str, df: DataFrame):
        for index, row in df.iterrows():
            filepath = row['filepath']
            # print('copy_to_file:' + str(filepath))
            copy_to_file = os.path.join(
                stragehome_path,
                str(row['quality_props']),
                str(row['testDescriptionID']),
                os.path.basename(filepath)
            )
            # print('copy_to_file:' + str(copy_to_file))
            if row['required']:
                self.__download(filepath, copy_to_file)

    def collect_template(self, dbinfo: SQLAlchemy, stragehome_path: str, downloadfiles_json: str):
        # templateはreportディレクトリに抱えこみ、DBや共通ディレクトリは利用しない
        # 今後DBで一元管理することになった場合、実装が必要
        pass

    def collect_commoninfo(self, dbinfo: SQLAlchemy, df: DataFrame):
        from qai_testbed_backend.entities.quality_dimension import QualityDimensionMapper
        from qai_testbed_backend.entities.ml_component import MLComponentMapper
        from qai_testbed_backend.entities.test_description import TestDescriptionMapper
        from qai_testbed_backend.entities.run import RunMapper

        # testdescriptionのIdリストを作成
        test_description_list = [data_frame for data_frame in df.testDescriptionID]
        test_description_list = list(set(test_description_list))
        # test_description_listと一致するTestDescriptionを取得
        test_descriptions = dbinfo.session.query(TestDescriptionMapper).\
            filter(
            or_(TestDescriptionMapper.id == test_description_id for test_description_id in test_description_list))\
            .all()
        # 内部品質のリストを取得
        qualities = dbinfo.session.query(QualityDimensionMapper).all()
        quality_props = {str(q.id): q.name for q in qualities}
        # # TDと紐づいている内部品質のリストを取得
        # qualities = dbinfo.session.query(QualityDimensionMapper).all()
        # quality_props = {str(q.id): q.name for q in qualities
        #                  for td in test_descriptions if q.id == td.quality_dimension_id}
        # 機械学習コンポーネント名、開発部を取得
        ml_component = dbinfo.session.query(MLComponentMapper).\
            filter(
            or_(MLComponentMapper.id == test_description.test.ml_component_id for test_description in test_descriptions))\
            .first()
        # TestEnvironmentの情報を取得
        run = dbinfo.session.query(RunMapper).\
            filter(
            or_(RunMapper.test_description_id == test_description_id for test_description_id in test_description_list))\
            .first()
        test_environment = {
            'cpu_brand': run.cpu_brand,
            'cpu_arch': run.cpu_arch,
            'cpu_clocks': run.cpu_clocks,
            'cpu_cores': run.cpu_cores,
            'memory_capacity': run.memory_capacity
        }
        # TestDescriptionDetailの取得
        test_description_details = {str(td.id): td.to_dto_report() for td in test_descriptions}
        # TDIDで紐づけされた表示順にソートされたグラフ名とファイル名を取得({'TDID':[['ファイル名', 'グラフ名']]})
        graph_matrix = [[td_id, name, Path(file).name] for td_id, name, file
                        in zip(df.testDescriptionID, df.name.values, df.filepath)]
        graph_dic = []
        for td_id in test_description_list:
            graph_dic.extend({'TD': str(gm_id), 'Name': name, 'File': file}
                             for gm_id, name, file in graph_matrix if gm_id == td_id)
        detecting_td_change = -1
        order = 1
        for gd in graph_dic:
            td = dbinfo.session.query(TestDescriptionMapper).filter(TestDescriptionMapper.id == gd['TD']).first()
            # TDのIDが変わった場合、カウンター(order)をリセットする
            if not detecting_td_change == td.id:
                detecting_td_change = td.id
                order = 1
            # Opinionファイルのときorderには"0"を設定して、orderのカウントを戻す
            if gd['Name'] == 'Opinion':
                gd['Order'] = '0'.zfill(self.zero_padding)
                order += -1
            else:
                gd['Order'] = str(order).zfill(self.zero_padding)
            gd['QualityDimensionId'] = [qd.id for qd in qualities if qd.id == td.quality_dimension_id]
            gd['QualityDimensionId'] = str(gd['QualityDimensionId'][0])
            order += 1

        report_dataset = {
            "TestDescriptionID": test_description_list,
            "QualityDimension": quality_props,
            "MLComponentName": ml_component.name,
            "Author": ml_component.org_id,
            "TestbedEnvironment": platform.platform(),
            "TestEnvironment": test_environment,
            "TestDescriptionDetail": test_description_details,
            "Date": str(datetime.date.today()),
            "Resources": graph_dic
        }
        return report_dataset

    def output_report_dataset(self, work_path: str, report_dataset: dict):
        from qai_testbed_backend.controllers.dto.test_description import GetTestDescriptionForReportResSchema
        output_filepath = work_path + 'report_dataset.json'
        test_descriptions = {}
        # 空のbase_report.htmlを作成
        os.makedirs(Path(output_filepath).parent, exist_ok=True)
        Path(output_filepath).touch()
        if report_dataset['TestDescriptionDetail'] is None:
            report_dataset['TestDescriptionDetail'] = {}
        else:
            for td in report_dataset['TestDescriptionDetail'].values():
                data = {'test_description_detail': td}
                dump_data = GetTestDescriptionForReportResSchema().dump(data)
                test_descriptions.update([(str(td.id_), dump_data['TestDescriptionDetail'])])
            report_dataset['TestDescriptionDetail'] = test_descriptions
            tools.write_file(output_filepath, json.dumps(report_dataset, ensure_ascii=False, indent=4), "w")

    # source_file_path: ファイルがもともと置かれている場所
    # destination_file_path: この関数によりダウンロードされ、配置される場所
    def __download(self, source_file_path, destination_file_path):
        # ☆TODO: 2020/03時点ではデータは同一マシン上にあるはずなので、
        # 単なるのファイルコピーで処理を代替します。
        # したがって、将来的に書き直すことになります。
        shutil.copyfile(source_file_path, destination_file_path)


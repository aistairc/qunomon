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
from qlib.utils.logging import get_logger, log

logger = get_logger()

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
    @log(logger)
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
            print("ResourceCollector.ReportGeneratorException: {}".format(e))
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

        # リソース0件の場合、スキップ
        if pd.isnull(df.filepath).any():
            return

        for index, row in df.iterrows():
            filepath = row['filepath']
            # print('copy_to_file:' + str(filepath))

            # Resourceが指定された場合のみ実施 
            if len(str(filepath)) > 0:
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
        from qai_testbed_backend.entities.run_measure import RunMeasureMapper
        from qai_testbed_backend.entities.run import RunMapper
        from qai_testbed_backend.entities.organization import OrganizationMapper
        from qai_testbed_backend.entities.scope_quality_dimension import ScopeQualityDimensionMapper
        from qai_testbed_backend.entities.scope import ScopeMapper
        from qai_testbed_backend.entities.guideline import GuidelineMapper
        from qai_testbed_backend.entities.inventory import InventoryMapper
        from qai_testbed_backend.entities.inventory_td import InventoryTDMapper
        from qai_testbed_backend.entities.data_type import DataTypeMapper

        # testdescriptionのIdリストを作成
        test_description_list = [data_frame for data_frame in df.testDescriptionID]
        test_description_list = list(set(test_description_list))
        # test_description_listと一致するTestDescriptionを取得
        test_descriptions = dbinfo.session.query(TestDescriptionMapper).\
            filter(
            or_(TestDescriptionMapper.id == test_description_id for test_description_id in test_description_list))\
            .all()

        data_type_mapper_list = dbinfo.session.query(DataTypeMapper).all()
        data_type_table = {}
        for data_type in data_type_mapper_list:
            data_type_table[str(data_type.id)] = data_type.name

        # 使用されたTDに対応するinventoryを取得
        inventory_td_list = dbinfo.session.query(InventoryTDMapper).\
            filter(
            or_(InventoryTDMapper.test_description_id == test_description_id for test_description_id in test_description_list))\
            .all()
        # 使用されたすべてのinventoryのidのリストを取得(重複は除く)
        inventory_id_list = list(set([i_td.inventory_id for i_td in inventory_td_list]))
        # 使用されたすべてのinventoryのmapperのリストを取得
        inventory_mapper_list = dbinfo.session.query(InventoryMapper).\
            filter(
            or_(InventoryMapper.id == inventory_id for inventory_id in inventory_id_list))\
            .all()
        # 使用されたすべてのinventoryのリストを取得
        inventory_list = self.__make_inventory_list(inventory_mapper_list, data_type_table)

        # 使用されたTDのIDをkeyに、
        # inventoryのidのリストをvalueとするdictを作成
        td_inventory_id_dict = {}
        for i_td in inventory_td_list:
            td_id = i_td.test_description_id
            i_id  = i_td.inventory_id
            if not(str(td_id) in td_inventory_id_dict.keys()):
                td_inventory_id_dict[str(td_id)] = []
            td_inventory_id_dict[str(td_id)].append(i_id)
        # 使用されたTDのIDをkeyに、
        # inventoryのリストをvalueとするdictを作成
        td_inventory_dict = {}
        for td_id, inventory_id_list in td_inventory_id_dict.items():
            inventory_mapper_list = dbinfo.session.query(InventoryMapper).\
                filter(
                or_(InventoryMapper.id == inventory_id for inventory_id in inventory_id_list))\
                .all()
            td_inventory_list = self.__make_inventory_list(inventory_mapper_list, data_type_table)
            td_inventory_dict[str(td_id)] = td_inventory_list
        # 使用されたTDのmesurementのmapperのリストを取得
        td_measures_mapper_list = dbinfo.session.query(RunMeasureMapper).\
            filter(
            or_(RunMeasureMapper.run_id == test_description.run_id for test_description in test_descriptions))\
            .all()
        # 使用されたTDのIDをkeyにmeasurementのnameとvalueを持つ辞書をvalueとするdictを作成
        # 使用されたTDのmesurementのnameをkeyに,mesurementのvalueをvalueとするsub_dictを作成
        td_measures_dict={}
        for test_description_id in test_description_list:
            td_measures_sub_dict= {str(td_measure.measure_name):None for td_measure in td_measures_mapper_list}
            for td_measure in td_measures_mapper_list:
                td_measures=''
                for test_description in test_descriptions:
                    if td_measure.run_id== test_description.run_id and test_description_id==test_description.id:
                        if td_measures_sub_dict[str(td_measure.measure_name)] is None:
                            td_measures_sub_dict[str(td_measure.measure_name)] = str(td_measure.measure_value)
                        else:
                            td_measures = td_measures_sub_dict[str(td_measure.measure_name)] +','+ str(td_measure.measure_value)
                            td_measures_sub_dict[str(td_measure.measure_name)]=td_measures
                        td_measures_dict[str(test_description_id)] = td_measures_sub_dict
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


        guideline_dict = {}

        # ガイドラインのメタデータを取得
        guideline = dbinfo.session.query(GuidelineMapper).\
            filter(
            or_(GuidelineMapper.id == ml_component.guideline_id))\
            .first()
        guideline_dict['metainfo'] = self.__get_guideline_metainfo(guideline)

        # Scopeを取得
        scope_id = ml_component.scope_id
        scope = dbinfo.session.query(ScopeMapper).\
            filter(
            or_(ScopeMapper.id == scope_id))\
            .first()
        guideline_dict['scope'] = self.__make_guideline_scope_dict(scope)
        
        # Scopeに紐づかれるQDを取得
        scope_qd_mapper_list = dbinfo.session.query(ScopeQualityDimensionMapper).\
            filter(
            or_(ScopeQualityDimensionMapper.scope_id == scope_id))\
            .all()
        scoped_qualities = []
        for mapper in scope_qd_mapper_list:
            scoped_qd_id = mapper.quality_dimension_id
            scoped_quality = dbinfo.session.query(QualityDimensionMapper).\
                filter(
                or_(QualityDimensionMapper.id == scoped_qd_id))\
                .first()
            scoped_qualities.append(scoped_quality)
        guideline_dict['quality_dimensions'] = self.__make_guideline_qd_dict(scoped_qualities, test_descriptions)

        # 主に理由関係を取得
        user_dict = self.__make_user_dict(ml_component)

        # 総評を取得
        opinion = ml_component.report_opinion

        # Resource未定義のAITの場合（リソースファイルが存在せず、TDIDだけ指定されている状態）、グラフデータを作成しない
        graph_matrix = []
        if not pd.isnull(df.filepath).any():
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

        # 組織名の取得
        org = OrganizationMapper.query.filter(OrganizationMapper.id == ml_component.org_id).first()

        report_dataset = {
            "TestDescriptionID": test_description_list,
            "QualityDimension": quality_props,
            "MLComponentName": ml_component.name,
            "Author": org.name,
            "TestbedEnvironment": platform.platform(),
            "TestEnvironment": test_environment,
            "TestDescriptionDetail": test_description_details,
            "TDInventoryDict": td_inventory_dict,
            "TDMeasurementDict":td_measures_dict,
            "Date": str(datetime.date.today()),
            "Resources": graph_dic,
            "Guideline": guideline_dict,
            "User": user_dict,
            "Inventories": inventory_list,
            "Opinion": opinion
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

    def __get_guideline_metainfo(self, guideline_mapper):
        date_str = guideline_mapper.publish_datetime.strftime('%Y/%m/%d')
        metainfo = [
            {
                "property": "title",
                "content": guideline_mapper.name
            },
            {
                "property": "creator",
                "content": guideline_mapper.creator
            },
            {
                "property": "publisher",
                "content": guideline_mapper.publisher
            },
            {
                "property": "date",
                "term": "issued",
                "content": date_str
            },
            {
                "property": "identifier",
                "content": guideline_mapper.identifier
            }
        ]
        return metainfo

    def __make_inventory_list(self, inventory_mapper_list, data_type_table):
        inventory_list = []
        for inventory_mapper in inventory_mapper_list:
            type_id = str(inventory_mapper.type_id)
            current_inventory = {
                'id':          inventory_mapper.id,
                'name':        inventory_mapper.name,
                'file_path':   inventory_mapper.file_path,
                'hash':        inventory_mapper.file_hash_sha256,
                'data_type':   data_type_table[type_id],
                'description': inventory_mapper.description
            }
            inventory_list.append(current_inventory)
        return inventory_list

    def __make_guideline_scope_dict(self, scope_mapper):
        scope_dict = {
            "name": scope_mapper.name
        }
        return scope_dict

    def __make_guideline_qd_dict(self, qd_mapper_list, td_mapper_list):
        temp_dict = {}
        for qd_mapper in qd_mapper_list:
            temp_dict[qd_mapper.id] = {
                "name": qd_mapper.name,
                "description": qd_mapper.description,
                "count": 0,
                "num_run_td": 0,
                "num_passed_td": 0
            }

        count = 0
        for td_mapper in td_mapper_list:
            qd_id = td_mapper.quality_dimension_id
            if temp_dict[qd_id]['count']==0:
                count = count + 1
                temp_dict[qd_id]['count'] = count
            
            temp_dict[qd_id]['num_run_td'] += 1
            result = td_mapper.to_dto().result
            if result=='OK':
                temp_dict[qd_id]['num_passed_td'] += 1

        quality_dimensions = []
        for qd_id, qd_temp_dict in temp_dict.items():
            qd = {
                "id": qd_id,
                "name":          qd_temp_dict['name'],
                "description":   qd_temp_dict['description'],
                "count":         qd_temp_dict['count'],
                "num_run_td":    qd_temp_dict['num_run_td'],
                "num_passed_td": qd_temp_dict['num_passed_td']
            }
            quality_dimensions.append(qd)
        return quality_dimensions

    def __make_user_dict(self, ml_component_mapper):
        user_dict = {
            'guideline_reason': ml_component_mapper.guideline_reason,
            'scope_reason': ml_component_mapper.scope_reason
        }
        return user_dict

    # source_file_path: ファイルがもともと置かれている場所
    # destination_file_path: この関数によりダウンロードされ、配置される場所
    @log(logger)
    def __download(self, source_file_path, destination_file_path):
        # ☆TODO: 2020/03時点ではデータは同一マシン上にあるはずなので、
        # 単なるのファイルコピーで処理を代替します。
        # したがって、将来的に書き直すことになります。
        shutil.copyfile(source_file_path, destination_file_path)


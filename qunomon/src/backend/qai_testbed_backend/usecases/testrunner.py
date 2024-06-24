# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from datetime import datetime, timedelta, timezone
from requests import post, get
from pathlib import Path
import json
from injector import singleton
import os
import shutil
from distutils.dir_util import remove_tree, copy_tree
from sqlalchemy import asc
from qlib.utils.logging import get_logger, log
from reportgenerator import ReportGenerator

from ..across.exception import QAINotFoundException, QAIBadRequestException,\
    QAIInvalidRequestException
from ..across.file_checker import FileChecker
from ..controllers.dto.testrunner import PostTestRunnerReq, PostTestRunnerRes, Result, Job, \
    GetTestRunnerStatusRes, JobStatus, PostReportGeneratorRes, PostReportGeneratorReq
from ..entities.test import TestMapper
from ..entities.test_description import TestDescriptionMapper
from ..entities.ml_component import MLComponentMapper
from ..entities.dowmload import DownloadMapper
from ..entities.organization import OrganizationMapper
from ..entities.setting import SettingMapper
from ..entities.graph import GraphMapper
from ..entities.report_template import ReportTemplateMapper
from ..gateways.extensions import sql_db


logger = get_logger()


@singleton
class TestRunnerService:
    def __init__(self):
        self.ip_entry_point = SettingMapper.query.get('ip_entry_point').value
        self._file_checker = FileChecker()

    @log(logger)
    def post(self, organizer_id: str, ml_component_id: int, request: PostTestRunnerReq) -> PostTestRunnerRes:

        org = OrganizationMapper.query.filter(OrganizationMapper.organizer_id == organizer_id).first()
        if org is None:
            raise QAINotFoundException(result_code='R14004', result_msg=f'organizer_id:{organizer_id} is not found')
        test = TestMapper.query.\
                          filter(TestMapper.ml_component_id == ml_component_id).\
                          filter(MLComponentMapper.org_id == org.id).first()
        if test is None:
            raise QAINotFoundException('R14000', 'not found test descriptions')

        td_ids = request.test_description_ids
        if len(td_ids) == 0:
            # 以下条件を除外したTestDescriptionMapperを作る
            # 既に削除済み, 既に実行済み（OK or NG）
            tds = TestDescriptionMapper.query. \
                filter(TestDescriptionMapper.test_id == test.id). \
                filter(TestDescriptionMapper.delete_flag == False). \
                all()
            # 既に実行済み（OK or NG）を削除
            # ※sqlalchemyでリレーション先のテーブルをfilterに加えられないため、python側で絞り込む
            tds = [t for t in tds if
                   (t.run is None) or
                   ((t.run is not None) and (t.run.result != 'OK' and t.run.result != 'NG'))]
            if not tds:
                raise QAINotFoundException('R14001', 'all test descriptions are deleted or executed \n'
                                                     'You can\'t re-execute a previously executed TD,'
                                                     ' so create a new one or duplicate it.')
            td_ids = [t.id for t in tds]
        else:
            # td_id指定時は、それぞれ削除済みか、実行済みかをチェックする
            for td_id in td_ids:
                td = TestDescriptionMapper.query.get(td_id)
                if td is None:
                    raise QAINotFoundException('R14001', f'test description[id={td_id}] is not exists.')
                if td.delete_flag:
                    raise QAINotFoundException('R14001', 'test description[id={}, name={}] are deleted.'
                                               .format(td_id, td.name))
                if (td.run_id is not None) and (td.run.result == 'OK' or td.run.result == 'NG'):
                    raise QAINotFoundException('R14001', 'test description[id={}, name={}] are executed.\n'
                                                         'You can\'t re-execute a previously executed TD,'
                                                         ' so create a new one or duplicate it.'
                                               .format(td_id, td.name))

        # インベントリ登録時とファイルが変更されていないか、ハッシュ値チェック
        for td_id in td_ids:
            td = TestDescriptionMapper.query.get(td_id)
            for inventory_td_mapper in td.inventories:
                file_check_result = self._file_checker.execute(inventory_td_mapper.inventory.file_path,
                                                               inventory_td_mapper.inventory.file_system_id)

                if not file_check_result['exists']:
                    raise QAINotFoundException('R14002', f'inventory file not found.'
                                                         f'file:{inventory_td_mapper.inventory.file_path}')
                if file_check_result['hash_sha256'] != inventory_td_mapper.inventory.file_hash_sha256:
                    raise QAIInvalidRequestException('R14003', f'inventory file hash is not much.'
                                                               f'file:{inventory_td_mapper.inventory.file_path}')

        res = post(url=self.ip_entry_point + '/' + organizer_id + '/mlComponents/' + str(ml_component_id) + '/job',
                   headers={'content-type': 'application/json'},
                   json={'TestDescriptionIds': td_ids})
        # レスポンスエラーチェック
        if res.status_code != 200:
            raise QAIInvalidRequestException('R19999', 'testrunner error: {}'.format(res.text))

        job_id = res.json()['JobId']

        return PostTestRunnerRes(
            result=Result(code='R12000', message="job launch success."),
            job=Job(id_=str(job_id),
                    start_datetime=datetime.now(timezone(timedelta(hours=+9), 'JST')))
        )


@singleton
class TestRunnerStatusService:
    def __init__(self):
        self.ip_entry_point = SettingMapper.query.get('ip_entry_point').value

    @log(logger)
    def get(self, organizer_id: str, ml_component_id: int) -> GetTestRunnerStatusRes:

        org = OrganizationMapper.query.filter(OrganizationMapper.organizer_id == organizer_id).first()
        if org is None:
            raise QAINotFoundException(result_code='R24002', result_msg=f'organizer_id:{organizer_id} is not found')
        test = TestMapper.query.\
                          filter(TestMapper.ml_component_id == ml_component_id).\
                          filter(MLComponentMapper.org_id == org.id).first()
        if test is None:
            raise QAINotFoundException('R24000', 'not found test descriptions')

        if test.job_id is None:
            return GetTestRunnerStatusRes(
                result=Result(code='R24001', message="job is not found."),
                job_status=JobStatus(id_=0, status='NA', result='NA', result_detail='OK:0 NG:0 ERR:0 NA:0'),
                run_statuses=[])

        return GetTestRunnerStatusRes(
            result=Result(code='R22000', message="get job status success."),
            job_status=test.job.to_dto(),
            run_statuses=[r.to_dto() for r in test.job.runs]
        )


@singleton
class ReportGeneratorService:
    def __init__(self):
        self.func_table = {
            "SetParam": self._invoke_set_params,
            "Generate": self._invoke_report_generate
        }

        self.backend_entry_point = SettingMapper.query.get('backend_entry_point').value

        # Windowsとそれ以外でマウント先を変更する
        if os.name == 'nt':
            mount_dst_path = Path(SettingMapper.query.get('mount_src_path').value)
        else:
            mount_dst_path = Path(SettingMapper.query.get('mount_dst_path').value)

        self.mount_dst_path = mount_dst_path

        self.backend_report_home = mount_dst_path/'backend'/'report_gen'

    def _initialize_report_dir(self, path):
        # workdirを作成
        if path.exists():
            remove_tree(str(path))
        path.mkdir(parents=True, exist_ok=True)
        # templateをコピー
        copy_src_dir = Path(__file__).joinpath('../../../report/template')
        copy_dst_dir = path / 'template'
        if copy_dst_dir.exists():
            remove_tree(str(copy_dst_dir))
        copy_tree(src=str(copy_src_dir.resolve()), dst=str(copy_dst_dir.resolve()))

    def _invoke_set_params(self, request: PostReportGeneratorReq, _=None) -> {}:
        # 先頭のdestinationのみ反映
        td_id = int(request.destination[0])
        td = TestDescriptionMapper.query.get(td_id)
        if td.run is not None:
            for td_graph in td.run.graphs:
                param_graphs = [g for g in request.params.graphs if g.id_ == td_graph.id]
                if len(param_graphs) > 0:
                    param_graph = param_graphs[0]
                    td_graph.report_required = param_graph.report_required
                    if param_graph.report_required:
                        td_graph.report_index = param_graph.report_index
                        td_graph.report_name = param_graph.report_name
                else:
                    td_graph.report_required = False

        if request.params.opinion is not None:
            td.opinion = request.params.opinion
        sql_db.session.commit()

    def _invoke_report_generate(self, request: PostReportGeneratorReq,
                                test_descriptions: [TestDescriptionMapper] = None) -> {}:
        # 事前処理
        # フォルダ準備
        dt_now_jst = datetime.now(timezone(timedelta(hours=9))).strftime('%Y%m%d%H%M%S')
        base_dir = self.backend_report_home / dt_now_jst
        in_dir = base_dir / 'in'
        in_dir.mkdir(parents=True)
        out_dir = base_dir / 'out'
        out_dir.mkdir(parents=True)
        # 作業フォルダをタイムスタンプで独立させる
        report_home_path = self.mount_dst_path / dt_now_jst / 'report'
        self._initialize_report_dir(report_home_path)
        self.report_generator = ReportGenerator(home_path=str(report_home_path) + os.sep)

        # requestに指定されたテンプレートIDがあればそちらのテンプレートを使用する
        target_report_template_flag = False
        if request.params is not None:
            if request.params.target_report_template_id is not None:
                template_id = request.params.target_report_template_id

                # レポートテンプレートのDB存在確認
                report_template = ReportTemplateMapper.query.filter(ReportTemplateMapper.id == template_id).first()
                if report_template is None:
                    raise QAINotFoundException('D17001', 'not found ReportTemplate in DB')

                copy_src_dir = Path(__file__).joinpath('../../../report/templates', str(template_id))
                # レポートテンプレートのディレクトリ存在確認
                if not copy_src_dir.resolve().exists():
                    raise QAINotFoundException('D17002', 'not found ReportTemplate in directory')

                copy_dst_dir = report_home_path / 'template'
                if copy_dst_dir.exists():
                    remove_tree(str(copy_dst_dir))
                copy_tree(src=str(copy_src_dir.resolve()), dst=str(copy_dst_dir.resolve()))

                target_report_template_flag = True

        # 入力JSON作成
        in_json = {}
        target_td_ids = []
        # 以下条件を除外したtarget_td_idsを作る
        # 既に削除済み, 未実行（None）、実行時失敗（ERR）
        if len(request.destination) == 0:
            # test_descriptionsは既に削除済みTDを除外したリスト
            target_td_ids = [td.id for td in test_descriptions if td.run and td.run.result != 'ERR']
        else:
            tmp_td_ids = [int(td_id) for td_id in request.destination]
            for td_id in tmp_td_ids:
                td = TestDescriptionMapper.query\
                    .filter(TestDescriptionMapper.id == td_id)\
                    .filter(TestDescriptionMapper.delete_flag == False).first()
                if td.run and td.run.result != 'ERR':
                    target_td_ids.append(td_id)
        if len(target_td_ids) == 0:
            raise QAINotFoundException('D14004', 'these test description is not running')

        file_path_list = []
        type_list = []
        quality_props_list = []
        td_id__list = []
        required_list = []
        report_name = []
        for td_id in target_td_ids:
            td = TestDescriptionMapper.query.get(td_id)
            if td.run_id is None:
                raise QAINotFoundException('D14002', 'test description\'s result is None')

            # opinionファイル出力
            if len(td.opinion) != 0:
                opinion_path = in_dir / ('opinion' + str(td_id) + ".txt")
                with open(str(opinion_path), mode='w', encoding='utf-8') as f:
                    f.write(td.opinion)
                file_path_list.append(str(opinion_path))
                type_list.append('text')
                quality_props_list.append(td.quality_dimension_id)
                td_id__list.append(str(td_id))
                required_list.append(True)
                report_name.append('Opinion')

            graphs = GraphMapper.query.\
                filter(GraphMapper.run_id == td.run_id).\
                filter(GraphMapper.report_required == True).\
                order_by(asc(GraphMapper.report_index)).\
                all()
            
            # Resourceが0件のAITの場合、GraphMapperにレコードが存在されないため、TDIDとQDIDのみ設定
            if not graphs:
                file_path_list.append("")
                type_list.append("")
                quality_props_list.append(td.quality_dimension_id)
                td_id__list.append(str(td_id))
                required_list.append("")
                report_name.append("")
            
            # Resourceが1件以上の場合、GraphMapperのレコードの件数分を作成
            else:
                for graph in graphs:
                    file_path_list.append(graph.download.path)
                    type_list.append(graph.graph_template.resource_type.type)
                    quality_props_list.append(td.quality_dimension_id)
                    td_id__list.append(str(td_id))
                    required_list.append(graph.report_required)
                    report_name.append(graph.report_name)

        in_json['filepath'] = dict(zip(range(len(file_path_list)), file_path_list))
        in_json['type'] = dict(zip(range(len(type_list)), type_list))
        in_json['quality_props'] = dict(zip(range(len(quality_props_list)), quality_props_list))
        in_json['testDescriptionID'] = dict(zip(range(len(td_id__list)), td_id__list))
        in_json['required'] = dict(zip(range(len(required_list)), required_list))
        in_json['name'] = dict(zip(range(len(report_name)), report_name))
        in_json_path = in_dir/'input.json'
        with open(str(in_json_path), 'w', encoding='utf-8') as f:
            json.dump(in_json, f, indent=4, ensure_ascii=False)

        # レポート生成
        pdf_file_path = report_home_path / 'work' / 'report.pdf'
        template_format_path = (Path(__file__).joinpath('../../../report/template_format')).resolve()
        pdf_file = self.report_generator.report_generate(sql_db, str(in_json_path), str(pdf_file_path),
                                                         str(template_format_path), target_report_template_flag)
        if not pdf_file or not Path(pdf_file).exists():
            raise QAINotFoundException('D16000', 'failed report generate')

        # 事後処理
        res = {}
        try:
            dst_path = out_dir / Path(pdf_file).name
            shutil.copy(src=pdf_file, dst=str(dst_path))
            dl = DownloadMapper(path=str(dst_path))
            sql_db.session.add(dl)
            sql_db.session.commit()
            res['ReportUrl'] = self.backend_entry_point + '/download/' + str(dl.id)
            # 作業フォルダを削除
            if report_home_path.exists():
                remove_tree(str(report_home_path.parent))
        except Exception as e:
            print('Exception: {}'.format(e))
            sql_db.session.rollback()
            raise e
        return res

    @log(logger)
    def post(self, organizer_id: str, ml_component_id: int, request: PostReportGeneratorReq) -> PostReportGeneratorRes:

        org = OrganizationMapper.query.filter(OrganizationMapper.organizer_id == organizer_id).first()
        if org is None:
            raise QAINotFoundException(result_code='D14000', result_msg=f'organizer_id:{organizer_id} is not found')
        test = TestMapper.query.\
                          filter(TestMapper.ml_component_id == ml_component_id).\
                          filter(MLComponentMapper.org_id == org.id).first()
        if test is None:
            raise QAINotFoundException('D14000', 'not found test descriptions')

        if request.command not in self.func_table:
            raise QAIBadRequestException('D10001', 'invaid command')

        # delete_flagがTrueのTDを除外したTestDescriptionMapperを作る
        mapper = TestDescriptionMapper.query. \
            filter(TestDescriptionMapper.test_id == test.id). \
            filter(TestDescriptionMapper.delete_flag == False). \
            all()
        if not mapper:
            raise QAINotFoundException('D14001', 'test descriptions are all deleted')

        try:
            func = self.func_table[request.command]
            out_params = func(request, mapper)
        except Exception as e:
            print('Exception: {}'.format(e))
            sql_db.session.rollback()
            raise e

        return PostReportGeneratorRes(
            result=Result(code='D12000', message="command invoke success."),
            out_params=out_params
        )

# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from pathlib import Path
from injector import singleton
import json
import datetime
import os
import glob
from sqlalchemy.exc import SQLAlchemyError
import shutil
from operator import lt, le, eq, ne, ge, gt
import re
from qlib.utils.logging import get_logger, log

from ..across.exception import QAIException, QAINotFoundException, \
    QAIInvalidRequestException, QAIInternalServerException
from ..controllers.dto import Result
from ..controllers.dto.run import PostNotifyCompleteRunRes
from ..entities.ml_component import MLComponentMapper
from ..entities.dowmload import DownloadMapper
from ..entities.job import JobMapper
from ..entities.run import RunMapper
from ..entities.graph import GraphMapper
from ..entities.setting import SettingMapper
from ..entities.test_description import TestDescriptionMapper
from ..entities.quality_measurement import QualityMeasurementMapper
from ..entities.operand import OperandMapper
from ..entities.relational_operator import RelationalOperatorMapper
from ..entities.graph_template import GraphTemplateMapper
from ..entities.downloadable_template import DownloadableTemplateMapper
from ..entities.downloadable_data import DownloadableDataMapper
from ..gateways.extensions import sql_db


logger = get_logger()


@singleton
class NotifyRunCompeteService:

    def __init__(self):
        # windows/Linuxで、summary.jsonの参照先を変更する
        if os.name == 'nt':
            self.result_dir = Path(SettingMapper.query.get('mount_src_path').value) / 'ip' / 'job_result'
            self.logging_root_path = '.\\..\\docker-airflow\\logs'
        else:
            self.result_dir = Path(SettingMapper.query.get('mount_dst_path').value) / 'ip' / 'job_result'
            self.logging_root_path = '/src/airflow_logs'
        self.backend_entry_point = SettingMapper.query.get('backend_entry_point').value

        self.report_resource_limit = int(SettingMapper.query.get('report_resource_limit').value)

    @log(logger)
    def post(self, organizer_id: str, ml_component_id: int, job_id: int, run_id: int) \
            -> PostNotifyCompleteRunRes:
        td = None
        ml_component = MLComponentMapper.query. \
            filter(MLComponentMapper.id == ml_component_id). \
            filter(MLComponentMapper.org_id == organizer_id).first()
        if ml_component is None:
            raise QAINotFoundException(result_code='R49000', result_msg='not found ml_component.')

        # run更新
        run = RunMapper.query. \
            filter(RunMapper.id == run_id). \
            filter(RunMapper.job_id == job_id). \
            first()
        if run is None:
            raise QAINotFoundException(result_code='R49000', result_msg='not found run.')

        if run.status == 'DONE':
            raise QAIException(result_code='R49010', result_msg='already run is done.')

        try:
            td = TestDescriptionMapper.query.filter(TestDescriptionMapper.run_id == run_id).first()
            if td is None:
                raise QAINotFoundException(result_code='R49000', result_msg='not found test description.')

            output_file = self.result_dir / str(job_id) / str(run_id) / 'ait.output.json'
            if not output_file.exists():
                self._update_run_err(td, job_id, run, detail_msg='ait.output.json is not exits.')
                raise QAINotFoundException(result_code='R49020', result_msg='not found ait.output.json.')

            with open(str(output_file), encoding='utf-8') as f:
                output_json = json.load(f)

            run.status = 'DONE'
            run.ait_output_file = str(output_file)
            run.done_datetime = datetime.datetime.utcnow()

            if 'Result' in output_json:
                # measurementごとにチェック
                measure_results = {}

                # マシン情報をDBに登録
                machine_info = output_json['ExecuteInfo']['MachineInfo']
                run.cpu_brand = machine_info['cpu_brand']
                run.cpu_arch = machine_info['cpu_arch']
                run.cpu_clocks = machine_info['cpu_clocks']
                run.cpu_cores = machine_info['cpu_cores']
                run.memory_capacity = machine_info['memory_capacity']

                # Measuresが存在しないAITは無条件でrun.resultをOKに設定する
                if 'Measures' not in output_json['Result']:
                    run.result = 'OK'
                    run.result_detail = 'No Measure'
                else:
                    result_detail = ''
                    for measurement in output_json['Result']['Measures']:
                        # quality_measurement取得
                        quality_measurement = QualityMeasurementMapper.query. \
                            filter(QualityMeasurementMapper.test_runner_id == td.test_runner_id). \
                            filter(QualityMeasurementMapper.name == measurement['Name']). \
                            first()
                        if quality_measurement is None:
                            raise QAIInternalServerException(result_code='R49030',
                                                             result_msg='quality_measurement(name={}) is not exits.'
                                                             .format(measurement['Name']))

                        # operand取得
                        operand = OperandMapper.query. \
                            filter(OperandMapper.test_description_id == run.test_description_id). \
                            filter(OperandMapper.quality_measurement_id == quality_measurement.id). \
                            first()
                        if operand is None:
                            raise QAIInternalServerException(result_code='R49030',
                                                             result_msg='operand(name={}) is not exits.'
                                                             .format(measurement['Name']))

                        if not operand.enable:
                            # 無効の場合、チェックなしでOKに変更する
                            measure_results[measurement['Name']] = True
                            result_detail += '{} : skip, because operand is disable.\n'.format(measurement['Name'])
                            continue

                        # 変換
                        metric_value = self._convert_operand(operand.value, quality_measurement.type)
                        actual_value = self._convert_operand(measurement['Value'], quality_measurement.type,
                                                             quality_measurement.structure.structure)

                        # 比較
                        result = self.compare(metric_value, actual_value, operand.relational_operator_id,
                                              quality_measurement.structure.structure)
                        measure_results[measurement['Name']] = result

                        result_detail += '{} : {}.\n'.format(measurement['Name'], "OK" if result else "NG")

                    if all(measure_results.values()):
                        run.result = 'OK'
                    else:
                        run.result = 'NG'

                    run.result_detail = result_detail
            else:
                run.result = 'ERR'
                # エラー発生時、エラー詳細をdetailに設定する
                if 'Error' in output_json['ExecuteInfo']:
                    run.result_detail = output_json['ExecuteInfo']['Error']
                else:
                    run.result_detail = run.result

            # job更新
            self._update_job_without_commit(job_id)

            # test_description_result更新
            self._update_graph_without_commit(td, output_json, output_file.parent)

            # Downloadable_dataの追加
            self._update_downloadable_data_without_commit(td, output_json, output_file.parent)

            # ログデータをDownloadsに格納
            self._update_log_without_commit(td)

            sql_db.session.commit()
        except SQLAlchemyError as e:
            self._update_run_err(td, job_id, run, detail_msg=str(e))
            raise QAIInvalidRequestException('R49000', 'database error: {}'.format(e))
        except QAIException as e:
            self._update_run_err(td, job_id, run, detail_msg=e.result_msg)
            raise
        except Exception as e:
            self._update_run_err(td, job_id, run, detail_msg=str(e))
            raise QAIInternalServerException(result_code='R49999', result_msg='internal server error: {}'.format(e))

        return PostNotifyCompleteRunRes(result=Result(code='R40000', message='notify success.'))

    @staticmethod
    def _convert_operand(value: str, type_: str, structure: str = 'single') -> object:
        type_convert_dict = {
            'int': int,
            'float': float,
            'bool': bool,
            'str': str
        }
        type_lower = type_.lower()
        if type_lower not in type_convert_dict:
            raise QAIInternalServerException(result_code='R49030',
                                             result_msg='type:{} is not defined'.format(type_lower))
        structure_lower = structure.lower()
        if structure_lower == 'single':
            return type_convert_dict[type_lower](value)
        elif structure_lower == 'sequence':
            return [type_convert_dict[type_lower](s) for s in value.split(',')]
        else:
            raise QAIInternalServerException(result_code='R49030',
                                             result_msg='structure:{} is not defined'.format(structure_lower))

    @staticmethod
    def compare(metric_value, actual_value, relational_operator_id: int, structure: str) -> bool:
        relation_ope = RelationalOperatorMapper.query.get(relational_operator_id)
        relation_ope_dict = {
            '==': eq,
            '!=': ne,
            '>': gt,
            '>=': ge,
            '<': lt,
            '<=': le
        }
        if relation_ope.expression not in relation_ope_dict:
            raise QAIInternalServerException(result_code='R49030',
                                             result_msg='expression:{} is not defined'.format(relation_ope.expression))

        structure_lower = structure.lower()
        if structure_lower == 'single':
            return relation_ope_dict[relation_ope.expression](actual_value, metric_value)
        elif structure_lower == 'sequence':
            return all([relation_ope_dict[relation_ope.expression](a, metric_value) for a in actual_value])
        else:
            raise QAIInternalServerException(result_code='R49030',
                                             result_msg='structure:{} is not defined'.format(structure_lower))

    @staticmethod
    def _update_job_without_commit(job_id):
        job = JobMapper.query.get(job_id)
        is_done = all([run.status == 'DONE' for run in job.runs])
        if is_done:
            job.status = 'DONE'
        cnt_err = len([run for run in job.runs if run.result == 'ERR'])
        cnt_ng = len([run for run in job.runs if run.result == 'NG'])
        cnt_na = len([run for run in job.runs if run.result == 'NA'])
        cnt_ok = len([run for run in job.runs if run.result == 'OK'])
        if cnt_err > 0:
            job.result = 'ERR'
        elif cnt_ng > 0:
            job.result = 'NG'
        elif cnt_na > 0:
            job.result = 'NA'
        elif cnt_ok == len(job.runs):
            job.result = 'OK'
        job.result_detail = 'OK:{} NG:{} ERR:{} NA:{}'.format(cnt_ok, cnt_ng, cnt_err, cnt_na)

    # TestRunnerの実行結果（グラフなど）をテーブルに格納する
    def _update_graph_without_commit(self, td: TestDescriptionMapper, output_json: dict, output_dir: Path):
        graph_index = 0

        for res in output_json['Result']['Resources']:
            graph_index += 1

            graph_template = GraphTemplateMapper.query. \
                filter(GraphTemplateMapper.test_runner_id == td.test_runner_id). \
                filter(GraphTemplateMapper.name == res['Name']). \
                first()
            if graph_template is None:
                raise QAIInternalServerException(result_code='R49030',
                                                 result_msg='graph_template(name={}) is not exits.'
                                                 .format(res['Name']))

            # グラフをT_Downloadテーブルへ追加する
            # /usr/local/qai/mnt/ip/job_result/{job_id}/{run_id}配下をait.output.jsonのフォルダに配置する
            item_path = re.sub('/usr/local/qai/mnt/ip/job_result/\d+/\d+/', '', res['Path'])
            download_path = output_dir / item_path
            dl = DownloadMapper(path=str(download_path))
            sql_db.session.add(dl)
            sql_db.session.flush()

            # グラフをT_Graphテーブルへ追加する
            insert_graph = GraphMapper()
            if self.report_resource_limit >= graph_index:
                insert_graph.report_required = True
            else:
                insert_graph.report_required = False
            insert_graph.graph_address = self._get_dl_url(dl)
            insert_graph.report_index = graph_index
            insert_graph.report_name = graph_template.name
            insert_graph.download_id = dl.id
            insert_graph.graph_template_id = graph_template.id
            insert_graph.run_id = td.run_id
            sql_db.session.add(insert_graph)

    def _update_downloadable_data_without_commit(self, td: TestDescriptionMapper, output_json: dict, output_dir: Path):
        for res in output_json['Result']['Downloads']:
            downloadable_template_mapper = DownloadableTemplateMapper.query. \
                filter(DownloadableTemplateMapper.test_runner_id == td.test_runner_id). \
                filter(DownloadableTemplateMapper.name == res['Name']). \
                first()
            if downloadable_template_mapper is None:
                raise QAIInternalServerException(result_code='R49030',
                                                 result_msg='downloadable_template(name={}) is not exits.'
                                                 .format(res['Name']))

            # ダウンロード可能データをT_Downloadテーブルへ追加する
            # /usr/local/qai/mnt/ip/job_result/{job_id}/{run_id}配下をait.output.jsonのフォルダに配置する
            item_path = re.sub('/usr/local/qai/mnt/ip/job_result/\d+/\d+/', '', res['Path'])
            download_path = output_dir / item_path
            dl = DownloadMapper(path=str(download_path))
            sql_db.session.add(dl)
            sql_db.session.flush()

            # ダウンロード可能データをT_Downloadable_Dataテーブルへ追加する
            downloadable_mapper = DownloadableDataMapper(run_id=td.run_id,
                                                         download_id=dl.id,
                                                         downloadable_template_id=downloadable_template_mapper.id,
                                                         download_address=self._get_dl_url(dl))
            sql_db.session.add(downloadable_mapper)

    def _get_dl_url(self, dl):
        return self.backend_entry_point + '/download/' + str(dl.id)

    # ログのパスをDownloadテーブルに追加して、ダウンロードリンクをT_Runテーブルに格納する
    def _update_log_without_commit(self, td: TestDescriptionMapper):
        run = td.run
        print('logging_root_path: {}'.format(self.logging_root_path))
        # pathを定義
        current_dir = os.getcwd()
        print('current dir : {}'.format(current_dir))
        log_path = ''
        log_file = ''

        try:
            dag_name = td.test_runner.name + '_' + td.test_runner.version
            # pre,main,postのログをひとつにまとめる
            processes = ['pre_process', 'main_process', 'post_process']
            for process in processes:
                if os.name == 'nt':
                    src_path = os.path.join(self.logging_root_path, dag_name, process, run.execution_date). \
                        replace('\\', '/').replace(':', '')
                    dst_path = os.path.join(self.logging_root_path, 'tmp', run.execution_date, process). \
                        replace('\\', '/').replace(':', '')
                else:
                    src_path = os.path.join(self.logging_root_path, dag_name, process, run.execution_date)
                    dst_path = os.path.join(self.logging_root_path, 'tmp', run.execution_date, process)
                os.makedirs(dst_path, exist_ok=True)
                for file in glob.glob(src_path + '/*'):
                    shutil.copy(file, dst_path)

            tmp_dir = os.path.join(self.logging_root_path, 'tmp', run.execution_date)
            if os.name == 'nt':
                tmp_dir = tmp_dir.replace('\\', '/').replace(':', '')
            os.chdir(tmp_dir)
            log_path = os.getcwd()
            os.chdir(current_dir)
            if os.name == 'nt':
                os.rename(log_path, str(log_path.replace('\\', '/').replace('', '-')))
                log_path = log_path.replace('\\', '/').replace('', '-')
            else:
                os.rename(log_path, str(log_path.replace(':', '-')))
                log_path = log_path.replace(':', '-')
            shutil.make_archive(log_path, 'zip', root_dir=log_path)
            print('log_path: {}'.format(log_path))
            log_file = os.path.join(str(log_path) + '.zip')
            print('log_file: {}'.format(log_file))

            # zip元のディレクトリを削除
            shutil.rmtree(log_path)

            # ログをT_Downloadテーブルへ追加する
            dl = DownloadMapper(path=str(log_file))
            sql_db.session.add(dl)
            sql_db.session.flush()

            run.log_file = self._get_dl_url(dl)
            sql_db.session.flush()
        except Exception as e:
            print('logging error: {}'.format(e))
            os.chdir(current_dir)
            # zip元のディレクトリを削除
            if os.path.exists(log_path):
                shutil.rmtree(log_path)
            # zipファイルを削除
            if os.path.exists(log_file):
                os.remove(log_file)

    def _update_run_err(self, td: TestDescriptionMapper, job_id: int, run: RunMapper, detail_msg: str):
        run.status = 'DONE'
        run.result = 'ERR'
        run.done_datetime = datetime.datetime.utcnow()
        run.result_detail = detail_msg
        self._update_job_without_commit(job_id)
        if td is not None:
            self._update_log_without_commit(td)
        sql_db.session.commit()

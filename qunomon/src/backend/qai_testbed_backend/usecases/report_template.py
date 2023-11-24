# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from qlib.utils.logging import get_logger, log
from injector import singleton
from flask import make_response
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from ..controllers.dto import Result
from ..entities.report_template import ReportTemplateMapper
from ..entities.guideline import GuidelineMapper
from ..entities.quality_dimension import QualityDimensionMapper
from ..across.exception import QAINotFoundException, QAIException, QAIInvalidRequestException
from ..controllers.dto.report_template import PostReportTemplateRes, GetReportTemplatesRes
from sqlalchemy.exc import SQLAlchemyError
from ..gateways.extensions import sql_db
from datetime import datetime

from urllib.parse import quote

import werkzeug
import shutil
import os


logger = get_logger()


@singleton
class ReportTemplateService:

    def __init__(self):
        # レポートテンプレートのディレクトリ
        self.root_report_templates_path = Path(__file__).parent.joinpath('../../report/templates')
        self.root_report_template_path = Path(__file__).parent.joinpath('../../report/template')
        self.root_report_template_format_path = Path(__file__).parent.joinpath('../../report/template_format')
        self.unzip_dir_path = ''

    @staticmethod
    def _clean_create_dir(dir_path: Path):
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
        else:
            shutil.rmtree(str(dir_path))
            dir_path.mkdir(parents=True)

    @log(logger)
    def get(self) -> GetReportTemplatesRes:
        report_template_list = ReportTemplateMapper.query.all()

        return GetReportTemplatesRes(
            result=Result(code='R01000', message="get list success."),
            report_templates=[d.to_dto() for d in report_template_list]
        )

    @log(logger)
    def post(self, request) -> PostReportTemplateRes:
        try:
            with TemporaryDirectory() as temp_dir:
                # レポートテンプレートのzip保存
                zip_path = self._save_zip(request, Path(temp_dir))

                # ZIP解凍
                self.unzip_dir_path = self._unzip(zip_path)

                # レポートテンプレート名の空チェック
                request_name = request.form['Name']
                if not request_name or len(request_name) == 0:
                    raise QAIInvalidRequestException(result_code='R02001', result_msg='Name must not empty.')
                # ガイドラインIDの空チェック
                request_gideline_id = request.form['GidelineId']
                if not request_gideline_id or len(request_gideline_id) == 0:
                    raise QAIInvalidRequestException(result_code='R02002', result_msg='GidelineId must not empty.')

                # レポートテンプレート登録
                rt_id = self._add_report_template(self.unzip_dir_path, request_name, int(request_gideline_id))

        except Exception as e:
            sql_db.session.rollback()
            raise e
        finally:
            # 作業フォルダ削除
            if self.unzip_dir_path.exists():
                shutil.rmtree(str(self.unzip_dir_path.parent))
        return PostReportTemplateRes(
            result=Result(code='R02000', message="add ReportTemplate success."),
            report_template_id=rt_id
        )

    @staticmethod
    def _save_zip(request, save_dir_path: Path) -> Path:
        if not request.files:
            raise QAIInvalidRequestException(result_code='R02999', result_msg='uploadFile is required.')

        file = request.files['File']
        filename = file.filename
        if '' == filename:
            raise QAIInvalidRequestException(result_code='R02999', result_msg='filename must not empty.')

        if not filename.endswith('.zip'):
            raise QAIInvalidRequestException(result_code='R02999', result_msg='file extension must be zip.')

        basefilename = os.path.basename(Path(filename))
        save_filename = werkzeug.utils.secure_filename(basefilename)
        save_path = save_dir_path.joinpath(save_filename)
        file.save(str(save_path))

        return save_path

    def _unzip(self, zip_path: Path) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        work_report_templates_path = self.root_report_templates_path.joinpath(timestamp)
        self._clean_create_dir(work_report_templates_path)

        with ZipFile(zip_path) as existing_zip:
            existing_zip.extractall(work_report_templates_path)

        # zip解凍直下のフォルダを返却する
        dir_name = os.listdir(work_report_templates_path)[0]
        unzip_dir_path = work_report_templates_path.joinpath(dir_name)

        return unzip_dir_path

    def _add_report_template(self, unzip_dir_path: Path, template_name: str, guideline_id: int) -> int:
        try:
            # base_report_format.html存在チェック
            base_report_format_html_file = unzip_dir_path / 'base_report_format.html'
            if not base_report_format_html_file.exists():
                raise QAIInvalidRequestException(result_code='R02003',
                                                 result_msg='not found base_report_format.html in zip.')

            # base_report.css存在チェック
            base_report_css_file = unzip_dir_path / 'css/base_report.css'
            if not base_report_css_file.exists():
                raise QAIInvalidRequestException(result_code='R02004',
                                                 result_msg='not found base_report.css in zip.')

            # ガイドラインの存在チェック
            guideline = GuidelineMapper.query.filter(GuidelineMapper.id == guideline_id).first()
            if guideline is None:
                raise QAINotFoundException('R02005', 'not found guideline')

            # 同じ名前とガイドラインIDの存在確認
            report_template_exist = ReportTemplateMapper.query.filter(ReportTemplateMapper.name == template_name) \
                                                              .filter(ReportTemplateMapper.guideline_id == guideline_id) \
                                                              .first()
            if report_template_exist is not None:
                # 存在していたらupdate_datetimeを更新
                report_template_exist.update_datetime = datetime.utcnow()
                sql_db.session.flush()
                report_template_id = report_template_exist.id
            else:
                # 存在しなかったら新規登録
                report_template_mapper = ReportTemplateMapper(name=template_name,
                                                              guideline_id=guideline_id)
                sql_db.session.add(report_template_mapper)
                sql_db.session.flush()
                report_template_id = report_template_mapper.id

            # レポートテンプレートIDのディレクトリパス
            report_template_dir_path = self.root_report_templates_path.joinpath(str(report_template_id))

            # 存在するレポートテンプレートIDのディレクトリがあれば一度リネームしておく
            old_report_template_dir_path = str(report_template_dir_path) + '_old'
            if report_template_dir_path.exists():
                os.rename(str(report_template_dir_path), old_report_template_dir_path)

            try:
                # ファイルのコピー
                shutil.copytree(str(unzip_dir_path), report_template_dir_path)
            except Exception as e:
                # ファイルのコピーが失敗したら、リネームした元ディレクトリの名前を戻す
                os.rename(old_report_template_dir_path, str(report_template_dir_path))
            else:
                # 正常終了時は、リネームした元ディレクトリを削除
                if Path(old_report_template_dir_path).exists():
                    shutil.rmtree(old_report_template_dir_path)

            sql_db.session.commit()

        except QAIException as e:
            sql_db.session.rollback()
            raise e
        except SQLAlchemyError as e:
            sql_db.session.rollback()
            raise QAIInvalidRequestException('R02999', 'database error: {}'.format(e))
        return report_template_id

    @log(logger)
    # レポートテンプレートひな型作成
    def post_generate(self, guideline_id: int):
        # 作業フォルダ
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        work_report_templates_path = self.root_report_template_format_path.joinpath(timestamp, 'dummy')

        try:
            # ガイドラインの存在確認
            guideline = GuidelineMapper.query.filter(GuidelineMapper.id == guideline_id).first()
            if guideline is None:
                raise QAINotFoundException('R03001', 'not found guideline')

            # ガイドラインに品質特性が存在するか確認
            quality_dim = QualityDimensionMapper.query.filter(QualityDimensionMapper.guideline_id == guideline_id).all()
            if not quality_dim:
                raise QAINotFoundException('R03002', 'not found QualityDimension')

            work_report_templates_path = self.root_report_template_format_path.joinpath(timestamp, guideline.name)

            # 作業フォルダにテンプレートフォルダをコピー
            shutil.copytree(str(self.root_report_template_path), str(work_report_templates_path))

            # zip圧縮
            guideline_name_path = self.root_report_template_format_path.joinpath(guideline.name + timestamp)
            shutil.make_archive(str(guideline_name_path), 'zip', root_dir=str(work_report_templates_path.parent))

            zip_file_path = str(guideline_name_path) + '.zip'
            response = make_response()
            response.data = open(zip_file_path, "rb").read()

            file_name = guideline.name + '.zip'
            response.headers['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}'.format(quote(file_name.encode('utf-8')))
            # MIME設定
            response.mime_type = 'application/zip'

            # zip削除
            if os.path.isfile(zip_file_path):
                os.remove(zip_file_path)

        except QAIException as e:
            raise e
        except SQLAlchemyError as e:
            raise QAIInvalidRequestException('R03999', 'database error: {}'.format(e))
        finally:
            # 作業フォルダ削除
            if work_report_templates_path.exists():
                shutil.rmtree(str(work_report_templates_path.parent))
        return response

    @log(logger)
    # レポートテンプレートテーブルzip出力
    def get_zip(self, report_template_id: int):
        # 作業フォルダ
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        work_report_templates_path = self.root_report_templates_path.joinpath(timestamp)

        try:
            # レポートテンプレートのDB存在確認
            report_template = ReportTemplateMapper.query.filter(ReportTemplateMapper.id == report_template_id).first()
            if report_template is None:
                raise QAINotFoundException('R04001', 'not found ReportTemplate in DB')

            # レポートテンプレートのディレクトリ存在確認
            report_template_dir = self.root_report_templates_path.joinpath(str(report_template.id))
            if not report_template_dir.exists():
                raise QAINotFoundException('R04002', 'not found ReportTemplate in directory')

            # 作業フォルダにコピー
            work_report_templates_name_path = work_report_templates_path.joinpath(report_template.name)
            shutil.copytree(str(report_template_dir), str(work_report_templates_name_path))

            # zip圧縮
            report_template_path = self.root_report_templates_path.joinpath(report_template.name)
            shutil.make_archive(str(report_template_path), 'zip', root_dir=str(work_report_templates_path))

            zip_file_path = str(report_template_path) + '.zip'
            response = make_response()
            response.data = open(zip_file_path, "rb").read()

            file_name = report_template.name + '.zip'
            response.headers['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'{}'.format(quote(file_name.encode('utf-8')))
            # MIME設定
            response.mime_type = 'application/zip'

            # zip削除
            if os.path.isfile(zip_file_path):
                os.remove(zip_file_path)

        except QAIException as e:
            raise e
        except SQLAlchemyError as e:
            raise QAIInvalidRequestException('R04999', 'database error: {}'.format(e))
        finally:
            # 作業フォルダ削除
            if work_report_templates_path.exists():
                shutil.rmtree(str(work_report_templates_path))
        return response

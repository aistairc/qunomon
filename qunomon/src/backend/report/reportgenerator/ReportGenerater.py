from sqlalchemy.sql.sqltypes import Boolean
import pdfkit
import os
import shutil
import re
import reportgenerator.ResourceCollector
import reportgenerator.ResourceManager
import reportgenerator.SectionReportMaker
import reportgenerator.BaseReportGenerater
from distutils.dir_util import copy_tree, remove_tree
import reportgenerator.Tools as tools
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

DEF_RESOURCE_DIR = "tds_results" + os.sep
DEF_WORK_DIR = "work" + os.sep
DEF_SUMMARY_DIR = "summary" + os.sep
DEF_TEMPLATE_DIR = "template" + os.sep

class ReportGenerator():
    home_path     = ""
    resource_path = ""
    work_path     = ""
    template_path = ""

    def __init__(self, home_path):
        self.home_path     = home_path
        self.resource_path = self.home_path + DEF_RESOURCE_DIR
        self.work_path     = self.home_path + DEF_WORK_DIR
        self.template_path = self.home_path + DEF_TEMPLATE_DIR
        self.summary_path  = self.work_path + DEF_SUMMARY_DIR

    def __init_resource(self):
        # ディレクトリ初期化
        if os.path.exists(self.work_path):
            remove_tree(self.work_path)
        if os.path.exists(self.resource_path):
            remove_tree(self.resource_path)
        # if not os.path.exists(self.template_path):
        #     remove_tree(self.template_path)
        os.mkdir(self.resource_path)
        os.mkdir(self.work_path)
        # os.mkdir(self.template_path)

    def make_reporthtml(self, report_dataset: dict):
        try:
            # 全リソースからレポート出力用のHTMLを作成
            rm = reportgenerator.ResourceManager(self.template_path, report_dataset)
            rm.make_testdescription_result(self.work_path)

            summary_file_path = self.summary_path+'summary.html'
            rm.make_summary_result(self.work_path, self.summary_path, summary_file_path)

            # work_pathに空のbase_report.htmlを作成
            output_filepath   = self.work_path + 'base_report.html'
            tools.write_file(output_filepath, "")

            sm = reportgenerator.SectionReportMaker(self.work_path, summary_file_path, report_dataset)
            # template_pathに生成されたbase_report.htmlでwork_path直下のbase_report.htmlに内容をコピーする
            with open(self.template_path + "base_report.html", mode="rt", encoding="utf-8_sig") as file:
                for line in file:
                    match = re.search("<!--%%[A-Z0-9_]*%%-->", line)
                    if match:
                        html_iframe = sm.collation_replacement_str(match.group())
                        if html_iframe is None:
                            tools.write_file(output_filepath, line, "a")
                        else:
                            tools.write_file(output_filepath, line.replace(match.group(), html_iframe), "a")
                    else:
                        tools.write_file(output_filepath, line, "a")
        except Exception as e:
            raise e

    def export_pdf(self, pdf_path: str):
        print('ReportGenerator() export_pdf() start')
        # PDF変換
        try:
            options = {
                'page-size': 'A4',
                'margin-top': '0.1in',
                'margin-right': '0.1in',
                'margin-bottom': '0.1in',
                'margin-left': '0.1in',
                'encoding': "UTF-8",
                'no-outline': None
            }
            # work_patht直下のbase_report.htmlでPDFを生成する
            pdfkit.from_file(self.work_path + "base_report.html", pdf_path, options=options)
        except Exception as e:
            raise e
        return 1

    def report_generate(self, db_info: SQLAlchemy, downloadfiles_json: str, pdf_path: str = "UNSPECIFIED",
                        template_format_path: str = "",
                        target_report_template_flag: Boolean = False,
                        app_debug_flg: Flask = None):
        try:
            # 作業ディレクトリ初期化
            self.__init_resource()
            # テスト結果取得
            rc = reportgenerator.ResourceCollector()
            report_dataset = rc.collect(app_debug_flg, db_info, self.resource_path, downloadfiles_json, self.work_path)

            # base_report.htmlの作成
            brg = reportgenerator.BaseReportGenerater(home_path=self.home_path, 
                                                      format_path=template_format_path)

            if not target_report_template_flag:
                # template_idを指定されない場合は、ダミーのテンプレートでbase_report.htmlを生成する
                brg.make_base_report_html(report_dataset)
            else:
                # template_idを指定された場合は、ユーザ作成済みのテンプレートでbase_report.htmlを生成する
                brg.make_base_report_html_with_user_create_template(report_dataset)

            # templateからworkへの必要ファイルコピー
            copy_tree(self.resource_path, self.work_path)

            # レポート生成
            self.make_reporthtml(report_dataset)

            # PDF生成
            pdf_path = self.work_path + "report.pdf" if pdf_path == "UNSPECIFIED" else pdf_path
            self.export_pdf(pdf_path)

            # exportしたPDFのpathを返す。
            return pdf_path
        except Exception as e:
            print("ReportGeneratorException: {}".format(e))
        return None


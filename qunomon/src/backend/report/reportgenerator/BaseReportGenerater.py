import os
from pathlib import Path
import shutil

from jinja2 import Environment, FileSystemLoader
from qlib.utils.logging import get_logger, log

logger = get_logger()

DEF_TEMPLATE_DIR = "template" + os.sep


class BaseReportGenerater():
    home_path = ""
    template_path = ""
    format_path = ""

    def __init__(self, home_path, format_path):
        self.home_path = home_path
        self.template_path = self.home_path + DEF_TEMPLATE_DIR
        self.format_path = format_path

    @log(logger)
    def make_base_report_html(self, report_dataset: dict):
        data = {}
        data['guideline']   = report_dataset['Guideline']
        data['user']        = report_dataset['User']
        data['inventories'] = report_dataset['Inventories']
        data['opinion']     = report_dataset['Opinion']

        # テンプレートなしの場合、format_pathからbase_report_format.htmlを取得する
        env = Environment(loader=FileSystemLoader(self.format_path))
        template = env.get_template('base_report_format.html')

        # cssの中身を複製
        src_css_path = Path(self.format_path)   / 'css'
        dst_css_path = Path(self.template_path) / 'css'
        src_css_ls = os.listdir(path=src_css_path)
        os.makedirs(dst_css_path, exist_ok=True)
        for filename in src_css_ls:
            shutil.copy(src_css_path/filename, dst_css_path)

        try:
            # base_report.htmlを作成する
            with open(self.template_path + 'base_report.html', 'w', encoding="utf-8_sig") as f:
                print(template.render(data), file=f)

        except Exception as e:
            raise e
    
    @log(logger)
    def make_base_report_html_with_user_create_template(self, report_dataset: dict):
        data = {}
        data['guideline']   = report_dataset['Guideline']
        data['user']        = report_dataset['User']
        data['inventories'] = report_dataset['Inventories']
        data['opinion']     = report_dataset['Opinion']

        # テンプレートありの場合、template_pathからbase_report_format.htmlを取得する
        env = Environment(loader=FileSystemLoader(self.template_path))
        template = env.get_template('base_report_format.html')

        try:
            # base_report.htmlを作成する
            with open(self.template_path + 'base_report.html', 'w', encoding="utf-8_sig") as f:
                print(template.render(data), file=f)

        except Exception as e:
            raise e

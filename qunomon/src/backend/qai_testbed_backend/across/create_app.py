# Copyright c 2019 National Institute of Advanced Industrial Science and Technology �iAIST�j. All rights reserved.

import flask
from flask_injector import FlaskInjector
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager
from pathlib import Path
import shutil
import os
import requests
import json

from ..controllers import api
from ..gateways import extensions, config
from ..gateways.auth import jwt
from ..di_module import di_module
from .init_db_local import init_db
from ..entities.setting import SettingMapper
from ..entities.guideline import GuidelineMapper
from ..entities.report_template import ReportTemplateMapper
from ..usecases.guideline_schema_file import GuidelineSchemaFileService

jwt_mng = JWTManager()

def create_app(config_name='default', is_init_db: bool = True):
    """Flask app factory
    :config_name: a string object.
    :returns: flask.Flask object
    """

    app = flask.Flask(__name__)

    # set the config vars using the config name and current_app
    config.config[config_name](app)

    jwt.set_jwt_handlers(extensions.jwt)

    register_extensions(app)
    register_blueprints(app)

    if is_init_db:
        init_db(app, config_name=config_name)

    clean_up_mount_dir(app)

    FlaskInjector(app=app, modules=[di_module])

    Limiter(app, key_func=get_remote_address, default_limits=["100 per minute"])

    jwt_mng.init_app(app)

    return app


def register_extensions(app):
    """Call the method 'init_app' to register the extensions in the flask.Flask
    object passed as parameter.
    :app: flask.Flask object
    :returns: None
    """
    extensions.jwt.init_app(app)
    extensions.sql_db.init_app(app)
    extensions.ma.init_app(app)


def register_blueprints(app):
    """Register all blueprints.
    :app: flask.Flask object
    :returns: None
    """
    app.register_blueprint(api.blueprint)


def clean_up_mount_dir(app):
    with app.app_context():
        # windowsとLinuxで格納先を変更する
        if os.name == 'nt':
            mount_root_path = Path(SettingMapper.query.get('mount_src_path').value)
        else:
            mount_root_path = Path(SettingMapper.query.get('mount_dst_path').value)

        inventory_check_result_path = mount_root_path / 'inventory_check'
        if inventory_check_result_path.exists():
            shutil.rmtree(str(inventory_check_result_path))

def init_guideline(app):
    with app.app_context():

        # ガイドラインスキーマファイルパスを取得
        guideline_schema_files_path = SettingMapper.query.get('guideline_schema_files_path').value

        # ガイドラインスキーマファイル毎に登録
        for guideline_schema_file_name in os.listdir(guideline_schema_files_path):

            # ガイドラインスキーマファイル
            guideline_schema_file = guideline_schema_files_path + '/' + guideline_schema_file_name
        
            with open(str(guideline_schema_file), encoding='utf-8') as gs_file:
                # ガイドラインスキーマをJSONファイルに変更
                guideline_schema_json = json.load(gs_file)
            
            # ガイドライン名称を取得
            for gsj in guideline_schema_json["guideline"]["meta_info"]:
                if gsj["property"] == 'title':
                    guideline_name = gsj["content"]

            if guideline_name is not None and len(guideline_name) != 0 and ' ' not in guideline_name:
                if GuidelineMapper.query.filter(GuidelineMapper.name == guideline_name).\
                    filter(GuidelineMapper.delete_flag.is_(False)).first() is None:
        
                    # ガイドラインスキーマファイルファイルから登録
                    GuidelineSchemaFileService().post(guideline_schema_json)

                    # M_ReportTemplateにレコード追加
                    report_template = ReportTemplateMapper(name='AIQM Report Template',
                                                           guideline_id=1)

                    extensions.sql_db.session.add(report_template)
                    extensions.sql_db.session.commit()
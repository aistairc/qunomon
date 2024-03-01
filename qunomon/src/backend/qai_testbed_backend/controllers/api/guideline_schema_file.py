# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from qlib.utils.logging import get_logger, log

from ..dto import ResultSchema, Result
from ..dto.guideline_schema_file import GetGuidelineSchemaFileResSchema, PostGuidelineSchemaFileResSchema, \
    PutGuidelineSchemaFileResSchema, DeleteGuidelineSchemaFileResSchema, CheckGuidelineSchemaFileResSchema
from ...usecases.guideline_schema_file import GuidelineSchemaFileService
from ...across.exception import QAIException
from tempfile import TemporaryDirectory
import json
import pathlib
import os


logger = get_logger()


class GuidelineSchemaFileCoreAPI(Resource):

    def __init__(self):
        self.service = GuidelineSchemaFileService()

    @log(logger)

    def post(self):
        """
        ガイドラインスキーマファイルからガイドライン登録
        """
        try:
            guideline_schema_file = request.files['guideline_schema']
            guideline_aithub_id = request.form['guideline_aithub_id']

            with TemporaryDirectory() as temp_dir:
                # ファイルをtmpフォルダに保存
                filename = os.path.basename(guideline_schema_file.filename)
                p_temp_dir = pathlib.Path(temp_dir)
                save_path = p_temp_dir.joinpath(filename)
                guideline_schema_file.save(str(save_path))
                # ファイルをオープン
                with open(str(save_path), mode='r', encoding='utf-8') as f:
                    guideline_schema_json = json.load(f)
            
            # ローカルガイドライン登録の場合
            if guideline_aithub_id == "":
                res = self.service.post(guideline_schema_json)
            # AITHUBからガイドライン登録の場合
            else:
                res = self.service.post(guideline_schema_json, int(guideline_aithub_id))
            
            return PostGuidelineSchemaFileResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='G25999', message='internal server error: {}'.format(e))), 500

class GuidelineSchemaFileAPI(GuidelineSchemaFileCoreAPI):

    def __init__(self):
        self.service = GuidelineSchemaFileService()

    # csfrトークンチェックなし
    @log(logger)
    def post(self):
        # スーパークラスのpostを呼び出す
        res = super().post()
        return res


class GuidelineSchemaFileFrontAPI(GuidelineSchemaFileCoreAPI):

    def __init__(self):
        self.service = GuidelineSchemaFileService()

    # csfrトークンチェックあり
    @jwt_required()
    @log(logger)
    def post(self):
        # スーパークラスのpostを呼び出す
        res = super().post()
        return res


class GuidelineSchemaFileDetailCoreAPI(Resource):

    def __init__(self):
        self.service = GuidelineSchemaFileService()

    @log(logger)

    def put(self, guideline_id: str):
        """
        ガイドラインスキーマファイルからガイドライン更新。
        """
        try:
            res = self.service.put(int(guideline_id), request)
            return PutGuidelineSchemaFileResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='G27999', message='internal server error: {}'.format(e))), 500

    def delete(self, guideline_id: str):
        """
        ガイドライン削除。
        """
        try:
            res = self.service.delete(int(guideline_id))
            return DeleteGuidelineSchemaFileResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='G28999', message='internal server error: {}'.format(e))), 500


class GuidelineSchemaFileDetailAPI(GuidelineSchemaFileDetailCoreAPI):

    def __init__(self):
        self.service = GuidelineSchemaFileService()

    @log(logger)
    def get(self, guideline_id: str):
        """
        ガイドラインスキーマファイル取得。
        """
        try:
            res = self.service.get(int(guideline_id))
            return GetGuidelineSchemaFileResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='G26999', message='internal server error: {}'.format(e))), 500

    # csfrトークンチェックなし
    @log(logger)
    def put(self, guideline_id: str):
        # スーパークラスのputを呼び出す
        res = super().put(guideline_id)
        return res

    # csfrトークンチェックなし
    @log(logger)
    def delete(self, guideline_id: str):
        # スーパークラスのdeleteを呼び出す
        res = super().delete(guideline_id)
        return res


class GuidelineSchemaFileDetailFrontAPI(GuidelineSchemaFileDetailCoreAPI):

    def __init__(self):
        self.service = GuidelineSchemaFileService()

    # csfrトークンチェックあり
    @jwt_required()
    @log(logger)
    def put(self, guideline_id: str):
        # スーパークラスのputを呼び出す
        res = super().put(guideline_id)
        return res

    # csfrトークンチェックあり
    @jwt_required()
    @log(logger)
    def delete(self, guideline_id: str):
        # スーパークラスのdeleteを呼び出す
        res = super().delete(guideline_id)
        return res


class GuidelineSchemaFileEditCheckAPI(Resource):

    def __init__(self):
        self.service = GuidelineSchemaFileService()

    @log(logger)

    def get(self, guideline_id: str):
        """
        ガイドライン編集チェック。
        """
        try:
            res = self.service.edit_check(int(guideline_id), request)
            return CheckGuidelineSchemaFileResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='G29999', message='internal server error: {}'.format(e))), 500

class GuidelineSchemaFileDeleteCheckAPI(Resource):

    def __init__(self):
        self.service = GuidelineSchemaFileService()

    @log(logger)

    def get(self, guideline_id: str):
        """
        ガイドライン削除チェック。
        """
        try:
            res = self.service.delete_check(int(guideline_id))
            return CheckGuidelineSchemaFileResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='G30999', message='internal server error: {}'.format(e))), 500

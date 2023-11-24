# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import requests
import datetime

from sqlalchemy.exc import SQLAlchemyError
from requests.exceptions import RequestException
from qlib.utils.logging import get_logger, log

from ..controllers.dto import Result
from ..controllers.dto.guideline_schema_file import PostGuidelineSchemaFileRes, GetGuidelineSchemaFileRes, \
    PutGuidelineSchemaFileRes, DeleteGuidelineSchemaFileRes, CheckGuidelineSchemaFileRes
from ..entities.guideline import GuidelineMapper
from ..entities.guideline_schema_file import GuidelineSchemaFileMapper
from ..entities.ml_component import MLComponentMapper
from ..entities.quality_dimension import QualityDimensionMapper
from ..entities.quality_dimension_level import QualityDimensionLevelMapper
from ..entities.scope import ScopeMapper
from ..entities.scope_quality_dimension import ScopeQualityDimensionMapper
from ..entities.test_description import TestDescriptionMapper
from ..across.exception import QAINotFoundException, QAIInternalServerException, QAIBadRequestException, \
    QAIException, QAIInvalidRequestException
from ..gateways.extensions import sql_db

from tempfile import TemporaryDirectory
import json
import pathlib
import os

logger = get_logger()


class GuidelineSchemaFileService:
    @log(logger)

    def get(self, guideline_id: int) -> GetGuidelineSchemaFileRes:

        gsf_mapper = GuidelineSchemaFileMapper.query\
            .filter(GuidelineSchemaFileMapper.delete_flag.is_(False))\
            .filter(GuidelineSchemaFileMapper.guideline_id == guideline_id).one_or_none()

        # 存在しないまたは削除されている場合エラー
        if gsf_mapper is None:
            raise QAINotFoundException(result_code='G26404', result_msg='Not found.')

        # ガイドラインスキーマファイル
        source_file = gsf_mapper.guideline_schema_file

        return GetGuidelineSchemaFileRes(
            result=Result(code='G26000', message='Success.'),
            guideline_schema_file=source_file
        )

    def post(self, guideline_schema_json, guideline_aithub_id = None) -> PostGuidelineSchemaFileRes:
        try:
            g_file_id = 0
            guideline_name = ""
            creator = ""
            publisher = ""
            identifier = ""
            publish_datetime = ""
            description = ""

            for gsj in guideline_schema_json["guideline"]["meta_info"]:
                if gsj["property"] == 'title':
                    guideline_name = gsj["content"]
                if gsj["property"] == 'creator':
                    creator = gsj["content"]
                if gsj["property"] == 'publisher':
                    publisher = gsj["content"]
                if gsj["property"] == 'identifier':
                    identifier = gsj["content"]
                if gsj["property"] == 'date':
                    publish_datetime = gsj["content"]
                if gsj["property"] == 'description':
                    description = gsj["content"]

            # Guidelineテーブル
            # 入力チェック
            # Nameの存在確認、項目が存在しない場合、空文字の場合、スペースが含まれている場合エラー
            if guideline_name is None or len(guideline_name) == 0 or ' ' in guideline_name:
                raise QAIBadRequestException(result_code='G25400', 
                                                result_msg='invalid request. (guideline name is empty or contains space)')
            
            # 既に存在するガイドライン名の場合エラー
            if GuidelineMapper.query.filter(GuidelineMapper.name == guideline_name).\
                    filter(GuidelineMapper.delete_flag.is_(False)).first() is not None:
                raise QAIBadRequestException(result_code='G25400', 
                                                result_msg='invalid request. (guideline existed)')

            # ガイドラインテーブル登録
            guideline = GuidelineMapper(
                aithub_guideline_id=guideline_aithub_id,
                name=guideline_name,
                description=description,
                creator=creator,
                publisher=publisher,
                identifier=identifier,
                publish_datetime=datetime.datetime.strptime(publish_datetime, '%Y-%m-%d')
            )

            sql_db.session.add(guideline)
            sql_db.session.flush()

            guideline_id = guideline.id

            # Quality_dimensionテーブル登録
            qd_key_dick = {}
            guideline_schema_qd_list = guideline_schema_json["guideline"]["quality_dimensions"]

            # Quality_dimension名称dick
            qd_name_dick = {}
            for qd in guideline_schema_qd_list:
                qd_name_dick.update({qd["id"] : qd["name"]})

            for qd in guideline_schema_qd_list:
                # 入力チェック
                # 品質特性名が存在しないまたは空文字の場合
                # 品質特性名にスペースが含まれている場合
                qd_name = qd["name"]
                if qd_name is None or qd_name == '' or ' ' in qd_name:
                    raise QAIBadRequestException(result_code='G25400', 
                                                    result_msg='invalid request. (quality dimension name is empty or contains space)')

                # 同じ名称で品質特性を作成しようとした場合エラー
                if QualityDimensionMapper.query.filter(QualityDimensionMapper.name == qd_name).\
                        filter(QualityDimensionMapper.delete_flag.is_(False)).one_or_none() is not None:
                    raise QAIBadRequestException(result_code='G25400', 
                                                    result_msg='invalid request.(quality dimension existed)')

                quality_dimension = QualityDimensionMapper(
                    json_id=qd["id"],
                    name=qd_name,
                    description=qd["description"],
                    guideline_id=guideline_id
                )

                # サブ品質特性の編集
                if qd.get('sub_dimensions') is not None and len(qd.get('sub_dimensions')) > 0 :
                    sub_dimensions = qd["sub_dimensions"]
                    sub_dimensions_edited = list(map(lambda sub_qd: qd_name_dick.get(sub_qd), sub_dimensions))
                    sub_dimensions_filtered = list(filter(lambda s: s is not None, sub_dimensions_edited))

                    if len(sub_dimensions_filtered) > 0:
                        quality_dimension.sub_dimensions = ",".join(sub_dimensions_filtered)

                sql_db.session.add(quality_dimension)
                sql_db.session.flush()

                qd_key_dick.update({qd["id"] : quality_dimension.id})

                # 品質特性レベルが存在したら登録
                if qd.get('levels') is not None and len(qd.get('levels')) > 0:
                    for qd_level in qd["levels"]:
                        # nameは無い場合がある
                        qd_level_name = ""
                        if qd_level.get("name") is not None:
                            qd_level_name = qd_level["name"]

                        qd_level_mapper = QualityDimensionLevelMapper(
                            quality_dimension_level_id=qd_level["id"],
                            name=qd_level_name,
                            description=qd_level["description"],
                            level=qd_level["level"],
                            quality_dimension_id=quality_dimension.id
                        )
                        sql_db.session.add(qd_level_mapper)
                        sql_db.session.flush()

            # Scopeテーブル
            for scp in guideline_schema_json["guideline"]["scopes"]:
                scope = ScopeMapper(
                    name=scp["name"],
                    guideline_id=guideline_id
                )

                sql_db.session.add(scope)
                sql_db.session.flush()

                # Scope_QualityDimensionテーブル登録
                scope_id = scope.id
                for scp_qd_key in scp["quality_scopes"].get("quality_dimensions"):

                    if scp_qd_key not in qd_key_dick :
                        raise QAIBadRequestException(result_code='G25400', 
                                                        result_msg='invalid request. (scope : quality dimension not exist)')

                    quality_dimension_id = qd_key_dick.get(scp_qd_key)

                    scope_quality_dimension = ScopeQualityDimensionMapper(
                        guideline_id=guideline_id,
                        scope_id=scope_id,
                        quality_dimension_id=quality_dimension_id
                    )
                    sql_db.session.add(scope_quality_dimension)
                    sql_db.session.flush()

            # Guideline_Schema_Fileテーブル登録
            guideline_schema_file_mapper = GuidelineSchemaFileMapper(name=guideline_name,
                                                                        guideline_id=guideline_id,
                                                                        guideline_schema_file=guideline_schema_json)
            sql_db.session.add(guideline_schema_file_mapper)
            sql_db.session.commit()

            g_file_id = guideline_schema_file_mapper.id

        except QAIException as e:
            sql_db.session.rollback()
            raise e
        except Exception as e:
            sql_db.session.rollback()
            raise QAIInternalServerException('G25999', 'internal server error: {}'.format(e))
        return PostGuidelineSchemaFileRes(
            result=Result(code='G25000', message="append Guideline success."),
            guideline_schema_file_id=g_file_id
        )

    def put(self, guideline_id: int, request) -> PutGuidelineSchemaFileRes:

        # Guideline_Schema_Fileテーブル
        gsf_mapper = GuidelineSchemaFileMapper.query\
            .filter(GuidelineSchemaFileMapper.delete_flag.is_(False))\
            .filter(GuidelineSchemaFileMapper.guideline_id == guideline_id).first()
        # 存在しないまたは削除されている場合エラー
        if gsf_mapper is None:
            raise QAINotFoundException(result_code='G27404', result_msg='Not found.')

        # ガイドラインテーブル
        guideline_mapper = GuidelineMapper.query.\
            filter(GuidelineMapper.id == guideline_id).\
            filter(GuidelineMapper.delete_flag.is_(False)).first()
        # 存在しないまたは削除されている場合エラー
        if guideline_mapper is None:
            raise QAINotFoundException(result_code='G27404', result_msg='Not found.')

        # scopeテーブル
        scope_mapper = ScopeMapper.query. \
            filter(ScopeMapper.guideline_id == guideline_id). \
            filter(ScopeMapper.delete_flag.is_(False)).all()
        # 全部削除フラグをTrueにしておく（後でupdateする時にFalseに戻す → updateされないデータは削除のままになる）
        for scp in scope_mapper:
            scp.update_datetime = datetime.datetime.utcnow()
            scp.delete_flag = True

        # quality_dimensionsテーブル
        quality_dimensions_mapper = QualityDimensionMapper.query. \
            filter(QualityDimensionMapper.delete_flag.is_(False)). \
            filter(QualityDimensionMapper.guideline_id == guideline_id).all()
        # 全部削除フラグをTrueにしておく（後でupdateする時にFalseに戻す → updateされないデータは削除のままになる）
        for qd in quality_dimensions_mapper:
            qd.delete_flag = True
            for qdl in qd.quality_dimension_level:
                qdl.update_datetime = datetime.datetime.utcnow()
                qdl.delete_flag = True
        
        sqd_mapper = ScopeQualityDimensionMapper.query. \
            filter(ScopeQualityDimensionMapper.delete_flag.is_(False)). \
            filter(ScopeQualityDimensionMapper.guideline_id == guideline_id).all()
        # ScopeQualityDimensionは全部削除
        for sqd in sqd_mapper:
            sqd.update_datetime = datetime.datetime.utcnow()
            sqd.delete_flag = True

        try:
            with TemporaryDirectory() as temp_dir:

                # ファイルをtmpフォルダに保存
                file = request.files['guideline_schema']
                filename = os.path.basename(file.filename)
                p_temp_dir = pathlib.Path(temp_dir)
                save_path = p_temp_dir.joinpath(filename)
                file.save(str(save_path))

                g_file_id = 0
                guideline_name = ""
                creator = ""
                publisher = ""
                identifier = ""
                publish_datetime = ""
                description = ""

                # ファイルをオープン
                with open(str(save_path), mode='r', encoding='utf-8') as f:
                    guideline_schema_json = json.load(f)

                    for gsj in guideline_schema_json["guideline"]["meta_info"]:
                        if gsj["property"] == 'title':
                            guideline_name = gsj["content"]
                        if gsj["property"] == 'creator':
                            creator = gsj["content"]
                        if gsj["property"] == 'publisher':
                            publisher = gsj["content"]
                        if gsj["property"] == 'identifier':
                            identifier = gsj["content"]
                        if gsj["property"] == 'date':
                            publish_datetime = gsj["content"]
                        if gsj["property"] == 'description':
                            description = gsj["content"]

                    # Guidelineテーブル
                    # 入力チェック
                    # Nameの存在確認、項目が存在しない場合、空文字の場合、スペースが含まれている場合エラー
                    if guideline_name is None or len(guideline_name) == 0 or ' ' in guideline_name:
                        raise QAIBadRequestException(result_code='G27400', 
                                                     result_msg='invalid request. (guideline name is empty or contains space)')
                    
                    # ガイドライン名が違う場合はエラー（ガイドライン名を変える場合は新規登録になる）
                    if guideline_name != guideline_mapper.name:
                        raise QAIBadRequestException(result_code='G27400', 
                                                     result_msg='invalid request. (guideline name is changed)')

                    # ガイドラインテーブル更新
                    guideline_mapper.description = description
                    guideline_mapper.creator = creator
                    guideline_mapper.publisher = publisher
                    guideline_mapper.identifier = identifier
                    guideline_mapper.publish_datetime = datetime.datetime.strptime(publish_datetime, '%Y-%m-%d')
                    guideline_mapper.update_datetime = datetime.datetime.utcnow()
                    sql_db.session.flush()

                    # quality_dimensionsテーブル更新
                    qd_key_dick = {}
                    guideline_schema_qd_list = guideline_schema_json["guideline"]["quality_dimensions"]

                    # Quality_dimension名称dick
                    qd_name_dick = {}
                    for qd in guideline_schema_qd_list:
                        qd_name_dick.update({qd["id"] : qd["name"]})

                    for qd in guideline_schema_qd_list:
                        # 入力チェック
                        # 品質特性名が存在しないまたは空文字の場合
                        # 品質特性名にスペースが含まれている場合
                        qd_name = qd["name"]
                        if qd_name is None or qd_name == '' or ' ' in qd_name:
                            raise QAIBadRequestException(result_code='G27400', 
                                                         result_msg='invalid request. (quality dimension name is empty or contains space)')

                        qd_exist_flag = False
                        # quality_dimensionsテーブル
                        for qd_before in quality_dimensions_mapper:
                            # IDが同じQDが存在すれば更新する
                            if qd_before.json_id == qd["id"]:
                                qd_before.name = qd["name"]
                                qd_before.description = qd["description"]
                                qd_before.update_datetime = datetime.datetime.utcnow()
                                qd_before.delete_flag = False
                                qd_exist_flag = True
                                break

                        # IDが存在しなければ新規登録する
                        if not qd_exist_flag:
                            qd_new = QualityDimensionMapper(
                                json_id=qd["id"],
                                name=qd_name,
                                description=qd["description"],
                                guideline_id=guideline_mapper.id
                            )
                            sql_db.session.add(qd_new)
                            sql_db.session.flush()

                        # サブ品質特性の編集
                        if qd.get('sub_dimensions') is not None and len(qd.get('sub_dimensions')) > 0 :
                            sub_dimensions = qd["sub_dimensions"]
                            sub_dimensions_edited = list(map(lambda sub_qd: qd_name_dick.get(sub_qd), sub_dimensions))
                            sub_dimensions_filtered = list(filter(lambda s: s is not None, sub_dimensions_edited))

                            if len(sub_dimensions_filtered) > 0:
                                if qd_exist_flag:
                                    # 更新
                                    qd_before.sub_dimensions = ",".join(sub_dimensions_filtered)
                                else:
                                    # 新規
                                    qd_new.sub_dimensions = ",".join(sub_dimensions_filtered)

                        if qd_exist_flag:
                            # 更新
                            qd_key_dick.update({qd["id"] : qd_before.id})
                        else:
                            # 新規
                            qd_key_dick.update({qd["id"] : qd_new.id})

                        # 品質特性レベルが存在したら登録
                        if qd.get('levels') is not None and len(qd.get('levels')) > 0 :

                            for qd_level in qd["levels"]:
                                # nameは無い場合がある
                                qd_level_name = ""
                                if qd_level.get("name") is not None:
                                    qd_level_name = qd_level["name"]

                                # QDを更新する場合
                                if qd_exist_flag:
                                    for qdl in qd_before.quality_dimension_level:
                                        qdl_exist_flag = False
                                        # 同じIDなら更新
                                        if qdl.quality_dimension_level_id == qd_level["id"]:
                                            qdl.name = qd_level_name
                                            qdl.description = qd_level["description"]
                                            qdl.level = qd_level["level"]
                                            qdl.update_datetime = datetime.datetime.utcnow()
                                            qdl.delete_flag = False
                                            qdl_exist_flag = True
                                            break

                                    # QDあり、QDレベル無しの場合、新規登録
                                    if not qdl_exist_flag:
                                        qd_level_mapper = QualityDimensionLevelMapper(
                                            quality_dimension_level_id=qd_level["id"],
                                            name=qd_level_name,
                                            description=qd_level["description"],
                                            level=qd_level["level"],
                                            quality_dimension_id=qd_before.id
                                        )
                                        sql_db.session.add(qd_level_mapper)
                                        sql_db.session.flush()

                                else:
                                    # 新規登録
                                    qd_level_mapper = QualityDimensionLevelMapper(
                                        quality_dimension_level_id=qd_level["id"],
                                        name=qd_level_name,
                                        description=qd_level["description"],
                                        level=qd_level["level"],
                                        quality_dimension_id=qd_new.id
                                    )
                                    sql_db.session.add(qd_level_mapper)
                                    sql_db.session.flush()

                    # Scopeテーブル更新（nameをキーにする）
                    for scp in guideline_schema_json["guideline"]["scopes"]:
                        scope_exist_flag = False
                        for scope_before in scope_mapper:
                            if scp["name"] == scope_before.name:
                                # nameが同じなら更新
                                scope_before.update_datetime = datetime.datetime.utcnow()
                                scope_before.delete_flag = False
                                scope_exist_flag = True
                                break

                        # 存在しない場合は新規登録
                        if not scope_exist_flag:
                            scope_new = ScopeMapper(
                                name=scp["name"],
                                guideline_id=guideline_mapper.id
                            )
                            sql_db.session.add(scope_new)
                            sql_db.session.flush()

                        # Scope_ID
                        if scope_exist_flag:
                            scope_id = scope_before.id
                        else:
                            scope_id = scope_new.id
                        # Scope_QualityDimensionテーブルは全部新規登録
                        for scp_qd_key in scp["quality_scopes"].get("quality_dimensions"):

                            if scp_qd_key not in qd_key_dick :
                                raise QAIBadRequestException(result_code='G27400', 
                                                             result_msg='invalid request. (scope : quality dimension not exist)')

                            quality_dimension_id = qd_key_dick.get(scp_qd_key)

                            scope_quality_dimension = ScopeQualityDimensionMapper(
                                guideline_id=guideline_mapper.id,
                                scope_id=scope_id,
                                quality_dimension_id=quality_dimension_id
                            )
                            sql_db.session.add(scope_quality_dimension)
                            sql_db.session.flush()

                    # Guideline_Schema_Fileテーブル更新
                    gsf_mapper.guideline_schema_file = guideline_schema_json

                    sql_db.session.commit()

                    g_file_id = gsf_mapper.id

        except QAIException as e:
            sql_db.session.rollback()
            raise e
        except Exception as e:
            sql_db.session.rollback()
            raise QAIInternalServerException('G27999', 'internal server error: {}'.format(e))
        return PutGuidelineSchemaFileRes(
            result=Result(code='G27000', message="updated Guideline success."),
            guideline_schema_file_id=g_file_id
        )

    def delete(self, guideline_id: int) -> DeleteGuidelineSchemaFileRes:
        try:
            # Guideline_Schema_Fileテーブル
            gsf_mapper = GuidelineSchemaFileMapper.query\
                .filter(GuidelineSchemaFileMapper.delete_flag.is_(False))\
                .filter(GuidelineSchemaFileMapper.guideline_id == guideline_id).first()

            if gsf_mapper is None:
                raise QAINotFoundException('G28404', 'not found guideline')

            if gsf_mapper.delete_flag is True:
                raise QAINotFoundException('G28404', 'guideline has already been deleted')

            # Guideline_Schema_File削除
            gsf_mapper.update_datetime = datetime.datetime.utcnow()
            gsf_mapper.delete_flag = True
            sql_db.session.flush()
            
            guideline = GuidelineMapper.query. \
                filter(GuidelineMapper.id == guideline_id).first()

            if guideline is None:
                raise QAINotFoundException('G28404', 'not found guideline')

            if guideline.delete_flag is True:
                raise QAINotFoundException('G28404', 'guideline has already been deleted')

            # ガイドラインがMlComponentに登録済みの場合は削除不可
            ml_component = MLComponentMapper.query. \
                filter(MLComponentMapper.guideline_id == guideline_id). \
                filter(MLComponentMapper.delete_flag == False).all()
            if len(ml_component) > 0:
                raise QAIInvalidRequestException('G28403', 'guideline is already registered in MlComponent.')

            # guideline削除
            guideline.update_datetime = datetime.datetime.utcnow()
            guideline.delete_flag = True
            sql_db.session.flush()

            # scopes削除
            scopes = ScopeMapper.query. \
                filter(ScopeMapper.guideline_id == guideline_id).all()
            for scope in scopes:
                scope.update_datetime = datetime.datetime.utcnow()
                scope.delete_flag = True
            sql_db.session.flush()

            # quality_dimensions削除
            qds = QualityDimensionMapper.query. \
                filter(QualityDimensionMapper.guideline_id == guideline_id).all()
            for qd in qds:
                qd.update_datetime = datetime.datetime.utcnow()
                qd.delete_flag = True
            sql_db.session.flush()

            # scopes_quality_dimensions削除
            sqds = ScopeQualityDimensionMapper.query. \
                filter(ScopeQualityDimensionMapper.guideline_id == guideline_id).all()
            for sqd in sqds:
                sqd.update_datetime = datetime.datetime.utcnow()
                sqd.delete_flag = True
            sql_db.session.commit()

        except QAIException as e:
            sql_db.session.rollback()
            raise e
        except SQLAlchemyError as e:
            sql_db.session.rollback()
            raise QAIInvalidRequestException(result_code='G28999', result_msg='database error: {}'.format(e))
        except Exception as e:
            sql_db.session.rollback()
            raise QAIInternalServerException(result_code='G28999', result_msg='internal server error: {}'.format(e))

        return DeleteGuidelineSchemaFileRes(
            result=Result(code='G28000', message="delete success.")
        )

    def edit_check(self, guideline_id: int, request) -> CheckGuidelineSchemaFileRes:

        check_result = True
        warning_message = []

        # ガイドライン
        guideline_mapper = GuidelineMapper.query. \
            filter(GuidelineMapper.id == guideline_id).first()

        if guideline_mapper is None:
            raise QAINotFoundException('G29404', 'not found guideline')

        if guideline_mapper.delete_flag is True:
            raise QAINotFoundException('G29404', 'guideline has already been deleted')

        # quality_dimensionsテーブル
        quality_dimensions_mapper = QualityDimensionMapper.query. \
            filter(QualityDimensionMapper.delete_flag.is_(False)). \
            filter(QualityDimensionMapper.guideline_id == guideline_id).all()
        # ガイドラインに紐づくqdのIDのリスト
        qd_id_list = []
        for qd in quality_dimensions_mapper:
            qd_id_list.append(qd.json_id)

        # scopeテーブル
        scope_mapper = ScopeMapper.query. \
            filter(ScopeMapper.guideline_id == guideline_id). \
            filter(ScopeMapper.delete_flag.is_(False)).all()
        # ガイドラインに紐づくscopeのnameのリスト
        scope_name_list = []
        for scope in scope_mapper:
            scope_name_list.append(scope.name)

        try:
            with TemporaryDirectory() as temp_dir:

                # ファイルをtmpフォルダに保存
                file = request.files['guideline_schema']
                filename = os.path.basename(file.filename)
                p_temp_dir = pathlib.Path(temp_dir)
                save_path = p_temp_dir.joinpath(filename)
                file.save(str(save_path))

                guideline_name = ""

                # ファイルをオープン
                with open(str(save_path), mode='r', encoding='utf-8') as f:
                    guideline_schema_json = json.load(f)

                    for gsj in guideline_schema_json["guideline"]["meta_info"]:
                        if gsj["property"] == 'title':
                            guideline_name = gsj["content"]

                    # Guidelineテーブル
                    # 入力チェック
                    # Nameの存在確認、項目が存在しない場合、空文字の場合、スペースが含まれている場合エラー
                    if guideline_name is None or len(guideline_name) == 0 or ' ' in guideline_name:
                        # ワーニング 
                        warning_message.append('guideline name is empty or contains space')
                        check_result = False
                    
                    # ガイドライン名が違う場合はエラー（ガイドライン名を変える場合は新規登録になる）
                    if guideline_name != guideline_mapper.name:
                        # ワーニング 
                        warning_message.append('guideline name is changed')
                        check_result = False

                    json_qd_id_list = []
                    for qd in guideline_schema_json["guideline"]["quality_dimensions"]:
                        # 入力チェック
                        # 品質特性名が存在しないまたは空文字の場合
                        # 品質特性名にスペースが含まれている場合
                        qd_name = qd["name"]
                        if qd_name is None or qd_name == '' or ' ' in qd_name:
                            # ワーニング 
                            warning_message.append('quality dimension name is empty or contains space')
                            check_result = False
                        json_qd_id_list.append(qd["id"])

                    for qd_id in qd_id_list:
                        if qd_id not in json_qd_id_list:
                            # jsonファイルから削除されたQDがTestDescriptionで使用中か確認
                            subquery = sql_db.session.query(TestDescriptionMapper.quality_dimension_id).\
                                filter(TestDescriptionMapper.delete_flag.is_(False)).subquery()
                            qd_check_mapper = QualityDimensionMapper.query. \
                                filter(QualityDimensionMapper.id.in_(subquery)). \
                                filter(QualityDimensionMapper.guideline_id == guideline_id). \
                                filter(QualityDimensionMapper.delete_flag.is_(False)). \
                                filter(QualityDimensionMapper.json_id == qd_id).all()
                    
                            if len(qd_check_mapper) > 0:
                                # ワーニング 
                                warning_message.append('{} is already in use on the TestDescription'.format(qd_id))
                                check_result = False

                    json_scope_name_list = []
                    for scp in guideline_schema_json["guideline"]["scopes"]:
                        json_scope_name_list.append(scp["name"])
                    for scope_name in scope_name_list:
                        if scope_name not in json_scope_name_list:
                            # jsonファイルから削除されたscopeがMLComponentで使用中か確認
                            subquery = sql_db.session.query(MLComponentMapper.scope_id).\
                                filter(MLComponentMapper.delete_flag.is_(False)).subquery()
                            scope_check_mapper = ScopeMapper.query. \
                                filter(ScopeMapper.id.in_(subquery)). \
                                filter(ScopeMapper.guideline_id == guideline_id). \
                                filter(ScopeMapper.name == scope_name). \
                                filter(ScopeMapper.delete_flag.is_(False)).all()

                            if len(scope_check_mapper) > 0:
                                # ワーニング 
                                warning_message.append('{} is already in use on the MLComponent'.format(scope_name))
                                check_result = False

        except QAIException as e:
            sql_db.session.rollback()
            raise e
        except Exception as e:
            sql_db.session.rollback()
            raise QAIInternalServerException('G29999', 'internal server error: {}'.format(e))
        return CheckGuidelineSchemaFileRes(
            result=Result(code='G29000', message='Success.'),
            check_result=check_result,
            warning_message=warning_message
        )

    def delete_check(self, guideline_id: int) -> CheckGuidelineSchemaFileRes:

        check_result = True
        warning_message = []

        # ガイドライン
        guideline_mapper = GuidelineMapper.query. \
            filter(GuidelineMapper.id == guideline_id).first()

        if guideline_mapper is None:
            raise QAINotFoundException('G30404', 'not found guideline')

        if guideline_mapper.delete_flag is True:
            raise QAINotFoundException('G30404', 'guideline has already been deleted')

        subquery = sql_db.session.query(TestDescriptionMapper.quality_dimension_id).\
            filter(TestDescriptionMapper.delete_flag.is_(False)).subquery()
        qd_check_mapper = QualityDimensionMapper.query. \
            filter(QualityDimensionMapper.id.in_(subquery)). \
            filter(QualityDimensionMapper.guideline_id == guideline_id). \
            filter(QualityDimensionMapper.delete_flag.is_(False)).all()

        if len(qd_check_mapper) > 0:
            # ワーニング 
            for qd in qd_check_mapper:
                warning_message.append('{} is already in use on the TestDescription'.format(qd.json_id))
            check_result = False

        subquery = sql_db.session.query(MLComponentMapper.scope_id).\
            filter(MLComponentMapper.delete_flag.is_(False)).subquery()
        scope_check_mapper = ScopeMapper.query. \
            filter(ScopeMapper.id.in_(subquery)). \
            filter(ScopeMapper.guideline_id == guideline_id). \
            filter(ScopeMapper.delete_flag.is_(False)).all()

        if len(scope_check_mapper) > 0:
            # ワーニング 
            for scope in scope_check_mapper:
                warning_message.append('{} is already in use on the MLComponent'.format(scope.name))
            check_result = False

        return CheckGuidelineSchemaFileRes(
            result=Result(code='G30000', message='Success.'),
            check_result=check_result,
            warning_message=warning_message
        )

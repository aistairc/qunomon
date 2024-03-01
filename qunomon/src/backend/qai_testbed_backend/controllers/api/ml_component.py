# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from injector import inject
from marshmallow import ValidationError
from qlib.utils.logging import get_logger, log

from ..dto import ResultSchema, Result
from ..dto.ml_component import GetMLComponentSchemaResSchema, PostMLComponentReqSchema, PostMLComponentResSchema, DeleteMLComponentResSchema,\
    PutMLComponentReqSchema, PutMLComponentResSchema, PutReportOpinionReqSchema, PutReportOpinionResSchema
from ...usecases.ml_component import MLComponentService, MLComponentReportOpinionService
from ...across.exception import QAIException, QAINotFoundException


logger = get_logger()


class MLComponentCoreAPI(Resource):

    @inject
    def __init__(self, service: MLComponentService):
        self.service = service

    def post(self, organizer_id: str):

        # リクエストパース
        # TODO いずれはデコレータに分離
        json_input = request.get_json()
        try:
            req = PostMLComponentReqSchema().load(json_input)
        except TypeError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='P28000', message='TypeError: {}'.format(e))), 400
        except ValidationError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='P28000', message='ValidationError: {}'.format(e))), 400
        except ValueError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='P28000', message='ValueError: {}'.format(e))), 400
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='P29999', message='internal server error: {}'.format(e))), 500

        try:
            res = self.service.post(organizer_id, req)
            return PostMLComponentResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='P29999', message='internal server error: {}'.format(e))), 500


class MLComponentAPI(MLComponentCoreAPI):

    @inject
    def __init__(self, service: MLComponentService):
        self.service = service

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    @log(logger)
    def get(self, organizer_id: str):
        try:
            res = self.service.get_ml_component_list(organizer_id)
            return GetMLComponentSchemaResSchema().dump(res), 200
        except QAINotFoundException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except ValueError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='P10000', message='bad request: {}'.format(e))), 422
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='P19999', message='internal server error: {}'.format(e))), 500

    # csfrトークンチェックなし
    @log(logger)
    def post(self, organizer_id: str):
        # スーパークラスのpostを呼び出す
        res = super().post(organizer_id)
        return res


class MLComponentFrontAPI(MLComponentCoreAPI):

    @inject
    def __init__(self, service: MLComponentService):
        self.service = service

    # csfrトークンチェックあり
    @jwt_required()
    @log(logger)
    def post(self, organizer_id: str):
        # スーパークラスのpostを呼び出す
        res = super().post(organizer_id)
        return res


class MLComponentDetailCoreAPI(Resource):
    @inject
    def __init__(self, service: MLComponentService):
        self.service = service

    @log(logger)
    def delete(self, organizer_id: str, ml_component_id: str):
        try:
            res = self.service.delete_ml_component(organizer_id, int(ml_component_id))
            return DeleteMLComponentResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='P39999', message='internal server error: {}'.format(e))), 500

    @log(logger)
    def put(self, organizer_id: str, ml_component_id: str):

        # リクエストパース
        # TODO いずれはデコレータに分離
        json_input = request.get_json()
        try:
            req = PutMLComponentReqSchema().load(json_input)
        except TypeError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='P08000', message='TypeError: {}'.format(e))), 400
        except ValidationError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='P08000', message='ValidationError: {}'.format(e))), 400
        except ValueError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='P08000', message='ValueError: {}'.format(e))), 400
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='P09999', message='internal server error: {}'.format(e))), 500

        try:
            res = self.service.put(organizer_id, int(ml_component_id), req)
            return PutMLComponentResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='P09999', message='internal server error: {}'.format(e))), 500


class MLComponentDetailAPI(MLComponentDetailCoreAPI):
    @inject
    def __init__(self, service: MLComponentService):
        self.service = service

    # csfrトークンチェックなし
    @log(logger)
    def delete(self, organizer_id: str, ml_component_id: str):
        # スーパークラスのdeleteを呼び出す
        res = super().delete(organizer_id, ml_component_id)
        return res

    # csfrトークンチェックなし
    @log(logger)
    def put(self, organizer_id: str, ml_component_id: str):
        # スーパークラスのputを呼び出す
        res = super().put(organizer_id, ml_component_id)
        return res


class MLComponentDetailFrontAPI(MLComponentDetailCoreAPI):
    @inject
    def __init__(self, service: MLComponentService):
        self.service = service

    # csfrトークンチェックあり
    @jwt_required()
    @log(logger)
    def delete(self, organizer_id: str, ml_component_id: str):
        # スーパークラスのdeleteを呼び出す
        res = super().delete(organizer_id, ml_component_id)
        return res

    # csfrトークンチェックあり
    @jwt_required()
    @log(logger)
    def put(self, organizer_id: str, ml_component_id: str):
        # スーパークラスのputを呼び出す
        res = super().put(organizer_id, ml_component_id)
        return res


class MLComponentReportOpinionCoreAPI(Resource):
    @inject
    def __init__(self, service: MLComponentReportOpinionService):
        self.service = service

    @log(logger)
    def put(self, organizer_id: str, ml_component_id: str):

        # リクエストパース
        # TODO いずれはデコレータに分離
        json_input = request.get_json()
        try:
            req = PutReportOpinionReqSchema().load(json_input)
        except TypeError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='P40500', message='TypeError: {}'.format(e))), 400
        except ValidationError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='P40500', message='ValidationError: {}'.format(e))), 400
        except ValueError as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='P40500', message='ValueError: {}'.format(e))), 400
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='P40999', message='internal server error: {}'.format(e))), 500

        try:
            res = self.service.put(organizer_id, int(ml_component_id), req)
            return PutReportOpinionResSchema().dump(res), 200
        except QAIException as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            logger.exception('Raise Exception: %s', e)
            return ResultSchema().dump(Result(code='P40999', message='internal server error: {}'.format(e))), 500


class MLComponentReportOpinionAPI(MLComponentReportOpinionCoreAPI):
    @inject
    def __init__(self, service: MLComponentReportOpinionService):
        self.service = service

    # csfrトークンチェックなし
    @log(logger)
    def put(self, organizer_id: str, ml_component_id: str):
        # スーパークラスのputを呼び出す
        res = super().put(organizer_id, ml_component_id)
        return res


class MLComponentReportOpinionFrontAPI(MLComponentReportOpinionCoreAPI):
    @inject
    def __init__(self, service: MLComponentReportOpinionService):
        self.service = service

    # csfrトークンチェックあり
    @jwt_required()
    @log(logger)
    def put(self, organizer_id: str, ml_component_id: str):
        # スーパークラスのputを呼び出す
        res = super().put(organizer_id, ml_component_id)
        return res

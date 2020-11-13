# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from ..dto import ResultSchema, Result
from ..dto.inventory import GetInventoriesResSchema, DeleteInventoryResSchema, AppendInventoryReqSchema,\
    AppendInventoryResSchema, PutInventoryReqSchema, PutInventoryResSchema
from ...usecases.inventory import InventoryService
from ...across.exception import QAIException, QAINotFoundException


class InventoryAPI(Resource):

    def __init__(self):
        # TODO 要DI
        self.service = InventoryService()

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    def get(self, organizer_id: str, ml_component_id: str):
        try:
            res = self.service.get_inventories(organizer_id, int(ml_component_id))
            return GetInventoriesResSchema().dump(res), 200
        except QAIException as e:
            return ResultSchema().dump(e.to_result()), e.status_code
        except ValueError as e:
            return ResultSchema().dump(Result(code='I10000', message='bad request: {}'.format(e))), 422
        except Exception as e:
            return ResultSchema().dump(Result(code='I19999', message='internal server error: {}'.format(e))), 500

    def post(self, organizer_id: str, ml_component_id: str):
        json_input = request.get_json()
        try:
            req = AppendInventoryReqSchema().load(json_input)
        except ValidationError as e:
            result = Result(code='I28000', message='ValidationError: {}'.format(e))
            return ResultSchema().dump(result), 400

        try:
            res = self.service.append_inventory(organizer_id, int(ml_component_id), req)
            return AppendInventoryResSchema().dump(res), 200
        except QAINotFoundException as e:
            return ResultSchema().dump(e.to_result()), e.status_code
        except QAIException as e:
            return ResultSchema().dump(e.to_result()), e.status_code
        except ValueError:
            return ResultSchema().dump(Result(code='I20000', message='invalid path request')), 500


class InventoryDetailAPI(Resource):
    def __init__(self):
        # TODO 要DI
        self.service = InventoryService()

    # @jwt_required()
    # @helpers.standardize_api_response
    # TODO 要変換アノテーション
    def delete(self, organizer_id: str, ml_component_id: str, inventory_id: str):
        try:
            res = self.service.delete_inventory(organizer_id, int(ml_component_id), int(inventory_id))
            return DeleteInventoryResSchema().dump(res), 200
        except QAIException as e:
            return ResultSchema().dump(e.to_result()), e.status_code
        except ValueError as e:
            return ResultSchema().dump(Result(code='I40000', message='bad request: {}'.format(e))), 422
        except Exception as e:
            return ResultSchema().dump(Result(code='I49999', message='internal server error: {}'.format(e))), 500

    def put(self, organizer_id: str, ml_component_id: str, inventory_id: str):
        json_input = request.get_json()
        try:
            req = PutInventoryReqSchema().load(json_input)
        except ValidationError as e:
            return ResultSchema().dump(Result(code='I38001', message='ValidationError: {}'.format(e))), 400

        try:
            res = self.service.put_inventory(organizer_id, int(ml_component_id), int(inventory_id), req)
            return PutInventoryResSchema().dump(res), 200
        except TypeError as e:
            return ResultSchema().dump(Result(code='I38000', message='TypeError: {}'.format(e))), 400
        except ValueError as e:
            return ResultSchema().dump(Result(code='I30000', message='Bad Request: {}'.format(e))), 422
        except QAIException as e:
            return ResultSchema().dump(e.to_result()), e.status_code
        except Exception as e:
            return ResultSchema().dump(Result(code='I39999', message='internal server error: {}'.format(e))), 500

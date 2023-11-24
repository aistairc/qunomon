# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.

from ..controllers.dto import Result


class QAIException(Exception):
    status_code: int = 500

    def __init__(self, result_code: str, result_msg: str):
        self.result_code = result_code
        self.result_msg = result_msg

    def to_result(self):
        return Result(code=self.result_code, message=self.result_msg)


class QAIBadRequestException(QAIException):
    status_code: int = 400  # Jsonのパースエラー等、データ形式が間違っている


class QAIUnauthoredException(QAIException):
    status_code: int = 401  # 認証エラー


class QAINotFoundException(QAIException):
    status_code: int = 404  # 存在しない、または削除されている


class QAIMethodNotAllowedException(QAIException):
    status_code: int = 405  # 無効、または使用できないメソッド


class QAIMethodNotAcceptableException(QAIException):
    status_code: int = 406  # Acceptヘッダに受理できない内容が含まれている


class QAIConflictException(QAIException):
    status_code: int = 409  # コンフリクトしている


class QAIUnsupportedMediaTypeException(QAIException):
    status_code: int = 415  # リクエストされたデータのメディア形式をサーバーが対応していない


class QAIInvalidRequestException(QAIException):
    status_code: int = 422  # 不正なリクエスト


class QAIInternalServerException(QAIException):
    status_code: int = 500  # その他のサーバに起因するエラー
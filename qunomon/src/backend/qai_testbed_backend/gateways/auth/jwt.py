# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import datetime
from flask import current_app

from ...across import helpers


# TODO 認証機能は未実装
def set_jwt_handlers(jwt):
    """Define handlers to jwt.

    :jwt: flask_jwt.JWT object
    :returns: None

    """

    @jwt.authentication_handler
    def authenticate(username, password):
        pass

    @jwt.jwt_error_handler
    def error_handler(error):
        return 'Auth Failed: {}'.format(error.description), 400

    @jwt.jwt_payload_handler
    def make_payload(user):
        return {
            'user_id': str(user.id),
            'exp': (datetime.datetime.utcnow() +
                    current_app.config['JWT_EXPIRATION_DELTA']).isoformat()
        }

    @jwt.request_handler
    def load_user(payload):
        pass

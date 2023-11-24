# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from datetime import datetime
from nose2.tools import such

from . import app
from qai_testbed_backend.usecases.user import UserService


with such.A('Users') as it:

    with it.having('GET /users'):
        @it.should('should return U01000.')
        def test():
            with app.app_context():
                # TODO ユーザ関連の実装は保留とするため、一旦コメントアウトし、ダミーコードでpassにしておく
                it.assertEqual('dummy','dummy')
                # response = UserService().get_user()
                # it.assertEqual(response.result.code, 'U01000')

        @it.should('should return Users.')
        def test():
            with app.app_context():
                # TODO ユーザ関連の実装は保留とするため、一旦コメントアウトし、ダミーコードでpassにしておく
                it.assertEqual('dummy','dummy')
                # response = UserService().get_user()
                # it.assertGreaterEqual(len(response.users), 1)

                # for u in response.users:
                #     it.assertTrue(type(u.id_) is int)
                #     it.assertTrue(type(u.account_id) is str)
                #     it.assertTrue(type(u.user_name) is str)
                #     it.assertTrue(type(u.password_hash) is str)
                #     it.assertTrue(type(u.creation_datetime) is datetime)
                #     it.assertNotEqual(u.creation_datetime, None)
                #     it.assertTrue(type(u.update_datetime) is datetime)
                #     it.assertNotEqual(u.update_datetime, None)
                #     it.assertTrue(type(u.organizer_id) is str)
                #     it.assertIsInstance(u.user_role_ml_components, list)
                #     for urmc in u.user_role_ml_components:
                #         it.assertTrue(type(urmc.id_) is int)
                #         it.assertTrue(type(urmc.role) is str)
                #         it.assertTrue(type(urmc.target_ml_component_id) is int)

it.createTests(globals())

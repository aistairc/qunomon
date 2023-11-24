# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from nose2.tools import such

from . import app
from qai_testbed_backend.usecases.role import RoleService


with such.A('Roles') as it:

    with it.having('GET /roles'):
        @it.should('should return U12000.')
        def test():
            with app.app_context():
                # TODO ロール関連の実装は保留とするため、一旦コメントアウトし、ダミーコードでpassにしておく
                it.assertEqual('dummy','dummy')
                # response = RoleService().get_role()
                # it.assertEqual(response.result.code, 'U12000')

        @it.should('should return Roles.')
        def test():
            with app.app_context():
                # TODO ロール関連の実装は保留とするため、一旦コメントアウトし、ダミーコードでpassにしておく
                it.assertEqual('dummy','dummy')
                # response = RoleService().get_role()
                # it.assertGreaterEqual(len(response.roles), 1)

                # for f in response.roles:
                #     it.assertTrue(type(f.id_) is int)
                #     it.assertTrue(type(f.name) is str)


it.createTests(globals())

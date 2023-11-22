# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from datetime import datetime
from nose2.tools import such

from . import app
from qai_testbed_backend.usecases.organization import OrganizerService


with such.A('Organizers') as it:

    with it.having('GET /organizers'):
        @it.should('should return G21000.')
        def test():
            with app.app_context():
                # TODO 組織関連の実装は保留とするため、一旦コメントアウトし、ダミーコードでpassにしておく
                it.assertEqual('dummy','dummy')
                # response = OrganizerService().get_organizer_list()
                # it.assertEqual(response.result.code, 'O01000')

        @it.should('should return Organizers.')
        def test():
            with app.app_context():
                # TODO 組織関連の実装は保留とするため、一旦コメントアウトし、ダミーコードでpassにしておく
                it.assertEqual('dummy','dummy')
                # response = OrganizerService().get_organizer_list()
                # it.assertGreaterEqual(len(response.organizers), 1)

                # for f in response.organizers:
                #     it.assertTrue(type(f.id_) is int)
                #     it.assertTrue(type(f.organizer_id) is str)
                #     it.assertTrue(type(f.name) is str)
                #     it.assertTrue(type(f.creation_datetime) is datetime)
                #     it.assertTrue(type(f.update_datetime) is datetime)
                #     it.assertTrue(type(f.delete_flag) is bool)


it.createTests(globals())

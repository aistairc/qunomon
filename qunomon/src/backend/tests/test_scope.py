# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from datetime import datetime
from nose2.tools import such

from . import app
from qai_testbed_backend.usecases.scope import ScopeService


with such.A('Guidelines') as it:

    with it.having('GET /scopes'):
        @it.should('should return S00000.')
        def test():
            with app.app_context():
                response = ScopeService().get()
                it.assertEqual(response.result.code, 'S00000')

        @it.should('should return Scopes.')
        def test():
            with app.app_context():
                response = ScopeService().get()
                it.assertGreaterEqual(len(response.scopes), 2)

                for f in response.scopes:
                    it.assertTrue(type(f.id_) is int)
                    it.assertTrue(type(f.guideline_id) is int)
                    it.assertTrue(type(f.name) is str)
                    it.assertTrue(type(f.creation_datetime) is datetime)
                    it.assertTrue(type(f.update_datetime) is datetime)

    with it.having('GET /GuidelineId/scopes'):
        @it.should('should return S01000.')
        def test():
            with app.app_context():
                response = ScopeService().get_guideline_scopes(guideline_id=1)
                it.assertEqual(response.result.code, 'S01000')

it.createTests(globals())

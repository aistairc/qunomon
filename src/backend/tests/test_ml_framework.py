# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from nose2.tools import such

from . import app
from qai_testbed_backend.usecases.ml_framework import MLFrameworkService


with such.A('MLFrameworks') as it:

    with it.having('GET /mlFrameworks'):
        @it.should('should return M11000.')
        def test():
            with app.app_context():
                response = MLFrameworkService().get()
                it.assertEqual(response.result.code, 'M11000')

        @it.should('should return MLFrameworks.')
        def test():
            with app.app_context():
                response = MLFrameworkService().get()
                it.assertGreaterEqual(len(response.ml_frameworks), 1)

                for f in response.ml_frameworks:
                    it.assertTrue(type(f.id) is int)
                    it.assertTrue(type(f.name) is str)

                    it.assertNotEqual(f.id, 0)
                    it.assertNotEqual(f.name, '')


it.createTests(globals())

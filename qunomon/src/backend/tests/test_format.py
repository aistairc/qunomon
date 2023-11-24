# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from nose2.tools import such
import glob
from pathlib import Path
import os

from . import app
from qai_testbed_backend.usecases.format import FormatService


with such.A('Formats') as it:

    with it.having('GET /formats'):
        @it.should('should return I72000.')
        def test():
            with app.app_context():
                response = FormatService().get()
                it.assertEqual(response.result.code, 'I72000')

        @it.should('should return Formats.')
        def test():
            with app.app_context():
                response = FormatService().get()
                it.assertGreaterEqual(len(response.formats), 1)

                for f in response.formats:
                    it.assertTrue(type(f.id) is int)
                    it.assertTrue(type(f.format) is str)

it.createTests(globals())

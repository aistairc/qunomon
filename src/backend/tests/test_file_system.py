# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from nose2.tools import such

from . import app
from qai_testbed_backend.usecases.file_system import FileSystemService


with such.A('FileSystems') as it:

    with it.having('GET /fileSystems'):
        @it.should('should return I92000.')
        def test():
            with app.app_context():
                response = FileSystemService().get_file_system()
                it.assertEqual(response.result.code, 'I92000')

        @it.should('should return FileSystems.')
        def test():
            with app.app_context():
                response = FileSystemService().get_file_system()
                it.assertGreaterEqual(len(response.file_systems), 1)

                for f in response.file_systems:
                    it.assertTrue(type(f.id_) is int)
                    it.assertTrue(type(f.name) is str)


it.createTests(globals())

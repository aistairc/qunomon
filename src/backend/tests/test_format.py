# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from nose2.tools import such
import glob
from pathlib import Path
import os

from . import app
from qai_testbed_backend.usecases.format import FormatService
from qai_testbed_backend.across.file_checker import FileChecker


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
                    it.assertTrue(type(f.type) is str)
                    it.assertTrue(type(f.format) is str)

    with it.having('FileCheck'):
        @it.should('check file mime_type.')
        def test():
            with app.app_context():
                from qai_testbed_backend.entities.format import FormatMapper
                from qai_testbed_backend.entities.file_system import FileSystemMapper
                file_dir_path = Path(__file__).parent / 'files' / '*'
                files = glob.glob(str(file_dir_path))

                file_checker = FileChecker()

                file_systems = FileSystemMapper.query.all()
                if os.name == 'nt':
                    file_system_id = file_systems[1].id
                else:
                    file_system_id = file_systems[0].id

                for file in files:
                    suffix = Path(file).suffix[1:]
                    format_mapper = FormatMapper.query.filter(FormatMapper.format_ == suffix).first()
                    if format_mapper.mime_type == '*':
                        continue

                    result = file_checker.execute(file, file_system_id)
                    it.assertEqual(format_mapper.mime_type, result['mime_type'])

it.createTests(globals())

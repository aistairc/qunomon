# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from nose2.tools import such

from . import app
from qai_testbed_backend.usecases.data_type import DataTypeService


with such.A('DataTypes') as it:

    with it.having('GET /dataTypes'):
        @it.should('should return I82000.')
        def test():
            with app.app_context():
                response = DataTypeService().get_data_type()
                it.assertEqual(response.result.code, 'I82000')

        @it.should('should return DataTypes.')
        def test():
            with app.app_context():
                response = DataTypeService().get_data_type()
                it.assertGreaterEqual(len(response.data_types), 1)

                for f in response.data_types:
                    it.assertTrue(type(f.id_) is int)
                    it.assertTrue(type(f.name) is str)


it.createTests(globals())

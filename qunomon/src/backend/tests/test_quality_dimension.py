# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from nose2.tools import such

from . import app
from qai_testbed_backend.controllers.api.quality_dimension import QualityDimensionAPI, GuidelineQualityDimensionAPI


with such.A('QualityDimensions') as it:

    with it.having('GET /quality_dimensions'):
        @it.should('should return 200.')
        def test():
            with app.app_context():
                response = QualityDimensionAPI().get(scope_id=1)
                it.assertEqual(response[1], 200)

        @it.should('should return 8 quality dimensions.')
        def test():
            with app.app_context():
                response = QualityDimensionAPI().get(scope_id=1)
                it.assertEqual(len(response[0]['QualityDimensions']), 8)

                for dims in response[0]['QualityDimensions']:
                    it.assertTrue(type(dims['Id']) is int)
                    it.assertTrue(type(dims['GuidelineId']) is int)
                    it.assertTrue(type(dims['Name']) is str)
                    it.assertTrue(type(dims['Description']) is str)
                    it.assertTrue(type(dims['Url']) is str)
                    it.assertTrue(type(dims['CreationDatetime']) is str)
                    it.assertTrue(type(dims['UpdateDatetime']) is str)
                    for level in dims['QualityDimensionLevels']:
                        it.assertTrue(type(level['Id']) is int)
                        it.assertTrue(type(level['QualityDimensionLevelId']) is str)
                        it.assertTrue(type(level['Name']) is str)
                        it.assertTrue(type(level['Description']) is str)
                        it.assertTrue(type(level['Level']) is float)
                        it.assertTrue(type(level['CreationDatetime']) is str)
                        it.assertTrue(type(level['UpdateDatetime']) is str)


    with it.having('GET /guideline/GuidelineId/quality_dimensions'):
        @it.should('should return 200.')
        def test():
            with app.app_context():
                response = GuidelineQualityDimensionAPI().get(guideline_id=1)
                it.assertEqual(response[1], 200)

it.createTests(globals())

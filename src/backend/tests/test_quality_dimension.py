# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from nose2.tools import such

from . import app
from qai_testbed_backend.controllers.api.quality_dimension import QualityDimensionAPI


with such.A('QualityDimensions') as it:

    with it.having('GET /QualityDimensions'):
        @it.should('should return 200.')
        def test():
            with app.app_context():
                response = QualityDimensionAPI().get()
                it.assertEqual(response[1], 200)

        @it.should('should return 8 quality dimensions.')
        def test():
            with app.app_context():
                response = QualityDimensionAPI().get()
                it.assertEqual(len(response[0]['QualityDimensions']), 8)

                dims = response[0]['QualityDimensions']
                it.assertTrue(any(d['Name'] == '要求分析の十分性' for d in dims))
                it.assertTrue(any(d['Name'] == 'データ設計の十分性' for d in dims))
                it.assertTrue(any(d['Name'] == 'データセットの被覆性' for d in dims))
                it.assertTrue(any(d['Name'] == 'データセットの均一性' for d in dims))
                it.assertTrue(any(d['Name'] == '機械学習モデルの正確性' for d in dims))
                it.assertTrue(any(d['Name'] == '機械学習モデルの安定性' for d in dims))
                it.assertTrue(any(d['Name'] == '運用時品質の維持性' for d in dims))
                it.assertTrue(any(d['Name'] == 'プログラムの健全性' for d in dims))


it.createTests(globals())

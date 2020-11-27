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
                it.assertTrue(any(d['Name'] == 'Completeness_of_problem_domain_analysis' for d in dims))
                it.assertTrue(any(d['Name'] == 'Coverage_for_distinguished_problem_cases' for d in dims))
                it.assertTrue(any(d['Name'] == 'Diversity_of_test_data' for d in dims))
                it.assertTrue(any(d['Name'] == 'Distribution_of_training_data' for d in dims))
                it.assertTrue(any(d['Name'] == 'Accuracy_of_trained_model' for d in dims))
                it.assertTrue(any(d['Name'] == 'Robustness_of_trained_model' for d in dims))
                it.assertTrue(any(d['Name'] == 'Stability_Maintainability_of_quality' for d in dims))
                it.assertTrue(any(d['Name'] == 'Dependability_of_underlying_software' for d in dims))


it.createTests(globals())

# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from datetime import datetime
from nose2.tools import such

from . import app
from qai_testbed_backend.usecases.scope_quality_dimension import ScopeQualityDimensionService


with such.A('Guidelines') as it:

    with it.having('GET /GuidelineId/scopes'):
        @it.should('should return S02000.')
        def test():
            with app.app_context():
                response = ScopeQualityDimensionService().get_guideline_scope_quality_dimensions(guideline_id=1)
                it.assertEqual(response.result.code, 'S02000')

it.createTests(globals())

# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from nose2.tools import such

from qai_testbed_backend.controllers.api.healthcheck import HealthCheckAPI


with such.A('health-check') as it:

    # テスト実行時に1回実行
    @it.has_setup
    def setup():
        pass

    # テスト関数読むたびに実行
    @it.has_test_setup
    def setup_each_test_case():
        pass

    # グループ化
    with it.having('GET /health-check'):
        @it.should('should return 200.')
        def test():
            response = HealthCheckAPI().get()
            it.assertEqual(response[1], 200)

it.createTests(globals())

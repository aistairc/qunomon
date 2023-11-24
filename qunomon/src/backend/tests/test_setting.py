# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from nose2.tools import such

from . import app
from qai_testbed_backend.usecases.setting import SettingService
from qai_testbed_backend.controllers.dto.setting import PutSettingReq
from qai_testbed_backend.across.exception import QAIException, QAINotFoundException


with such.A('Users') as it:

    with it.having('GET /setting'):
        @it.should('should return V00000.')
        def test():
            with app.app_context():
                response = SettingService().get(key='aithub_linkage_flag')
                it.assertEqual(response.result.code, 'V00000')
                it.assertEqual(response.value, '1')

        @it.should('should return V00404 if key is not found.')
        def test():
            with app.app_context():
                try:
                    SettingService().get(key='dummy')
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'V00404')

    with it.having('PUT /setting'):
        @it.should('should return V10000.')
        def test():
            with app.app_context():
                req = PutSettingReq(value='0')
                response = SettingService().put(key='aithub_linkage_flag',req=req)
                it.assertEqual(response.result.code, 'V10000')
                it.assertEqual(response.value, '0')
                # 元に戻す
                req = PutSettingReq(value='1')
                response = SettingService().put(key='aithub_linkage_flag',req=req)

        @it.should('should return V10404 if key is not found.')
        def test():
            with app.app_context():
                req = PutSettingReq(value='0')
                try:
                    SettingService().put(key='dummy', req=req)
                except QAIException as e:
                    it.assertTrue(type(e) is QAINotFoundException)
                    it.assertEqual(e.result_code, 'V10404')

it.createTests(globals())

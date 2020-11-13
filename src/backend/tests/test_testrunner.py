# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from nose2.tools import such

from . import app
from qai_testbed_backend.usecases.testrunner import TestRunnerService


with such.A('TestRunners') as it:

    with it.having('GET /testRunners'):
        @it.should('should return I52000.')
        def test():
            with app.app_context():
                response = TestRunnerService().get_test_runners()
                it.assertEqual(response.result.code, 'I52000')

        @it.should('should return TestRunners.')
        def test():
            with app.app_context():
                response = TestRunnerService().get_test_runners()

                for t in response.test_runners:
                    it.assertTrue(type(t.id_) is int)
                    it.assertNotEqual(t.id_, 0)
                    it.assertTrue(type(t.name) is str)
                    it.assertNotEqual(t.name, '')
                    it.assertTrue(type(t.quality_dimension_id) is int)
                    it.assertNotEqual(t.quality_dimension_id, 0)
                    it.assertTrue(type(t.description) is str)
                    it.assertTrue(type(t.author) is str)
                    it.assertTrue(type(t.version) is str)
                    it.assertTrue(type(t.quality) is str)
                    it.assertNotEqual(t.quality, '')
                    it.assertTrue(type(t.landing_page) is str)
                    it.assertNotEqual(t.landing_page, '')
                    for r in t.reference:
                        it.assertTrue(type(r.reference) is str)
                        it.assertNotEqual(r.reference, '')
                    for p in t.params:
                        it.assertTrue(type(p.id_) is int)
                        it.assertNotEqual(p.id_, 0)
                        it.assertTrue(type(p.name) is str)
                        it.assertNotEqual(p.name, '')
                        it.assertTrue(type(p.type_) is str)
                        it.assertNotEqual(p.type_, '')
                        it.assertTrue(type(p.description) is str)
                        it.assertNotEqual(p.description, '')
                        it.assertTrue(type(p.default_value) is str)
                    for tit in t.test_inventory_templates:
                        it.assertTrue(type(tit.id_) is int)
                        it.assertNotEqual(tit.id_, 0)
                        it.assertTrue(type(tit.name) is str)
                        it.assertNotEqual(tit.name, '')
                        it.assertTrue(type(tit.type_.id_) is int)
                        it.assertNotEqual(tit.type_.id_, 0)
                        it.assertTrue(type(tit.type_.name) is str)
                        it.assertNotEqual(tit.type_.name, '')
                        it.assertTrue(type(tit.description) is str)
                        for f in tit.formats:
                            it.assertTrue(type(f.id) is int)
                            it.assertNotEqual(f.id, 0)
                            it.assertTrue(type(f.type) is str)
                            it.assertNotEqual(f.type, '')
                            it.assertTrue(type(f.format) is str)
                            it.assertNotEqual(f.format, '')
                        it.assertTrue(type(tit.schema) is str)
                    for rm in t.report.measures:
                        it.assertTrue(type(rm.id_) is int)
                        it.assertNotEqual(rm.id_, 0)
                        it.assertTrue(type(rm.name) is str)
                        it.assertNotEqual(rm.name, '')
                        it.assertTrue(type(rm.type_) is str)
                        it.assertNotEqual(rm.type_, '')
                        it.assertTrue(type(rm.description) is str)
                        it.assertNotEqual(rm.description, '')
                        it.assertTrue(type(rm.structure) is str)
                        it.assertNotEqual(rm.structure, '')
                    for rr in t.report.resources:
                        it.assertTrue(type(rr.id_) is int)
                        it.assertNotEqual(rr.id_, 0)
                        it.assertTrue(type(rr.name) is str)
                        it.assertNotEqual(rr.name, '')
                        it.assertTrue(type(rr.path) is str)
                        it.assertNotEqual(rr.path, '')
                        it.assertTrue(type(rr.type_) is str)
                        it.assertNotEqual(rr.type_, '')
                        it.assertTrue(type(rr.description) is str)
                    for d in t.downloads:
                        it.assertTrue(type(d.id_) is int)
                        it.assertNotEqual(d.id_, 0)
                        it.assertTrue(type(d.name) is str)
                        it.assertNotEqual(d.name, '')
                        it.assertTrue(type(d.path) is str)
                        it.assertNotEqual(d.path, '')
                        it.assertTrue(type(d.description) is str)


it.createTests(globals())

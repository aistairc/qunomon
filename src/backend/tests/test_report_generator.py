# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
import time
from nose2.tools import such

from . import app
from qai_testbed_backend.usecases.testrunner import ReportGeneratorService, TestRunnerService, TestRunnerStatusService
from qai_testbed_backend.usecases.test_description import TestDescriptionService
from qai_testbed_backend.usecases.ml_framework import MLFrameworkService
from qai_testbed_backend.controllers.dto.testrunner import PostReportGeneratorReq, PostTestRunnerReq, GraphsTemplate, GraphParam
from qai_testbed_backend.controllers.dto.test_description import GetTestDescriptionDetailRes
from qai_testbed_backend.across.exception import QAIException
from qai_testbed_backend.gateways.extensions import sql_db


with such.A('/<organizer_id>/ml_components/<ml_component_id>/testDescriotions/reportGenerator') as it:

    # テスト実行時に1回実行
    @it.has_setup
    def setup():
        # TD1 run 作成
        with app.app_context():
            from qai_testbed_backend.entities.test_description import TestDescriptionMapper
            from qai_testbed_backend.entities.run import RunMapper
            from qai_testbed_backend.entities.job import JobMapper
            from qai_testbed_backend.entities.test import TestMapper
            from qai_testbed_backend.entities.ml_component import MLComponentMapper
            from qai_testbed_backend.entities.graph import GraphMapper
            from qai_testbed_backend.entities.graph_template import GraphTemplateMapper
            from qai_testbed_backend.entities.test_runner import TestRunnerMapper

            test_runner = TestRunnerMapper.query.\
                filter(TestRunnerMapper.name == 'acc_check_1.0.py').first()

            test_mapper = TestMapper.query. \
                filter(TestMapper.ml_component_id == 1). \
                filter(MLComponentMapper.org_id == 'dep-a').first()

            job = JobMapper(status='DONE', result='OK', result_detail='OK', test_id=test_mapper.id)
            sql_db.session.add(job)
            sql_db.session.flush()

            run = RunMapper(status='DONE', result='OK', result_detail='OK', job_id=job.id)
            sql_db.session.add(run)
            sql_db.session.flush()

            graph_templates = GraphTemplateMapper.query.\
                filter(GraphTemplateMapper.test_runner_id == test_runner.id).all()

            graph_list = []
            graph_index = 1
            for graph_template in graph_templates:
                graph_list.append(GraphMapper(report_required=True, graph_address='', report_index=graph_index,
                                              report_name=graph_template.name,
                                              graph_template_id=graph_template.id, run_id=run.id, download_id=1))
                graph_index += 1
            sql_db.session.add_all(graph_list)
            sql_db.session.flush()

            td = TestDescriptionMapper.query.get(1)
            td.run_id = run.id

            sql_db.session.commit()

            # TestRunnerService().post(organizer_id='dep-a', ml_component_id=1, request=req)
            # while(True):
            #     res = TestRunnerStatusService().get(organizer_id='dep-a', ml_component_id=1)
            #     if res.job_status.status == 'DONE' or res.result.code == 'R24001':
            #         break
            #     time.sleep(0.5)


    with it.having('POST /<organizer_id>/ml_components/<ml_component_id>/testDescriotions/reportGenerator'):
        @it.should('should return D14000 if ml_component_id is not found.')
        def test():
            req = PostReportGeneratorReq(command='SetParam',
                                         destination=['3'],
                                         params=GraphsTemplate(opinion='XXX',
                                                               graphs=[
                                                                   GraphParam(1, True, 1, 'Graph-A')]))
            with app.app_context():
                try:
                    ReportGeneratorService().post(organizer_id='dep-a', ml_component_id=999, request=req)
                    it.fail()
                except QAIException as e:
                    it.assertEqual(e.result_code, 'D14000')

        @it.should('should return D10001 if command is invalid.')
        def test():
            req = PostReportGeneratorReq(command='invalid command',  # command not found
                                         destination=['3'],
                                         params=GraphsTemplate(opinion='XXX',
                                                               graphs=[
                                                                   GraphParam(1, True, 1, 'Graph-A')]))
            with app.app_context():
                try:
                    ReportGeneratorService().post(organizer_id='dep-a', ml_component_id=1, request=req)
                    it.fail()
                except QAIException as e:
                    it.assertEqual(e.result_code, 'D10001')

        @it.should('should return D14001 if test description is not exists.')
        def test():
            req = PostReportGeneratorReq(command='SetParam',
                                         destination=['3'],
                                         params=GraphsTemplate(opinion='XXX',
                                                               graphs=[
                                                                   GraphParam(1, True, 1, 'Graph-A')]))
            with app.app_context():
                from qai_testbed_backend.entities.ml_component import MLComponentMapper
                from qai_testbed_backend.entities.test import TestMapper
                empty_ml_component = MLComponentMapper(name='empty ml_component', org_id='dep-a',
                                                       description='description',
                                                       problem_domain='problem_domain',
                                                       ml_framework_id=MLFrameworkService().get().ml_frameworks[0].id)
                sql_db.session.add(empty_ml_component)
                sql_db.session.flush()
                empty_test = TestMapper(ml_component_id=empty_ml_component.id)
                sql_db.session.add(empty_test)
                sql_db.session.flush()

                try:
                    ReportGeneratorService().post(organizer_id='dep-a', ml_component_id=empty_ml_component.id, request=req)
                    it.fail()
                except QAIException as e:
                    it.assertEqual(e.result_code, 'D14001')

        @it.should('should return D12000.')
        def test():
            req = PostReportGeneratorReq(command='SetParam',
                                         destination=['3'],
                                         params=GraphsTemplate(opinion=None, graphs=None))
            with app.app_context():
                res = ReportGeneratorService().post(organizer_id='dep-a', ml_component_id=1, request=req)
                it.assertEqual(res.result.code, 'D12000')

        @it.should('should change opinion')
        def test():
            opinion = 'changed opinion text'
            req = PostReportGeneratorReq(command='SetParam',
                                         destination=['1'],
                                         params=GraphsTemplate(opinion=opinion, graphs=[]))
            with app.app_context():
                ReportGeneratorService().post(organizer_id='dep-a', ml_component_id=1, request=req)
                res = TestDescriptionService().get(organizer_id='dep-a', ml_component_id=1, testdescription_id=1)
                it.assertEqual(res.test_description_detail.opinion, opinion)

        @it.should('should change graphs')
        def test():
            req = PostReportGeneratorReq(command='SetParam',
                                         destination=['1'],
                                         params=GraphsTemplate(opinion='XXX',
                                                               graphs=[
                                                                   GraphParam(1, True, 2, 'Graph-A'),
                                                                   GraphParam(2, True, 1, 'Graph-B')]))
            with app.app_context():
                ReportGeneratorService().post(organizer_id='dep-a', ml_component_id=1, request=req)
                res = TestDescriptionService().get(organizer_id='dep-a', ml_component_id=1, testdescription_id=1)
                it.assertEqual(res.test_description_detail.test_description_result.graphs[0].report_index, 2)
                it.assertEqual(res.test_description_detail.test_description_result.graphs[1].report_index, 1)
                it.assertEqual(res.test_description_detail.test_description_result.graphs[2].report_index, 3)

                it.assertTrue(res.test_description_detail.test_description_result.graphs[0].report_required)
                it.assertTrue(res.test_description_detail.test_description_result.graphs[1].report_required)
                it.assertFalse(res.test_description_detail.test_description_result.graphs[2].report_required)

                it.assertEqual(res.test_description_detail.test_description_result.graphs[0].report_name, 'Graph-A')
                it.assertEqual(res.test_description_detail.test_description_result.graphs[1].report_name, 'Graph-B')
                it.assertEqual(res.test_description_detail.test_description_result.graphs[2].report_name, 'distribution_graph')


it.createTests(globals())

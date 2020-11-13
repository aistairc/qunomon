# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.

from flask import Blueprint
from ...across import helpers
from . import healthcheck, job, run, deploy_dag


blueprint = Blueprint('qai-testbed', __name__)
api = helpers.MyApi(blueprint, prefix='/qai-ip/api/0.0.1')

api.add_resource(job.JobAPI,
                 '/<organizer_id>/mlComponents/<ml_component_id>/job')
api.add_resource(healthcheck.HealthCheckAPI,
                 '/health-check')
api.add_resource(run.NotifyRunCompeteAPI,
                 '/<organizer_id>/mlComponents/<ml_component_id>/jobs/<job_id>/runs/<run_id>/notify-complete')
api.add_resource(deploy_dag.DeployDAGAPI,
                 '/deploy-dag')
api.add_resource(deploy_dag.DeployDAGAsyncAPI,
                 '/async-deploy-dag')
api.add_resource(deploy_dag.DeployDAGNonBuildAPI,
                 '/deploy-dag-non-build')

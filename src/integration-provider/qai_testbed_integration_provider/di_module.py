# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.

from injector import Binder

from .usecases.job import JobService
from .usecases.run import NotifyRunCompeteService
from .usecases.healthcheck import HealthcheckService
from .usecases.deploy_dag import DeployDAGService


def di_module(binder: Binder):
    binder.bind(
        HealthcheckService,
        to=HealthcheckService
    )
    binder.bind(
        JobService,
        to=JobService
    )
    binder.bind(
        NotifyRunCompeteService,
        to=NotifyRunCompeteService
    )
    binder.bind(
        DeployDAGService,
        to=DeployDAGService
    )

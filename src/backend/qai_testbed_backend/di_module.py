# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.

from injector import Binder

from .usecases.format import FormatService
from .usecases.testrunner import TestRunnerService, TestRunnerStatusService, ReportGeneratorService
from .usecases.ait_manifest import AITManifestService
from .usecases.ml_component import MLComponentService
from .usecases.ml_framework import MLFrameworkService
from .usecases.test_description import TestDescriptionService


def di_module(binder: Binder):
    binder.bind(
        TestRunnerService,
        to=TestRunnerService
    )
    binder.bind(
        TestRunnerStatusService,
        to=TestRunnerStatusService
    )
    binder.bind(
        FormatService,
        to=FormatService
    )
    binder.bind(
        ReportGeneratorService,
        to=ReportGeneratorService
    )
    binder.bind(
        AITManifestService,
        to=AITManifestService
    )
    binder.bind(
        MLComponentService,
        to=MLComponentService
    )
    binder.bind(
        MLFrameworkService,
        to=MLFrameworkService
    )
    binder.bind(
        TestDescriptionService,
        to=TestDescriptionService
    )

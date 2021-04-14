# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.

from flask import Blueprint
from ...across import helpers
from . import healthcheck, testrunner, test_description, quality_dimension, quality_measurement, download, inventory, \
    tag, ml_component, format, ml_framework, data_type, file_system


blueprint = Blueprint('qai-testbed', __name__)
api = helpers.MyApi(blueprint, prefix='/qai-testbed/api/0.0.1')

api.add_resource(healthcheck.HealthCheckAPI,
                 '/health-check')
api.add_resource(ml_component.MLComponentAPI,
                 '/<organizer_id>/mlComponents')
api.add_resource(ml_component.MLComponentDetailAPI,
                 '/<organizer_id>/mlComponents/<ml_component_id>')
api.add_resource(testrunner.TestRunnerAPI,
                 '/<organizer_id>/mlComponents/<ml_component_id>/testDescriotions/runners')
api.add_resource(testrunner.TestRunnerStatusAPI,
                 '/<organizer_id>/mlComponents/<ml_component_id>/testDescriotions/run-status')
api.add_resource(testrunner.ReportGeneratorAPI,
                 '/<organizer_id>/mlComponents/<ml_component_id>/testDescriotions/reportGenerator')
api.add_resource(test_description.TestDescriptionAPI,
                 '/<organizer_id>/mlComponents/<ml_component_id>/testDescriotions')
api.add_resource(test_description.TestDescriptionDetailAPI,
                 '/<organizer_id>/mlComponents/<ml_component_id>/testDescriotions/<testdescription_id>')
api.add_resource(test_description.TestDescriptionStarAPI,
                 '/<organizer_id>/mlComponents/<ml_component_id>/testDescriotions/<test_description_id>/star')
api.add_resource(test_description.TestDescriptionUnstarAPI,
                 '/<organizer_id>/mlComponents/<ml_component_id>/testDescriotions/<test_description_id>/unstar')
api.add_resource(test_description.TestDescriptionAncestorAPI,
                 '/<organizer_id>/mlComponents/<ml_component_id>/testDescriotions/<test_description_id>/ancestors')
api.add_resource(quality_dimension.QualityDimensionAPI,
                 '/QualityDimensions')
api.add_resource(quality_measurement.QualityMeasurementAPI,
                 '/QualityMeasurements')
api.add_resource(quality_measurement.RelationalOperatorAPI,
                 '/QualityMeasurements/RelationalOperators')
api.add_resource(testrunner.TestRunnerListAPI,
                 '/testRunners')
api.add_resource(testrunner.AITManifestAPI,
                 '/testRunners/manifest')
api.add_resource(download.DownloadAPI,
                 '/download/<id_>')
api.add_resource(inventory.InventoryAPI,
                 '/<organizer_id>/mlComponents/<ml_component_id>/inventories')
api.add_resource(inventory.InventoryDetailAPI,
                 '/<organizer_id>/mlComponents/<ml_component_id>/inventories/<inventory_id>')
api.add_resource(tag.TagAPI,
                 '/tags')
api.add_resource(format.FormatAPI,
                 '/formats')
api.add_resource(data_type.DataTypeAPI,
                 '/dataTypes')
api.add_resource(file_system.FileSystemAPI,
                 '/fileSystems')
api.add_resource(ml_framework.MLFrameworkAPI,
                 '/mlFrameworks')

# Copyright © 2019 National Institute of Advanced Industrial Science and Technology （AIST）. All rights reserved.
from typing import List
from marshmallow import fields, post_dump
from typing import List, Optional

from . import Result, ResultSchema, BaseSchema
from .format import Format, FormatSchema
from .data_type import DataType, DataTypeSchema
from .downloadable_template import DownloadableTemplate, DownloadableTemplateSchema


# POST /testRunners start
class Reference:
    def __init__(self, bib_info: str, additional_info: str = None, url: str = None) -> None:
        self.bib_info = bib_info
        self.additional_info = additional_info
        self.url = url


class ReferenceSchema(BaseSchema):
    __model__ = Reference
    bib_info = fields.Str(data_key='bib_info', required=True)
    additional_info = fields.Str(data_key='additional_info', required=False)
    url = fields.Str(data_key='url', required=False)


class Parameter:
    def __init__(self, name: str, type_: str, description: str, default_value: str = None, 
                 min_value: float = None, max_value: float = None, depends_on_parameter: str = None) -> None:
        self.name = name
        self.type = type_
        self.description = description
        self.default_value = default_value
        self.min_value = min_value
        self.max_value = max_value
        self.depends_on_parameter = depends_on_parameter


class ParameterSchema(BaseSchema):
    __model__ = Parameter
    name = fields.Str(data_key='name', required=True)
    type_ = fields.Str(data_key='type', required=True)
    description = fields.Str(data_key='description', required=True)
    default_value = fields.Str(data_key='default_val', required=False)
    min_value = fields.Float(data_key='min', required=False)
    max_value = fields.Float(data_key='max', required=False)
    depends_on_parameter = fields.Str(data_key='depends_on_parameter', required=False)


class InventoryRequirementCompatiblePackage:
    def __init__(self, name: str, version: str = None, additional_info: str = None) -> None:
        self.name = name
        self.version = version
        self.additional_info = additional_info


class InventoryRequirementCompatiblePackageSchema(BaseSchema):
    __model__ = InventoryRequirementCompatiblePackage
    name = fields.Str(data_key='name', required=True)
    version = fields.Str(data_key='version', required=False)
    additional_info = fields.Str(data_key='additional_info', required=False)


class InventoryRequirement:
    def __init__(self, 
                 format_: List[str],
                 depends_on_parameter: str = None,
                 compatible_packages: List[InventoryRequirementCompatiblePackage] = None, 
                 additional_info: List[dict] = None, 
                 min: str = None, 
                 max: str = None) -> None:
        self.format = format_
        self.depends_on_parameter = depends_on_parameter
        self.compatible_packages = compatible_packages
        self.additional_info = additional_info
        self.min = min
        self.max = max


class InventoryRequirementSchema(BaseSchema):
    __model__ = InventoryRequirement
    format_ = fields.List(fields.String(), data_key='format', required=True)
    depends_on_parameter = fields.Str(data_key='depends_on_parameter', required=False)
    compatible_packages = fields.Nested(InventoryRequirementCompatiblePackageSchema, data_key='compatible_packages',
                                 many=True, required=False)
    additional_info = fields.List(fields.Dict(), data_key='additional_info', 
                                 many=True, required=False)
    min = fields.Str(data_key='min', required=False)
    max = fields.Str(data_key='max', required=False)


class Inventory:
    def __init__(self, 
                 name: str, 
                 type_: str, 
                 description: str, 
                 requirement: InventoryRequirement,
                 depends_on_parameter: str = None) -> None:
        self.name = name
        self.type = type_
        self.description = description
        self.requirement = requirement
        self.depends_on_parameter = depends_on_parameter


class InventorySchema(BaseSchema):
    __model__ = Inventory
    name = fields.Str(data_key='name', required=True)
    type_ = fields.Str(data_key='type', required=True)
    description = fields.Str(data_key='description', required=True)
    requirement = fields.Nested(InventoryRequirementSchema, data_key='requirement', many=False, required=True)
    depends_on_parameter = fields.Str(data_key='depends_on_parameter', required=False)


class ReportMeasure:
    def __init__(self, name: str, description: str, type_: str, 
                 structure: str, min_value: float = None, max_value: float = None) -> None:
        self.name = name
        self.description = description
        self.type = type_
        self.min_value = min_value
        self.max_value = max_value
        self.structure = structure


class ReportMeasureSchema(BaseSchema):
    __model__ = ReportMeasure
    name = fields.Str(data_key='name', required=True)
    description = fields.Str(data_key='description', required=True)
    type_ = fields.Str(data_key='type', required=True)
    min_value = fields.Float(data_key='min', required=False)
    max_value = fields.Float(data_key='max', required=False)
    structure = fields.Str(data_key='structure', required=True)


class ReportResource:
    def __init__(self, name: str, type_: str, description: str) -> None:
        self.name = name
        self.type = type_
        self.description = description


class ReportResourceSchema(BaseSchema):
    __model__ = ReportResource
    name = fields.Str(data_key='name', required=True)
    type_ = fields.Str(data_key='type', required=True)
    description = fields.Str(data_key='description', required=True)


class Report:
    def __init__(self, measures: List[ReportMeasure], resources: List[ReportResource]) -> None:
        self.measures = measures
        self.resources = resources


class ReportSchema(BaseSchema):
    __model__ = Report
    measures = fields.Nested(ReportMeasureSchema, data_key='measures', many=True, required=True)
    resources = fields.Nested(ReportResourceSchema, data_key='resources', many=True, required=True)


class Download:
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description


class DownloadSchema(BaseSchema):
    __model__ = Download
    name = fields.Str(data_key='name', required=True)
    description = fields.Str(data_key='description', required=True)


class AITManifest:
    def __init__(self, 
                 name: str, 
                 description: str, 
                 source_repository: str, 
                 version: str, 
                 quality: str,
                 keywords: List[str], 
                 references: List[Reference], 
                 licenses: List[str],
                 inventories: List[Inventory], 
                 parameters: List[Parameter],
                 report: Report, 
                 downloads: List[Download]) -> None:
        self.name = name
        self.description = description
        self.source_repository = source_repository
        self.version = version
        self.quality = quality
        self.keywords = keywords
        self.references = references
        self.licenses = licenses
        self.inventories = inventories
        self.parameters = parameters
        self.report = report
        self.downloads = downloads


class AITManifestSchema(BaseSchema):
    __model__ = AITManifest
    name = fields.Str(data_key='name', required=True)
    description = fields.Str(data_key='description', required=True)
    source_repository = fields.Str(data_key='source_repository', required=False)
    version = fields.Str(data_key='version', required=True)
    quality = fields.Str(data_key='quality', required=True)
    keywords = fields.List(fields.String(), data_key='keywords', required=False)
    references = fields.Nested(ReferenceSchema, data_key='references',  many=True, required=False)
    licenses = fields.List(fields.String(), data_key='licenses', required=False)
    inventories = fields.Nested(InventorySchema, data_key='inventories', many=True, required=True)
    parameters = fields.Nested(ParameterSchema, data_key='parameters', many=True, required=True)
    report = fields.Nested(ReportSchema, data_key='report', many=False, required=True)
    downloads = fields.Nested(DownloadSchema, data_key='downloads', many=True, required=True)


class PostAITManifestRes:
    def __init__(self, result: Result, test_runner_id: int) -> None:
        self.result = result
        self.test_runner_id = test_runner_id


class PostAITManifestResSchema(BaseSchema):
    __model__ = PostAITManifestRes
    result = fields.Nested(ResultSchema, data_key='Result')
    test_runner_id = fields.Integer(data_key='TestRunnerId')

# POST /testRunners end


# GET /testRunners start
class ReferenceTemplate:
    def __init__(self, id_: int, bib_info: str, additional_info: str = None, url_: str = None) -> None:
        self.id_ = id_
        self.bib_info = bib_info
        self.additional_info = additional_info
        self.url_ = url_


class ReferenceTemplateSchema(BaseSchema):
    __model__ = ReferenceTemplate
    id_ = fields.Int(data_key='Id', required=True)
    bib_info = fields.Str(data_key='Bib_info', required=True)
    additional_info = fields.Str(data_key='Additional_info', required=False)
    url_ = fields.Str(data_key='Url', required=False)


class ParamTemplate:
    def __init__(self, type_: str, description: str, default_value: str = None, id_: Optional[int] = None,
                 name: Optional[str] = None, test_runner_param_template_id: Optional[int] = None,
                 min_value: float = None, max_value: float = None, depends_on_parameter: str = None) -> None:
        self.id_ = id_
        self.name = name
        self.type_ = type_
        self.test_runner_param_template_id = test_runner_param_template_id
        self.description = description
        self.default_value = default_value
        self.min_value = min_value
        self.max_value = max_value
        self.depends_on_parameter = depends_on_parameter


class ParamTemplateSchema(BaseSchema):
    __model__ = ParamTemplate
    id_ = fields.Int(data_key='Id', required=True)
    name = fields.Str(data_key='Name', required=True)
    type_ = fields.Str(data_key='Type', required=True)
    min_value = fields.Float(data_key='Min', required=False)
    max_value = fields.Float(data_key='Max', required=False)
    description = fields.Str(data_key='Description', required=True)
    default_value = fields.Str(data_key='DefaultVal', required=True)
    depends_on_parameter = fields.Str(data_key='depends_on_parameter', required=False)

    @post_dump
    def remove_skip_values(self, data, **_):
        return {
            key: value for key, value in data.items()
            if (key != 'DefaultVal') or (value is not None)
        }


class TestInventoryTemplateCompatiblePackage:
    def __init__(self, id_: int, name: str, version: str,  additional_info: str) -> None:
        self.id_ = id_
        self.name = name
        self.version = version
        self.additional_info = additional_info


class TestInventoryTemplateCompatiblePackageSchema(BaseSchema):
    __model__ = TestInventoryTemplateCompatiblePackage
    id_ = fields.Int(data_key='Id', required=True)
    name = fields.Str(data_key='Name', required=True)
    version = fields.Str(data_key='Version', required=False)
    additional_info = fields.Str(data_key='Additional_info', required=False)


class TestInventoryTemplateAdditionalInfo:
    def __init__(self, id_: int, key: str, value: str) -> None:
        self.id_ = id_
        self.key = key
        self.value = value


class TestInventoryTemplateAdditionalInfoSchema(BaseSchema):
    __model__ = TestInventoryTemplateAdditionalInfo
    id_ = fields.Int(data_key='Id', required=True)
    key = fields.Str(data_key='Key', required=True)
    value = fields.Str(data_key='Value', required=True)

class TestInventoryTemplate:
    def __init__(self, 
                 id_: int, 
                 name: str, 
                 type_: DataType, 
                 description: str, 
                 formats: List[Format],
                 depends_on_parameter: str = None, 
                 compatible_packages: List[TestInventoryTemplateCompatiblePackage] = None,
                 additional_info: List[TestInventoryTemplateAdditionalInfo] = None,
                 min: str = None, 
                 max: str = None) -> None:
        self.id_ = id_
        self.name = name
        self.type_ = type_
        self.description = description
        self.formats = formats
        self.depends_on_parameter = depends_on_parameter
        self.compatible_packages = compatible_packages
        self.additional_info = additional_info
        self.min = min
        self.max = max


class TargetInventoryTemplateSchema(BaseSchema):
    __model__ = TestInventoryTemplate
    id_ = fields.Int(data_key='Id', required=True)
    name = fields.Str(data_key='Name', required=True)
    type_ = fields.Nested(DataTypeSchema, data_key='DataType', required=True)
    description = fields.Str(data_key='Description', required=True)
    formats = fields.Nested(FormatSchema, data_key='Formats', many=True)
    depends_on_parameter = fields.Str(data_key='depends_on_parameter', required=False)
    compatible_packages = fields.Nested(TestInventoryTemplateCompatiblePackageSchema, data_key='CompatiblePackages',  many=True)
    additional_info = fields.Nested(TestInventoryTemplateAdditionalInfoSchema, data_key='AdditionalInfo',  many=True)
    min = fields.Str(data_key='Min', required=False)
    max = fields.Str(data_key='Max', required=False)


class Measure:
    def __init__(self, id_: int, name: str, type_: str, description: str, min_value: float,
                 max_value: float, structure: str) -> None:
        self.id_ = id_
        self.name = name
        self.type_ = type_
        self.description = description
        self.min_value = min_value
        self.max_value = max_value
        self.structure = structure


class MeasureSchema(BaseSchema):
    __model__ = Measure
    id_ = fields.Int(data_key='Id', required=True)
    name = fields.Str(data_key='Name', required=True)
    type_ = fields.Str(data_key='Type', required=True)
    description = fields.Str(data_key='Description', required=True)
    min_value = fields.Str(data_key='Min', required=False)
    max_value = fields.Str(data_key='Max', required=False)
    structure = fields.Str(data_key='Structure', required=True)


class Resource:
    def __init__(self, id_: int, name: str, type_: str, description: str) -> None:
        self.id_ = id_
        self.name = name
        self.type_ = type_
        self.description = description


class ResourceSchema(BaseSchema):
    __model__ = Resource
    id_ = fields.Int(data_key='Id', required=True)
    name = fields.Str(data_key='Name', required=True)
    type_ = fields.Str(data_key='Type', required=True)
    description = fields.Str(data_key='Description', required=True)


class ReportTemplate:
    def __init__(self, measures: List[Measure], resources: List[Resource]) -> None:
        self.measures = measures
        self.resources = resources


class ReportTemplateSchema(BaseSchema):
    __model__ = Report
    measures = fields.Nested(MeasureSchema, data_key='Measures', many=True)
    resources = fields.Nested(ResourceSchema, data_key='Resources', many=True)


class TestRunnerTemplate:
    def __init__(self, 
                 id_: int, 
                 name: str, 
                 description: str,
                 source_repository: str, 
                 create_user_account: str,
                 create_user_name: str,
                 version: str, 
                 quality: str,
                 keywords: str, 
                 references: List[ReferenceTemplate], 
                 licenses: str,
                 landing_page: str, 
                 install_mode: str, 
                 install_status: str,
                 params: List[ParamTemplate],
                 test_inventory_templates: List[TestInventoryTemplate],
                 report, downloads: List[DownloadableTemplate]) -> None:
        self.id_ = id_
        self.name = name
        self.description = description
        self.source_repository = source_repository
        self.create_user_account = create_user_account
        self.create_user_name = create_user_name
        self.version = version
        self.quality = quality
        self.keywords = keywords
        self.references = references
        self.licenses = licenses
        self.landing_page = landing_page
        self.install_mode = install_mode
        self.install_status = install_status
        self.params = params
        self.test_inventory_templates = test_inventory_templates
        self.report = report
        self.downloads = downloads


class TestRunnersTemplateSchema(BaseSchema):
    __model__ = TestRunnerTemplate
    id_ = fields.Int(data_key='Id', required=True)
    name = fields.Str(data_key='Name', required=True)
    description = fields.Str(data_key='Description', required=True)
    source_repository = fields.Str(data_key='Source_repository', required=False)
    create_user_account = fields.Str(data_key='CreateUserAccount', required=False)
    create_user_name = fields.Str(data_key='CreateUserName', required=False)
    version = fields.Str(data_key='Version', required=True)
    quality = fields.Str(data_key='Quality', required=True)
    keywords = fields.Str(data_key='Keywords', required=False)
    references = fields.Nested(ReferenceTemplateSchema, data_key='References', many=True)
    licenses = fields.Str(data_key='Licenses', required=False)
    landing_page = fields.Str(data_key='LandingPage', required=True)
    install_mode = fields.Str(data_key='InstallMode', required=True)
    install_status = fields.Str(data_key='InstallStatus', required=True)
    params = fields.Nested(ParamTemplateSchema, data_key='ParamTemplates', many=True)
    test_inventory_templates = fields.Nested(TargetInventoryTemplateSchema, data_key='TargetInventories', many=True)
    report = fields.Nested(ReportTemplateSchema, data_key='Report', many=False)
    downloads = fields.Nested(DownloadableTemplateSchema, data_key='Downloads', many=True)

    @post_dump
    def remove_skip_values(self, data, **_):
        return {
            key: value for key, value in data.items()
            if (key != 'Email') or (value is not None)
        }


class GetTestRunnerRes:
    def __init__(self, result: Result, test_runners: List[TestRunnerTemplate]) -> None:
        self.result = result
        self.test_runners = test_runners


class GetTestRunnerResSchema(BaseSchema):
    __model__ = GetTestRunnerRes
    result = fields.Nested(ResultSchema, data_key='Result')
    test_runners = fields.Nested(TestRunnersTemplateSchema, data_key='TestRunners', many=True)

# GET /testRunners end

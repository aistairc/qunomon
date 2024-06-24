import { urlParameterMixin } from '../mixins/urlParameterMixin';
import { csrfMixin } from '../mixins/csrfMixin';

export const tdMixin = {
    mixins: [urlParameterMixin, csrfMixin],
    data() {
        return {
            qualityMeasurements: null,
            testRunners: null,
            inventories: null,
            qualityDimensions: null,
            relationalOperators: null,
            setOperands: [],
            setParams: [],
            selectedMeasurement: null,
            selectedTestrunner: null,
            selectedInventories: [],
            errorMessages : [],
            maxCharacters : 100,
            checkedMeasurements: [],
            // count: 1,
            requestData:
             {
                Name: '',
                QualityDimensionID: 1,
                QualityMeasurements: [],
                TargetInventories: [],
                TestRunner: {
                    Id: 1,
                    Params: []
                },
            },
            result: null,
            selectedQualityDimension: null,
            measurementFormsList: [],
            previousPageSettingData: {},
            backTestDescriptionAppendData: {},
            backTestDescriptionEditData: {},
            testDescriptionName: null,
            changeTestrunner: null,
            paramTemplateDisableList: [],
            paramTemplateRequiredList: [],
            paramTemplateDependencyList: [],
            targetInventoryDisableList: [],
            targetInventoryRequiredList: [],
            targetInventoryDependencyList: [],
            filterTestRunnersDisplayList: [],
            aitNameFilter: '',
            aitDescriptionFilter: '',
            aitNameFilterDisplay: null,
            aitDescriptionFilterDisplay: null,
            sort_key: "",
            sort_asc: true
        }
    },
    created(){
        this.mlComponentIdCheck();
        this.organizationIdCheck = sessionStorage.getItem('organizationId');
        this.mlComponentId = sessionStorage.getItem('mlComponentId');
        this.scopeId = sessionStorage.getItem('scopeId');
        this.getMeasurements();
        this.getTestRunners();
        this.getInventories();
        this.getQualityDImensions();
        this.getRelationalOperators();
    },
    computed: {
        changeDemension:{
            get(){
                return this.selectedQualityDimension;
            },
            set(qualityDimension){
                this.selectedQualityDimension = qualityDimension;
                this.selectedTestrunner = null;
            }
        },
        // AssetsがMeasurementに依存する場合、下記のメソッドを使う。現状はassetsのAPIで取得できたAssetsを表示させている。
        changeAssets(){
            let AssetsList = null;
            if (this.selectedMeasurement) {
                this.qualityMeasurements.forEach(quality_measurement => {
                    if (this.selectedMeasurement.OperandTemplateId == quality_measurement.Id) {
                        AssetsList = quality_measurement.TargetAssets;
                        return AssetsList;
                    }
                });
            }
            return AssetsList;
        },

        // changeTestrunner:{
        //     get(){
        //         return this.selectedTestrunner;
        //     },
        //     set(testRunner){
        //         if(typeof testRunner === 'undefined'){
        //             return;
        //         }
        //         this.selectedTestrunner = testRunner;
        //         this.selectedInventories = {};
        //         this.checkedMeasurements = [];
        //         this.setMeasurementForms();
        //     }
        // }
    },
    methods: {
        getMeasurements(){
            this.$axios.get(this.$backendURL + '/QualityMeasurements')
            .then((response) => {
                this.qualityMeasurements = response.data.QualityMeasurements;
            })
            .catch((error) => {
                this.$router.push({
                    name: 'Information',
                    params: {error}
                })
            });
        },
        getTestRunners(){
            this.$axios.get(this.$backendURL + '/testRunners')
            .then((response) => {
                this.testRunners = response.data.TestRunners;
            })
            .catch((error) => {
                this.$router.push({
                    name: 'Information',
                    params: {error}
                })
            });
        },
        getInventories(){
            this.$axios.get(this.$backendURL
                            + '/'
                            + this.organizationIdCheck
                            + '/mlComponents/'
                            + this.mlComponentId
                            + '/inventories')
            .then((response) => {
                this.inventories = response.data.Inventories;
            })
            .catch((error) => {
               this.$router.push({
                   name: 'Information',
                   params: {error}
               })
            });
        },
        getQualityDImensions(){
            this.$axios.get(this.$backendURL
                            + '/scopes/'
                            + this.scopeId
                            + '/quality_dimensions')
            .then((response) => {
                this.qualityDimensions = response.data;
            })
            .catch((error) => {
               this.$router.push({
                   name: 'Information',
                   params: {error}
               })
            });
        },
        getRelationalOperators(){
            this.$axios.get(this.$backendURL + '/QualityMeasurements/RelationalOperators')
            .then((response) => {
                this.relationalOperators = response.data;
            })
            .catch((error) => {
               this.$router.push({
                   name: 'Information',
                   params: {error}
               })
            });
        },
        clearForm() {
            this.selectedSpecificationAttribute = null;
            this.selectedTraindataAttribute = null;
            this.selectedInventories = [];
            this.selectedTestrunner = null;
        },
        filterInventories(targetDataTypeId, targetFormats) {
            const inventoriesList = [];
            if(this.inventories != null){
                this.inventories.forEach(inventory => {
                    if(inventory.DataType.Id == targetDataTypeId){
                        inventory.Formats.forEach(format => {
                            targetFormats.forEach(targetFormat =>{
                                if(format && format.Id == targetFormat.Id){
                                    if(inventoriesList.indexOf(inventory) == -1){
                                        inventoriesList.splice(0, 0, inventory);
                                    }
                                }
                            })
                        })
                    }
                });
            }
            return inventoriesList;
        },
        inventoryAdd(history, selectDataType, selectedFormat) {
            this.setPreviousPageSettingData();
            this.$refs.addInventoryBtn.show(history, selectDataType, selectedFormat);
        },
        postHistory_testDescriptionEdit(history,testDescriptionId) {
            this.setTestDescription(testDescriptionId);
            this.$router.push({
                name: 'TestDescriptionEdit',
                params: {history: history}
            })
        },
        postHistory_testDescriptionCopy(history,testDescriptionId) {
            this.setTestDescription(testDescriptionId);
            this.$router.push({
                name: 'TestDescriptionCopy',
                params: {history: history}
            })
        },
        setMeasurementForms(){
            const forms = [];
            if(this.selectedTestrunner != null){
                for(var i = 0; i < this.selectedTestrunner.Report.Measures.length; i++){
                    var measurementForm = [
                        {
                            Id: this.selectedTestrunner.Report.Measures[i].Id,
                            Value: '',
                            RelationalOperatorId: 1,
                            Enable: true
                        }
                    ];
                    forms.push(measurementForm);
                    this.checkedMeasurements.push(measurementForm[0].Id);
                }
            }
            this.measurementFormsList = forms;
        },
        addInventories() {
            this.getInventories();
        },
        setDependencyParamNameList(){
            var paramTemplates = this.selectedTestrunner.ParamTemplates;
            var targetInventories = this.selectedTestrunner.TargetInventories;

            // paramTemplatesの名称リストを取得
            var  paramTemplatesNameList = [];
            paramTemplates.forEach(paramTemplate => {
                paramTemplatesNameList.push(paramTemplate.Name);
            });

            // paramTemplatesのDependencyIndex関連リスト作成
            paramTemplates.forEach(paramTemplate => {
                var dependencyParamNameOfPT = paramTemplate.depends_on_parameter;
                if (dependencyParamNameOfPT == null || dependencyParamNameOfPT.length === 0) {
                    this.paramTemplateDependencyList.push(-1);
                    this.paramTemplateRequiredList.push(true);
                } else {
                    this.paramTemplateDependencyList.push(paramTemplatesNameList.indexOf(dependencyParamNameOfPT));
                    this.paramTemplateRequiredList.push(false);
                }
            });

            // paramTemplatesの必須項目リスト作成
            this.paramTemplateDependencyList.forEach(dependency => {
                if (dependency != -1) {
                    this.paramTemplateRequiredList['' + dependency] = false;
                }
            });

            // targetInventoriesのDependencyIndex関連リスト作成
            targetInventories.forEach(targetInventory => {
                var dependencyParamNameOfTI = targetInventory.depends_on_parameter;
                if (dependencyParamNameOfTI == null || dependencyParamNameOfTI.length === 0) {
                    this.targetInventoryDependencyList.push(-1);
                    this.targetInventoryRequiredList.push(true);
                } else {
                    this.targetInventoryDependencyList.push(paramTemplatesNameList.indexOf(dependencyParamNameOfTI));
                    this.targetInventoryRequiredList.push(false);
                }
            });
            
            this.setDependencyParamNameDisable();
        },
        setDependencyParamNameDisable() {
            this.paramTemplateDisableList = [];
            this.targetInventoryDisableList = [];
            var paramTemplates = this.selectedTestrunner.ParamTemplates;
            var targetInventories = this.selectedTestrunner.TargetInventories;

            // paramTemplatesの「活性・非活性」「必須・非必須」設定
            for (var i = 0; i < paramTemplates.length; i++){
                var dependencyParamNameIndexOfPT = this.paramTemplateDependencyList['' + i];
                if (dependencyParamNameIndexOfPT != -1) {
                    if (this.selectedTestrunner.ParamTemplates['' + dependencyParamNameIndexOfPT].DefaultVal !== '') {
                        this.paramTemplateDisableList.push(false);
                        this.paramTemplateRequiredList['' + i] = true;
                    } else {
                        this.paramTemplateDisableList.push(true);
                        this.selectedTestrunner.ParamTemplates['' + i].DefaultVal = '';
                        this.paramTemplateRequiredList['' + i] = false;
                    }
                } else {
                    this.paramTemplateDisableList.push(false);
                }
            }

            // targetInventoriesの「活性・非活性」「必須・非必須」設定 
            for (var j = 0; j < targetInventories.length; j++){
                var dependencyParamNameIndexOfTI = this.targetInventoryDependencyList['' + j];
                if (dependencyParamNameIndexOfTI != -1) {
                    if (this.selectedTestrunner.ParamTemplates['' + dependencyParamNameIndexOfTI].DefaultVal !== '') {
                        this.targetInventoryDisableList.push(false);
                        this.targetInventoryRequiredList['' + j] = true;
                    } else {
                        this.targetInventoryDisableList.push(true);
                        for (var inv_i=0; inv_i<this.selectedInventories.length; inv_i++) {
                            if (this.selectedInventories[inv_i].name == targetInventories[j].Name) {
                               for (var inv_j = 0; inv_j < this.selectedInventories[inv_i].value_list.length; inv_j++) {
                                this.selectedInventories[inv_i].value_list[inv_j] = '';
                               }
                            }
                        }
                        this.targetInventoryRequiredList['' + j] = false;
                    }
                } else {
                    this.targetInventoryDisableList.push(false);
                }
            }
        },
        setStar(testDescriptionId) {
            const url = this.$backendURL + '/'
                        + this.organizationIdCheck + '/mlComponents/'
                        + this.mlComponentId + '/testDescriptions/'
                        + testDescriptionId + '/starFront'
            //リクエスト時のオプションの定義
            const config = {
                headers:{
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRF-TOKEN' : this.getCookie("csrf_access_token")
                },
                withCredentials:true,
            }
            this.$axios.post(url, {}, config)
            .catch((error) => {
                this.$router.push({
                    name: 'Information',
                    params: {error}
                })
            });
        },
        setUnStar(testDescriptionId) {
            const url = this.$backendURL + '/'
                        + this.organizationIdCheck + '/mlComponents/'
                        + this.mlComponentId + '/testDescriptions/'
                        + testDescriptionId + '/unstarFront'
            //リクエスト時のオプションの定義
            const config = {
                headers:{
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRF-TOKEN' : this.getCookie("csrf_access_token")
                },
                withCredentials:true,
            }
            this.$axios.post(url, {}, config)
            .catch((error) => {
                this.$router.push({
                    name: 'Information',
                    params: {error}
                })
            });
        }, 
        setTestDescription(testDescriptionId){
            sessionStorage.setItem('testDescriptionId', testDescriptionId);
        },
        setFilterTestRunnersList(testRunnersList){
            
            var aitNameFilter = this.aitNameFilter || '';
            var aitDescriptionFilter = this.aitDescriptionFilter || '';
            this.filterTestRunnersDisplayList = [];

            if (testRunnersList != null) {
                if (testRunnersList.length > 1) {
                    this.aitNameFilterDisplay = true;
                    this.aitDescriptionFilterDisplay = true;
                } else {
                    this.aitNameFilterDisplay = false;
                    this.aitDescriptionFilterDisplay = false;
                }

                testRunnersList.forEach(testRunner => {
                    var nameFilterFlg = true;
                    if (aitNameFilter != '' && testRunner.Name.indexOf(aitNameFilter) < 0) {
                        nameFilterFlg = false;
                    }
    
                    var descriptionFilterFlg  = true;
                    if (aitDescriptionFilter != '' && testRunner.Description.indexOf(aitDescriptionFilter) < 0) {
                        descriptionFilterFlg = false;
                    }
    
                    var displayFlg = null;
                    if (aitNameFilter != '' && aitDescriptionFilter == '') {
                        displayFlg = nameFilterFlg;
                    } else if (aitNameFilter == '' && aitDescriptionFilter != ''){
                        displayFlg = descriptionFilterFlg;
                    } else if (aitNameFilter != '' && aitDescriptionFilter != '') {
                        displayFlg = nameFilterFlg && descriptionFilterFlg;
                    } else {
                        displayFlg = true;
                    }
    
                    this.filterTestRunnersDisplayList.push(displayFlg);
                });
            }
        },
        filterTestRunnersByItem(){
            this.changeTestrunner = null;
            this.changeColorTable();
            this.nextBtnCheck();
        },
        sortObjectMethod(sortObject){
            if(this.sort_key != "") {
                let set = 1;
                this.sort_asc ? (set = 1) : (set = -1)
                sortObject.sort((a, b) => {
                    if (a[this.sort_key] < b[this.sort_key]) return -1 * set;
                    if (a[this.sort_key] > b[this.sort_key]) return 1 * set;
                    return 0;
                })
                return sortObject
            }
            else {
                return sortObject
            }
        },
        sortBy(key) {
            this.sort_key === key
            ? (this.sort_asc = !this.sort_asc)
            : (this.sort_asc = true)
            this.sort_key = key
        },
        addClass(key) {
            return {
                asc: this.sort_key === key && this.sort_asc,
                desc: this.sort_key === key && !this.sort_asc
            }
        }
    }
}

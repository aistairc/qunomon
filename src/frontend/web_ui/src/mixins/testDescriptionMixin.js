import { urlParameterMixin } from '../mixins/urlParameterMixin';

export const tdMixin = {
    mixins: [urlParameterMixin],
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
            selectedInventories: {},
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
        }
    },
    created(){
        this.mlComponentIdCheck();
        this.organizationIdCheck = sessionStorage.getItem('organizationId');
        this.mlComponentId = sessionStorage.getItem('mlComponentId');
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
            this.$axios.get(this.$backendURL + '/QualityDimensions')
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
            this.selectedInventories = {};
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
        inventoryAdd(history) {
            this.setPreviousPageSettingData();
            this.$refs.addInventoryBtn.show(history);
        },
        postHistory_testDescriptionEdit(history,testDescriptionId) {
            this.$router.push({
                name: 'TestDescriptionEdit',
                params: {history: history,
                        testDescriptionId: testDescriptionId}
            })
        },
        postHistory_testDescriptionCopy(history,testDescriptionId) {
            this.$router.push({
                name: 'TestDescriptionCopy',
                params: {history: history,
                        testDescriptionId: testDescriptionId}
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
                            RelationalOperatorId: '',
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
        
        setStar(testDescriptionId) {
            const url = this.$backendURL + '/'
                        + this.organizationIdCheck + '/mlComponents/'
                        + this.mlComponentId + '/testDescriotions/'
                        + testDescriptionId + '/star'
            this.$axios.post(url)
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
                        + this.mlComponentId + '/testDescriotions/'
                        + testDescriptionId + '/unstar'
            this.$axios.post(url)
            .catch((error) => {
                this.$router.push({
                    name: 'Information',
                    params: {error}
                })
            });
        }, 
    }
}

<template>
<div>
    <!-- ヘッダ -->
    <header id="head">
        <div id="title">
            <h1 class="title" v-if="this.mlComponent">
                {{ this.mlComponent.Name }}
            </h1>
        </div>
    </header>

    <!-- サブメニュー（左カラム） -->
    <div id="submenu">
        <div id="logo">
            <img src="~@/assets/logo.svg" alt="logo" class="logo" />
        </div>
        <div id="header_set">
            <div id="company_name">
                <p class="company_name">{{$t("common.organizationName")}}</p>
                <p class="company_name2">産総研</p>
            </div>
            <!--言語ボタン■-->
            <div id="btn_language">
                <template v-if="$i18n.locale === 'en'">
                    <a href="#" v-on:click.prevent="changeLanguage('ja')" class="btn_unselect">{{$t("common.lanJa")}}</a>
                    <a href="#" class="btn_select">{{$t("common.lanEn")}}</a>
                </template>
                <template v-else>
                    <a href="#" class="btn_select">{{$t("common.lanJa")}}</a>
                    <a href="#" v-on:click.prevent="changeLanguage('en')" class="btn_unselect">{{$t("common.lanEn")}}</a>
                </template>
            </div>
        </div>
        <ul id="submenu_body">
            <hr />
            <li class="un_place">
                <router-link :to="{ name: 'Inventories' }" class="move_">{{$t("common.menuInventories")}}</router-link>
            </li>
            <li class="un_place">
                <router-link :to="{ name: 'TestDescriptions' }" class="move_">{{$t("common.menuTestDescriptions")}}</router-link>
            </li>
            <li class="place submenu_detail">
                <a class="submenu_detail" href="#">{{$t("testDescriptionEdit.edit")}}</a>
            </li>
            <li class="mlcomponent un_place">
                <router-link :to="{ name: 'MLComponents' }" class="move_">{{$t("common.menuMLComponents")}}</router-link>
            </li>
            <li class="btn_logout">
                <a href="javascript:void(0);" @click="signOut()" class="btn_unselect">
                    <img src="~@/assets/logout.svg" alt="logout" class="icon">
                    {{$t("common.signOut")}}
                </a>
            </li>
        </ul>
    </div>

    <!-- ニュース（中央カラム） -->
    <div id="main">
        <div id="main_body">
            <div id="search_table">
                <form>
                    <!-- General -->
                    <div>
                        <table class="table_block">
                            <tr>
                                <td class="th1">
                                    <span class="subtitle"><strong>{{$t("testDescriptionEdit.general")}}</strong></span>
                                    <div class="category_description">
                                        <span>{{$t("testDescriptionEdit.generalExp")}}</span>
                                    </div>
                                </td>
                                <td class="th2">
                                    <table class="setting_table">
                                        <tr>
                                            <td class="left">
                                                <span>{{$t("testDescriptionEdit.name")}}</span><span class="asterisk">&#042;</span>
                                            </td>
                                            <td class="right">
                                                <template v-if="$i18n.locale === 'en'">
                                                    <input type="text" v-model="testDescriptionName" placeholder="name" name="name" :key="testDescriptionName" @blur="nextBtnCheck" />
                                                </template>
                                                <template v-else>
                                                    <input type="text" v-model="testDescriptionName" placeholder="テストディスクリプション名称" name="name" :key="testDescriptionName" @blur="nextBtnCheck" />
                                                </template>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td>
                                                <span>{{$t("testDescriptionEdit.qualityDimension")}}</span>
                                                <span class="asterisk">&#042;</span>
                                            </td>
                                            <td>
                                                <select id="qualityDimensionId" class="select" v-model="changeDemension" v-if="qualityDimensions" @click="aitProgramReset" @change="nextBtnCheck">
                                                    <option value="null" style="color: gray" disabled>
                                                        {{$t("common.defaultPulldown")}}
                                                    </option>
                                                    <option v-for="qualityDimension in qualityDimensions.QualityDimensions" :key="qualityDimension.Id" v-bind:value="qualityDimension.Id">
                                                        {{ qualityDimension.Name }}
                                                    </option>
                                                </select>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </div>
                    <hr />

                    <!-- AIT Program -->
                    <div>
                        <table class="table_block">
                            <tr>
                                <td class="th1">
                                    <span class="subtitle"><strong>{{$t("testDescriptionEdit.ait")}}</strong></span>
                                    <div class="category_description">
                                        <span>{{$t("testDescriptionEdit.aitExp")}}</span>
                                    </div>
                                </td>
                                <td class="th2">
                                    <div v-if="selectedQualityDimension">
                                        <table class="ait_table">
                                            <thead>
                                                <tr>
                                                    <td class="ait_check center">
                                                        <span></span>
                                                    </td>
                                                    <td class="ait_name center">
                                                        <span>{{$t("testDescriptionEdit.name")}}</span>
                                                    </td>
                                                    <td class="ait_description center">
                                                        <span>{{$t("testDescriptionEdit.description")}}</span>
                                                    </td>
                                                </tr>
                                            </thead>
                                            <tbody class="tbody">
                                                <tr class="trName" v-for="TestRunner in filterTestRunners" :key="TestRunner.Id">
                                                    <template v-if="$route.params.backTestDescriptionEditData != null">
                                                        <template v-if="TestRunner.Id == $route.params.backTestDescriptionEditData.selectedTestrunner.Id">
                                                            <td class="ait_check aitProgramTableColor background">
                                                                <input type="radio" class="list_ radioCheck" name="radio" v-model="changeTestrunner" v-bind:value="TestRunner" @change="nextBtnCheck" @click="changeColorTable" />
                                                            </td>
                                                            <td class="ait_name aitProgramTableColor background">
                                                                <span>{{ TestRunner.Name }}</span>
                                                            </td>
                                                            <td class="ait_description aitProgramTableColor background">
                                                                <span>{{ TestRunner.Description }}</span>
                                                            </td>
                                                        </template>
                                                        <template v-else>
                                                            <td class="ait_check background">
                                                                <input type="radio" class="list_ radioCheck" name="radio" v-model="changeTestrunner" v-bind:value="TestRunner" @change="nextBtnCheck" @click="changeColorTable" />
                                                            </td>
                                                            <td class="ait_name background">
                                                                <span>{{ TestRunner.Name }}</span>
                                                            </td>
                                                            <td class="ait_description background">
                                                                <span>{{ TestRunner.Description }}</span>
                                                            </td>
                                                        </template>
                                                    </template>
                                                    <template v-else>
                                                        <template v-if="TestRunner.Id == test_description_detail.TestRunner.Id">
                                                            <td class="ait_check aitProgramTableColor background">
                                                                <input type="radio" class="list_ radioCheck" name="radio" v-model="changeTestrunner" v-bind:value="TestRunner" @change="nextBtnCheck" @click="changeColorTable" />
                                                            </td>
                                                            <td class="ait_name aitProgramTableColor background">
                                                                <span>{{ TestRunner.Name }}</span>
                                                            </td>
                                                            <td class="ait_description aitProgramTableColor background">
                                                                <span>{{ TestRunner.Description }}</span>
                                                            </td>
                                                        </template>
                                                        <template v-else>
                                                            <td class="ait_check background">
                                                                <input type="radio" class="list_ radioCheck" name="radio" v-model="changeTestrunner" v-bind:value="TestRunner" @change="nextBtnCheck" @click="changeColorTable" />
                                                            </td>
                                                            <td class="ait_name background">
                                                                <span>{{ TestRunner.Name }}</span>
                                                            </td>
                                                            <td class="ait_description background">
                                                                <span>{{ TestRunner.Description }}</span>
                                                            </td>
                                                        </template>
                                                    </template>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                    <div v-else class="center">
                                        <span>{{$t("testDescriptionEdit.mes1")}}</span>
                                    </div>
                                </td>
                            </tr>
                        </table>
                    </div>
                    <hr />

                    <!-- submit -->
                    <div id="btn_set">
                        <p>
                            {{$t("testDescriptionEdit.mes2")}}
                        </p>
                        <br />
                        <template v-if="$i18n.locale === 'en'">
                            <input type="button" value="Cancel" class="btn_left" @click="postTestDescriptionCancel" />
                            <input type="button" value="Next" id="next" class="btn_right" @click="postTestDescriptionEdit" />
                        </template>
                        <template v-else>
                            <input type="button" value="キャンセル" class="btn_left" @click="postTestDescriptionCancel" />
                            <input type="button" value="次へ" id="next" class="btn_right" @click="postTestDescriptionEdit" />
                        </template>

                    </div>
                </form>
            </div>
            <!-- フッタ -->
            <div id="footer">
                <address>
                    Copyright © National Institute of Advanced Industrial Science and
                    Technology （AIST）
                </address>
            </div>
        </div>
    </div>

</div>
</template>

<script>
import {
    urlParameterMixin
} from "../mixins/urlParameterMixin";
import {
    tdMixin
} from "../mixins/testDescriptionMixin";
import "vue-good-table/dist/vue-good-table.css";

export default {
    mixins: [urlParameterMixin, tdMixin],
    data() {
        return {
            mlComponents: null,
            nameCheck: false,
            aitProgramCheck: false,
            test_description_detail: null,
            setTempTestRunner: null,

        };
    },
    created() {
        this.organizationIdCheck = sessionStorage.getItem("organizationId");
        this.mlComponentId = sessionStorage.getItem("mlComponentId");
        this.testDescriptionId = sessionStorage.getItem("testDescriptionId");
        this.getTestDescription();
    },
    mounted: function () {
        this.mlComponentIdCheck();
        this.getMLComponent();
        this.setLanguageData();
    },
    computed: {
        filterTestRunners() {
            const testRunnersList = [];
            if (this.testRunners != null) {
                this.testRunners.forEach((testRunner) => {
                    if (
                        this.selectedTestrunner != null &&
                        this.selectedTestrunner.Id == testRunner.Id
                    ) {
                        testRunner = this.selectedTestrunner;
                    }
                    if (testRunner.QualityDimensionId == this.selectedQualityDimension) {
                        testRunnersList.splice(0, 0, testRunner);
                    }
                });
            }
            return testRunnersList;
        },
    },
    methods: {
        //言語データ読み込み
        setLanguageData() {
            // 画面遷移時にセッションから言語情報を取得する。
            // ない場合は英語とする
            var lang = sessionStorage.getItem('language')
            if (lang === null) {
                this.$i18n.locale = 'en';
            } else {
                this.$i18n.locale = lang;
            }
        },
        changeLanguage(lang) {
            sessionStorage.setItem('language', lang);
            this.$i18n.locale = lang;
        },
        //編集2画面目への遷移
        postTestDescriptionEdit() {
            //Quality Dimensionの名前の取得
            var qualityDimensionIdGet = document.getElementById("qualityDimensionId");
            var qualityDimensionIndex = qualityDimensionIdGet.selectedIndex; //インデックス番号を取得
            var qualityDimensionName = qualityDimensionIdGet.options[qualityDimensionIndex].text;
            if (this.setTempTestRunner.Id == this.changeTestrunner.Id) {
                for (var i = 0; i < this.test_description_detail.TargetInventories.length; i++) {
                    for (var j = 0; j < this.test_description_detail.TargetInventories.length; j++) {
                        if (this.changeTestrunner.TargetInventories[i].Id == this.test_description_detail.TargetInventories[j].TemplateInventoryId) {
                            this.selectedInventories["selectedInventory" + i] = this.test_description_detail.TargetInventories[j].Id;
                        }
                    }
                }
                this.setMeasurementFormsList();
                sessionStorage.setItem('setTempTestRunnerId', this.setTempTestRunner.Id);
                sessionStorage.setItem('setTempTestRunner',JSON.stringify(this.setTempTestRunner));
                sessionStorage.setItem('changeTestrunnerId',this.changeTestrunner.Id);
                sessionStorage.setItem('testDescriptionName',this.testDescriptionName);
                sessionStorage.setItem('qualityDimension',this.changeDemension);
                sessionStorage.setItem('testRunner',JSON.stringify(this.changeTestrunner));
                sessionStorage.setItem('qualityDimensionName',qualityDimensionName);
                sessionStorage.setItem('testDescriptionId',this.testDescriptionId);
                sessionStorage.setItem('selectedInventories',JSON.stringify(this.selectedInventories));
                sessionStorage.setItem('selectedTestrunner',JSON.stringify(this.selectedTestrunner));
                sessionStorage.setItem('checkedMeasurements',this.checkedMeasurements);
                sessionStorage.setItem('measurementFormsList',JSON.stringify(this.measurementFormsList));
                sessionStorage.setItem('test_description_detail',JSON.stringify(this.test_description_detail));
                this.$router.push({
                    name: "TestDescriptionEdit2"
                });
            } else {
                sessionStorage.setItem('setTempTestRunnerId', this.setTempTestRunner.Id);
                sessionStorage.setItem('setTempTestRunner', JSON.stringify(this.setTempTestRunner));
                sessionStorage.setItem('changeTestrunnerId', this.changeTestrunner.Id);
                sessionStorage.setItem('testDescriptionName', this.testDescriptionName);
                sessionStorage.setItem('qualityDimension', this.changeDemension);
                sessionStorage.setItem('testRunner', JSON.stringify(this.changeTestrunner));
                sessionStorage.setItem('qualityDimensionName', qualityDimensionName);
                sessionStorage.setItem('testDescriptionId', this.testDescriptionId);
                sessionStorage.setItem('checkedMeasurements', JSON.stringify(this.checkedMeasurements));
                this.$router.push({
                    name: "TestDescriptionEdit2"
                });
            }
        },
        getTestDescription() {
            const url = this.$backendURL +
                "/" +
                this.organizationIdCheck +
                "/mlComponents/" +
                this.mlComponentId +
                "/testDescriotions/" +
                this.testDescriptionId;
            this.$axios.get(url)
                .then((response) => {
                    this.test_description_detail = response.data.TestDescriptionDetail;
                    // 初期値の代入
                    if (this.$route.params.backTestDescriptionEditData == null) {
                        this.testDescriptionName = this.test_description_detail.Name;
                        this.selectedQualityDimension = this.test_description_detail.QualityDimension.Id;
                        this.setTempTestRunner = this.test_description_detail.TestRunner;
                        this.setTestRunner();
                        this.changeTestrunner = this.selectedTestrunner;
                        for(var i=0; i<this.test_description_detail.TargetInventories.length; i++){
                            for(var j=0; j<this.test_description_detail.TargetInventories.length; j++){
                                if(this.changeTestrunner.TargetInventories[i].Id == this.test_description_detail.TargetInventories[j].TemplateInventoryId){
                                    this.selectedInventories['selectedInventory' + i] = this.test_description_detail.TargetInventories[j].Id
                                }
                            }
                        }
                    } else {
                        this.getBackTestDescriptionData();
                    }
                })
                .catch((error) => {
                    this.$router.push({
                        name: "Information",
                        params: {
                            error
                        },
                    });
                });
        },
        setTestRunner() {
            this.testRunners.forEach((testRunner) => {
                if (this.setTempTestRunner.Id == testRunner.Id) {
                    this.selectedTestrunner = testRunner;
                    if (this.selectedTestrunner.ParamTemplates != null) {
                        for (var paramTemplate of this.selectedTestrunner.ParamTemplates) {
                            for (var param of this.setTempTestRunner.Params) {
                                if (paramTemplate.Id == param.TestRunnerParamTemplateId) {
                                    paramTemplate.DefaultVal = param.Value;
                                }
                            }
                        }
                    }
                }
            });
        },
        setMeasurementFormsList() {
            if (this.test_description_detail.QualityMeasurements.length == 0){
                this.count = 0;
                return;
            }

            var forms = [];
            var preId = this.test_description_detail.QualityMeasurements[0].Id;
            var cnt = 0;
            for (var qualityMeasurement of this.test_description_detail.QualityMeasurements) {
                var measurementForm = {
                    Id: qualityMeasurement.Id,
                    Value: qualityMeasurement.Value,
                    RelationalOperatorId: qualityMeasurement.RelationalOperatorId,
                    Enable: qualityMeasurement.Enable,
                };
                if (preId != qualityMeasurement.Id) {
                    this.measurementFormsList.push(forms);
                    forms = [];
                    forms.push(measurementForm);
                    preId = qualityMeasurement.Id;
                } else if (preId == qualityMeasurement.Id) {
                    forms.push(measurementForm);
                }
                cnt += 1;
                if (qualityMeasurement.Enable == true) {
                    this.checkedMeasurements.push(qualityMeasurement.Id);
                }
            }
            if (forms != []) {
                this.measurementFormsList.push(forms);
            }
            this.count = cnt;
        },
        postTestDescriptionCancel() {
            if (confirm(this.$t("confirm.loseInformation"))) {
                this.$router.push({
                    name: "TestDescriptions",
                });
            }
        },
        aitProgramReset() {
            this.changeTestrunner = null;
        },
        //NEXTボタンの活性化処理
        nextBtnCheck() {
            const div = document.getElementById("next");
            div.classList.add("un_btn");
            var nameCheck = false;
            var qualityDimensionCheck = false;
            var aitProgramCheck = false;
            if (this.testDescriptionName != null && this.testDescriptionName != "") {
                nameCheck = true;
                if (this.changeDemension != null && this.changeDemension != "") {
                    qualityDimensionCheck = true;
                    if (this.changeTestrunner != null && this.changeTestrunner != "") {
                        aitProgramCheck = true;
                        if (
                            nameCheck == true &&
                            qualityDimensionCheck == true &&
                            aitProgramCheck == true
                        ) {
                            div.classList.remove("un_btn");
                        }
                    }
                }
            }
        },
        //TestDescriptionEdit2画面から戻ってきたときの処理
        getBackTestDescriptionData() {
            this.testDescriptionName = this.$route.params.backTestDescriptionEditData.testDescriptionName;
            this.selectedQualityDimension = this.$route.params.backTestDescriptionEditData.selectedQualityDimension;
            this.setTempTestRunner = this.test_description_detail.TestRunner;
            this.changeTestrunner = this.$route.params.backTestDescriptionEditData.selectedTestrunner;
        },
        //選択行の色変化
        changeColorTable() {
            var aitRadio = document.getElementsByClassName("radioCheck");
            for (var i = 0; i < aitRadio.length; i++) {
                var aitTr = aitRadio[i].parentNode.parentNode;
                var aitTd = aitTr.childNodes;
                if (aitRadio[i].checked) {
                    aitTd[0].classList.add("aitProgramTableColor");
                    aitTd[1].classList.add("aitProgramTableColor");
                    aitTd[2].classList.add("aitProgramTableColor");
                } else {
                    aitTd[0].classList.remove("aitProgramTableColor");
                    aitTd[1].classList.remove("aitProgramTableColor");
                    aitTd[2].classList.remove("aitProgramTableColor");
                }
            }
        },
    },
};
</script>

<style scoped>
#search_table {
    margin-bottom: 20px;
}

/*サブメニュー*/
.submenu_detail a {
    margin-left: 15px;
    padding: 5px 30px;
}

.aitProgramTableColor {
    background-color: #d1ff8c;
}

/*メイン*/
.subtitle {
    text-align: left;
    margin-left: 10px;
}

input[type="text"] {
    width: 330px;
}

input[type="text"]:focus,
select:focus {
    background-color: #d0e2be;
}

.select {
    width: 338px;
}

.center {
    text-align: center;
}

.table_block {
    width: 1050px;
}

.th1 {
    width: 25%;
    text-align: left;
    background-color: #d0e2be;
}

.th2 {
    width: 75%;
}

table tr {
    background: none;
}

td {
    padding: 3px;
}

.asterisk {
    color: #ff0000;
}

.category_description {
    padding-left: 10px;
    font-size: 12px;
    word-break: normal;
}

/*Generalテーブル*/
.setting_table {
    width: 720px;
    margin-left: auto;
    margin-right: auto;
}

.setting_table td {
    text-align: left;
}

.setting_table th {
    background: none;
}

.setting_table td span {
    font-size: 14px;
}

.setting_table .center {
    text-align: center;
}

.setting_table .description span {
    font-size: 10px;
}

.check_left {
    width: 5%;
}

.left {
    width: 35%;
}

.right {
    width: 27%;
}

.dashed {
    border-bottom: 1px dashed;
    padding-bottom: 5px;
}

.dashed_tr:last-child .dashed {
    border-bottom: none;
}

/*ボタン*/
.un_btn {
    background-color: #a1a1bb;
    pointer-events: none;
    box-shadow: 0px 2px 3px 1px rgba(0, 0, 0, 0.29);
}

/*AIT Programテーブル*/
.ait_table td {
    text-align: left;
}

.ait_table .center {
    text-align: center;
    background: #d0e2be;
}

thead,
.ait_table {
    display: block;
}

.ait_table .tbody {
    overflow: auto;
    overflow-x: hidden;
    display: block;
    height: 200px;
}

.ait_name {
    width: 350px;
}

.ait_check {
    width: 60px;
}

.ait_description {
    width: 350px;
}

.tbody .ait_check {
    text-align: center;
}
</style>

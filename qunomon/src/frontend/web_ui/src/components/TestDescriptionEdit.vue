<template>
<div>
    <!-- ヘッダ -->
    <header id="head" :class="{ active: this.isActive }">
        <div id="title">
            <button @click="toggleSubmenu(isActive)" class="qq"><img :src="this.isActive ? this.icon2 : this.icon1" alt="Image" width="30" height="auto"></button>
            <h1 class="head_title" v-if="this.mlComponent">{{ this.mlComponent.Name }}
            </h1>
        </div>
    </header>

    <!-- サブメニュー（左カラム） -->

    <SubMenuMLComponent :isActive="this.isActive">
    <!--SubMenuのアイコンとメニューの間の言語項目は各コンポーネントで実施-->
        <template v-slot:language>
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
        </template>
    </SubMenuMLComponent>

    <!-- ニュース（中央カラム） -->
    <div id="main" :class="{ active: isActive }">
        <div id="main_body">
            <div id="search_table">
                <form>
                    <!-- General -->
                    <div class="eachCard">
                        <label class="subtitleArea">
                            <span class="subtitle">
                                <strong>{{$t("testDescriptionEdit.general")}}</strong>
                            </span>
                            <span class="category_description">
                                {{$t("testDescriptionEdit.generalExp")}}
                            </span>
                        </label>
                        <table class="table_block">
                            <tr class="contents-area">
                                <td class="left">
                                    <span>{{$t("testDescriptionEdit.name")}}</span><span class="asterisk">&#042;</span>
                                </td>
                                <td class="right">
                                    <template v-if="$i18n.locale === 'en'">
                                        <input type="text" v-model="testDescriptionName" placeholder="name" name="name" @blur="nextBtnCheck" />
                                    </template>
                                    <template v-else>
                                        <input type="text" v-model="testDescriptionName" placeholder="テストディスクリプション名称" name="name" @blur="nextBtnCheck" />
                                    </template>
                                </td>
                            </tr>
                        </table>
                    </div>
                    <hr />

                    <!-- AIT Program -->
                    <div class="eachCard">
                        <label class="subtitleArea">
                            <span class="subtitle">
                                <strong>{{$t("testDescriptionEdit.ait")}}</strong>
                            </span>
                            <span class="category_description">
                                {{$t("testDescriptionEdit.aitExp")}}
                            </span>
                        </label>
                        <div style="background: white" v-if="selectedQualityDimension">
                            <table class="table_block">
                                <thead>
                                    <tr>
                                        <td class="ait_check center">
                                            <span></span>
                                        </td>
                                        <td @click="sortBy('Name')" :class="addClass('Name')" class="ait_name center sortable">
                                            <span>{{$t("testDescriptionEdit.name")}}</span>
                                            <template v-if="$i18n.locale === 'en'">
                                                <input type="text" placeholder="Search by Name"
                                                        v-model="aitNameFilter"
                                                        v-show="aitNameFilterDisplay"
                                                        @keydown="filterTestRunnersByItem"/>
                                            </template>
                                            <template v-else>
                                                <input type="text" placeholder="名前で検索"
                                                        v-model="aitNameFilter"
                                                        v-show="aitNameFilterDisplay"
                                                        @keydown="filterTestRunnersByItem"/>
                                            </template>
                                        </td>
                                        <td @click="sortBy('Version')" :class="addClass('Version')" class="ait_version center sortable">
                                            <label>{{$t("testDescriptionCreate.version")}}</label>
                                        </td>
                                        <td @click="sortBy('Description')" :class="addClass('Description')" class="ait_description center sortable">
                                            <span>{{$t("testDescriptionEdit.description")}}</span>
                                            <template v-if="$i18n.locale === 'en'">
                                                <input type="text" placeholder="Search by Description"
                                                        v-model="aitDescriptionFilter"
                                                        v-show="aitDescriptionFilterDisplay"
                                                        @keydown="filterTestRunnersByItem"/>
                                            </template>
                                            <template v-else>
                                                <input type="text" placeholder="詳細で検索"
                                                        v-model="aitDescriptionFilter"
                                                        v-show="aitDescriptionFilterDisplay"
                                                        @keydown="filterTestRunnersByItem"/>
                                            </template>
                                        </td>
                                    </tr>
                                </thead>
                                <tbody class="tbody">
                                    <tr class="trName" @click="toggleRow" v-for="(TestRunner, i) in sortFilterTestRunners" :key="TestRunner.Id" v-show="filterTestRunnersDisplayList[i]">
                                        <template v-if="queryBackTestDescriptionEditData != null">
                                            <template v-if="TestRunner.Id == queryBackTestDescriptionEditData.selectedTestrunner.Id">
                                                <td class="ait_check aitProgramTableColor background">
                                                    <input v-bind:value="TestRunner" type="radio" class="list_ radioCheck" name="radio" v-model="changeTestrunner" @change="nextBtnCheck" @click="changeColorTable" />
                                                </td>
                                                <td class="ait_name aitProgramTableColor background">
                                                    <span>{{ TestRunner.Name }}</span>
                                                </td>
                                                <td class="ait_version aitProgramTableColor background">
                                                    <span>{{ TestRunner.Version }}</span>
                                                </td>
                                                <td class="ait_description aitProgramTableColor background">
                                                    <span>{{ TestRunner.Description }}</span>
                                                </td>
                                            </template>
                                            <template v-else>
                                                <td class="ait_check background">
                                                    <input v-bind:value="TestRunner" type="radio" class="list_ radioCheck" name="radio" v-model="changeTestrunner" @change="nextBtnCheck" @click="changeColorTable" />
                                                </td>
                                                <td class="ait_name background">
                                                    <span>{{ TestRunner.Name }}</span>
                                                </td>
                                                <td class="ait_version background">
                                                    <span>{{ TestRunner.Version }}</span>
                                                </td>
                                                <td class="ait_description background">
                                                    <span>{{ TestRunner.Description }}</span>
                                                </td>
                                            </template>
                                        </template>
                                        <template v-else>
                                            <template v-if="TestRunner.Id == test_description_detail.TestRunner.Id">
                                                <td class="ait_check aitProgramTableColor background">
                                                    <input v-bind:value="TestRunner" type="radio" class="list_ radioCheck" name="radio" v-model="changeTestrunner" @change="nextBtnCheck" @click="changeColorTable" />
                                                </td>
                                                <td class="ait_name aitProgramTableColor background">
                                                    <span>{{ TestRunner.Name }}</span>
                                                </td>
                                                <td class="ait_version aitProgramTableColor background">
                                                    <span>{{ TestRunner.Version }}</span>
                                                </td>
                                                <td class="ait_description aitProgramTableColor background">
                                                    <span>{{ TestRunner.Description }}</span>
                                                </td>
                                            </template>
                                            <template v-else>
                                                <td class="ait_check background">
                                                    <input v-bind:value="TestRunner" type="radio" class="list_ radioCheck" name="radio" v-model="changeTestrunner" @change="nextBtnCheck" @click="changeColorTable" />
                                                </td>
                                                <td class="ait_name background">
                                                    <span>{{ TestRunner.Name }}</span>
                                                </td>
                                                <td class="ait_version background">
                                                    <span>{{ TestRunner.Version }}</span>
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
                        <div style="background: white" v-else class="center">
                            <span>{{$t("testDescriptionEdit.mes1")}}</span>
                        </div>
                    </div>
                    <hr />

                    <!-- qualityDimension -->
                    <div class="eachCard">
                        <label class="subtitleArea">
                            <span class="subtitle">
                                <strong>{{$t("testDescriptionEdit.qualityDimension")}}</strong>
                            </span>
                            <span class="category_description">
                                {{$t("testDescriptionEdit.qualityDimensionExp")}}
                            </span>
                        </label>
                        <table class="table_block">
                            <tr class="contents-area">
                                <td class="left">
                                    <span>{{$t("testDescriptionEdit.qualityDimension")}}</span>
                                    <span class="asterisk">&#042;</span>
                                </td>
                                <td class="right">
                                    <select id="qualityDimensionId" class="select" v-model="changeDemension" v-if="qualityDimensions" @change="nextBtnCheck">
                                        <option value=null style="color: gray" disabled>
                                            {{$t("common.defaultPulldown")}}
                                        </option>
                                        <option v-for="qualityDimension in qualityDimensions.QualityDimensions" v-bind:value="qualityDimension.Id" :key="qualityDimension.Id">
                                            {{ qualityDimension.Name }}
                                        </option>
                                    </select>
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
import SubMenuMLComponent from './SubMenuMLComponent.vue';
import { subMenuMixin } from "../mixins/subMenuMixin";
import { urlParameterMixin } from "../mixins/urlParameterMixin";
import { tdMixin } from "../mixins/testDescriptionMixin";
import { AccountControlMixin } from '../mixins/AccountControlMixin';
import "vue-good-table-next/dist/vue-good-table-next.css";

export default {
    components: {SubMenuMLComponent},
    mixins: [subMenuMixin, urlParameterMixin, tdMixin, AccountControlMixin],
    data() {
        return {
            mlComponents: null,
            nameCheck: false,
            aitProgramCheck: false,
            test_description_detail: null,
            setTempTestRunner: null,
            queryBackTestDescriptionEditData: this.$route.query.backTestDescriptionEditData === undefined ? undefined : JSON.parse(this.$route.query.backTestDescriptionEditData)
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
            this.setFilterTestRunnersList(this.testRunners);
            return this.testRunners;
        },
        sortFilterTestRunners() {
            return this.sortObjectMethod(this.filterTestRunners);
        }
    },
    methods: {
        toggleRow(params) {
            if (params.target.parentElement.tagName.includes("TD")){
                params.target.parentElement.parentElement.classList.toggle("expanded")
            } else {
                params.target.parentElement.classList.toggle("expanded")
            }
        },
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

                // inventory設定
                this.setSelectedInventories();
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
                sessionStorage.setItem('aitNameFilter',this.aitNameFilter);
                sessionStorage.setItem('aitDescriptionFilter', this.aitDescriptionFilter);
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
                sessionStorage.setItem('aitNameFilter',this.aitNameFilter);
                sessionStorage.setItem('aitDescriptionFilter', this.aitDescriptionFilter);
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
                "/testDescriptions/" +
                this.testDescriptionId;
            this.$axios.get(url)
                .then((response) => {
                    this.test_description_detail = response.data.TestDescriptionDetail;
                    // 初期値の代入
                    if (this.queryBackTestDescriptionEditData == null) {
                        this.testDescriptionName = this.test_description_detail.Name;
                        this.selectedQualityDimension = this.test_description_detail.QualityDimension.Id;
                        this.setTempTestRunner = this.test_description_detail.TestRunner;
                        this.setTestRunner();
                        this.changeTestrunner = this.selectedTestrunner;
                        // inventory設定
                        this.setSelectedInventories();
                    } else {
                        this.getBackTestDescriptionData();
                    }
                })
                .catch((error) => {
                    this.$router.push({
                        name: "Information",
                        query: {error: JSON.stringify({...error, response: error.response})}
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
            this.aitNameFilter = '';
            this.aitDescriptionFilter = '';
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
            this.testDescriptionName = this.queryBackTestDescriptionEditData.testDescriptionName;
            this.selectedQualityDimension = this.queryBackTestDescriptionEditData.selectedQualityDimension;
            this.setTempTestRunner = this.test_description_detail.TestRunner;
            this.changeTestrunner = this.queryBackTestDescriptionEditData.selectedTestrunner;
            this.aitNameFilter = this.queryBackTestDescriptionEditData.aitNameFilter;
            this.aitDescriptionFilter = this.queryBackTestDescriptionEditData.aitDescriptionFilter;
        },
        //選択行の色変化
        changeColorTable() {
            var aitRadio = document.getElementsByClassName("radioCheck");
            for (var i = 0; i < aitRadio.length; i++) {
                var aitTr = aitRadio[i].parentNode.parentNode;
                var aitTd = aitTr.children;
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
        setSelectedInventories(){
            var selected_inventories_map = new Map();
            for(var inv_i=0; inv_i<this.test_description_detail.TargetInventories.length; inv_i++){
                var template_inventory_id = this.test_description_detail.TargetInventories[inv_i].TemplateInventoryId;
                var inventory_id = this.test_description_detail.TargetInventories[inv_i].Id;
                var temp_arr = [];
                if (selected_inventories_map.get(template_inventory_id) !== undefined) {
                    temp_arr = selected_inventories_map.get(template_inventory_id);
                } 
                temp_arr.push(inventory_id);
                selected_inventories_map.set(template_inventory_id, temp_arr)
            }
            
            this.selectedInventories = [];
            for (var inv_j=0; inv_j<this.changeTestrunner.TargetInventories.length; inv_j++) {
                var target_invtentory_id = this.changeTestrunner.TargetInventories[inv_j].Id;
                var selected_inventories_arr = selected_inventories_map.get(target_invtentory_id);
                if (selected_inventories_arr === undefined) {
                    selected_inventories_arr = [];
                }
                var display_flag_list = [];
                var target_invtentory_min = this.changeTestrunner.TargetInventories[inv_j].Min;
                for (var min_i = 0; min_i<selected_inventories_arr.length; min_i++) {
                    if (min_i + 1 <= target_invtentory_min) {
                        display_flag_list.push(false);
                    } else {
                        display_flag_list.push(true);
                    }
                }
                this.selectedInventories.push({
                    name: this.changeTestrunner.TargetInventories[inv_j].Name,
                    value_list: selected_inventories_arr,
                    display_flag_list: display_flag_list
                });
            }
        },
    },
};
</script>

<style scoped>

#head {
    z-index: 1;
}

#main {
    overflow: hidden;
}

#main #main_body {
    /*position: relative;*/
    z-index: 0;
}

#search_table {
    padding-top: 2rem;
    margin: 0 auto;
    text-align: center;
    width: 90%;
}
.eachCard {
    width: 100%;
    background: #fff;
    border-radius: 5px;
    max-height:30rem;
    overflow:auto
}
.subtitleArea {
    background-color: var(--secondary-color);
    color: #ffffff;
    border-top-right-radius: 5px;
    border-top-left-radius: 5px;
    margin: 0;
    width: 100%;
    height: 4.5rem;
    font-weight: bold;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.subtitleArea label {
    font-size: 1rem;
    font-weight: bold;
}
.subtitle{
    color: #fff;
}
.table_block {
    width: 95%;
    margin: 0.5rem auto;
    vertical-align: middle;
    position: relative;
    border-collapse: separate;
    border-spacing: 0 5px;
    font-size: 0.85rem;
}
.table_block thead {
    color: white;
    background: var(--secondary-color);
    text-align: center;
    border: none;
    width: 1rem;
    height: 2.5rem;
    padding: unset;
    vertical-align: middle;
    font-weight: bold;
}
.table_block thead tr td:first-child {
    border-top-left-radius: 5px;
}
.table_block thead tr td:last-child {
    border-top-right-radius: 5px;
}
.trName td:nth-child(1) {
    width: 5%;
}
.table_block .tbody tr td{
    text-align: center;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 140px;
    height: 2rem;
}
.table_block .tbody .expanded td {
    white-space: normal;
    overflow: visible;
    text-overflow: unset;
}
.table_block tbody tr {
    background-color: var(--gray-thema); /* Set row background color */
    border: rgba(0, 0, 0, 0.2);
    box-shadow: 0 0 2px rgba(0, 0, 0, 0.1); /* Add a box shadow for depth */
    border-radius: 5px;
}
.table_block tbody tr td:nth-child(1) {
    border-bottom-left-radius: 5px;
    border-top-left-radius: 5px;
}
.table_block tbody tr td:last-child {
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
}

.table_block tbody tr:hover{
    background: var(--primary-color-light) !important;

}
.table_block .contents-area {
    height: 2rem;
}
.table_block .contents-area td{
    width: 50%;
    height: 2rem;
    font-size: 0.85rem;
}
.table_block .left {
    background: var(--primary-color);
    color: white;
    width: 100%;
    font-weight: bold;
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
}
.table_block .right {
    border: 1px solid;
    border-color: var(--primary-color);
    background: var(--gray-thema);
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
}
.table_block .right input {
    width: 100%;
    height: 2rem;
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
}
.table_block .right select {
    width: 100%;
    height: 2rem;
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
}
.ait_name.center {
    width: 50%;
}
.ait_name.center label {
    width: 20%;
    height: 100%;
    font-weight: bold;
    font-size: 1rem;
}
.ait_name.center input {
    width: 50%;
    padding-left: 1rem;
    border-radius: 5px;
}
.ait_version.center {
    width: 10%;
}
.ait_version.center label {
    width: 50%;
    height: 100%;
    font-weight: bold;
    font-size: 1rem;
}
.ait_description.center {
    width: 50%;
}
.ait_description.center label{
    width: 20%;
    height: 100%;
    font-weight: bold;
    font-size: 1rem;
}
.aitProgramTableColor {
    background-color: var(--primary-color-light);
}
.ait_description.center input{
    width: 50%;
    margin-left: 1rem;
    border-radius: 5px;
}
.asterisk {
    color: #ff0000;
}
.category_description {
    font-size: 0.8rem;
    color: var(--text-color-black);
}
.table_block .sortable{
    cursor:pointer;
    text-align: center;
    border: none;
    vertical-align: middle;
    position: relative;
    &::before {
        content: "";
        position: absolute;
        height: 0;
        width: 0;
        right: 0;
        top: 50%;
        margin-bottom: -7px;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid #cfd3e0;
    }
    &::after {
        content: "";
        position: absolute;
        height: 0;
        width: 0;
        right: 0;
        top: 50%;
        margin-top: -7px;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-bottom: 5px solid #cfd3e0;
    }
    &.desc::before{
        border-top: 5px solid #409eff;
    }
    &.asc::after{
        border-bottom: 5px solid #409eff;
    }
}
</style>

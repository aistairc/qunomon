<template>
    <div>
        <header id="head" :class="{ active: this.isActive }">
            <div id="title">
                <button @click="toggleSubmenu(isActive)" class="qq"><img :src="this.isActive ? this.icon2 : this.icon1"
                                                                alt="Image" width="30" height="auto"></button>
                <h1 class="head_title" v-if="this.mlComponent">
                    {{ this.mlComponent.Name }}
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
                        <a href="#" v-on:click.prevent="changeLanguage('ja')"
                           class="btn_unselect">{{ $t("common.lanJa") }}</a>
                        <a href="#" class="btn_select">{{ $t("common.lanEn") }}</a>
                    </template>
                    <template v-else>
                        <a href="#" class="btn_select">{{ $t("common.lanJa") }}</a>
                        <a href="#" v-on:click.prevent="changeLanguage('en')"
                           class="btn_unselect">{{ $t("common.lanEn") }}</a>
                    </template>
                </div>
            </template>
        </SubMenuMLComponent>


        <!-- ニュース（中央カラム） -->
        <div id="main" :class="{ active: this.isActive }">
            <div id="main_body">
                <div id="search_table">

                    <!-- General -->
                    <div class="eachCard">
                        <label class="subtitleArea">
                            <span class="subtitle">
                                <strong>{{ $t("testDescriptionEdit.general") }}</strong>
                            </span>
                            <span class="category_description">
                                {{ $t("testDescriptionEdit.generalExp") }}
                            </span>
                        </label>
                        <table class="table_block">
                            <tr class="contents-area">
                                <td class="left">
                                    <span>{{ $t("testDescriptionEdit.name") }}</span>
                                </td>
                                <td class="right">
                                    <span>{{testDescriptionName}}</span>
                                </td>
                            </tr>
                            <tr class="contents-area">
                                <td class="left">
                                    <span>{{ $t("testDescriptionEdit.qualityDimension") }}</span>
                                </td>
                                <td class="right">
                                  <span>{{qualityDimensionName}}</span>
                                </td>
                            </tr>
                            <tr class="contents-area">
                                <td class="left">
                                    <span>{{ $t("testDescriptionEdit.ait") }}</span>
                                </td>
                                <td class="right">
                                    <span>{{ selectedTestrunner.Name }}</span>
                                </td>
                            </tr>
                        </table>
                    </div>
                    <hr/>

                    <!-- Acceptance Criteria -->
                    <div class="eachCard">
                        <label class="subtitleArea">
                            <span class="subtitle">
                                <strong>{{ $t("testDescriptionEdit.qualityMeasurement") }}</strong>
                            </span>
                            <span class="category_description">
                                {{ $t("testDescriptionEdit.qualityMeasurementExp") }}
                            </span>
                            <span class="asterisk">
                                {{ $t("testDescriptionEdit.qualityMeasurementNote") }}
                            </span>
                        </label>
                        <table class="table_block">
                            <template v-for="(measure, i) in this.report.Measures">
                                <tr class="dashed_tr2" v-for="measurementForm in measurementFormsList[i]" :key="measurementForm.Id">
                                    <td class="tdQACheck dashed">
                                        <input v-bind:value="measurementForm.Id" type="checkbox" class="list_ checkboxCheck" name="listCheck" v-model="checkedMeasurements" @change="changecheckbox"/>
                                    </td>
                                    <td class="tdQAName dashed" id="checkbox">
                                        <span>{{ measure.Name }}</span>
                                        <span class="asterisk">&#042;</span>
                                        <span class="type">&#058; {{ measure.Type }}</span>
                                    </td>
                                    <td class="tdQAName dashed" id="checkbox">
                                        <span class="range" v-if="measure.Type == 'float' || measure.Type == 'int'">
                                            <span class="max" v-if="measure.Max !== null">Max: {{ measure.Max }}</span>
                                            <span class="max unlimited" v-else>Max: unlimited</span>
                                        </span>
                                    </td>
                                    <td class="tdQAName dashed" id="checkbox">
                                        <span class="range" v-if="measure.Type == 'float' || measure.Type == 'int'">
                                            <span class="min" v-if="measure.Min !== null">Min: {{ measure.Min }}</span>
                                            <span class="min unlimited" v-else>Min: unlimited</span>
                                        </span>
                                    </td>
                                    <td class="tdQAName dashed" id="checkbox">
                                        <span class="description">{{measure.Description}}</span>
                                    </td>
                                    <td class="tdQARelationalOperator td_margin">
                                        <select
                                                class="select_mini"
                                                name="myText"
                                                v-model="measurementForm.RelationalOperatorId"
                                                v-if="relationalOperators"
                                        >
                                            <option
                                                    v-for="relationalOperator in relationalOperators.RelationalOperator"
                                                    v-bind:value="relationalOperator.Id"
                                                    :key="relationalOperator.Id"
                                            >{{ relationalOperator.Expression }}
                                            </option>
                                        </select>
                                    </td>
                                    <td class="tdQAValue td_margin">
                                        <input
                                                type="text"
                                                placeholder="0"
                                                class="text_mini"
                                                name="myText"
                                                size="5"
                                                v-model="measurementForm.Value"
                                        />
                                    </td>
                                </tr>
                            </template>
                        </table>
                    </div>
                    <hr/>

                    <!-- AIT Parameter -->
                    <div class="eachCard">
                        <label class="subtitleArea">
                            <span class="subtitle">
                                <strong>{{ $t("testDescriptionEdit.aitParam") }}</strong>
                            </span>
                            <span class="category_description">
                                {{ $t("testDescriptionEdit.aitParamExp") }}
                            </span>
                        </label>
                        <table class="table_block">
                            <thead>
                                <tr>
                                    <td class="ait_terms center">
                                        <span>{{ $t("testDescriptionEdit.name") }}</span>
                                    </td>
                                    <td class="ait_description center">
                                        <span>{{ $t("testDescriptionEdit.description") }}</span>
                                    </td>
                                    <td class="ait_input center">
                                        <span>{{ $t("testDescriptionEdit.aitInput") }}</span>
                                    </td>
                                </tr>
                            </thead>
                            <tbody class="tbody">
                                <tr v-for="(param, i) in this.selectedTestrunner.ParamTemplates" :key="param.Id">
                                    <td class="ait_terms">
                                        <span v-bind:class="{disabledStyle: paramTemplateDisableList[i]}">{{param.Name}}</span>
                                        <span class="asterisk" v-if="paramTemplateRequiredList[i]">&#042;</span>
                                        <span v-bind:class="{disabledStyle: paramTemplateDisableList[i]}" class="type">&#058; {{param.Type}}</span>
                                        <span v-bind:class="{disabledStyle: paramTemplateDisableList[i]}" class="range"
                                              v-if="param.Type == 'float' || param.Type == 'int'">
                                            <br/>
                                            <span v-bind:class="{disabledStyle: paramTemplateDisableList[i]}" class="min"
                                                    v-if="param.Min !== null">Min: {{ param.Min }}</span>
                                              <span class="min unlimited" v-else>Min: unlimited</span>
                                              <span v-bind:class="{disabledStyle: paramTemplateDisableList[i]}" class="max"
                                                    v-if="param.Max !== null">Max: {{ param.Max }}</span>
                                              <span class="max unlimited" v-else>Max: unlimited</span>
                                        </span>
                                    </td>
                                    <td class="ait_description">
                                        <span v-bind:class="{disabledStyle: paramTemplateDisableList[i]}">{{
                                                param.Description
                                            }}</span>
                                    </td>
                                    <td class="ait_input">
                                        <input
                                                v-bind:disabled="paramTemplateDisableList[i]"
                                                type="text"
                                                placeholder=""
                                                name="myText"
                                                v-model="param.DefaultVal"
                                                @change="setDependencyParamNameDisable"
                                        />
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <hr/>

                    <!-- Inventory Edit -->
                    <div class="eachCard">
                        <label class="subtitleArea">
                            <span class="subtitle">
                                <strong>{{ $t("testDescriptionEdit.targetInventory") }}</strong>
                            </span>
                            <span class="category_description">
                                {{ $t("testDescriptionEdit.taegetInventoryExp") }}
                            </span>
                        </label>
                        <table class="table_block">
                            <thead>
                                <tr>
                                    <td class="inventory_terms center">
                                        <span>{{ $t("testDescriptionEdit.name") }}</span>
                                    </td>
                                    <td class="inventory_data_type center">
                                        <span>{{ $t("testDescriptionEdit.dataType") }}</span>
                                    </td>
                                    <td class="inventory_formats center">
                                        <span>{{ $t("testDescriptionEdit.formats") }}</span>
                                    </td>
                                    <td class="inventory_description center">
                                        <span>{{ $t("testDescriptionEdit.description") }}</span>
                                    </td>
                                    <td class="inventory_input center">
                                        <span>{{ $t("testDescriptionEdit.inventoryInput") }}</span>
                                    </td>
                                    <td class="inventory_add center"/>
                                </tr>
                            </thead>
                            <tbody class="tbody">
                                <tr v-for="(TargetInventory, i) in this.selectedTestrunner.TargetInventories" :key="TargetInventory.Id">
                                    <td class="inventory_terms">
                                        <span v-bind:class="{disabledStyle: targetInventoryDisableList[i]}">{{
                                                TargetInventory.Name
                                            }}</span>
                                        <span class="asterisk"
                                              v-if="targetInventoryRequiredList[i]">&#042;</span>
                                    </td>
                                    <td class="inventory_data_type">
                                        <span v-bind:class="{disabledStyle: targetInventoryDisableList[i]}">{{ TargetInventory.DataType.Name }}</span>
                                    </td>
                                    <td class="inventory_formats">
                                        <span
                                                v-bind:class="{disabledStyle: targetInventoryDisableList[i]}"
                                                v-for="Format in TargetInventory.Formats"
                                                :key="Format.Id"
                                        >{{ Format.Format }}
                                        </span>
                                    </td>
                                    <td class="inventory_description">
                                        <span v-bind:class="{disabledStyle: targetInventoryDisableList[i]}">{{
                                                TargetInventory.Description
                                            }}</span>
                                    </td>
                                    <template v-if="TargetInventory.Max != '1'">
                                        <template
                                                v-if="filterInventories(TargetInventory.DataType.Id, TargetInventory.Formats).length">
                                            <td class="inventory_input" colspan="2">
                                                <table class="inv_tbl">
                                                    <tr>
                                                        <td colspan="2">
                                                            <template
                                                                    v-if="TargetInventory.Min == TargetInventory.Max">
                                                                <template v-if="$i18n.locale === 'en'">
                                                                    <span>Please set {{ TargetInventory.Max }} items.</span>
                                                                </template>
                                                                <template v-else>
                                                                    <span>{{ TargetInventory.Max }}個を設定してください。</span>
                                                                </template>
                                                            </template>
                                                            <template v-else>
                                                                <template v-if="$i18n.locale === 'en'">
                                                                    <span>Configurable items <br> from {{ TargetInventory.Min }} to {{ TargetInventory.Max }}.</span>
                                                                </template>
                                                                <template v-else>
                                                                    <span>設定可能な個数は<br>{{ TargetInventory.Min }}～{{ TargetInventory.Max }}です。</span>
                                                                </template>
                                                            </template>
                                                        </td>
                                                        <td class="inventory_add">
                                                            <template v-if="$i18n.locale === 'en'">
                                                                <button v-bind:disabled="targetInventoryDisableList[i]" class="btnImg" alt="add" title="add"
                                                                        @click="inventoryAdd($route.path, TargetInventory.DataType.Id, TargetInventory.Formats[0].Format)">
                                                                </button>
                                                            </template>
                                                            <template v-else>
                                                                <button v-bind:disabled="targetInventoryDisableList[i]" class="btnImg" alt="追加" title="追加"
                                                                        @click="inventoryAdd($route.path, TargetInventory.DataType.Id, TargetInventory.Formats[0].Format)">
                                                                </button>
                                                            </template>
                                                        </td>
                                                    </tr>
                                                    <tr v-for="(selectedInventory, invindex) in selectedInventories[i].value_list" :key="selectedInventory">
                                                        <td colspan="2">
                                                            <select  v-model=" selectedInventories[i].value_list[invindex]" class="select_multi_inv" v-bind:disabled="targetInventoryDisableList[i]">
                                                                <option
                                                                        v-for="inventory in filterInventories(TargetInventory.DataType.Id,TargetInventory.Formats)"
                                                                        v-bind:value="inventory.Id"
                                                                        :key="inventory.Id">
                                                                    {{ inventory.Name }}
                                                                </option>
                                                            </select>
                                                        </td>
                                                        <td>
                                                            <template
                                                                    v-if="selectedInventories[i].display_flag_list[invindex] == true">
                                                                <input v-bind:disabled="targetInventoryDisableList[i]"
                                                                       type="button" value="－"
                                                                       class="btn_single inv_btn"
                                                                       @click="deleteSelectedInventory(i, invindex)"
                                                                       />
                                                            </template>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td colspan="2">
                                                        </td>
                                                        <td>
                                                            <template
                                                                    v-if="selectedInventories[i].value_list.length < TargetInventory.Max">
                                                                <input v-bind:disabled="targetInventoryDisableList[i]"
                                                                       type="button" value="＋"
                                                                       class="btn_single inv_btn"
                                                                       @click="addSelectedInventory(i)"
                                                                       />
                                                            </template>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </template>
                                        <template v-else>
                                            <td>
                                                <span class="error" v-if="!targetInventoryDisableList[i]">
                                                    <img src="~@/assets/error2.svg" alt="Please Add Inventory" class="icon status">
                                                        {{ $t("testDescriptionCreate.inventoryNote") }}
                                                </span>
                                            </td>
                                            <td class="inventory_add">
                                                <template v-if="$i18n.locale === 'en'">
                                                    <button v-bind:disabled="targetInventoryDisableList[i]" class="btnImg" alt="add" title="add"
                                                            @click="inventoryAdd($route.path, TargetInventory.DataType.Id, TargetInventory.Formats[0].Format)">
                                                    </button>
                                                </template>
                                                <template v-else>
                                                    <button v-bind:disabled="targetInventoryDisableList[i]" class="btnImg" alt="追加" title="追加"
                                                            @click="inventoryAdd($route.path, TargetInventory.DataType.Id, TargetInventory.Formats[0].Format)">
                                                    </button>
                                                </template>
                                            </td>
                                        </template>
                                    </template>
                                    <template v-else>
                                        <td class="inventory_input">
                                            <span v-if="filterInventories(TargetInventory.DataType.Id, TargetInventory.Formats).length" class="single_btn">
                                                <select v-bind:disabled="targetInventoryDisableList[i]" v-model=" selectedInventories[i].value_list[0]" class="select">
                                                    <option
                                                        v-for="inventory in filterInventories(TargetInventory.DataType.Id,TargetInventory.Formats)" v-bind:value="inventory.Id"
                                                        :key="inventory.Id"
                                                        >
                                                        {{ inventory.Name }}
                                                    </option>
                                                </select>
                                            </span>
                                            <span class="error" v-else>
                                                 <span v-if="!targetInventoryDisableList[i]">
                                                        <img src="~@/assets/error2.svg" alt="Please Add Inventory" class="icon status">
                                                     {{ $t("testDescriptionCreate.inventoryNote") }}
                                                 </span>
                                            </span>
                                        </td>
                                        <td class="inventory_add">
                                            <template v-if="$i18n.locale === 'en'">
                                                <button v-bind:disabled="targetInventoryDisableList[i]" class="btnImg" alt="add" title="add"
                                                        @click="inventoryAdd($route.path, TargetInventory.DataType.Id, TargetInventory.Formats[0].Format)">
                                                </button>
                                            </template>
                                            <template v-else>
                                                <button v-bind:disabled="targetInventoryDisableList[i]" class="btnImg" alt="追加" title="追加"
                                                        @click="inventoryAdd($route.path, TargetInventory.DataType.Id, TargetInventory.Formats[0].Format)">
                                                </button>
                                            </template>
                                        </td>
                                    </template>
                                </tr>
                            </tbody>
                            <inventoryAdd :key="edit_key" ref="addInventoryBtn" @addInventory="addInventories"></inventoryAdd>
                        </table>
                    </div>
                    <hr/>

                    <!-- errorMessage -->
                    <span v-if="errorMessages">
                        <span class="error_message" v-for="errorMessage in errorMessages" :key="errorMessage">
                            {{ errorMessage }}<br/>
                        </span>
                    </span>

                    <!-- submit -->
                    <div id="btn_set">
                        <template v-if="$i18n.locale === 'en'">
                            <input type="button" value="Back" class="btn_left" @click="backTestDescriptionEdit"/>
                            <input type="button" value="Update" class="btn_right" @click="postTestDescription"/>
                        </template>
                        <template v-else>
                            <input type="button" value="戻る" class="btn_left" @click="backTestDescriptionEdit"/>
                            <input type="button" value="更新" class="btn_right" @click="postTestDescription"/>
                        </template>
                    </div>
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
import {urlParameterMixin} from "../mixins/urlParameterMixin";
import {tdMixin} from "../mixins/testDescriptionMixin";
import {AccountControlMixin} from '../mixins/AccountControlMixin';
import {csrfMixin} from '../mixins/csrfMixin';
import "vue-good-table-next/dist/vue-good-table-next.css";
import inventoryAdd from "./InventoryAdd.vue";

export default {
    components: {
        SubMenuMLComponent,
        inventoryAdd,
    },
    mixins: [subMenuMixin, urlParameterMixin, tdMixin, AccountControlMixin, csrfMixin],
    data() {
        return {
            mlComponents: null,
            test_description_edit2: null,
            edit_key: 0,
            testDescriptionName: '',
            qualityDimension: '',
            selectedTestrunner: {},
            qualityDimensionName: '',
            report: {}
        };
    },
    mounted() {
        this.mlComponentIdCheck();
        this.organizationIdCheck = sessionStorage.getItem("organizationId");
        this.mlComponentId = sessionStorage.getItem("mlComponentId");
        this.getMLComponent();
        this.getEdit();

    },
    computed: {},
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
        postTestDescription() {
            this.errorMessages = [];
            this.commonCheckTestDescription();
            if (this.errorMessages.length === 0) {
                if (confirm(this.$t("confirm.edit"))) {
                    this.setTestDescription();
                    const url = this.$backendURL
                        + '/'
                        + this.organizationIdCheck
                        + '/mlComponents/'
                        + this.mlComponentId
                        + '/testDescriptions/'
                        + this.testDescriptionId;
                    //リクエスト時のオプションの定義
                    const config = {
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest',
                            'X-CSRF-TOKEN': this.getCookie("csrf_access_token")
                        },
                        withCredentials: true,
                    }
                    this.$axios
                        .put(url, this.requestData, config)
                        .then((response) => {
                            this.result = response.data;
                            this.$router.push({
                                name: 'TestDescriptions'
                            });
                        })
                        .catch((error) => {
                            this.$router.push({
                                name: "Information",
                                query: {error: JSON.stringify({...error, response: error.response})},
                            });
                        });
                }
            } else {
                scrollTo(0, 0);
            }
        },
        getEdit() {
            this.testDescriptionId = sessionStorage.getItem('testDescriptionId');
            this.testDescriptionName = sessionStorage.getItem('testDescriptionName');
            this.qualityDimension = sessionStorage.getItem('qualityDimension');
            this.selectedTestrunner = JSON.parse(sessionStorage.getItem('testRunner'));
            this.report = this.selectedTestrunner.Report;
            this.qualityDimensionName = sessionStorage.getItem('qualityDimensionName');
            this.aitNameFilter = sessionStorage.getItem('aitNameFilter');
            this.aitDescriptionFilter = sessionStorage.getItem('aitDescriptionFilter');
            if (sessionStorage.getItem('setTempTestRunnerId') == sessionStorage.getItem('changeTestrunnerId')) {
                this.selectedInventories = JSON.parse(sessionStorage.getItem('selectedInventories'));
                this.checkedMeasurements = JSON.parse(sessionStorage.getItem('measurementFormsList'));
                this.setMeasurementFormsEdit();
            } else {
                // inventoryの初期設定
                this.selectedInventories = [];
                for (var targetInventory_index in this.selectedTestrunner.TargetInventories) {
                    var value_list = [];
                    var display_flag_list = [];
                    for (var min_i = 0; min_i < this.selectedTestrunner.TargetInventories[targetInventory_index].Min; min_i++) {
                        value_list.push('');
                        display_flag_list.push(false);
                    }
                    this.selectedInventories.push({
                        name: this.selectedTestrunner.TargetInventories[targetInventory_index].Name,
                        value_list: value_list,
                        display_flag_list: display_flag_list
                    });
                }
                this.checkedMeasurements = [];
                this.setMeasurementForms();
            }
            this.setDependencyParamNameList();
        },
        //TestDescriptionEdit1の画面へ戻る処理
        backTestDescriptionEdit() {
            if (confirm(this.$t("confirm.loseInformation"))) {
                this.setTestDescriptionData();
                this.$router.push({
                    name: "TestDescriptionEdit",
                    query: {backTestDescriptionEditData: JSON.stringify(this.backTestDescriptionEditData), testDescriptionId: this.testDescriptionId}
                });
            }
        },
        setTestDescriptionData() {
            this.backTestDescriptionEditData.testDescriptionName = this.testDescriptionName;
            this.backTestDescriptionEditData.selectedQualityDimension = this.qualityDimension;
            this.backTestDescriptionEditData.selectedTestrunner = this.selectedTestrunner;
            this.backTestDescriptionEditData.aitNameFilter = this.aitNameFilter;
            this.backTestDescriptionEditData.aitDescriptionFilter = this.aitDescriptionFilter;
        },
        //Acceptance Criteriaのチェックボックスの処理
        changecheckbox() {
            var qaCheckbox = document.getElementsByClassName("checkboxCheck");
            for (var i = 0; i < qaCheckbox.length; i++) {
                var qaName = qaCheckbox[i].parentNode.nextSibling;
                var qaRelationalOperator = qaName.nextSibling;
                var qaValue = qaRelationalOperator.nextSibling;
                if (qaCheckbox[i].checked) {
                    qaName.classList.remove("acceptanceCriteriaChecked");
                    qaRelationalOperator.classList.remove("acceptanceCriteriaChecked");
                    qaValue.classList.remove("acceptanceCriteriaChecked");
                } else {
                    qaName.classList.add("acceptanceCriteriaChecked");
                    qaRelationalOperator.classList.add("acceptanceCriteriaChecked");
                    qaValue.classList.add("acceptanceCriteriaChecked");
                }
            }
        },
        setMeasurementFormsEdit() {
            if (JSON.parse(sessionStorage.getItem('test_description_detail')).QualityMeasurements.length == 0) {
                this.count = 0;
                return;
            }

            var forms = [];
            var preId = JSON.parse(sessionStorage.getItem('test_description_detail')).QualityMeasurements[0].Id;
            var cnt = 0;
            for (var qualityMeasurement of JSON.parse(sessionStorage.getItem('test_description_detail')).QualityMeasurements) {
                var measurementForm = {
                    Id: qualityMeasurement.Id,
                    Value: qualityMeasurement.Value,
                    RelationalOperatorId: qualityMeasurement.RelationalOperatorId,
                    Enable: qualityMeasurement.Enable
                };
                if (preId != qualityMeasurement.Id) {
                    this.measurementFormsList.push(forms);
                    forms = [];
                    forms.push(measurementForm);
                    preId = qualityMeasurement.Id
                } else if (preId == qualityMeasurement.Id) {
                    forms.push(measurementForm);
                }
                cnt += 1;
                if (qualityMeasurement.Enable == true) {
                    this.checkedMeasurements.push(qualityMeasurement.Id)
                }
            }
            if (forms != []) {
                this.measurementFormsList.push(forms);
            }
            this.count = cnt;
        },
        commonCheckTestDescription() {
            // criteriaが正常な値か判定
            for (let checkedMeasurement of this.checkedMeasurements) {
                if (typeof (checkedMeasurement) == "number") {
                    let matchedValueStr = null;
                    for (let measurementForm of this.measurementFormsList) {
                        if (measurementForm[0].Id == checkedMeasurement) {
                            matchedValueStr = measurementForm[0].Value;
                            break;
                        }
                    }

                    let matchedMeasure = null;
                    for (let measure of this.report.Measures) {
                        if (measure.Id == checkedMeasurement) {
                            matchedMeasure = measure;
                            break;
                        }
                    }

                    let matchedMeasureType = matchedMeasure.Type;
                    let isValidValue = true;
                    if (matchedMeasureType == 'float' || matchedMeasureType == 'int') {
                        if (isNaN(matchedValueStr)) {
                            // 入力値が非数値の場合
                            isValidValue = false;
                        } else {
                            let matchedValue = parseFloat(matchedValueStr);
                            if (!isNaN(matchedMeasure.Min)) {
                                let matchedMin = parseFloat(matchedMeasure.Min);
                                if (matchedValue < matchedMin) {
                                    isValidValue = false;
                                }
                            }
                            if (isValidValue && !isNaN(matchedMeasure.Max)) {
                                let matchedMax = parseFloat(matchedMeasure.Max);
                                if (matchedMax < matchedValue) {
                                    isValidValue = false;
                                }
                            }
                        }

                        if (!isValidValue) {
                            this.errorMessages.push('The criteria "' + matchedMeasure.Name + '" is invalid value.');
                        }

                    }
                }
            }

            if (this.testDescriptionName == null || this.testDescriptionName === "") {
                this.errorMessages.push('Name is required.');
            } else if (this.testDescriptionName.length > this.maxCharacters) {
                this.errorMessages.push('Name must be ' + this.maxCharacters + ' characters or less.');
            }
            if (this.qualityDimension == null || this.qualityDimension === "") {
                this.errorMessages.push('Quality Dimension is required.');
            } else {
                if (this.selectedTestrunner == null || this.selectedTestrunner === "") {
                    this.errorMessages.push('Test Runner is required.');
                } else {
                    for (var ptindex = 0; ptindex < this.selectedTestrunner.ParamTemplates.length; ptindex++) {
                        var paramTemplate = this.selectedTestrunner.ParamTemplates['' + ptindex];
                        // 必須項目の判断
                        if (this.paramTemplateRequiredList['' + ptindex]) {
                            if (paramTemplate.DefaultVal == null || paramTemplate.DefaultVal === "") {
                                this.errorMessages.push(paramTemplate.Name + ' is required.');
                            } else if (paramTemplate.DefaultVal.length > this.maxCharacters) {
                                this.errorMessages.push(paramTemplate.Name + ' must be ' + this.maxCharacters + ' characters or less.');
                            }
                            // parameterが正常な値か判定
                            else if (paramTemplate.Type == 'float' || paramTemplate.Type == 'int') {
                                let isValidValue = true;
                                if (isNaN(paramTemplate.DefaultVal)) {
                                    // 入力値が非数値の場合
                                    isValidValue = false;
                                } else {
                                    let inputParamValue = parseFloat(paramTemplate.DefaultVal);
                                    if (!isNaN(paramTemplate.Min)) {
                                        let minParamValue = parseFloat(paramTemplate.Min);
                                        if (inputParamValue < minParamValue) {
                                            isValidValue = false;
                                        }
                                    }
                                    if (isValidValue && !isNaN(paramTemplate.Max)) {
                                        let maxParamValue = parseFloat(paramTemplate.Max);
                                        if (inputParamValue > maxParamValue) {
                                            isValidValue = false;
                                        }
                                    }
                                }
                                if (!isValidValue) {
                                    this.errorMessages.push('The parameter "' + paramTemplate.Name + '" is invalid value.');
                                }
                            }
                        }
                    }
                    if (this.selectedInventories == null || this.selectedInventories == {}) {
                        this.errorMessages.push('Target Inventory is required.');
                    } else {
                        for (var inv_i = 0; inv_i < this.selectedTestrunner.TargetInventories.length; inv_i++) {
                            if (this.targetInventoryRequiredList['' + inv_i] == true) {
                                var targetInventory = this.selectedTestrunner.TargetInventories['' + inv_i];
                                var selectedInventory = this.selectedInventories['' + inv_i];
                                if (targetInventory.Min > selectedInventory.value_list.length) {
                                    this.errorMessages.push('Target Inventory "' + targetInventory.Name + '" Invalid of files(min).');
                                } else if (targetInventory.Max < selectedInventory.value_list.length) {
                                    this.errorMessages.push('Target Inventory "' + targetInventory.Name + '" Invalid of files(max).');
                                } else {
                                    for (var inv_j = 0; inv_j < selectedInventory.value_list.length; inv_j++) {
                                        if (selectedInventory.value_list['' + inv_j] == '') {
                                            this.errorMessages.push('Target Inventory "' + targetInventory.Name + '" is required.');
                                            break;
                                        }
                                    }
                                }
                            }
                        }
                    }
                    for (var j = 0; j < this.selectedTestrunner.Report.Measures.length; j++) {
                        for (var form of this.measurementFormsList[j]) {
                            if (this.checkedMeasurements.includes(form.Id)) {
                                if (form.RelationalOperatorId == null || form.RelationalOperatorId === "") {
                                    if (this.errorMessages.indexOf('RelationalOperator is required.') == -1) {
                                        this.errorMessages.push('RelationalOperator is required.');
                                    }
                                }
                                if (form.Value == null || form.Value === "") {
                                    if (this.errorMessages.indexOf('Measurement Value is required.') == -1) {
                                        this.errorMessages.push('Measurement Value is required.');
                                    }
                                } else if (form.Value.length > this.maxCharacters) {
                                    if (this.errorMessages.indexOf('Measurement Value must be ' + this.maxCharacters + ' characters or less.') == -1) {
                                        this.errorMessages.push('Measurement Value must be ' + this.maxCharacters + ' characters or less.');
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        setTestDescription() {
            this.selectedTestrunner.ParamTemplates.forEach(paramTemplate => {
                delete paramTemplate["ValueType"]
            });

            this.requestData.Name = this.testDescriptionName;
            this.requestData.QualityDimensionID = this.qualityDimension;
            if (this.selectedTestrunner != null) {
                for (var j = 0; j < this.selectedTestrunner.Report.Measures.length; j++) {
                    for (var form of this.measurementFormsList[j]) {
                        if (this.checkedMeasurements.includes(form.Id)) {
                            form.Enable = true;
                        } else {
                            form.Enable = false;
                        }
                        this.requestData.QualityMeasurements.push(form);
                    }
                }
            }
            for (var inv_i = 0; inv_i < this.selectedInventories.length; inv_i++) {
                var value_list = this.selectedInventories[inv_i].value_list;
                for (var inv_j = 0; inv_j < value_list.length; inv_j++) {
                    if (value_list[inv_j] != '') {
                        this.requestData.TargetInventories.push({
                            Id: inv_i + 1,
                            InventoryId: value_list[inv_j],
                            TemplateInventoryId: this.selectedTestrunner.TargetInventories[inv_i].Id
                        });
                    }
                }
            }
            if (this.selectedTestrunner != null) {
                this.requestData.TestRunner.Id = this.selectedTestrunner.Id;
                var params = [];
                for (var paramTemplate of this.selectedTestrunner.ParamTemplates) {
                    var param = {};
                    param.TestRunnerParamTemplateId = paramTemplate.Id;
                    param.Value = paramTemplate.DefaultVal;
                    params.push(param);
                }
                this.requestData.TestRunner.Params = params;
            }
        },
        setPreviousPageSettingData() {
            // modalなのでセッションでの受け渡しとする
            sessionStorage.setItem('testDescriptionId', this.testDescriptionId);
            sessionStorage.setItem('testDescriptionName', this.testDescriptionName);
            sessionStorage.setItem('selectedQualityDimension', this.qualityDimension);
            sessionStorage.setItem('qualityDimensionName', this.qualityDimensionName);
            sessionStorage.setItem('selectedTestrunner', JSON.stringify(this.selectedTestrunner));
            sessionStorage.setItem('report', JSON.stringify(this.report));
            sessionStorage.setItem('selectedInventories', JSON.stringify(this.selectedInventories));
            sessionStorage.setItem('measurementFormsList', JSON.stringify(this.measurementFormsList));
        },
        addSelectedInventory(target_inventory_index) {
            this.selectedInventories[target_inventory_index].value_list.push('');
            this.selectedInventories[target_inventory_index].display_flag_list.push(true);
        },
        deleteSelectedInventory(target_inventory_index, invindex) {
            this.selectedInventories[target_inventory_index].value_list.splice(invindex, 1);
            this.selectedInventories[target_inventory_index].display_flag_list.splice(invindex, 1);
        }
    }
};
</script>

<style scoped>
/*サブメニュー*/
/*メイン*/
#head {
    z-index: 1;
}

#main {
    overflow: hidden;
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
    max-height: 30rem;
    overflow: auto
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

.category_description {
    font-size: 0.8rem;
    color: var(--text-color-black);
}
.table_block .contents-area {
    height: 2rem;
}
.table_block .contents-area td {
    width: 50%;
    height: 2rem;
    font-size: 0.85rem;
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

.table_block .left {
    background: var(--primary-color);
    width: 100%;
    font-weight: bold;
    color: white;
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
    font-weight: bold;
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
.table_block thead{
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
.table_block tbody tr td input{
    width: 100%;
    border-radius: 5px;
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
.inv_tbl {
    width: 188px;
}
.inv_btn {
    width: 30px;
    display: block;
    text-align: center;
    padding: 0px 0px;
}
.btnImg {
    border: 0;
    width: 30px;
    height: 30px;
    background: url(~@/assets/plus.svg);
    background-size: 100%;
    border-radius: 50%;
}

.btnImg:disabled {
    background: none;
}
.dashed_tr {
    background-color: var(--gray-thema); /* Set row background color */
    border: rgba(0, 0, 0, 0.2);
    box-shadow: 0 0 2px rgba(0, 0, 0, 0.1); /* Add a box shadow for depth */
    border-radius: 10px;
}
.dashed_tr td select {
    width: 50%;
}
.dashed_tr td:nth-child(1) {
    border-bottom-left-radius: 10px;
    border-top-left-radius: 10px;
}
.dashed_tr td:last-child {
    border-top-right-radius: 10px;
    border-bottom-right-radius: 10px;
}
.dashed_tr span td{
    text-align: center;
    vertical-align: middle;
}
.dashed_tr td:nth-child(1) {
    width: 1rem;
}
.dashed_tr td:nth-child(2) {
    width: 40rem;
}
.dashed_tr td:nth-child(3) {
    width: 20%;
}
.dashed_tr td:nth-child(3) {
    width: 20%;
}
.dashed_tr:hover {
    background: var(--primary-color-light) !important;
}
.dashed_tr:last-child .dashed {
    border-bottom: none;
}
.table_block .dashed_tr2 {
    background-color: var(--gray-thema); /* Set row background color */
    border: rgba(0, 0, 0, 0.2);
    box-shadow: 0 0 2px rgba(0, 0, 0, 0.1); /* Add a box shadow for depth */
    border-radius: 5px;
    width: 100%;
    position: relative;
}
.table_block .dashed_tr2 td{
    width: 100%;
    text-align: center;
}
.table_block .dashed_tr2 td select {
    width: 100%;
    height: 2rem;
    background: white;
    border-radius: 5px;
}
.table_block .dashed_tr2 td input {
    width: 100%;
    background: white;
    border-radius: 5px;
}
.table_block .dashed_tr2 td:nth-child(1) {
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
    width: 5%;
}
.table_block .dashed_tr2 td:nth-child(2) {
    width: 10%;
}
.table_block .dashed_tr2 td:nth-child(3) {
    width: 10%;
}
.table_block .dashed_tr2 td:nth-child(4) {
    width: 10%;
}
.table_block .dashed_tr2 td:nth-child(5) {
    width: 10%;
}
.table_block .dashed_tr2 td:nth-child(6) {
    width: 10%;
}
.table_block .dashed_tr2 td:nth-child(7) {
    width: 10%;
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
}
.asterisk{
    color: #ff0000;
}
.error_message{
    color: #ff0000;
}
</style>

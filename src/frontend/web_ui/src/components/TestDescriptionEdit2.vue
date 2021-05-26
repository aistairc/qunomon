<template>
  <div>
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
          <router-link :to="{ name: 'Inventories' }" class="move_">{{$t("common.menuInventories")}}</router-link
          >
        </li>
        <li class="un_place">
          <router-link :to="{ name: 'TestDescriptions' }" class="move_">{{$t("common.menuTestDescriptions")}}</router-link
          >
        </li>

        <li class="place submenu_detail">
          <a class="submenu_detail" href="#">{{$t("testDescriptionEdit.edit")}}</a>
        </li>
        <li class="mlcomponent un_place">
          <router-link :to="{ name: 'MLComponents' }" class="move_">{{$t("common.menuMLComponents")}}</router-link
          >
        </li>
        <li class="btn_logout">
          <a href="signin.htm" class="btn_unselect">
            <img src="~@/assets/logout.svg" alt="logout" class="icon" />
            {{$t("common.signOut")}}
          </a>
        </li>
      </ul>
    </div>

    <!-- ニュース（中央カラム） -->
    <div id="main">
      <div id="main_body">
        <div id="search_table">
          <!-- errorMessage -->
          <span v-if="errorMessages">
            <span
              class="error_message"
              v-for="errorMessage in errorMessages"
              :key="errorMessage"
            >
              {{ errorMessage }}<br />
            </span>
          </span>

          <!-- General -->
          <div>
            <table class="table_block">
              <tr>
                <td class="th1" valign="top">
                  <span class="subtitle already"
                    ><strong>{{$t("testDescriptionEdit.general")}}</strong></span
                  >
                  <div class="category_description">
                    <span class="already">{{$t("testDescriptionEdit.generalExp")}}</span>
                  </div>
                </td>
                <td class="th2">
                  <table class="setting_table">
                    <tr>
                      <td class="center description already">
                        <span>{{$t("testDescriptionEdit.name")}}</span>
                      </td>
                      <td class="center description already">
                        <span>{{
                          testDescriptionName
                        }}</span>
                      </td>
                    </tr>
                    <tr>
                      <td class="center description already">
                        <span>{{$t("testDescriptionEdit.qualityDimension")}}</span>
                      </td>
                      <td class="center description already">
                        <span>{{
                          qualityDimensionName
                        }}</span>
                      </td>
                    </tr>
                    <tr>
                      <td class="center description already">
                        <span>{{$t("testDescriptionEdit.ait")}}</span>
                      </td>
                      <td class="center description already">
                        <span>{{ selectedTestrunner.Name }}</span>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </div>
          <hr />

          <!-- Acceptance Criteria -->
          <div>
            <table class="table_block">
              <tr>
                <td class="th1" valign="top">
                  <span class="subtitle"
                    ><strong>{{$t("testDescriptionEdit.qualityMeasurement")}}</strong></span
                  >
                  <div class="category_description">
                    <span>
                      {{$t("testDescriptionEdit.qualityMeasurementExp")}}
                    </span>
                  </div>
                  <span id="conditions" class="asterisk">{{$t("testDescriptionEdit.qualityMeasurementNote")}}</span>
                </td>
                <td class="th2">
                  <div>
                    <table class="setting_table">
                      <tr
                        class="dashed_tr"
                        v-for="(measure, i) in this.report.Measures"
                        :key="measure.Id"
                      >
                        <span
                          v-for="measurementForm in measurementFormsList[i]"
                          :key="measurementForm.Id"
                        >
                          <td class="tdQACheck dashed">
                            <input
                              type="checkbox"
                              class="list_ checkboxCheck"
                              name="listCheck"
                              v-bind:value="measurementForm.Id"
                              v-model="checkedMeasurements"
                              @change="changecheckbox"
                            />
                          </td>
                          <td class="tdQAName dashed" id="checkbox">
                            <span> {{ measure.Name }}</span>
                            <span class="asterisk">&#042;</span>
                            <span class="type">&#058; {{ measure.Type }}</span>
                            <span class="range" v-if="measure.Type == 'float' || measure.Type == 'int'">
                              <br />
                              <span class="min" v-if="measure.Min !== null">Min: {{ measure.Min }}</span>
                              <span class="min unlimited" v-else>Min: unlimited</span>
                              <span class="max" v-if="measure.Max !== null">Max: {{ measure.Max }}</span>
                              <span class="max unlimited" v-else>Max: unlimited</span>
                            </span>
                            <br />
                            <span class="description">{{
                              measure.Description
                            }}</span>
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
                                :key="relationalOperator.Id"
                                v-bind:value="relationalOperator.Id"
                              >
                                {{ relationalOperator.Expression }}
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
                        </span>
                      </tr>
                    </table>
                  </div>
                </td>
              </tr>
            </table>
          </div>
          <hr />

          <!-- AIT Parameter -->
          <div>
            <table class="table_block">
              <tr>
                <td class="th1" valign="top">
                  <span class="subtitle"><strong>{{$t("testDescriptionEdit.aitParam")}}</strong></span>
                  <div class="category_description">
                    <span>{{$t("testDescriptionEdit.aitParamExp")}}</span>
                  </div>
                </td>
                <td class="th2">
                  <table class="set_table setting_table">
                    <thead>
                      <tr>
                        <td class="ait_terms center">
                          <span>{{$t("testDescriptionEdit.name")}}</span>
                        </td>
                        <td class="ait_description center">
                          <span>{{$t("testDescriptionEdit.description")}}</span>
                        </td>
                        <td class="ait_input center">
                          <span>{{$t("testDescriptionEdit.aitInput")}}</span>
                        </td>
                      </tr>
                    </thead>
                    <tbody class="tbody">
                      <tr
                        v-for="param in this.selectedTestrunner.ParamTemplates"
                        :key="param.Id"
                      >
                        <td class="ait_terms">
                          <span>{{ param.Name }}</span>
                          <span class="asterisk">&#042;</span>
                          <span class="type">&#058; {{ param.Type }}</span>
                          <span class="range" v-if="param.Type == 'float' || param.Type == 'int'">
                            <br />
                            <span class="min" v-if="param.Min !== null">Min: {{ param.Min }}</span>
                            <span class="min unlimited" v-else>Min: unlimited</span>
                            <span class="max" v-if="param.Max !== null">Max: {{ param.Max }}</span>
                            <span class="max unlimited" v-else>Max: unlimited</span>
                          </span>
                        </td>
                        <td class="ait_description">
                          <span>{{ param.Description }}</span>
                        </td>
                        <td class="ait_input">
                          <input
                            type="text"
                            placeholder=""
                            name="myText"
                            v-model="param.DefaultVal"
                          />
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </td>
              </tr>
            </table>
          </div>
          <hr />

          <!-- Inventory Edit -->
          <div>
            <table class="table_block">
              <tr>
                <td class="th1" valign="top">
                  <span class="subtitle"><strong>{{$t("testDescriptionEdit.targetInventory")}}</strong></span>
                  <div class="category_description">
                    <span>{{$t("testDescriptionEdit.taegetInventoryExp")}}</span>
                  </div>
                </td>
                <td class="th2">
                  <table class="set_table setting_table">
                    <thead>
                      <tr>
                        <td class="inventory_terms center">
                          <span>{{$t("testDescriptionEdit.name")}}</span>
                        </td>
                        <td class="inventory_data_type center">
                            <span>{{$t("testDescriptionEdit.dataType")}}</span>
                        </td>
                        <td class="inventory_formats center">
                          <span>{{$t("testDescriptionEdit.formats")}}</span>
                        </td>
                        <td class="inventory_description center">
                          <span>{{$t("testDescriptionEdit.description")}}</span>
                        </td>
                        <td class="inventory_input center">
                          <span>{{$t("testDescriptionEdit.inventoryInput")}}</span>
                        </td>
                        <td class="inventory_add center"/>
                      </tr>
                    </thead>
                    <tbody class="tbody">
                      <tr
                        v-for="(TargetInventory, i) in this.selectedTestrunner.TargetInventories"
                        :key="TargetInventory.Id"
                      >
                        <td class="inventory_terms">
                          <span>{{ TargetInventory.Name }}</span>
                          <span class="asterisk">&#042;</span>
                        </td>
                        <td class="inventory_data_type">
                            <span>{{TargetInventory.DataType.Name}}</span>
                        </td>
                        <td class="inventory_formats">
                          <span
                            v-for="Format in TargetInventory.Formats"
                            :key="Format.Id"
                            >{{ Format.Format }}
                          </span>
                        </td>
                        <td class="inventory_description">
                          <span>{{ TargetInventory.Description }}</span>
                        </td>
                        <td class="inventory_input">
                          <span v-if="filterInventories(TargetInventory.DataType.Id, TargetInventory.Formats).length" class="single_btn">
                            <select
                              v-model="
                                selectedInventories['selectedInventory' + i]
                              "
                              class="select"
                            >
                              <option value=null disabled>
                                {{$t("common.defaultPulldown")}}
                              </option>
                              <option
                                v-for="inventory in filterInventories(
                                  TargetInventory.DataType.Id,
                                  TargetInventory.Formats
                                )"
                                :key="inventory.Id"
                                v-bind:value="inventory.Id"
                              >
                                {{ inventory.Name }}
                              </option>
                            </select>
                          </span>
                          <span class="error" v-else>
                            <img src="~@/assets/error2.svg" alt="Please Add Inventory" class="icon status">
                            {{$t("testDescriptionEdit.inventoryNote")}}
                          </span>
                        </td>
                        <td class="inventory_add">
                            <template v-if="$i18n.locale === 'en'">
                                <img src="~@/assets/plus.svg" alt="add" title="add" class="icon" @click="inventoryAdd($route.path, TargetInventory.DataType.Id, TargetInventory.Formats[0].Format)">
                            </template>
                            <template v-else>
                                <img src="~@/assets/plus.svg" alt="追加" title="追加" class="icon" @click="inventoryAdd($route.path, TargetInventory.DataType.Id, TargetInventory.Formats[0].Format)">
                            </template>
                        </td>
                      </tr>
                    </tbody>
                  </table>

                  <inventoryAdd :key="edit_key" ref="addInventoryBtn" @addInventory="addInventories"></inventoryAdd>
                </td>
              </tr>
            </table>
          </div>
          <hr />

          <!-- submit -->
          <div id="btn_set">
            <template v-if="$i18n.locale === 'en'">
                <input type="button" value="Back" class="btn_left" @click="backTestDescriptionEdit" />
                <input type="button" value="Update" class="btn_right" @click="postTestDescription" />
            </template>
            <template v-else>
                <input type="button" value="戻る" class="btn_left" @click="backTestDescriptionEdit" />
                <input type="button" value="更新" class="btn_right" @click="postTestDescription" />
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
import { urlParameterMixin } from "../mixins/urlParameterMixin";
import { tdMixin } from "../mixins/testDescriptionMixin";
import "vue-good-table/dist/vue-good-table.css";
import inventoryAdd from "./InventoryAdd";

export default {
  components: {
    inventoryAdd,
  },
  mixins: [urlParameterMixin, tdMixin],
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
                                    + '/testDescriotions/'
                                    +  this.testDescriptionId;
          this.$axios
            .put(url, this.requestData)
            .then((response) => {
              this.result = response.data;
              this.$router.push({
                  name: 'TestDescriptions'
              });
            })
            .catch((error) => {
              this.$router.push({
                name: "Information",
                params: { error },
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
      this.selectedTestrunner =  JSON.parse(sessionStorage.getItem('testRunner'));
      this.report = this.selectedTestrunner.Report;
      this.qualityDimensionName = sessionStorage.getItem('qualityDimensionName');
      if(sessionStorage.getItem('setTempTestRunnerId') == sessionStorage.getItem('changeTestrunnerId')){
          this.selectedInventories =  JSON.parse(sessionStorage.getItem('selectedInventories'));
          this.checkedMeasurements =  JSON.parse(sessionStorage.getItem('measurementFormsList'));
          this.setMeasurementFormsEdit();
        } else {
          this.selectedInventories = {};
          this.checkedMeasurements = [];
          this.setMeasurementForms();
        }
    },
    //TestDescriptionEdit1の画面へ戻る処理
    backTestDescriptionEdit() {
      if (confirm(this.$t("confirm.loseInformation"))) {
        this.setTestDescriptionData();
        this.$router.push({
          name: "TestDescriptionEdit",
          params: {
            backTestDescriptionEditData: this.backTestDescriptionEditData,
            testDescriptionId: this.testDescriptionId,
          },
        });
      }
    },
    setTestDescriptionData() {
      this.backTestDescriptionEditData.testDescriptionName = this.testDescriptionName;
      this.backTestDescriptionEditData.selectedQualityDimension = this.qualityDimension;
      this.backTestDescriptionEditData.selectedTestrunner = this.selectedTestrunner;
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
    setMeasurementFormsEdit(){
          if (JSON.parse(sessionStorage.getItem('test_description_detail')).QualityMeasurements.length == 0){
            this.count = 0;
            return;
        }

        var forms = [];
        var preId = JSON.parse(sessionStorage.getItem('test_description_detail')).QualityMeasurements[0].Id;
        var cnt = 0;
        for(var qualityMeasurement of JSON.parse(sessionStorage.getItem('test_description_detail')).QualityMeasurements){
            var measurementForm = {
                Id: qualityMeasurement.Id,
                Value: qualityMeasurement.Value,
                RelationalOperatorId: qualityMeasurement.RelationalOperatorId,
                Enable: qualityMeasurement.Enable
            };
            if(preId != qualityMeasurement.Id){
                this.measurementFormsList.push(forms);
                forms = [];
                forms.push(measurementForm);
                preId = qualityMeasurement.Id
            }
            else if(preId == qualityMeasurement.Id){
                forms.push(measurementForm);
            }
            cnt += 1;
            if(qualityMeasurement.Enable == true){
                this.checkedMeasurements.push(qualityMeasurement.Id)
            }
        }
        if(forms != []){
            this.measurementFormsList.push(forms);
        }
        this.count = cnt;
    },
    commonCheckTestDescription(){
            // criteriaが正常な値か判定
            for(let checkedMeasurement of this.checkedMeasurements){
              if(typeof(checkedMeasurement) == "number"){
                let matchedValueStr = null;
                for(let measurementForm of this.measurementFormsList){
                  if(measurementForm[0].Id == checkedMeasurement){
                    matchedValueStr = measurementForm[0].Value;
                    break;
                  }
                }

                let matchedMeasure = null;
                for(let measure of this.report.Measures) {
                  if(measure.Id == checkedMeasurement){
                    matchedMeasure = measure;
                    break;
                  }
                }

                let matchedMeasureType = matchedMeasure.Type;
                let isValidValue = true;
                if(matchedMeasureType == 'float' || matchedMeasureType == 'int'){
                  if(isNaN(matchedValueStr)){
                    // 入力値が非数値の場合
                    isValidValue = false;
                  }
                  else{
                    let matchedValue = parseFloat(matchedValueStr);
                    if(!isNaN(matchedMeasure.Min)){
                      let matchedMin = parseFloat(matchedMeasure.Min);
                      if(matchedValue < matchedMin){
                        isValidValue = false;
                      }
                    }
                    if(isValidValue && !isNaN(matchedMeasure.Max)){
                      let matchedMax = parseFloat(matchedMeasure.Max);
                      if(matchedMax < matchedValue){
                        isValidValue = false;
                      }
                    }
                  }

                  if(!isValidValue){
                    this.errorMessages.push('The criteria "' + matchedMeasure.Name + '" is invalid value.');
                  }

                }
              }
            }

            if(this.testDescriptionName == null || this.testDescriptionName === ""){
                this.errorMessages.push('Name is required.');
            }
            else if(this.testDescriptionName.length > this.maxCharacters){
                this.errorMessages.push('Name must be ' + this.maxCharacters + ' characters or less.');
            }
            if(this.qualityDimension == null || this.qualityDimension === ""){
                this.errorMessages.push('Quality Dimension is required.');
            }
            else{
                if(this.selectedTestrunner == null || this.selectedTestrunner === ""){
                        this.errorMessages.push('Test Runner is required.');
                }
                else{
                    for(var paramTemplate of this.selectedTestrunner.ParamTemplates){
                        if(paramTemplate.DefaultVal == null || paramTemplate.DefaultVal === ""){
                            this.errorMessages.push(paramTemplate.Name + ' is required.');
                        }
                        else if(paramTemplate.DefaultVal.length > this.maxCharacters){
                            this.errorMessages.push(paramTemplate.Name + ' must be ' + this.maxCharacters + ' characters or less.');
                        }
                        // parameterが正常な値か判定
                        else if(paramTemplate.Type == 'float' || paramTemplate.Type == 'int'){
                            let isValidValue = true;
                            if(isNaN(paramTemplate.DefaultVal)){
                                // 入力値が非数値の場合
                                isValidValue = false;
                            }
                            else{
                                let inputParamValue = parseFloat(paramTemplate.DefaultVal);
                                if(!isNaN(paramTemplate.Min)){
                                    let minParamValue = parseFloat(paramTemplate.Min);
                                    if(inputParamValue < minParamValue){
                                        isValidValue = false;
                                    }
                                }
                                if(isValidValue && !isNaN(paramTemplate.Max)){
                                    let maxParamValue = parseFloat(paramTemplate.Max);
                                    if(inputParamValue > maxParamValue){
                                        isValidValue = false;
                                    }
                                }
                            }
                            if(!isValidValue){
                                this.errorMessages.push('The parameter "' + paramTemplate.Name + '" is invalid value.');
                            }
                        }
                    }
                    if(this.selectedInventories == null || this.selectedInventories == {}){
                        this.errorMessages.push('Target Inventory is required.');
                    }
                    else{
                        if(this.selectedTestrunner.TargetInventories.length != Object.keys(this.selectedInventories).length){
                            this.errorMessages.push('Target Inventory is required.');
                        }
                    }
                    for(var j = 0; j < this.selectedTestrunner.Report.Measures.length; j++){
                        for(var form of this.measurementFormsList[j]){
                            if(this.checkedMeasurements.includes(form.Id)){
                                if(form.RelationalOperatorId == null || form.RelationalOperatorId === ""){
                                    if(this.errorMessages.indexOf('RelationalOperator is required.') == -1){
                                        this.errorMessages.push('RelationalOperator is required.');
                                    }
                                }
                                if(form.Value == null || form.Value === ""){
                                    if(this.errorMessages.indexOf('Measurement Value is required.') == -1){
                                        this.errorMessages.push('Measurement Value is required.');
                                    }
                                }
                                else if(form.Value.length > this.maxCharacters){
                                    if(this.errorMessages.indexOf('Measurement Value must be ' + this.maxCharacters + ' characters or less.') == -1){
                                        this.errorMessages.push('Measurement Value must be ' + this.maxCharacters + ' characters or less.');
                                    }
                                }
                            }
                        }
                    }
                }
            }
    },
    setTestDescription(){
            this.selectedTestrunner.ParamTemplates.forEach(paramTemplate => {
                delete paramTemplate["ValueType"]
            });

            this.requestData.Name = this.testDescriptionName;
            this.requestData.QualityDimensionID = this.qualityDimension;
            if(this.selectedTestrunner != null){
                for(var j = 0; j < this.selectedTestrunner.Report.Measures.length; j++){
                    for(var form of this.measurementFormsList[j]){
                        if(this.checkedMeasurements.includes(form.Id)){
                            form.Enable = true;
                        }
                        else{
                            form.Enable = false;
                        }
                        this.requestData.QualityMeasurements.push(form);
                    }
                }
            }
            var i = 0;
            for(var selectedInventory in this.selectedInventories){
                this.requestData.TargetInventories.push({Id: i+1, 
                        InventoryId: this.selectedInventories[selectedInventory],
                        TemplateInventoryId: this.selectedTestrunner.TargetInventories[i].Id});
                i = i + 1;
            }
            if(this.selectedTestrunner != null){
                this.requestData.TestRunner.Id = this.selectedTestrunner.Id;
                var params = [];
                for(var paramTemplate of this.selectedTestrunner.ParamTemplates){
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
    }
  }
};
</script>

<style scoped>
/*サブメニュー*/
.submenu_detail a {
  margin-left: 15px;
  padding: 5px 30px;
}

/*メイン*/
#main_body {
  text-align: center;
}

#search_table {
  width: 1050px;
  margin-top: 10px;
  margin-bottom: 20px;
}

.subtitle {
  text-align: left;
  margin-left: 10px;
}

/*入力系*/
input {
  width: 180px;
}

input[type="text"]:focus,
select:focus {
  background-color: #d0e2be;
}

.select {
  width: 188px;
}

.setting_table td span.type{
  font-size: 10px;
}
.setting_table td span.range span.min,
.setting_table td span.range span.max{
  margin: 0 0.5em;
  font-size: 10px;
}

.setting_table td span.range span.unlimited{
  color: #bbb;
}

.asterisk {
  color: #ff0000;
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

/*設定入力テーブル*/
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

.tdQACheck {
  width: 5%;
}

.tdQAName {
  width: 65%;
}

.tdQARelationalOperator {
  width: 15%;
}

.tdQAValue {
  width: 15%;
}

.dashed {
  border-bottom: 1px dashed;
  padding-bottom: 5px;
}

.dashed_tr:last-child .dashed {
  border-bottom: none;
}

/*AIT Parameter*/
.ait_terms {
  width: 190px;
}

.ait_description {
  width: 370px;
}

.ait_input {
  width: 190px;
}

/*Inventory追加*/
.description {
  font-size: 10px;
}

#menu {
  margin: 10px auto;
}

#btn_menu {
  text-align: right;
}

.inventory_terms {
  width: 150px;
}

.inventory_data_type {
    width: 80px;
}

.inventory_formats {
    width: 80px;
}

.inventory_description {
  width: 220px;
}

.inventory_input {
  width: 190px;
}

.inventory_add {
    width: 30px;
}

/*Acceptance Criteria*/
#conditions {
  margin-left: 20px;
}

.select_mini {
  width: 60px;
  display: inline-block;
  font-size: 12px;
  padding: 4px;
  border: solid 2px gray;
  /*枠線の種類 太さ 色*/
}

input[type="checkbox"],
input[type="radio"] {
  width: auto;
}

.acceptanceCriteriaChecked {
  color: rgba(0, 0, 102, 0.4);
  user-select: none;
  pointer-events: none;
  color: #888;
  border-width: 0px;
  box-shadow: none;
}

.text_mini {
  width: 50px;
}

/*エラーメッセージ*/
.error_message {
  text-align: left;
  word-break: break-all;
  margin: 0px;
  color: #ff0000;
}

.td_margin {
  padding-right: 20px;
}

/*アイコン*/
.status {
  width: 15px;
  height: 15px;
}

.category_description {
  padding-left: 10px;
  font-size: 12px;
  word-break: normal;
}

.already {
  color: rgba(0, 0, 102, 0.4);
}

.set_table {
  margin-right: auto;
  margin-left: auto;
  border-collapse: collapse;
}

.set_table td {
  text-align: left;
}

.set_table .center {
  text-align: center;
  background: #d0e2be;
}

thead,
.set_table {
  display: block;
}

.set_table .tbody {
  overflow: auto;
  overflow-x: hidden;
  display: block;
  height: 200px;
}

.setting_table .description {
  font-size: 10px;
}
</style>

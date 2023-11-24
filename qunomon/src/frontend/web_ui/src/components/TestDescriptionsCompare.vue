<template>
<div>

    <!-- ヘッダ -->
    <header id="head" :class="{ active: this.isActive }">
        <div id="title">
            <button @click="toggleSubmenu(isActive)" class="qq"><img :src="this.isActive  ? this.icon2 : this.icon1" alt="Image" width="30" height="auto"></button>
            <h1 class="head_title" v-if="this.mlComponent">{{ this.mlComponent.Name }}</h1>
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


    <!-- 中央カラム -->
    <div id="main" :class="{ active: this.isActive  }" v-if="test_description_1 && test_description_1.Result.Code === 'T32000' && test_description_2 && test_description_2.Result.Code === 'T32000'">
        <div id="main_body">
            <!-- 取得グラフ -->
            <div id="compare_result">
                <div class="used_data">
                    <div id="graphs">
                        <span>{{$t("testDescriptionCompare.graph")}}</span>
                        <span class="message">{{$t("testDescriptionCompare.graphExp")}}</span>
                    </div>
                    <div id="table">
                        <VueGoodTable ref="tdTable" :columns="columns" :rows="rows" max-height="300px" :fixed-header="true" align="center" style-class="vgt-table" :sort-options="{enabled: false,}" @on-row-click="onRowClick">
                            <template slot="table-row" slot-scope="props">
                                <!--ラジオボタン-->
                                <span v-if="props.column.field == 'radiobox'">
                            <input type="radio" name="graph">
                        </span>
                                <span v-else>
                            {{props.formattedRow[props.column.field]}}
                        </span>
                            </template>
                        </VueGoodTable>
                    </div>
                </div>
                <div id="com_left">
                    <div class="testdescription_area">
                        <div id="testdescription_left">
                            <label>
                                {{td_compare_1.Name}}
                            </label>
                            <span v-if="td_compare_1.Star === true">
                                    <img src="~@/assets/like_white.svg" alt="like" title="like" class="icon status" @click="onStarChange(td_compare_1)">
                                </span>
                            <span v-else>
                                    <img src="~@/assets/unlike_white.svg" alt="unlike" title="unlike" class="icon status" @click="onStarChange(td_compare_1)">
                            </span>
                            <!--お気に入り-->

                        </div>
                        <!-- 結果 -->
                        <div id="status_left">
                            <table class="status_table">
                                <tr>
                                    <td>{{$t("testDescriptionCompare.runTestResult")}}</td>
                                    <td>
                                        <span v-if="td_compare_1.TestDescriptionResult.Summary === 'NG' || td_compare_1.TestDescriptionResult.Summary === 'ERR'" style="color: red">{{td_compare_1.TestDescriptionResult.Summary}}</span>
                                        <span v-else-if="td_compare_1.TestDescriptionResult.Summary === 'OK' || td_compare_1.TestDescriptionResult.Summary === 'NEW'" style="color: green">{{td_compare_1.TestDescriptionResult.Summary}}</span>
                                    </td>
                                </tr>
                            </table>

                        </div>
                    </div>
                    <div class="result_area">
                        <div id="result_left" class="accordion">
                            <!-- グラフ -->
                            <div class="result_img" v-show="selectedType != null && selectedType === 'picture'">
                                <a class="image" target="_blank">
                                    <img width="400px" name="imgsmp" id="image1" class="result_img" />
                                </a>
                            </div>
                            <!-- 表 -->
                            <table id="result_tbl1" rules="rows" v-show="selectedType != null && selectedType === 'table'">
                                <tbody id="output_table1"></tbody>
                            </table>
                            <!-- 見解 -->
                            <div id="opinion_left">
                                <table class="status_table">
                                    <tr>
                                        <td class="con">{{$t("testDescriptionCompare.opinion")}}</td>
                                        <td class="opinion">{{this.td_compare_1.Opinion}}</td>
                                    </tr>
                                </table>
                            </div>
                        </div>
                    </div>
                    <div id="quality_measurement_left" class="detail">
                        <label for="Panel_right">{{$t("testDescriptionCompare.qualityMeasurement")}}</label>
                        <table class="ac_text">
                            <tr>
                                <td class="tbl21">{{$t("testDescriptionCompare.qualityDimension")}}</td>
                                <td class="tbl22">{{td_compare_1.QualityDimension.Name}}</td>
                            </tr>
                            <tbody v-for="qualityMeasurement of td_compare_1.QualityMeasurements" :key="qualityMeasurement.Id">
                            <template v-if="qualityMeasurement.Enable">
                                <tr>
                                    <td class="tbl21">{{$t("testDescriptionCompare.measurement")}}</td>
                                    <td class="tbl22">{{qualityMeasurement.Name}}({{qualityMeasurement.RunMeasureValue}})</td>
                                </tr>
                                <tr>
                                    <td class="tbl21">{{$t("testDescriptionCompare.description")}}</td>
                                    <td class="tbl22">{{qualityMeasurement.Description}}</td>
                                </tr>
                                <tr>
                                    <td class="tbl21">{{$t("testDescriptionCompare.condition")}}</td>
                                    <td class="tbl22" v-if="relationalOperators">
                                        {{qualityMeasurement.Name}} {{getRelationalOperator(qualityMeasurement.RelationalOperatorId)}} {{qualityMeasurement.Value}}
                                    </td>
                                </tr>
                            </template>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div id="com_right">
                    <div class="testdescription_area">
                        <div id="testdescription_right">
                            <label>
                                {{td_compare_2.Name}}
                            </label>
                            <span v-if="td_compare_2.Star === true">
                                    <img src="~@/assets/like_white.svg" alt="like" title="like" class="icon status" @click="onStarChange(td_compare_2)">
                                </span>
                            <span v-else>
                                    <img src="~@/assets/unlike_white.svg" alt="unlike" title="unlike" class="icon status" @click="onStarChange(td_compare_2)">
                            </span>
                            <!--お気に入り-->
                        </div>
                        <!-- 結果 -->
                        <div id="status_right">
                            <table class="status_table">
                                <tr>
                                    <td>{{$t("testDescriptionCompare.runTestResult")}}</td>
                                    <td>
                                        <span v-if="td_compare_2.TestDescriptionResult.Summary === 'NG' || td_compare_2.TestDescriptionResult.Summary === 'ERR'" style="color: red">{{td_compare_2.TestDescriptionResult.Summary}}</span>
                                        <span v-else-if="td_compare_2.TestDescriptionResult.Summary === 'OK' || td_compare_2.TestDescriptionResult.Summary === 'NEW'" style="color: green">{{td_compare_2.TestDescriptionResult.Summary}}</span>
                                    </td>
                                </tr>
                            </table>
                        </div>
                    </div>
                    <div class="result_area">
                        <div class="result_img" v-show="selectedType != null && selectedType === 'picture'">
                            <a class="image" target="_blank">
                                <img width="400px" name="imgsmp" id="image2" class="result_img" />
                            </a>
                        </div>
                        <!-- 表 -->
                        <table id="result_tbl2" rules="rows" v-show="selectedType != null && selectedType === 'table'">
                            <tbody id="output_table2"></tbody>
                        </table>
                        <!-- 見解 -->
                        <div id="opinion_right">
                            <table class="status_table">
                                <tr>
                                    <td class="con">{{$t("testDescriptionCompare.opinion")}}</td>
                                    <td class="opinion">{{td_compare_2.Opinion}}</td>
                                </tr>
                            </table>
                        </div>
                    </div>
                    <div id="quality_measurement_right" class="detail">
                        <label for="Panel_left">{{$t("testDescriptionCompare.qualityMeasurement")}}</label>
                        <table class="ac_text">
                            <tr>
                                <td class="tbl21">{{$t("testDescriptionCompare.qualityDimension")}}</td>
                                <td class="tbl22">{{td_compare_2.QualityDimension.Name}}</td>
                            </tr>
                            <tbody v-for="qualityMeasurement of td_compare_2.QualityMeasurements" :key="qualityMeasurement.Id">
                            <template v-if="qualityMeasurement.Enable">
                                <tr>
                                    <td class="tbl21">{{$t("testDescriptionCompare.measurement")}}</td>
                                    <td class="tbl22">{{qualityMeasurement.Name}}({{qualityMeasurement.RunMeasureValue}})</td>
                                </tr>
                                <tr>
                                    <td class="tbl21">{{$t("testDescriptionCompare.description")}}</td>
                                    <td class="tbl22">{{qualityMeasurement.Description}}</td>
                                </tr>
                                <tr>
                                    <td class="tbl21">{{$t("testDescriptionCompare.condition")}}</td>
                                    <td class="tbl22" v-if="relationalOperators">
                                        {{qualityMeasurement.Name}} {{getRelationalOperator(qualityMeasurement.RelationalOperatorId)}} {{qualityMeasurement.Value}}
                                    </td>
                                </tr>
                            </template>
                            </tbody>
                        </table>
                    </div>
                </div>
                <div id="ait" class="detail">
                    <label for="Panel">{{$t("testDescriptionCompare.aitInformation")}}</label>
                    <table>
                        <tr>
                            <td>{{$t("testDescriptionCompare.name")}}</td>
                            <td>{{td_compare_1.TestRunner.Name}}</td>
                        </tr>
                        <tr>
                            <td>{{$t("testDescriptionCompare.version")}}</td>
                            <td>{{td_compare_1.TestRunner.Version}}</td>
                        </tr>
                        <tr>
                            <td>{{$t("testDescriptionCompare.description")}}</td>
                            <td>{{td_compare_1.TestRunner.Description}}</td>
                        </tr>
                        <tr>
                            <td>{{$t("testDescriptionCompare.create_user_account")}}</td>
                            <td>{{td_compare_1.TestRunner.CreateUserAccount}}</td>
                        </tr>
                        <tr>
                            <td>{{$t("testDescriptionCompare.create_user_name")}}</td>
                            <td v-if="td_compare_1.TestRunner.CreateUserName">
                                {{td_compare_1.TestRunner.CreateUserName}}
                            </td>
                        </tr>
                        <tr>
                            <td>{{$t("testDescriptionCompare.quality")}}</td>
                            <td>
                                <img v-if="td_compare_1.TestRunner.Quality" src="~@/assets/new_window.svg" alt="new-window" title="new-window" class="new-window">
                                <a v-bind:href=cleanUrl(td_compare_1.TestRunner.Quality) target="_blank">{{cleanUrl(td_compare_1.TestRunner.Quality)}}</a>
                            </td>
                        </tr>
                        <tr v-for="param of td_compare_1.TestRunner.Params" :key="param.Id">
                            <td>{{$t("testDescriptionCompare.params")}}:</td>
                            <td>
                                <div>{{param.Name}} : {{param.Value}}</div>
                            </td>
                        </tr>
                    </table>
                </div>
            </div>


            <!-- フッタ -->
            <div id="footer">
                <address>
                    Copyright © National Institute of Advanced Industrial Science and Technology （AIST）
                </address>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import SubMenuMLComponent from './SubMenuMLComponent.vue';
import { subMenuMixin } from "../mixins/subMenuMixin";
import { tdMixin } from "../mixins/testDescriptionMixin";
import { urlParameterMixin } from "../mixins/urlParameterMixin";
import { AccountControlMixin } from '../mixins/AccountControlMixin';
import 'vue-good-table/dist/vue-good-table.css';
import { VueGoodTable } from 'vue-good-table';

export default {
    components: {
        SubMenuMLComponent,
        VueGoodTable
    },
    mixins: [subMenuMixin, tdMixin, urlParameterMixin, AccountControlMixin],
    data() {
        return {
            selectedType: '',
            testDescriptionId: '',
            test_description_1: null,
            test_description_2: null,
            td_compare_1: null,
            td_compare_2: null,
            row_graphs: null,
            outputElement1: null,
            outputElement2: null,
            languagedata: null,
            columns: [
                {
                    label: this.setTableLanguage("radiobox"),
                    field: "radiobox",
                    width: "5%",
                    tdClass: "radio_display",
                    thClass: "radio_display",
                },
                {
                    label: this.setTableLanguage("graph_name"),
                    field: "graph_name",
                    width: "55%",
                    tdClass: "t_left",
                },
                {
                    label: this.setTableLanguage("graph_description"),
                    field: "graph_description",
                    width: "30%",
                    tdClass: "t_left",
                },
                {
                    label: this.setTableLanguage("graph_format"),
                    field: "graph_format",
                    width: "10%",
                    tdClass: "t_left",
                },
            ],
            rows: [],
            install_mode: ''
        };
    },
    mounted: function () {
        this.mlComponentIdCheck();
        this.organizationIdCheck = sessionStorage.getItem("organizationId");
        this.mlComponentId = sessionStorage.getItem("mlComponentId");
        this.getMLComponent();
        const url =
            this.$backendURL +
            "/" +
            this.organizationIdCheck +
            "/mlComponents/" +
            this.mlComponentId +
            "/testDescriotions/";
        const url_1 = url + sessionStorage.getItem('testDescriptionId1');
        const url_2 = url + sessionStorage.getItem('testDescriptionId2');

        //1つ目のTD情報を取得
        this.$axios
            .get(url_1)
            .then((response) => {
                this.test_description_1 = response.data;
                this.td_compare_1 = this.test_description_1.TestDescriptionDetail;
                // install_mode
                this.install_mode = this.td_compare_1.TestRunner.InstallMode;
                this.getTDGraphs(this.td_compare_1)
            })
            .catch((error) => {
                this.$router.push({
                    name: "Information",
                    params: {
                        error
                    },
                });
            });

        //2つ目のTD情報を取得
        this.$axios
            .get(url_2)
            .then((response) => {
                this.test_description_2 = response.data;
                this.td_compare_2 = this.test_description_2.TestDescriptionDetail;
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
        //テーブルのヘッダーにタイトルを設定。
        //現在の選択言語がjaなら日本語のテーブルを、enなら英語のテーブルを設定。
        setTableLanguage(fieldName) {
            // mountよりも先に呼び出されるので、ここで言語設定を呼び出す。
            this.setLanguageData()
            this.languagedata = require('./languages/languages.json');
            if (this.$i18n.locale == 'ja') {
                switch (fieldName) {
                    case 'graph_name':
                        return this.languagedata.ja.testDescriptionCompare.graphName;
                    case 'graph_description':
                        return this.languagedata.ja.testDescriptionCompare.graphDescription;
                    case 'graph_format':
                        return this.languagedata.ja.testDescriptionCompare.graphType;
                    case 'radiobox':
                        return this.languagedata.ja.testDescriptionCompare.radiobox;
                    default:
                }
            } else if (this.$i18n.locale == 'en') {
                switch (fieldName) {
                    case 'graph_name':
                        return this.languagedata.en.testDescriptionCompare.graphName;
                    case 'graph_description':
                        return this.languagedata.en.testDescriptionCompare.graphDescription;
                    case 'graph_format':
                        return this.languagedata.en.testDescriptionCompare.graphType;
                    case 'radiobox':
                        return this.languagedata.en.testDescriptionCompare.radiobox;
                    default:
                }
            }
        },
        changeLanguage(lang) {
            sessionStorage.setItem('language', lang);
            this.changeTableTitleLanguage();
        },
        changeTableTitleLanguage() {
            for (var i = 0; i < this.columns.length; i++) {
                this.columns[i].label = this.setTableLanguage(this.columns[i].field)
            }
        },
        getTDGraphs(val) {
            this.row_graphs = val.TestDescriptionResult.Graphs;
            for (var td in this.row_graphs) {
                this.rows.push({
                    graph_name: this.row_graphs[td].Name,
                    graph_description: this.row_graphs[td].Description,
                    graph_format: this.row_graphs[td].GraphType,
                })
            }
        },
        onRowClick(params) {

            //選択されている行数を取得
            var row_num = params.row.originalIndex
            this.selectedType = '';

            //全行を取得し、ループ
            var tdTable = this.$refs.tdTable;
            for (var j = 0; j < tdTable.rows.length; j++) {
                //選択された行の場合
                if (row_num == j) {
                    if (document.getElementsByName('graph')[j].checked) {
                        document.getElementsByName('graph')[j].checked = false;
                        document.getElementsByName('graph')[j].parentNode.parentNode.parentNode.classList.remove('checked');
                        this.selectedType = '';
                    } else {
                        this.selectedType = params.row.graph_format;
                        document.getElementsByName('graph')[j].checked = true;
                        document.getElementsByName('graph')[j].parentNode.parentNode.parentNode.classList.add('checked')
                        if (this.selectedType === "picture") {
                            this.getImage1(this.td_compare_1.TestDescriptionResult.Graphs[row_num].Graph);
                            this.getImage2(this.td_compare_2.TestDescriptionResult.Graphs[row_num].Graph);
                        }else if(this.selectedType === 'table'){
                            this.getTableData1(this.td_compare_1.TestDescriptionResult.Graphs[row_num].Graph);
                            this.getTableData2(this.td_compare_2.TestDescriptionResult.Graphs[row_num].Graph);
                        }
                    }
                    //選択されていない行の場合
                } else {
                    document.getElementsByName('graph')[j].checked = false;
                    document.getElementsByName('graph')[j].parentNode.parentNode.parentNode.classList.remove('checked');
                }
            }
        },
        getImage1(path) {
            const config = {
                responseType: "arraybuffer",
            };
            this.$axios.get(path, config).then((response) => {
                let blob = new Blob([response.data], {
                    type: "image/png"
                });
                let img = document.getElementById("image1");
                let url = window.URL || window.webkitURL;
                img.src = url.createObjectURL(blob);
                img.parentNode.href = url.createObjectURL(blob);
                // url.revokeObjectURL(img.src);
            });
        },
        getImage2(path) {
            const config = {
                responseType: "arraybuffer",
            };
            this.$axios.get(path, config).then((response) => {
                let blob = new Blob([response.data], {
                    type: "image/png"
                });
                let img = document.getElementById("image2");
                let url = window.URL || window.webkitURL;
                img.src = url.createObjectURL(blob);
                img.parentNode.href = url.createObjectURL(blob);
                // url.revokeObjectURL(img.src);
            });
        },
        getTableData1(dataPath) {
            this.outputElement1 = document.getElementById('output_table1');
            const request = new XMLHttpRequest();
            request.addEventListener('load', (event) => {
                const response = event.target.responseText;
                this.convertArray1(response);
            });
            request.open('get', dataPath, true);
            request.send();
        },
        getTableData2(dataPath) {
            this.outputElement2 = document.getElementById('output_table2');
            const request = new XMLHttpRequest();
            request.addEventListener('load', (event) => {
                const response = event.target.responseText;
                this.convertArray2(response);
            });
            request.open('get', dataPath, true);
            request.send();
        },
        convertArray1(data) {
            const dataArray = [];
            const dataString = data.replace( /^(\n+)|(\n+)$/g , "" ).split('\n');
            if(data.indexOf('\t') != -1){
                for (let i = 0; i < dataString.length; i++) {
                    dataArray[i] = dataString[i].split('\t');
                }
            }
            else{
                for (let i = 0; i < dataString.length; i++) {
                    dataArray[i] = dataString[i].split(',');
                }
            }
            let insertElement = '';
            for(var tr=0; tr<dataArray.length; tr++){
                insertElement += '<tr>';
                dataArray[tr].forEach((childElement) => {
                    if(tr==0){
                        insertElement += `<th class="t_center get_table">${childElement}</th>`
                    } else {
                        if(isFinite(childElement)) {
                            insertElement += `<td class="t_right">${childElement}</td>`
                        } else {
                            insertElement += `<td class="t_left">${childElement}</td>`
                        }
                    }
                });
                insertElement += '</tr>';
            }
            this.outputElement1.innerHTML = insertElement;
        },
        convertArray2(data) {
            const dataArray = [];
            const dataString = data.replace( /^(\n+)|(\n+)$/g , "" ).split('\n');
            if(data.indexOf('\t') != -1){
                for (let i = 0; i < dataString.length; i++) {
                    dataArray[i] = dataString[i].split('\t');
                }
            }
            else{
                for (let i = 0; i < dataString.length; i++) {
                    dataArray[i] = dataString[i].split(',');
                }
            }
            let insertElement = '';
            for(var tr=0; tr<dataArray.length; tr++){
                insertElement += '<tr>';
                dataArray[tr].forEach((childElement) => {
                    if(tr==0){
                        insertElement += `<th class="t_center get_table">${childElement}</th>`
                    } else {
                        if(isFinite(childElement)) {
                            insertElement += `<td class="t_right">${childElement}</td>`
                        } else {
                            insertElement += `<td class="t_left">${childElement}</td>`
                        }
                    }
                });
                insertElement += '</tr>';
            }
            this.outputElement2.innerHTML = insertElement;
        },
        getRelationalOperator(value) {
            var expression = "";
            for (var relationalOperator of this.relationalOperators
                    .RelationalOperator) {
                if (value === relationalOperator.Id) {
                    expression = relationalOperator.Expression;
                }
            }
            return expression;
        },
        onStarChange: function (testDescription) {
            if (testDescription.Star === true) {
                this.setUnStar(testDescription.Id);
            } else {
                this.setStar(testDescription.Id);
            }
            testDescription.Star = !testDescription.Star;
        }
    }
};
</script>

<style scoped>
/*-------------------全体-------------------*/
#head {
    z-index: 1;
}

#main {
    overflow: hidden;
}

#main #main_body {
    position: relative;
    z-index: 0;
}
#compare_result {
    /*margin-left: auto;*/
    /*margin-right: auto;*/
    /*margin-top: 10px;*/
    padding-top: 2rem;
    margin: 0 auto;
    text-align: center;
    width: 90%;
    /*background-color: red;*/
}
#graphs {
    width: 100%;
    height: 2.5rem;
    background: #dc722b;
    font-size: 1rem;
    font-weight: bold;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
}
#com_left {
    width: 49%;
    float: left;
    margin-right: 0.2rem;
    border-radius: 5px;
    margin-top: 1rem;
    background-color: white;
}
#com_right {
    width: 49%;
    float: right;
    margin-left: 0.2rem;
    border-radius: 5px;
    margin-top: 1rem;
    background-color: white;
}

.icon a {
    cursor: pointer;
    margin-left: 10px;
}

.icon img {
    width: 35px;
    height: 35px;
}

/*-------------------Table-------------------*/

#table>>>.vgt-table {
    text-align: center;
    border-collapse: separate;
    border-spacing: 0 5px;
    background-color: unset;
    border: none;
    width: 100%;
}

#table>>>.vgt-table thead th {
    color: white;
    background: #dc722b;
    text-align: center;
    border: none;
    width: 1rem;
    height: 2.5rem;
    padding: unset;
    vertical-align: middle;
}
#table>>>.vgt-table tbody {
    font-size: 0.85rem;
}
#table>>>.vgt-table tbody tr th {
    background: none;
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
}
#table>>>.vgt-table td {
    padding: unset;
    height: 2rem;
    vertical-align: middle;
}

#table>>>.vgt-table tbody tr td:nth-child(0) {
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
}

#table>>>.vgt-table tbody tr td:last-child {

    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
}
#table>>>.vgt-table tbody tr {
    background-color: #fff; /* Set row background color */
    border: rgba(0, 0, 0, 0.2);
    box-shadow: 0 0 2px rgba(0, 0, 0, 0.1); /* Add a box shadow for depth */
    border-radius: 5px;
    height: 2rem;
    vertical-align: middle;
}

#table>>>.vgt-table tbody tr:hover{
    background: #a9c7aa !important;
}


#table>>>.vgt-checkbox-col {
    width: 5% !important;
    border: none;
}
#table>>>.vgt-table tr td{
    border: none;
    text-align: center;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 140px;
}

#quality_measurement_left {
    margin-bottom: 0.2rem;
}
#quality_measurement_right {
    margin-bottom: 0.2rem;
}
#table>>>.vgt-table .expanded td, th {
    white-space: normal;
    overflow: visible;
    text-overflow: unset;
    max-width: 10%;
}

#compare_result .detail {
    display: inline-block;
    margin-top: 1rem;
    width: 100%;
}
#compare_result .detail label {
    color: white;
    background: #dc722b;
    font-size: 1rem;
    font-weight: bold;
    height: 2.5rem;
    width: 100%;
    vertical-align: middle;
    justify-items: center;
    justify-content: center;
    align-items: center;
    display: flex;
}
#compare_result .detail table {
    text-align: center;
    border-collapse: separate;
    border-spacing: 0 5px;
    background-color: white;
    border: none;
    width: 100%;
}
#compare_result .detail table tr {
    border-radius: 5px;
    font-size: 0.85rem;
}
#compare_result .detail table tr td{
    height: 2rem;
}
#compare_result .detail table td:nth-child(1){
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
    background: #43645b !important;
    color: white;
}
#compare_result .detail table td:last-child{
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
    background: #f0f0f0 !important;
    color: black;
}

#testdescription_left {
    display: flex;
    color: white;
    background: #dc722b;
    width: 100%;
    height: 2.5rem;
    justify-content: center;
    align-items: center;
}
#testdescription_left label{
    font-size: 1rem;
    font-weight: bold;
}
#testdescription_right {
    display: flex;
    color: white;
    background: #dc722b;
    width: 100%;
    height: 2.5rem;
    justify-content: center;
    align-items: center;
}
#testdescription_right label{
    font-size: 1rem;
    font-weight: bold;
}
.status_table {
    text-align: center;
    border-collapse: separate;
    border-spacing: 0 5px;
    background-color: unset;
    border: none;
    width: 100%;
    font-size: 0.85rem;
}
.status_table tr {
    border-radius: 5px;
}
.status_table tr td {
    width: 50%;
    height: 2rem;
}
.status_table tr td:nth-child(1){
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
    background: #43645b !important;
    color: white;
}
.status_table tr td:last-child{
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
    background: #f0f0f0 !important;
    font-weight: bold;
}
</style>

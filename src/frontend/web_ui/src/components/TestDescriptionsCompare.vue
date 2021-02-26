<template>
<div>
    <!-- ヘッダ -->
    <header id="head">
        <div id="title">
            <h1 v-if="this.mlComponent">{{ this.mlComponent.Name }}</h1>
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
                <router-link :to="{ name: 'TestDescriptions' }" class="move_">{{$t("testDescriptionCompare.compare")}}</router-link>
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

    <!-- 中央カラム -->
    <div id="main" v-if="test_description_1 && test_description_1.Result.Code === 'T32000' && test_description_2 && test_description_2.Result.Code === 'T32000'">
        <div id="main_body">
            <div class="compare_result">
                <div class="com_left">
                    <!-- TD名、アイコン、ボタン -->
                    <div id="testdiscription_left">
                        <p>{{td_compare_1.Name}}</p>
                        <!--お気に入り-->
                        <span v-if="td_compare_1.Star === true">
                            <img src="~@/assets/like.svg" alt="like" title="like" class="icon status" @click="onStarChange(td_compare_1)">
                        </span>
                        <span v-else>
                            <img src="~@/assets/unlike.svg" alt="unlike" title="unlike" class="icon status" @click="onStarChange(td_compare_1)">
                        </span>
                    </div>
                    <!-- 結果 -->
                    <div id="status_left">
                        <span>{{$t("testDescriptionCompare.runTestResult")}}:</span>
                        <span>{{td_compare_1.TestDescriptionResult.Summary}}</span>
                    </div>
                </div>
                <div class="com_right">
                    <!-- TD名、アイコン、ボタン -->
                    <div id="testdiscription_right">
                        <p>{{td_compare_2.Name}}</p>
                        <!--お気に入り-->
                        <span v-if="td_compare_2.Star === true">
                            <img src="~@/assets/like.svg" alt="like" title="like" class="icon status" @click="onStarChange(td_compare_2)">
                        </span>
                        <span v-else>
                            <img src="~@/assets/unlike.svg" alt="unlike" title="unlike" class="icon status" @click="onStarChange(td_compare_2)">
                        </span>
                    </div>
                    <!-- 結果 -->
                    <div id="status_right">
                        <span>{{$t("testDescriptionCompare.runTestResult")}}:</span>
                        <span>{{td_compare_2.TestDescriptionResult.Summary}}</span>
                    </div>
                </div>
            </div>

            <!-- 取得グラフ -->
            <div id="table">
                <div id="graphs">
                    <span>{{$t("testDescriptionCompare.graph")}}</span>
                    <span class="message">{{$t("testDescriptionCompare.graphExp")}}</span>
                </div>
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
            <div class="compare_result">
                <div class="com_left">
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
                            <div class="con">{{$t("testDescriptionCompare.opinion")}}</div>
                            <div class="z-depth__ opinion">{{this.td_compare_1.Opinion}}</div>
                        </div>
                    </div>
                </div>

                <div class="com_right">
                    <div id="result_right" class="accordion">
                        <!-- グラフ -->
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
                            <div class="con">{{$t("testDescriptionCompare.opinion")}}</div>
                            <div class="opinion z-depth__">{{td_compare_2.Opinion}}</div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="compare_result" id="con_opinion">
                <div class="com_left">
                    <div id="result_left" class="accordion">
                        <div id="quality_measurement_left" class="detail z-depth__">
                            <label for="Panel_right">{{$t("testDescriptionCompare.qualityMeasurement")}}</label>
                            <table class="ac_text">
                                <tr>
                                    <td class="tbl21">{{$t("testDescriptionCompare.qualityDimension")}}:</td>
                                    <td class="tbl22">{{td_compare_1.QualityDimension.Name}}</td>
                                </tr>
                                <tr>
                                    <td></td>
                                    <td></td>
                                </tr>
                                <tbody v-for="qualityMeasurement of td_compare_1.QualityMeasurements" :key="qualityMeasurement.Id">
                                    <template v-if="qualityMeasurement.Enable">
                                        <tr>
                                            <td class="tbl21">{{$t("testDescriptionCompare.measurement")}}:</td>
                                            <td class="tbl22">{{qualityMeasurement.Name}}</td>
                                        </tr>
                                        <tr>
                                            <td class="tbl21">{{$t("testDescriptionCompare.description")}}:</td>
                                            <td class="tbl22">{{qualityMeasurement.Description}}</td>
                                        </tr>
                                        <tr>
                                            <td class="tbl21">{{$t("testDescriptionCompare.configuration")}}:</td>
                                            <td class="tbl22" v-if="relationalOperators">
                                                {{qualityMeasurement.Name}} {{getRelationalOperator(qualityMeasurement.RelationalOperatorId)}} {{qualityMeasurement.Value}}
                                            </td>
                                        </tr>
                                    </template>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                <div class="com_right">
                    <div id="result_right" class="accordion">
                        <div id="quality_measurement_right" class="detail z-depth__">
                            <label for="Panel_left">{{$t("testDescriptionCompare.qualityMeasurement")}}</label>
                            <table class="ac_text">
                                <tr>
                                    <td class="tbl21">{{$t("testDescriptionCompare.qualityDimension")}}:</td>
                                    <td class="tbl22">{{td_compare_2.QualityDimension.Name}}</td>
                                </tr>
                                <tr>
                                    <td></td>
                                    <td></td>
                                </tr>
                                <tbody v-for="qualityMeasurement of td_compare_2.QualityMeasurements" :key="qualityMeasurement.Id">
                                    <template v-if="qualityMeasurement.Enable">
                                        <tr>
                                            <td class="tbl21">{{$t("testDescriptionCompare.measurement")}}:</td>
                                            <td class="tbl22">{{qualityMeasurement.Name}}</td>
                                        </tr>
                                        <tr>
                                            <td class="tbl21">{{$t("testDescriptionCompare.description")}}:</td>
                                            <td class="tbl22">{{qualityMeasurement.Description}}</td>
                                        </tr>
                                        <tr>
                                            <td class="tbl21">{{$t("testDescriptionCompare.configuration")}}:</td>
                                            <td class="tbl22" v-if="relationalOperators">
                                                {{qualityMeasurement.Name}} {{getRelationalOperator(qualityMeasurement.RelationalOperatorId)}} {{qualityMeasurement.Value}}
                                            </td>
                                        </tr>
                                    </template>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            <div id="ait" class="detail">
                <label for="Panel">{{$t("testDescriptionCompare.aitInformation")}}</label>
                <table>
                    <tr>
                        <td class="tbl21">{{$t("testDescriptionCompare.name")}}:</td>
                        <td class="tbl22">{{td_compare_1.TestRunner.Name}}</td>
                    </tr>
                    <tr>
                        <td class="tbl21">{{$t("testDescriptionCompare.version")}}:</td>
                        <td class="tbl22">{{td_compare_1.TestRunner.Version}}</td>
                    </tr>
                    <tr>
                        <td class="tbl21">{{$t("testDescriptionCompare.description")}}:</td>
                        <td class="tbl22">{{td_compare_1.TestRunner.Description}}</td>
                    </tr>
                    <tr>
                        <td class="tbl21">{{$t("testDescriptionCompare.author")}}:</td>
                        <td class="tbl22">{{td_compare_1.TestRunner.Author}}</td>
                    </tr>
                    <tr>
                        <td class="tbl21">{{$t("testDescriptionCompare.email")}}:</td>
                        <td class="tbl22" v-if="td_compare_1.TestRunner.Email">
                            {{td_compare_1.TestRunner.Email}}
                        </td>
                    </tr>
                    <tr>
                        <td class="tbl21">{{$t("testDescriptionCompare.quality")}}:</td>
                        <td class="tbl22">
                            <img src="~@/assets/new_window.svg" alt="new-window" title="new-window" class="new-window">
                            <a v-bind:href=td_compare_1.TestRunner.Quality target="_blank">{{td_compare_1.TestRunner.Quality}}</a>
                        </td>
                    </tr>
                    <tr v-for="param of td_compare_1.TestRunner.Params" :key="param.Id">
                        <td class="tbl21">{{$t("testDescriptionCompare.params")}}:</td>
                        <td class="tbl22">
                            <div>{{param.Name}} : {{param.Value}}</div>
                        </td>
                    </tr>
                </table>
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
import {
    tdMixin
} from "../mixins/testDescriptionMixin";
import {
    urlParameterMixin
} from "../mixins/urlParameterMixin";
import 'vue-good-table/dist/vue-good-table.css';
import {
    VueGoodTable
} from 'vue-good-table';
export default {
    components: {
        VueGoodTable,
    },
    mixins: [tdMixin, urlParameterMixin],
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
            columns: [{
                    label: this.setTableLanguage("graph_name"),
                    field: "graph_name",
                    width: "59%",
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
                    width: "11%",
                    tdClass: "t_left",
                },
                {
                    label: this.setTableLanguage("radiobox"),
                    field: "radiobox",
                    width: "0px",
                    tdClass: "radio_display",
                    thClass: "radio_display",
                }
            ],
            rows: [],
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
        // const url_1 = url + this.$route.params.testDescriptionId1;
        // const url_2 = url + this.$route.params.testDescriptionId2;
        const url_1 = url + sessionStorage.getItem('testDescriptionId1');
        const url_2 = url + sessionStorage.getItem('testDescriptionId2');

        //1つ目のTD情報を取得
        this.$axios
            .get(url_1)
            .then((response) => {
                this.test_description_1 = response.data;
                this.td_compare_1 = this.test_description_1.TestDescriptionDetail;
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

/*-------------------テーブル-------------------*/
#table>>>table tr:hover {
    background-color: rgb(233, 233, 233) !important;
}

#table>>>table.vgt-table td {
    padding: 4px 2px;
    vertical-align: top;
    border-bottom: 1px solid gray;
    color: #000066;
}

#table>>>.vgt-fixed-header {
    position: absolute !important;
    z-index: 10 !important;
    width: 100% !important;
    overflow-x: auto !important;
}

#table>>>.vgt-table thead th {
    color: white !important;
    background: #9bbb59 !important;
    padding: .11em .2em !important;
    font-weight: normal;
}

#table>>>table.vgt-table {
    font-size: 16px !important;
    max-width: 1000px !important;
}

#table>>>.t_left {
    text-align: left !important;
    vertical-align: middle !important;
}

#table>>>.t_right {
    text-align: right !important;
    vertical-align: middle !important;
    padding-right: 5px;
}

#table>>>.t_center {
    text-align: center !important;
    vertical-align: middle !important;
}

#table>>>.vgt-table th.sortable:after,
#table>>>.vgt-table th.sortable::before {
    right: 5px !important;
}

/*----------------
グラフ表
----------------*/
#table {
    padding-top: 20px;
    width: 700px;
    margin-left: auto;
    margin-right: auto;
}

#table_total tr:hover {
    background-color: rgb(233, 233, 233);
}

/*----------------
csvグラフ
----------------*/
#result_tbl1, #result_tbl2{
  table-layout:fixed;
  word-break : break-all;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 20px;
  margin-top: 20px;
  max-width: 90%;
}

#result_tbl1>>>.get_table ,
#result_tbl2>>>.get_table {
    background-color: #666666 ;
    font-weight: normal ;
    padding: .11em .2em ;
    font-weight: normal ;
}

.t_left{
	text-align:left;
	padding: 0px 5px;
}

.t_right{
	padding: 0px 5px;
	text-align:right;
}
/*----------------
サブメニュー
----------------*/
.submenu_detail a {
    margin-left: 15px;
    padding: 5px 30px;
}

/*----------------
TestDescriptionName
----------------*/
#testdiscription_right,
#testdiscription_left {
    padding: 10px 0 0px;
    display: flex;
    justify-content: start;
    align-items: center;
    font-size: 21px;
    font-weight: bold;
}

.icon a {
    cursor: pointer;
    margin-left: 10px;
}

.icon img {
    width: 35px;
    height: 35px;
}

/*----------------
status
----------------*/
#status_right,
#status_left {
    font-size: 18px;
    margin: 0;
    border-bottom: #000066 2px dashed;
}

/*----------------
全体配置
----------------*/
.compare_result {
    display: flex;
}

.com_left,
.com_right {
    width: 46%;
    padding: 0px 2%;
}

#opinion {
    position: fixed;
    overflow-y: auto;
    overflow-x: hidden;
    height: calc(100% - 85px);
    padding-bottom: 10px;
    border-left: 1px solid gray;
}

label {
    background-color: #9bbb59;
    color: #ffffff;
    font-size: 18px;
    padding: 2px 8px;
    display: block;
    margin: 0;
}

/*----------------
グラフ
----------------*/
#graphs {
    text-align: left;
    font-size: 20px;
}

.result_img {
    text-align: center;
    padding: 10px 0px;
}

.image {
    text-decoration: none;
    cursor: zoom-in;
}

.message {
    font-size: 13px;
    padding-left: 15px;
}

.radio_display input {
    display: none;
}

/*----------------
quality_measurement
----------------*/
#quality_measurement_left,
#quality_measurement_right {
    margin: 10px 0px;
}

/*----------------
見解
----------------*/
#com_opinion {
    height: auto;
}

#opinion_left,
#opinion_right {
    margin-bottom: 30px;
}

.opinion {
    width: 80%;
    min-height: 100px;
    height: auto;
    font-size: 15px;
    padding: 4px;
    margin-left: auto;
    margin-right: auto;
}

.con {
    padding-left: 5px;
}

/*----------------
AIT
----------------*/
.detail td {
    background-color: #f0f0f0;
    vertical-align: top;
}

.detail table {
    margin: 10px;
}

#ait {
    width: 96%;
    margin-top: 10px;
    margin-left: auto;
    margin-right: auto;
}

.detail {
    margin: 10px auto;
}

/*----------------
新しいタブを開く
----------------*/
.new-window {
    width: 20px;
    height: 20px;
    vertical-align: middle;
}
</style>

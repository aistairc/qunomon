<template>
<div>
    <!-- ヘッダ -->
    <header id="head" :class="{ active: this.isActive }">
        <div id="title">
            <button @click="toggleSubmenu(isActive)" class="qq"><img :src="this.isActive ? this.icon2 : this.icon1" alt="Image" width="30" height="auto"></button>
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
        <template v-slot:TestDescriptionDetail>
            <ul id="submenu_body">
                <li class="un_place submenu_detail">
                    <b-list-group-item :to="{ name: 'TestDescriptionsDetail', params: {testDescriptionId: testDescriptionId}}" variant="info" active-class="active">
                        <span v-if="!isActive">{{$t("testDescriptionDetail.detail")}}</span>
                        <img v-else :src="DetailIcon" alt="Image" class="imageBtn" width="30" height="auto">
                    </b-list-group-item>
                </li>
            </ul>
        </template>
    </SubMenuMLComponent>


    <!-- 中央カラム -->
    <div id="main" :class="{ active: this.isActive }" v-if="test_descriptions && test_descriptions.Result.Code === 'T32000'">
        <div id="main_body">
            <!-- TD名、アイコン、ボタン -->
            <div class="data_area">
                <div id="testdescriptions">
                    <div id="td_name"><h2>{{tdDtl.Name}}</h2></div>
                    <div id="status">
                        <span>{{$t("testDescriptionDownload.runTestResult")}}:
                            <span v-if="tdDtl.TestDescriptionResult.Summary === 'NG' || tdDtl.TestDescriptionResult.Summary === 'ERR'" style="color: red">{{tdDtl.TestDescriptionResult.Summary}}</span>
                            <span v-else-if="tdDtl.TestDescriptionResult.Summary === 'OK' || tdDtl.TestDescriptionResult.Summary === 'NEW'" style="color: green">{{tdDtl.TestDescriptionResult.Summary}}</span>
                        </span>

                    </div>
                </div>
                <!-- 結果 -->
                <div id="result">
                    <label>{{$t("testDescriptionDownload.title")}}</label>
                    <div id="table_frame">
                        <div id="table">
                            <!-- 取得グラフ -->
                            <VueGoodTable ref="tdTable"
                                          :columns="columns"
                                          :rows="rows"
                                          max-height="300px"
                                          :fixed-header="true"
                                          align="center"
                                          style-class="vgt-table"
                                          :sort-options="{enabled: false,}"
                                          @on-row-click="onRowClick"
                                          :pagination-options="pagenationSettings"
                                          @on-per-page-change="onPerPageChange"
                                          :group-options="groupSettings"
                                          :select-options="selectSettings">
                                <template slot="table-row" slot-scope="props">
                                    <!--ダウンロードアイコン-->
                                    <span v-if="props.column.field == 'download'">
                                        <img src="~@/assets/download.svg" alt="download" title="download" class="icon" @click="fileDownload(props.row.file_log)">
                                        <input type="radio" name="graph">
                                    </span>
                                    <span v-else>
                                        {{props.formattedRow[props.column.field]}}
                                    </span>
                                </template>
                            </VueGoodTable>
                        </div>
                    </div>
                    <!-- グラフ -->
                    <div class="result_img" v-show="selectedType != null && selectedType === 'picture'">
                        <a class="image" target="_blank">
                            <img name="imgsmp" id="image" class="result_img" />
                        </a>
                    </div>
                    <!-- 表 -->
                    <table id="result_tbl" rules="rows" v-show="selectedType != null && selectedType === 'table'">
                        <tbody id="output_table"></tbody>
                    </table>
                </div>
                <!-- フッタ -->
                <div id="footer">
                    <address>Copyright © National Institute of Advanced Industrial Science and Technology （AIST）
                    </address>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import SubMenuMLComponent from './SubMenuMLComponent.vue';
import { subMenuMixin } from "../mixins/subMenuMixin";
import { tdMixin } from '../mixins/testDescriptionMixin';
import { urlParameterMixin } from '../mixins/urlParameterMixin';
import { AccountControlMixin } from '../mixins/AccountControlMixin';
import 'vue-good-table/dist/vue-good-table.css';
import { VueGoodTable } from 'vue-good-table';
import DetailIcon from '@/assets/google_icon_detail.svg';

export default {
    components: {
        SubMenuMLComponent,
        VueGoodTable,
    },
    mixins: [subMenuMixin, tdMixin, urlParameterMixin, AccountControlMixin],
    data() {
        return {
            DetailIcon: DetailIcon,
            selectedType: '',
            testDescriptionId: '',
            test_descriptions: null,
            result: null,
            tdRsc: null,
            tdDtl: null,
            languagedata: null,
            columns: [
                {
                    label: this.setTableLanguage("file_name"),
                    field: "file_name",
                    thClass: 't_left',
                    width: "55%",
                },
                {
                    label: this.setTableLanguage("graph_description"),
                    field: "graph_description",
                    width: "25%",
                    tdClass: "t_left",
                },
                {
                    label: this.setTableLanguage("graph_format"),
                    field: "graph_format",
                    width: "15%",
                    tdClass: "t_left",
                },
                {
                    label: this.setTableLanguage("download"),
                    field: "download",
                    width: "5%",
                    tdClass: "t_center",
                },
                {
                    label: this.setTableLanguage("file_log"),
                    field: "file_log",
                    hidden: true,
                }
            ],
            rows: [],
            pagenationSettings:{
                enabled: true,
                mode: 'records',
                perPage: 5,
                perPageDropdown: [10, 50, 100],
                dropdownAllowAll: false,
                setCurrentPage: 1,
                nextLabel: this.setTableLanguage("pageNext"),
                prevLabel: this.setTableLanguage("pagePrev"),
                rowsPerPageLabel: this.setTableLanguage("rowsPerPageLabel"),
                ofLabel: 'of',
                allLabel: 'All',
            },
            groupSettings:{
                enabled: true,
                headerPosition: 'top',
                collapsable: true
            },
            selectSettings:{
                enabled: false,
                disableSelectInfo: true,
                selectAllByGroup: false
            },
            isExpanded: false,
        }
    },
    mounted: function () {
        this.mlComponentIdCheck();
        this.organizationIdCheck = sessionStorage.getItem('organizationId');
        this.mlComponentId = sessionStorage.getItem('mlComponentId');
        this.testDescriptionId = sessionStorage.getItem('testDescriptionId');
        this.getMLComponent();
        const url = this.$backendURL + '/' +
            this.organizationIdCheck + '/mlComponents/' +
            this.mlComponentId + '/testDescriptions/' +
            this.testDescriptionId;
        this.$axios.get(url)
            .then((response) => {
                this.test_descriptions = response.data;
                this.tdDtl = this.test_descriptions.TestDescriptionDetail;
                this.tdRsc = this.test_descriptions.TestDescriptionDetail.TestDescriptionResult;
                this.getTDResources(this.tdRsc);
            })
            .catch((error) => {
                this.$router.push({
                    name: 'Information',
                    params: {
                        error
                    }
                })
            });
    },
    updated(){
        if(this.$refs.tdTable != undefined && this.isExpanded == false){
            this.$refs.tdTable.expandAll();
            this.isExpanded = true;
        }
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
                        return this.languagedata.ja.testDescriptionDownload.graphName;
                    case 'file_name':
                        return this.languagedata.ja.testDescriptionDownload.fileName;
                    case 'graph_description':
                        return this.languagedata.ja.testDescriptionDownload.graphDescription;
                    case 'graph_format':
                        return this.languagedata.ja.testDescriptionDownload.graphType;
                    case 'download':
                        return this.languagedata.ja.testDescriptionDownload.radiobox;
                    case 'file_log':
                        return this.languagedata.ja.testDescriptionDownload.icon;
                    default:
                }
            } else if (this.$i18n.locale == 'en') {
                switch (fieldName) {
                    case 'graph_name':
                        return this.languagedata.en.testDescriptionDownload.graphName;
                    case 'file_name':
                        return this.languagedata.en.testDescriptionDownload.fileName;
                    case 'graph_description':
                        return this.languagedata.en.testDescriptionDownload.graphDescription;
                    case 'graph_format':
                        return this.languagedata.en.testDescriptionDownload.graphType;
                    case 'download':
                        return this.languagedata.en.testDescriptionDownload.radiobox;
                    case 'file_log':
                        return this.languagedata.en.testDescriptionDownload.icon;
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
        getTDResources(val) {
            var index = 1;
            var gourp_td = {}
            var row_graphs = val.Graphs;
            for (var td in row_graphs) {
                var name = "[Graphs]"+row_graphs[td].Name
                if (gourp_td[name] == null){
                    gourp_td[name] = []
                }
                gourp_td[name].push({
                    index: index,
                    graph_name: name,
                    file_name: row_graphs[td].FileName,
                    graph_description: row_graphs[td].Description,
                    graph_format: row_graphs[td].GraphType,
                    file_log: row_graphs[td].Graph,
                })
                index++;
            }
            for (var key in gourp_td){
                this.rows.push({
                    mode: "span",
                    label: key,
                    html: false,
                    children: gourp_td[key]
                })
            }

            gourp_td = {}
            var row_logs = val.Downloads;
            for (var td2 in row_logs) {
                name = "[Downloads]"+row_logs[td2].Name
                if (gourp_td[name] == null){
                    gourp_td[name] = []
                }
                gourp_td[name].push({
                    index: index,
                    graph_name: name,
                    file_name: row_logs[td2].FileName,
                    graph_description: row_logs[td2].Description,
                    graph_format: '-',
                    file_log: row_logs[td2].DownloadURL,
                })
                index++;
            }
            for (key in gourp_td){
                this.rows.push({
                    mode: "span",
                    label: key,
                    html: false,
                    children: gourp_td[key]
                })
            }
        },
        onRowClick(params) {
            //選択されている行数を取得
            var row_num = params.row.index - 1;
            this.selectedType = '';

            // クリック対象の行を取得
            var rowElement = undefined
            var composedPath = params.event.composedPath()
            for(var i in composedPath){
                if(composedPath[i].className=='clickable' || composedPath[i].className=='clickable checked'){
                    rowElement = composedPath[i];
                    break;
                }
            }
            var target_graph_element = rowElement.childNodes[7].childNodes[0].childNodes[1]

            //全行を取得し、ループ
            var tdTable = this.$refs.tdTable;
            var pageRemain = tdTable.currentPerPage

            for (var j = 0; j < pageRemain; j++) {
                var graph_element = document.getElementsByName('graph')[j]
                if (graph_element == undefined){
                    break;
                }
                //選択された行の場合
                if (graph_element == target_graph_element) {
                    if(graph_element.checked){
                        graph_element.checked = false;
                        graph_element.parentNode.parentNode.parentNode.classList.remove('checked');
                        this.selectedType = '';
                    } else {
                        this.selectedType = params.row.graph_format;
                        graph_element.checked = true;
                        graph_element.parentNode.parentNode.parentNode.classList.add('checked')
                        if (this.selectedType === "picture") {
                            this.getImage(this.tdRsc.Graphs[row_num].Graph);
                        }else if(this.selectedType === 'table'){
                            this.getTableData(this.tdRsc.Graphs[row_num].Graph);
                        }
                    }
                    //選択されていない行の場合
                } else {
                    graph_element.checked = false;
                    graph_element.parentNode.parentNode.parentNode.classList.remove('checked');
                }
            }
        },
        getImage(path) {
            const config = {
                responseType: "arraybuffer",
            };
            this.$axios.get(path, config).then((response) => {
                let blob = new Blob([response.data], {
                    type: "image/png"
                });
                let img = document.getElementById("image");
                let url = window.URL || window.webkitURL;
                img.src = url.createObjectURL(blob);
                img.parentNode.href = url.createObjectURL(blob);
                // url.revokeObjectURL(img.src);
            });
        },
        getTableData(dataPath) {
            this.outputElement = document.getElementById('output_table');
            const request = new XMLHttpRequest();
            request.addEventListener('load', (event) => {
                const response = event.target.responseText;
                this.convertArray(response);
            });
            request.open('get', dataPath, true);
            request.send();
        },
        convertArray(data) {
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
            this.outputElement.innerHTML = insertElement;
        },
        fileDownload(value) {
            if (value != null) {
                const link = document.createElement('a');
                link.href = value;
                link.click();
            }
        },
        updateStatus(data) {
            this.test_descriptions.Test.Status = data.Job.Status;
            // その他、更新内容が増えればここに記載する。
        },
        onPerPageChange(){
            var tdTable = this.$refs.tdTable;
            tdTable.currentPage = 1;
            this.selectedType = '';
        },
    },
    computed: {},
    filters: {}
}
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
.data_area {
    padding-top: 2rem;
    margin: 0 auto;
    text-align: center;
    width: 90%;
}


/*-------------------テーブル-------------------*/
#table {
    height: 90%;
    z-index: 10;
    background-color: #f0f0f0;
}
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
#table>>>.vgt-table tbody tr {
    background-color: #fff; /* Set row background color */
    border: rgba(0, 0, 0, 0.2);
    box-shadow: 0 0 2px rgba(0, 0, 0, 0.1); /* Add a box shadow for depth */
    border-radius: 5px;
    vertical-align: middle;
}
#table>>>.vgt-table tbody tr td:nth-child(1) {
    border-bottom-left-radius: 5px;
    border-top-left-radius: 5px;
}
#table>>>.vgt-table tbody tr td:last-child {
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
}

#table>>>.vgt-table tbody tr:hover{
    background: #a9c7aa !important;
}
#table>>>.vgt-table tr td{
    border: none;
    text-align: center;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 140px;
}
#table>>>.vgt-table .expanded td, th {
    white-space: normal;
    overflow: visible;
    text-overflow: unset;
    max-width: 10%;
}
#table>>>.vgt-table td {
    padding: unset;
    height: 2rem;
    vertical-align: middle;
}

#table>>>.t_center {
    text-align: center !important;
    vertical-align: middle !important;
}
#table input {
    display: none;
}

/* table footer*/
.vgt-wrap>>>.vgt-wrap__footer {
    padding: 0.5rem;
    border: none;
    background: unset;
}

#table>>>.vgt-inner-wrap {
    border-radius: unset;
    box-shadow: unset;
    background: none;
}
/*----------------
csvグラフ
----------------*/
#result_tbl{
  table-layout:fixed;
  word-break : break-all;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 20px;
  margin-top: 20px;
  max-width: 90%;
}

#result_tbl>>>.get_table {
    background-color: #666666 !important;
    font-weight: normal !important;
    padding: .11em .2em !important;
    font-weight: normal !important;
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
    padding: 5px 20px;
}
/*----------------
TestDescriptionName
----------------*/
#testdescriptions {
    background: #43645b;
    color: white;
}
#testdescriptions #status{
    font-size: 0.85rem;
}
#result label {
    background-color: #dc722b;
    color: white;
    font-size: 1rem;
    font-weight: bold;
    height: 2.5rem;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

/*アイコン*/

#icon_btn {
    text-align: right;
    display: flex;
}



/*----------------
status
----------------*/
#status {
    font-size: 20px;
    margin: 10px 0;
    font-weight: bold;
    border-bottom: #000066 2px dashed;
}

/*----------------
一覧表
----------------*/
#table>>>.vgt-table tr.checked {
    background-color: #d1ff8c;
}

/*----------------
グラフ
----------------*/
#image {
    max-height: 200px;
}

.image {
    display: inline;
    text-align: center;
    cursor: zoom-in;
}

.result_img {
    text-align: center;
    padding: 10px 0px;
}

/*----------------
フッター
----------------*/
#footer {
    padding-top: 30px;
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

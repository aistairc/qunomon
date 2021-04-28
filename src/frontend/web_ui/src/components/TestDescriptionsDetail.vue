<template>
<div v-if="test_description_details && test_description_details.Result.Code === 'T32000'">
    <!-- ヘッダ -->
    <header id="head">
        <div id="title">
            <h1 class="title" v-if="this.mlComponent">{{ this.mlComponent.Name }}</h1>
        </div>
    </header>

    <!-- サブメニュー（左カラム） -->
    <div id="submenu">
        <div id="logo">
            <img src="~@/assets/logo.svg" alt="logo" class="logo">
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
        <hr>
        <ul id="submenu_body">
            <li class="un_place">
                <router-link :to="{ name: 'Inventories'}" class="move_">{{$t("common.menuInventories")}}</router-link>
            </li>
            <li class="un_place">
                <router-link :to="{ name: 'TestDescriptions'}" class="move_">{{$t("common.menuTestDescriptions")}}</router-link>
            </li>
            <li class="place submenu_detail">
                <a class="submenu_detail" href="#">{{$t("testDescriptionDetail.detail")}}</a>
            </li>
            <!-- テストディスクリプションのテスト結果がOKかNGの場合のみ表示↓ -->
            <template v-if="tdDtl.TestDescriptionResult">
                <li class="un_place submenu_detail window" v-if="tdDtl.TestDescriptionResult.Summary ==='OK' || tdDtl.TestDescriptionResult.Summary === 'NG'">
                    <a class="move_" @click="download">{{$t("testDescriptionDetail.download")}}</a>
                </li>
            </template>
            <li class="mlcomponent un_place">
                <router-link :to="{ name: 'MLComponents'}" class="move_">{{$t("common.menuMLComponents")}}</router-link>
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
    <div id="main">
        <div id="main_body">
            <div id="accordion">
                <div id="acd_left">
                    <!-- TD名、アイコン、ボタン -->
                    <div id="testdiscriptions">
                        <div id="td_name">
                            <h2>{{tdDtl.Name}}</h2>
                            <!--お気に入り-->
                            <span v-if="tdDtl.Star === true">
                                <img src="~@/assets/like.svg" alt="like" title="like" class="icon status" @click="onStarChange(tdDtl)">
                            </span>
                            <span v-else>
                                <img src="~@/assets/unlike.svg" alt="unlike" title="unlike" class="icon status" @click="onStarChange(tdDtl)">
                            </span>
                        </div>
                        <div id="icon_btn">
                            <template v-if="$i18n.locale === 'en'">
                                <span id="btn_test" v-if="tdDtl.TestDescriptionResult == null || tdDtl.TestDescriptionResult.Summary ==='ERR' || tdDtl.TestDescriptionResult.Summary ==='NA'">
                                    <input type="submit" value="Run test" class="btn_single" v-bind:class="{ 'un_btn' : isPush }" @click="runTest">
                                </span>
                                <router-link :to="{ name: 'TestDescriptionEdit'}" class="icon" v-if="tdDtl.TestDescriptionResult == null || tdDtl.TestDescriptionResult.Summary ==='ERR' || tdDtl.TestDescriptionResult.Summary ==='NA'">
                                    <img src="~@/assets/edit.svg" alt="edit" title="edit" class="icon" @click="postHistory_testDescriptionEdit($route.name,tdDtl.Id)">
                                </router-link>
                                <router-link :to="{ name: 'TestDescriptionCopy'}" class="icon">
                                    <img src="~@/assets/copy.svg" alt="copy" title="copy" class="icon" @click='postHistory_testDescriptionCopy($route.name,tdDtl.Id)'>
                                </router-link>
                                <a href="#" class="icon">
                                    <img src="~@/assets/delete.svg" alt="delete" title="delete" class="icon" @click="testDescriptionDelete">
                                </a>
                            </template>
                            <template v-else>
                                <span id="btn_test" v-if="tdDtl.TestDescriptionResult == null || tdDtl.TestDescriptionResult.Summary ==='ERR' || tdDtl.TestDescriptionResult.Summary === 'NA'">
                                    <input type="submit" value="テスト実行" class="btn_single" v-bind:class="{ 'un_btn' : isPush }" @click="runTest">
                                </span>
                                <router-link :to="{ name: 'TestDescriptionEdit'}" class="icon" v-if="tdDtl.TestDescriptionResult == null || tdDtl.TestDescriptionResult.Summary ==='ERR' || tdDtl.TestDescriptionResult.Summary === 'NA'">
                                    <img src="~@/assets/edit.svg" alt="編集" title="編集" class="icon" @click="postHistory_testDescriptionEdit($route.name,tdDtl.Id)">
                                </router-link>
                                <router-link :to="{ name: 'TestDescriptionCopy'}" class="icon">
                                    <img src="~@/assets/copy.svg" alt="複製" title="複製" class="icon" @click='postHistory_testDescriptionCopy($route.name,tdDtl.Id)'>
                                </router-link>
                                <a href="#" class="icon">
                                    <img src="~@/assets/delete.svg" alt="削除" title="削除" class="icon" @click="testDescriptionDelete">
                                </a>
                            </template>
                        </div>
                    </div>
                    <!-- 結果 -->
                    <div id="result" class="accordion">
                        <label>{{$t("testDescriptionDetail.testResult")}}</label>
                        <div id="status">
                            <span>{{$t("testDescriptionDetail.runThisTest")}} : </span>
                            <template v-if="tdDtl.TestDescriptionResult">
                                <span>{{tdDtl.TestDescriptionResult.Summary}}</span>
                                <a id="log_download" v-bind:href=tdDtl.TestDescriptionResult.LogFile download="">{{$t("testDescriptionDetail.logDownload")}}</a>
                            </template>
                            <template v-else>
                                <span>NA</span>
                            </template>
                        </div>
                        <!-- エラー情報 -->
                        <template v-if="tdDtl.TestDescriptionResult">
                            <template v-if="tdDtl.TestDescriptionResult.Summary ==='ERR'">
                                <div id="error_info" class="accordion">
                                    <label>{{$t("testDescriptionDetail.errorInfo")}}</label>
                                    <div id="error_code" class="accordion detail">
                                        <label>{{$t("testDescriptionDetail.errorCode")}}</label>
                                        <template v-if="tdDtl.TestDescriptionResult.ErrorCode">
                                            <span>{{tdDtl.TestDescriptionResult.ErrorCode}}</span>
                                        </template>
                                        <template v-else>
                                            <span>undefined</span>
                                        </template>
                                    </div>
                                    <div id="error_message" class="accordion detail">
                                        <label>{{$t("testDescriptionDetail.errorMessage")}}</label>
                                        <span style="white-space:pre-wrap; word-wrap:break-word;">{{tdErrorMessage}}</span>
                                    </div>
                                    <div id="error_detail" class="accordion detail">
                                        <label>{{$t("testDescriptionDetail.errorDetail")}}</label>
                                        <span style="white-space:pre-wrap; word-wrap:break-word;">{{tdDtl.TestDescriptionResult.Detail}}</span>
                                    </div>
                                </div>
                            </template>
                        </template>
                        <!-- 取得グラフ -->
                        <template v-if="tdDtl.TestDescriptionResult">
                            <template v-if="tdDtl.TestDescriptionResult.Summary ==='OK' || tdDtl.TestDescriptionResult.Summary === 'NG'">
                                <div id="table" align="center" v-on:click="updateUsedRowStyle">
                                    <VueGoodTable :columns="columns" ref="tdTable" :rows="rows" max-height="300px" :fixed-header="true" align="center"
                                                  :sort-options="{enabled: false,}" style-class="vgt-table"
                                                  @on-select-all="onSelectAll"
                                                  @on-row-click="onRowClick"
                                                  @on-selected-rows-change="onSelectedRowsChange"
                                                  :pagination-options="pagenationSettings"
                                                  @on-per-page-change="onPerPageChange"
                                                  @on-page-change="onPageChange"
                                                  :group-options="groupSettings"
                                                  :select-options="selectSettings">
                                        <template slot="table-row" slot-scope="props">
                                            <!--ラジオボタン-->
                                            <span v-if="props.column.field == 'radiobox'">
                                                <input type="radio" name="graph">
                                            </span>
                                            <span v-else-if="props.column.field == 'index'">
                                                <span>{{props.row.index}}</span>
                                                <span v-if="props.row.index == preview_row_index">
                                                    <span class="material-icons" style="font-size:inherit;">
                                                        remove_red_eye
                                                    </span>
                                                </span>
                                            </span>
                                            <span v-else>
                                                {{props.formattedRow[props.column.field]}}
                                            </span>
                                        </template>
                                    </VueGoodTable>
                                </div>
                                <!-- 追加ボタン -->
                                <div id="add_btn_wrapper">
                                    <template v-if="$i18n.locale === 'en'">
                                        <div 
                                          id="add_btn" 
                                          class="btn_single" 
                                          v-bind:class="{ 'un_btn' : isActive }" 
                                          @click="addRowData"
                                        >
                                            <span class="add_count">
                                                <span v-if="isActive">0</span>
                                                <span v-else>{{add_graph_count}}</span>
                                            </span>
                                            add to Report→
                                        </div>
                                    </template>
                                    <template v-else>
                                        <div 
                                          id="add_btn" 
                                          class="btn_single" 
                                          v-bind:class="{ 'un_btn' : isActive }" 
                                          @click="addRowData"
                                        >
                                            <span class="add_count">
                                                <span v-if="isActive">0</span>
                                                <span v-else>{{add_graph_count}}</span>
                                            </span>
                                            レポートに追加→
                                        </div>
                                    </template>
                                    <br/>
                                    <span>{{$t("testDescriptionDetail.addReportNote")}}</span>
                                </div>
                                <!-- グラフ -->
                                <div class="result_img" v-show="preview_visible">
                                    Preview: Graph ID = {{preview_row_index}}<br>
                                    <a class="image" target="_blank">
                                        <img width="400px" name="imgsmp" id="image" class="result_img" />
                                    </a>
                                </div>
                                <!-- 表 -->
                                <table id="result_tbl" rules="rows" v-show="selectedType != null && selectedType === 'table'">
                                    <tbody id="output_table"></tbody>
                                </table>
                                <!-- 合格条件 -->
                                <div id="quality_measurement" class="accordion detail z-depth__">
                                    <label for="Panel1_1">+ {{$t("testDescriptionDetail.qualityMeasurement")}}</label>
                                    <input type="checkbox" id="Panel1_1" class="on_off" checked />
                                    <ul>
                                        <li>
                                            <table class="ac_text">
                                                <tr>
                                                    <td class="tbl21">{{$t("testDescriptionDetail.qualityDimension")}}:</td>
                                                    <td class="tbl22">{{tdDtl.QualityDimension.Name}}</td>
                                                </tr>
                                                <tr>
                                                    <td></td>
                                                    <td></td>
                                                </tr>
                                               <tbody v-for="qualityMeasurement of tdDtl.QualityMeasurements" :key="qualityMeasurement.Id">
                                                    <template v-if="qualityMeasurement.Enable">
                                                        <tr>
                                                            <td class="tbl21">{{$t("testDescriptionDetail.measurement")}}:</td>
                                                            <td class="tbl22">{{qualityMeasurement.Name}}</td>
                                                        </tr>
                                                        <tr>
                                                            <td class="tbl21">{{$t("testDescriptionDetail.description")}}:</td>
                                                            <td class="tbl22">{{qualityMeasurement.Description}}</td>
                                                        </tr>
                                                        <tr>
                                                            <td class="tbl21">{{$t("testDescriptionDetail.configuration")}}:</td>
                                                            <td class="tbl22" v-if="relationalOperators">
                                                                {{qualityMeasurement.Name}} {{getRelationalOperator(qualityMeasurement.RelationalOperatorId)}} {{qualityMeasurement.Value}}
                                                            </td>
                                                        </tr>
                                                        <tr>
                                                            <td></td>
                                                            <td></td>
                                                        </tr>
                                                    </template>
                                                </tbody>
                                            </table>
                                        </li>
                                    </ul>
                                </div>
                                <!-- データダウンロード -->
                                <div id="dl_message">
                                    <a @click="download" class="window">
                                        <img src="~@/assets/new_window.svg" alt="new-window" title="new-window" class="new-window">
                                        {{$t("testDescriptionDetail.downloadMes")}}
                                    </a>
                                </div>
                            </template>
                        </template>
                    </div>

                    <!-- TD詳細 -->
                    <div id="td_detail" class="accordion">
                        <label>{{$t("testDescriptionDetail.title")}}</label>
                        <!-- 合格条件 -->
                        <div class="accordion detail" v-if="tdDtl.TestDescriptionResult == null || tdDtl.TestDescriptionResult.Summary === 'ERR' || tdDtl.TestDescriptionResult.Summary === 'NA'">
                            <label for="Panel1_1">{{$t("testDescriptionDetail.qualityMeasurement")}}</label>
                            <table class="ac_text">
                                <tr>
                                    <td class="tbl21">{{$t("testDescriptionDetail.qualityDimension")}}:</td>
                                    <td class="tbl22">{{tdDtl.QualityDimension.Name}}</td>
                                </tr>
                                <tr>
                                    <td></td>
                                    <td></td>
                                </tr>
                                <tbody v-for="qualityMeasurement of tdDtl.QualityMeasurements" :key="qualityMeasurement.Id">
                                    <template v-if="qualityMeasurement.Enable">
                                        <tr>
                                            <td class="tbl21">{{$t("testDescriptionDetail.measurement")}}:</td>
                                            <td class="tbl22">{{qualityMeasurement.Name}}</td>
                                        </tr>
                                        <tr>
                                            <td class="tbl21">{{$t("testDescriptionDetail.description")}}:</td>
                                            <td class="tbl22">{{qualityMeasurement.Description}}</td>
                                        </tr>
                                        <tr>
                                            <td class="tbl21">{{$t("testDescriptionDetail.configuration")}}:</td>
                                            <td class="tbl22" v-if="relationalOperators">
                                                {{qualityMeasurement.Name}} {{getRelationalOperator(qualityMeasurement.RelationalOperatorId)}} {{qualityMeasurement.Value}}
                                            </td>
                                        </tr>
                                        <tr>
                                            <td></td>
                                            <td></td>
                                        </tr>
                                    </template>
                                </tbody>
                            </table>
                        </div>
                        <!-- TargetInventory -->
                        <div id="target_inventory" class="accordion detail">
                            <label>{{$t("testDescriptionDetail.targetInventory")}}</label>
                            <table>
                                <tr class="tbl22" v-for="targetInv of tdDtl.TargetInventories" :key="targetInv.Id">
                                    <td class="tbl21">{{targetInv.DataType.Name}} :</td>
                                    <td class="tbl22">{{targetInv.Name}} ({{targetInv.Description}})</td>
                                </tr>
                            </table>
                        </div>
                        <!-- AIT -->
                        <div id="ait" class="accordion detail">
                            <label for="Panel1_3">{{$t("testDescriptionDetail.aitInformation")}}</label>
                            <table>
                                <tr>
                                    <td class="tbl21">{{$t("testDescriptionDetail.name")}}:</td>
                                    <td class="tbl22">{{tdDtl.TestRunner.Name}}</td>
                                </tr>
                                <tr>
                                    <td class="tbl21">{{$t("testDescriptionDetail.version")}}:</td>
                                    <td class="tbl22">{{tdDtl.TestRunner.Version}}</td>
                                </tr>
                                <tr>
                                    <td class="tbl21">{{$t("testDescriptionDetail.description")}}:</td>
                                    <td class="tbl22">{{tdDtl.TestRunner.Description}}</td>
                                </tr>
                                <tr>
                                    <td class="tbl21">{{$t("testDescriptionDetail.author")}}:</td>
                                    <td class="tbl22">{{tdDtl.TestRunner.Author}}</td>
                                </tr>
                                <tr>
                                    <td class="tbl21">{{$t("testDescriptionDetail.email")}}:</td>
                                    <td class="tbl22" v-if="tdDtl.TestRunner.Email">
                                        {{tdDtl.TestRunner.Email}}
                                    </td>
                                </tr>
                                <tr>
                                    <td class="tbl21">{{$t("testDescriptionDetail.quality")}}:</td>
                                    <td class="tbl22">
                                        <img src="~@/assets/new_window.svg" alt="new-window" title="new-window" class="new-window">
                                        <a v-bind:href=tdDtl.TestRunner.Quality target="_blank">{{tdDtl.TestRunner.Quality}}</a>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="tbl21">{{$t("testDescriptionDetail.params")}}:</td>
                                    <td class="tbl22">
                                        <div v-for="param of tdDtl.TestRunner.Params" :key="param.Id">
                                            {{param.Name}} : {{param.Value}}
                                        </div>
                                    </td>
                                </tr>
                            </table>
                        </div>
                    </div>
                    <!-- フッタ -->
                    <div id="footer">
                        <address>Copyright © National Institute of Advanced Industrial Science and Technology （AIST）
                        </address>
                    </div>
                </div>

                <!-- レポート登録項目 -->
                <template v-if="tdDtl.TestDescriptionResult">
                    <div id="acd_right" v-if="tdDtl.TestDescriptionResult.Summary === 'OK' || tdDtl.TestDescriptionResult.Summary === 'NG'">
                        <div id="opinion" class="accordion">
                            <label for="Panel3">{{$t("testDescriptionDetail.reportContents")}}</label>
                            <!-- レポートに表示するグラフ一覧 -->
                            <div id="report_graph">
                                <span class="con">{{$t("testDescriptionDetail.graphs")}}</span>
                                <span class="message">{{$t("testDescriptionDetail.graphsNote")}}</span>
                            </div>
                            <div id="grid">
                                <AgGridVue class="ag-theme-fresh" 
                                    :columnDefs="columnDefs" 
                                    :rowData="rowData" 
                                    :gridOptions="gridOptions" 
                                    :tooltipShowDelay="tooltipShowDelay" @row-drag-end="sortChange"
                                    style="width: 97%;"
                                >
                                </AgGridVue>
                                
                                <!-- 削除ボタン -->
                                <div id="btn_del_all">
                                    <template v-if="$i18n.locale === 'en'">
                                        <input type="button" id="del_all_btn" value="←remove all Report graphs" class="btn_single" v-bind:class="{ 'un_btn' : isRemoveAllRowActive }" @click="removeAllRowData">
                                    </template>
                                    <template v-else>
                                        <input type="button" id="del_all_btn" value="←レポートから全グラフ削除" class="btn_single" v-bind:class="{ 'un_btn' : isRemoveAllRowActive }" @click="removeAllRowData">
                                    </template>
                                </div>
                            </div>
                            <!-- 見解 -->
                            <div class="opinion">
                                <span class="con">{{$t("testDescriptionDetail.opinion")}}</span>
                                <textarea class="z-depth__" name="example" cols="80" rows="6" v-model="changeOpinion"></textarea>
                                <div id="btn_reg">
                                    <template v-if="$i18n.locale === 'en'">
                                        <input type="submit" value="Save" class="btn_single" @click="postReportGenerator('SetParam')">
                                        <input type="submit" value="Complete" class="btn_single" @click="postReportGeneratorComplete('SetParam')">
                                    </template>
                                    <template v-else>
                                        <input type="submit" value="保存" class="btn_single" @click="postReportGenerator('SetParam')">
                                        <input type="submit" value="完了" class="btn_single" @click="postReportGeneratorComplete('SetParam')">
                                    </template>
                                </div>
                                <span v-if="errorMessages">
                                    <span class="error" v-for="errorMessage in errorMessages" :key="errorMessage">
                                        {{errorMessage}}<br>
                                    </span>
                                </span>
                            </div>
                        </div>
                    </div>
                </template>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import {
    tdMixin
} from '../mixins/testDescriptionMixin';
import {
    urlParameterMixin
} from '../mixins/urlParameterMixin';
//ag-grid インポート
import '../../node_modules/ag-grid-community/dist/styles/ag-grid.css';
import '../../node_modules/ag-grid-community/dist/styles/ag-theme-fresh.css';
import {
    AgGridVue
} from 'ag-grid-vue';

import 'vue-good-table/dist/vue-good-table.css';
import {
    VueGoodTable
} from 'vue-good-table';

export default {
    mixins: [tdMixin, urlParameterMixin],
    data() {
        return {
            selectedType: '',
            preview_visible: false,
            isActive: true,
            tdGraphs: '',
            tdDtl:'',
            graph_name: '',
            graph_rename: '',
            graph_id: '',
            graph_index: '',
            graph_list: [],
            add_graph_count: 0,
            preview_order: [],
            preview_row_index: null,
            row_num: '',
            fignum: '',
            test_description_details: null,
            opinion: '',
            opinionMaxCharacters: 2000,
            requestBody: [],
            isPush: false,
            selectedGraphs: null,
            targetInventories: [],
            outputElement: null,
            columnDefs: null,
            rowData: null,
            gridOptions: null,
            name: "dgDetail",
            languagedata: null,
            columns: [{
                    label: this.setTableLanguage("index"),
                    field: "index",
                    thClass: 't_left',
                    width: "7%",
                },
                {
                    label: this.setTableLanguage("file_name"),
                    field: "file_name",
                    thClass: 't_left',
                    width: "35%",
                },
                {
                    label: this.setTableLanguage("description"),
                    field: "description",
                    thClass: 't_left',
                    width: "43%",
                },
                {
                    label: this.setTableLanguage("format"),
                    field: "format",
                    thClass: 't_left',
                    width: "15%",
                },
                {
                    label: this.setTableLanguage("radiobox"),
                    field: "radiobox",
                    width: "0px",
                }
            ],
            rows: [],
            isRemoveAllRowActive: false,
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
                enabled: true,
                disableSelectInfo: true,
                selectAllByGroup: false
            },
            isExpanded: false,
            tdErrorMessage: '',
        }
    },
    components: {
        AgGridVue,
        VueGoodTable
    },
    beforeMount() {
        //ag-grid用のヘッダー定義
        this.columnDefs = [{
                headerName: this.setReportTableLanguage("id"),
                field: "viewId",
                width: 60,
                rowDrag: true,
            },
            {
                headerName: this.setReportTableLanguage("name"),
                field: "name",
                flex: 4,
                tooltipField: 'name',
            },
            {
                headerName: this.setReportTableLanguage("reportName"),
                field: "reportName",
                editable: true,
                cellEditorSelector: function (params) {
                    if(params.data.type === 'reportName')
                    return {
                        component: 'reportName'
                    }
                },
                flex: 5,
            },
            {
                field: "no",
                hide: true,
            },
            {
                headerName: this.setReportTableLanguage("remove"),
                field: "remove",
                cellRenderer: (params) => {
                    const element = document.createElement('button');
                    element.classList.add('minusBtn');
                    element.innerHTML = params.value.value;
                    element.addEventListener('click', () => {
                        this.onRemoveSelected(params.value.id);
                    });
                    return element;
                },
                width: 22,
            }
        ];
        //ag-grid用の行定義
        this.rowData = [];

        //ag-gridの設定
        this.gridOptions = {
            domLayout: 'autoHeight',
            rowDragManaged: true,
            animateRows: true,
        }
        
        this.tooltipShowDelay = 0;
    },
    mounted: function () {
        this.mlComponentIdCheck();
        this.organizationIdCheck = sessionStorage.getItem('organizationId');
        this.mlComponentId = sessionStorage.getItem('mlComponentId');
        this.testDescriptionId = sessionStorage.getItem('testDescriptionId');
        this.getMLComponent();
        const url = this.$backendURL +
            '/' +
            this.organizationIdCheck +
            '/mlComponents/' +
            this.mlComponentId +
            '/testDescriotions/' +
            this.testDescriptionId;
        this.$axios.get(url)
            .then((response) => {
                this.test_description_details = response.data;
                this.opinion = this.test_description_details.TestDescriptionDetail.Opinion;
                this.tdDtl = this.test_description_details.TestDescriptionDetail;
                if(this.test_description_details.TestDescriptionDetail.TestDescriptionResult){
                    this.tdGraphs = this.test_description_details.TestDescriptionDetail.TestDescriptionResult.Graphs
                    this.getTDResources(this.tdGraphs);
                }
                if(this.tdGraphs != null && this.tdGraphs != "") {
                    this.creatRowData();
                }
                this.setTDErrorMessage();
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
            this.beginUpdateUsedRowStyle();
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
                    case 'index':
                        return this.languagedata.ja.testDescriptionDetail.index;
                    case 'file_name':
                        return this.languagedata.ja.testDescriptionDetail.file_name;
                    case 'description':
                        return this.languagedata.ja.testDescriptionDetail.description;
                    case 'format':
                        return this.languagedata.ja.testDescriptionDetail.type;
                    case 'radiobox':
                        return this.languagedata.ja.testDescriptionDetail.radiobox;
                    case 'pageNext':
                        return this.languagedata.ja.testDescriptionDetail.pageNext;
                    case 'pagePrev':
                        return this.languagedata.ja.testDescriptionDetail.pagePrev;
                    case 'rowsPerPageLabel':
                        return this.languagedata.ja.testDescriptionDetail.rowsPerPageLabel;
                    default:
                }
            } else if (this.$i18n.locale == 'en') {
                switch (fieldName) {
                    case 'index':
                        return this.languagedata.en.testDescriptionDetail.index;
                    case 'file_name':
                        return this.languagedata.en.testDescriptionDetail.file_name;
                    case 'description':
                        return this.languagedata.en.testDescriptionDetail.description;
                    case 'format':
                        return this.languagedata.en.testDescriptionDetail.type;
                    case 'radiobox':
                        return this.languagedata.en.testDescriptionDetail.radiobox;
                    case 'pageNext':
                        return this.languagedata.en.testDescriptionDetail.pageNext;
                    case 'pagePrev':
                        return this.languagedata.en.testDescriptionDetail.pagePrev;
                    case 'rowsPerPageLabel':
                        return this.languagedata.en.testDescriptionDetail.rowsPerPageLabel;
                    default:
                }
            }
        },
        setReportTableLanguage(fieldName) {
            // mountよりも先に呼び出されるので、ここで言語設定を呼び出す。
            this.setLanguageData()
            this.languagedata = require('./languages/languages.json');
            if (this.$i18n.locale == 'ja') {
                switch (fieldName) {
                    case 'id':
                        return this.languagedata.ja.testDescriptionDetail.index;
                    case 'name':
                        return this.languagedata.ja.testDescriptionDetail.name;
                    case 'reportName':
                        return this.languagedata.ja.testDescriptionDetail.nameOnReport;
                    case 'remove':
                        return this.languagedata.ja.testDescriptionDetail.remove;
                    default:
                }
            } else if (this.$i18n.locale == 'en') {
                switch (fieldName) {
                    case 'id':
                        return this.languagedata.en.testDescriptionDetail.index;
                    case 'name':
                        return this.languagedata.en.testDescriptionDetail.name;
                    case 'reportName':
                        return this.languagedata.en.testDescriptionDetail.nameOnReport;
                    case 'remove':
                        return this.languagedata.en.testDescriptionDetail.remove;
                    default:
                }
            }
        },
        setTDErrorMessageLanguage(errorCode) {
            // mountよりも先に呼び出されるので、ここで言語設定を呼び出す。
            this.setLanguageData()
            this.languagedata = require('./languages/languages.json');
            if (this.$i18n.locale == 'ja') {
                if(typeof this.languagedata.ja.testDescriptionErrorMessage[errorCode] != 'undefined'){
                    return this.languagedata.ja.testDescriptionErrorMessage[errorCode];
                }else{
                    return this.languagedata.ja.testDescriptionErrorMessage['undefined'];
                }
            } else if (this.$i18n.locale == 'en') {
                if(typeof this.languagedata.en.testDescriptionErrorMessage[errorCode] != 'undefined'){
                    return this.languagedata.en.testDescriptionErrorMessage[errorCode];
                }else{
                    return this.languagedata.en.testDescriptionErrorMessage['undefined'];
                }
            }
        },
        changeLanguage(lang) {
            sessionStorage.setItem('language', lang);
            this.changeTableTitleLanguage();
            this.setTDErrorMessage();
        },
        changeTableTitleLanguage() {
            for (var i = 0; i < this.columns.length; i++) {
                this.columns[i].label = this.setTableLanguage(this.columns[i].field)
            }
            for (var j = 0; j < this.columnDefs.length; j++) {
                this.columnDefs[j].label = this.setReportTableLanguage(this.columnDefs[j].field)
            }
        },
        setTDErrorMessage(){
            if(this.tdDtl.TestDescriptionResult == null){
                return;
            }

            if(this.tdDtl.TestDescriptionResult.Summary == "ERR"){
                if(typeof this.tdDtl.TestDescriptionResult.ErrorCode == 'undefined'){
                    this.tdErrorMessage = this.setTDErrorMessageLanguage('undefined');
                }else{
                    this.tdErrorMessage = this.setTDErrorMessageLanguage(this.tdDtl.TestDescriptionResult.ErrorCode);
                }
            }
        },
        getTDResources(val) {
            var index = 1;
            var gourp_td = {}
            for (var td in val) {
                if (gourp_td[val[td].Name] == null){
                    gourp_td[val[td].Name] = []
                }
                gourp_td[val[td].Name].push({
                    index: index,
                    name: val[td].Name,
                    file_name: val[td].FileName,
                    description: val[td].Description,
                    format: val[td].GraphType,
                    graph_id: val[td].Id
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
        },
        onSelectAll(){
            this.preview_visible = false; //プレビュー非表示
            this.preview_row_index = -1; //プレビュー対象のidをダミー値に
            this.preview_order = []; //プレビュー対キリストを空に
        },
        onRowClick(params){
            var clicked_row_index = params.row.index;
            if(params.selected){
                // チェックを入れたなら、描写リストの優先順位に最高順位として追加
                this.preview_order.push(clicked_row_index);
            }else{
                // チェックを外したなら、描写リストから除外
                this.preview_order = this.preview_order.filter(row_index => row_index != clicked_row_index);
            }
        },
        onSelectedRowsChange(params) {
            this.graph_list = params.selectedRows;

            //何も選択されていなかったときの処理
            if(params.selectedRows.length <= 0){
                this.isActive = true; // addボタン非活性
                this.preview_visible = false; //プレビュー非表示
                this.preview_row_index = -1; //プレビュー対象のidをダミー値に
                this.updateUsedRowStyle();
                return;
            }

            //addボタンの活性判定
            this.checkAddBTNActive();
            
            //グラフのプレビュー
            this.preview_row_index = this.preview_order[this.preview_order.length-1];
            this.preview_result(this.preview_row_index);

            this.updateUsedRowStyle();
        },
        //addボタンの活性判定
        checkAddBTNActive(){
            this.isActive = true; //非活性状態で初期化
            this.add_graph_count = 0; //追加予定のグラフの個数を0個で初期化
            for (let j = 0; j < this.graph_list.length; j++) {
                var graph = this.graph_list[j];
                var registered = false;
                for (var r_id in this.rowData) {
                    if (graph.graph_id == this.rowData[r_id].graphId) {
                        registered = true;
                        break;
                    }
                }
                if(!registered){
                    this.isActive = false; //右欄に未登録なら活性状態
                    this.add_graph_count += 1;
                }
            }
        },
        preview_result(preview_row_index){
            this.preview_visible = false;
            var graph = this.graph_list.filter(graph => graph.index == preview_row_index)[0];

            if(!graph) return;
            this.selectedType = graph.format;
            if (graph.format === "picture") {
                this.getImage(this.tdGraphs[graph.index-1].Graph);
                this.preview_visible = true;
            }else if(graph.format === 'table'){
                this.getTableData(this.tdGraphs[graph.index-1].Graph);
                this.preview_visible = true;
            }
        },
        onPerPageChange(){
            var tdTable = this.$refs.tdTable;
            tdTable.currentPage = 1;
            this.graph_id = '';
            this.graph_index = '';
            this.graph_name = '';
            this.graph_rename = '';
            this.selectedType = '';
            this.isActive = true;
            this.beginUpdateUsedRowStyle();
        },
        onPageChange() {
            this.beginUpdateUsedRowStyle();
        },
        postReportGenerator(command) {
            this.errorMessages = [];
            this.checkOpinion();
            if (this.errorMessages.length === 0) {
                this.requestBody = this.setRequestBody(command)
                const url = this.$backendURL +
                    '/' +
                    this.organizationIdCheck +
                    '/mlComponents/' +
                    this.mlComponentId +
                    '/testDescriotions/reportGenerator';
                this.$axios.post(url, this.requestBody)
                    .then((response) => {
                        this.result = response.data;
                    })
                    .catch((error) => {
                        this.$router.push({
                            name: 'Information',
                            params: {
                                error
                            }
                        })
                    });
            } else {
                var element = document.documentElement;
                var bottom = element.scrollHeight - element.clientHeight;
                scrollTo(0, bottom);
            }
        },
        postReportGeneratorComplete(command) {
            this.errorMessages = [];
            this.checkOpinion();
            if (this.errorMessages.length === 0) {
                this.requestBody = this.setRequestBody(command)
                const url = this.$backendURL +
                    '/' +
                    this.organizationIdCheck +
                    '/mlComponents/' +
                    this.mlComponentId +
                    '/testDescriotions/reportGenerator';
                this.$axios.post(url, this.requestBody)
                    .then((response) => {
                        this.result = response.data;
                        this.$router.push({
                            name: 'TestDescriptions',
                        })
                    })
                    .catch((error) => {
                        this.$router.push({
                            name: 'Information',
                            params: {
                                error
                            }
                        })
                    });
            } else {
                var element = document.documentElement;
                var bottom = element.scrollHeight - element.clientHeight;
                scrollTo(0, bottom);
            }
        },
        setRequestBody(command){
            var body = {};
            var testDescriptionId_str = String(this.testDescriptionId);
            if (command == 'SetParam') {
                var graphBody = [];
                for(var left of this.tdGraphs){
                    if(this.rowData){
                        for(var i=0; i<this.rowData.length;i++){
                            if(left.Id === this.rowData[i].graphId){
                                var tempName = this.rowData[i].reportName;
                                if(this.rowData[i].reportName == null && this.rowData[i].reportName == ""){
                                    tempName = this.rowData[i].name;
                                }
                                var repoIndex = parseInt(this.rowData[i].no);
                                var tempBody_RequiredTrue = {
                                    "GraphId": this.rowData[i].graphId,
                                    "ReportRequired": true,
                                    "ReportIndex": repoIndex,
                                    "ReportName": tempName
                                }
                                graphBody.push(tempBody_RequiredTrue);
                                break;
                            }
                        }
                    }
                    else{
                        var tempBody_RequiredFalse = {
                            "GraphId": left.Id,
                            "ReportRequired": false
                        }
                        graphBody.push(tempBody_RequiredFalse);
                    }
                }
                body =
                    {
                        "Command": command,
                        "Destination": [testDescriptionId_str],
                        "Params": {
                            "Opinion": this.opinion,
                            "Graphs": graphBody
                        }
                    }
            } else {
                body =
                    {
                        "Command": command,
                        "Destination": [testDescriptionId_str],
                    }
            }
            return body
        },
        testDescriptionDelete() {
            if (confirm(this.$t("confirm.delete"))) {
                this.$axios.delete(this.$backendURL +
                        '/' +
                        this.organizationIdCheck +
                        '/mlComponents/' +
                        this.mlComponentId +
                        '/testDescriotions/' +
                        this.testDescriptionId
                )
                .then((response) => {
                    this.result = response.data;
                    this.$router.push({
                        name: 'TestDescriptions'
                    })
                })
                .catch((error) => {
                    this.$router.push({
                        name: 'Information',
                        params: {
                            error
                        }
                    })
                })
            }
        },
        postTestDescriptionId_toEdit: function (testDescriptionId) {
            this.$router.push({
                name: 'TestDescriptionEdit',
                params: {
                    testDescriptionId: testDescriptionId
                }
            })
        },
        postTestDescriptionId_toCopy: function (testDescriptionId) {
            this.$router.push({
                name: 'TestDescriptionCopy',
                params: {
                    testDescriptionId: testDescriptionId
                }
            })
        },
        runTest() {
            const that = this;
            this.isPush = true;
            const url = this.$backendURL +
                '/' +
                this.organizationIdCheck +
                '/mlComponents/' +
                this.mlComponentId +
                '/testDescriotions/runners'
            this.$axios.post(url, {
                    "Command": "AsyncStart",
                    "TestDescriptionIds": [this.testDescriptionId]
                })
                .then((response) => {
                    // eslint-disable-next-line no-console
                    console.log(response.data);
                    this.intervalId = setInterval(function () {
                        that.checkTestRunnerStatus();
                    }, 1000)
                })
                .catch((error) => {
                    this.isPush = false;
                    // eslint-disable-next-line no-console
                    console.log(error.response.data);
                    alert(error.response.data.Message);
                });
        },
        checkTestRunnerStatus() {
            const url = this.$backendURL +
                '/' +
                this.organizationIdCheck +
                '/mlComponents/' +
                this.mlComponentId +
                '/testDescriotions/run-status';
            this.$axios.get(url)
                .then(response => {
                    // eslint-disable-next-line no-console
                    console.log(response.data.Result.Code + ': ' + response.data.Result.Message)
                    const data = response.data;
                    if (data.Job.Status == 'DONE') {
                        this.isPush = false;
                        clearInterval(this.intervalId);
                        delete this.intervalId;
                        
                        const url = this.$backendURL +
                            '/' +
                            this.organizationIdCheck +
                            '/mlComponents/' +
                            this.mlComponentId +
                            '/testDescriotions/' +
                            this.testDescriptionId;
                        this.$axios.get(url)
                            .then((response) => {
                                // eslint-disable-next-line no-console
                                console.log(response.data);
                                this.test_description_details = response.data;
                                this.tdDtl = this.test_description_details.TestDescriptionDetail;
                                if(this.test_description_details.TestDescriptionDetail.TestDescriptionResult){
                                    this.tdGraphs = this.test_description_details.TestDescriptionDetail.TestDescriptionResult.Graphs
                                    this.getTDResources(this.tdGraphs);
                                }
                                if(this.tdGraphs != null && this.tdGraphs != "") {
                                    this.creatRowData();
                                }
                            })
                            .catch((error) => {
                                this.$router.push({
                                    name: 'Information',
                                    params: {
                                        error
                                    }
                                })
                            })

                        // eslint-disable-next-line no-console
                        console.log('status check roop fin')
                    }
                })
                .catch((error) => {
                    // eslint-disable-next-line no-console
                    console.log(error.response.data);
                    alert(error.response.data.Message + '\nPlease push "Run Test" after waiting a moment or canceling the job.');
                    this.isPush = false;
                });
        },
        checkOpinion() {
            if (this.opinion.length > this.opinionMaxCharacters) {
                this.errorMessages.push('Opinion must be ' + this.opinionMaxCharacters + ' characters or less.');
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
            if (value === 'file') {
                if (this.selectedGraphs != null) {
                    const link = document.createElement('a');
                    link.href = this.selectedGraphs.Graph;
                    link.click();
                }
            } else if (value === 'log') {
                if (this.test_description_details.TestDescriptionDetail.TestDescriptionResult != null) {
                    const link = document.createElement('a');
                    link.href = this.test_description_details.TestDescriptionDetail.TestDescriptionResult.LogFile;
                    link.click();
                }
            } else {
                if (value != null) {
                    const link = document.createElement('a');
                    link.href = value;
                    link.click();
                }
            }
        },
        getRelationalOperator(value) {
            var expression = '';
            for (var relationalOperator of this.relationalOperators.RelationalOperator) {
                if (value === relationalOperator.Id) {
                    expression = relationalOperator.Expression;
                }
            }
            return expression;
        },
        //-ボタンで表を削除するメソッド。変更不要。
        onRemoveSelected: function (id) {
            //RowDataをculRowDataへディープコピー
            var culRowData = [];
            this.gridOptions.api.forEachNode(node => culRowData.push(node.data));
            //作業変数定義
            var newNo = 1; //上から順に振られる番号(順序番号)を振り直すための変数
            var removeRow = -1; //削除対象の順序番号
            //削除対象を配列から削除
            for (var row in culRowData) {
                if (culRowData[row].remove.id == id) {
                    //削除対象の順序番号を控えておく
                    removeRow = row;
                }else{
                    //順序番号の振り直し
                    culRowData[row].no = newNo;
                    newNo += 1;
                }
            }
            culRowData.splice(removeRow, 1) //控えていた削除対象番号を用いて削除

            // 更新処理
            this.gridOptions.api.setRowData(culRowData);
            this.rowData = culRowData;
            this.sortChange();
            if (this.rowData.length == 0){
                this.isRemoveAllRowActive = true;
            }
            this.updateUsedRowStyle();
            this.checkAddBTNActive();
        },
        //右側の表にデータを追加するメソッド。引数を(no, name, graph)設定し,
        //newRowData[newRowData.length - 1] = {no: no, name: name, reportName: graph, remove:{value: '-', id: this.setRowId()}}
        //のように変更すれば任意のデータを追加することができる。
        addRowData: function () {
            this.checkAddBTNActive(); //追加するグラフ数を再計算

            var row_limit = 20;
            // 現在の右枠のグラフ数+追加予定のグラフ数が
            // 上限(row_limit)を超過したらアラートし、追加しない
            if(this.rowData.length + this.add_graph_count > row_limit){
                alert(this.$t("testDescriptionDetail.warnAddReportResource"));
                return;
            }

            var newRowData = [];
            this.gridOptions.api.forEachNode(node => newRowData.push(node.data));

            for(let i=0; i<this.graph_list.length; i++){
                var graph = this.graph_list[i];
                graph.vgtSelected = false;

                // 登録済みなら追加しない
                var registered = false;
                for (var r_id in this.rowData) {
                    if (graph.graph_id == this.rowData[r_id].graphId) {
                        registered = true;
                        break;
                    }
                }
                if(registered){
                    continue;
                }

                // 未登録なら新規追加
                var newRow = {
                    no: graph.index,
                    viewId: graph.index,
                    name: graph.name,
                    reportName: graph.name,
                    graphId: graph.graph_id,
                    remove: {
                        value: '',
                        id: this.setRowId()
                    }
                }
                newRowData.push(newRow);
            }
            this.preview_order = [];
            this.preview_row_index = -1;

            this.gridOptions.api.setRowData(newRowData);
            this.rowData = newRowData;

            this.sortChange();
            this.updateUsedRowStyle();
            this.checkAddBTNActive();
            this.isRemoveAllRowActive = false;
        },
        removeAllRowData: function () {
            this.rowData = [];
            this.gridOptions.api.setRowData(this.rowData);
            // 選択対象があれば追加ボタン活性、なければ非活性
            if (this.selectedType != ''){
                this.isActive = false;
            }
            else{
                this.isActive = true;
            }
            this.isRemoveAllRowActive = true;
            this.clearUsedRowStyle();
            this.checkAddBTNActive();
        },
        creatRowData: function () {
            this.fignum = 1

            var reportObj = {};
            var reportSize = 0;
            for(var i=0; i<this.tdGraphs.length; i++) {
                if(this.tdGraphs[i].ReportRequired){
                    reportObj[this.tdGraphs[i].ReportIndex] = this.tdGraphs[i]
                    reportSize += 1;
                }
            }
            for(var j=1; j<=reportSize; j++){
                var graph = reportObj[j]
                if(graph.ReportName != null && graph.ReportName != ""){
                    this.graph_rename = graph.ReportName
                } else {
                    this.graph_rename = graph.Name
                }

                // 表示中のIDを取得
                var viewId = -1;
                for(var rowSummaryKey in this.rows){
                    for(var rowKey in this.rows[rowSummaryKey].children){
                        if(this.rows[rowSummaryKey].children[rowKey].graph_id == graph.Id){
                            viewId = this.rows[rowSummaryKey].children[rowKey].index;
                            break;
                        }
                    }
                    if(viewId != -1){
                        break;
                    }
                }

                this.rowData[j-1] = {no: j,
                                    graphId: graph.Id,
                                    name: graph.Name,
                                    reportName: this.graph_rename,
                                    viewId: viewId,
                                    remove: {
                                        value: '',
                                        id: j
                                    }}
            }
            if(reportSize==0){
                this.isRemoveAllRowActive = true;
            }
        },
        //行のソート用のメソッド
        sortChange: function () {
            var culRowData = [];
            this.gridOptions.api.forEachNode(node => culRowData.push(node.data));
            for (var row in culRowData) {
                culRowData[row].no = (Number(row) + 1);
            }
            this.gridOptions.api.setRowData(culRowData);
        },

        download() {
            sessionStorage.setItem('testDescriptionId', this.test_description_details.TestDescriptionDetail.Id)
            this.$router.push({
                name: 'TestDescriptionsDownload'
            })
        },

        onStarChange: function (testDescription) {
            if (testDescription.Star === true) {
                this.setUnStar(testDescription.Id);
            } else {
                this.setStar(testDescription.Id);
            }
            testDescription.Star = !testDescription.Star;
        },

        //表削除用のidを設定するメソッド。
        setRowId() {
            //これはculRowDataに現在表に登録されているデータ群を配列として追加する。
            //saveやコンプリートボタン時に使うことも出来る。
            var culRowData = [];
            this.gridOptions.api.forEachNode(node =>{ 
                culRowData.push(node.data)
                });
            /////////////////////////////////////////////////////////////////////////
            //ここから下がID設定用メソッド。

            if(culRowData == ""){
                return 1;
            }else {
                var idList = [];
                for(var ro in culRowData){
                    // idListにculRowData[row].remove.idの値を収集
                    idList.push(Number(culRowData[ro].remove.id))
                }
                //idListの最大値を取得
                const aryMax = function (a, b) {return Math.max(a, b);}
                var MaxId = idList.reduce(aryMax);
                return MaxId + 1;
            }
        },
        clearUsedRowStyle(){
            var tdTable = this.$refs.tdTable;
            var pageRemain = tdTable.currentPerPage;

            for (var j = 0; j < pageRemain; j++) {
                var graph_element = document.getElementsByName('graph')[j];
                if (graph_element == undefined){
                    break;
                }

                var rowElement = graph_element.parentNode.parentNode.parentNode;
                rowElement.classList.remove('graph_used');
            }
        },
        updateUsedRowStyle(){
            var tdTable = this.$refs.tdTable;
            var pageRemain = tdTable.currentPerPage;

            // 使用済みスタイルの全解除
            this.clearUsedRowStyle();

            //使用済みの行にCSS「graph_used」適用
            for (var j = 0; j < pageRemain; j++) {
                var graph_element = document.getElementsByName('graph')[j];
                if (graph_element == undefined){
                    break;
                }

                // 選択中のスタイル適用はスキップ
                if (graph_element.checked) {
                    continue;
                }
                var rowElement = graph_element.parentNode.parentNode.parentNode;
                var viewId = rowElement.childNodes[4].childNodes[0].childNodes[0].childNodes[0].data;
                viewId = parseInt(viewId.trim());

                for (var r_id in this.rowData) {
                    if (this.rowData[r_id].viewId == viewId) {
                        rowElement.classList.add('graph_used');
                    }
                }

                // プレビュー中の行にハイライトのスタイル適用
                if (this.preview_row_index == viewId) {
                    rowElement.classList.add('graph_previewed');
                }else{
                    rowElement.classList.remove('graph_previewed');
                }
            }
        },
        beginUpdateUsedRowStyle() {
            // elementに反映されるまでのタイムラグを吸収して実行するためのメソッド
            var self = this;
            setTimeout(
                function () {
                    self.updateUsedRowStyle();
                },
                "100"
            );
        }
    },
    computed: {
        changeOpinion: {
            get() {
                return this.opinion;
            },
            set(value) {
                this.opinion = value;
            }
        }
    }
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

/*---------------
表
----------------*/
#table>>>table tr:hover {
    background-color: rgb(233, 233, 233) !important;
}

#table >>> table.vgt-table td {
    padding: 4px 2px;
    vertical-align: middle !important;
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

#table>>>.vgt-table tbody th,
#table>>>.vgt-table tbody td{
    cursor:pointer;
}

#table>>>.vgt-table th.vgt-row-header>span{
    display: block;
}

#table>>>.vgt-table th.vgt-row-header{
    color: black !important;
}

#table>>>.vgt-table th.sortable:after,
#table>>>.vgt-table th.sortable::before {
    right: 40px !important;
}

#table>>>table.vgt-table {
    font-size: 16px !important;
    max-width: 100% !important;
}

#table>>>.vgt-left-align {
    text-align: left !important;
    vertical-align: middle !important;
}

#table>>>.vgt-table tr.clickable.graph_used {
    background-color: #8cfff9;
}

#table>>>.vgt-table tr.clickable.graph_previewed {
    background-color: #faf500 !important;
}

.submenu_detail a {
    margin-left: 15px;
    padding: 5px 20px;
}

/*アイコン*/

#icon_btn {
    text-align: right;
    display: flex;
}

/*----------------
TestDescriptionName
----------------*/
#testdiscriptions {
    padding: 10px 2% 0px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
}

#td_name {
    vertical-align: middle;
}

#td_name h2 {
    text-align: left;
    word-break: break-all;
    display: inline;
}

/*----------------
status
----------------*/
.status {
    vertical-align: middle;
}

#status {
    font-size: 20px;
    margin: 10px 0;
    font-weight: bold;
    border-bottom: #000066 2px dashed;
}

#log_download {
    font-size: 12px;
    margin-left: 25px;
    font-weight: normal;
}

/*アイコン*/

#icon_btn {
    text-align: right;
}

#icon_btn .btn_single {
    margin: 0px 10px;
}

/*----------------
折り畳み   
----------------*/
#accordion {
    display: flex;

}

#acd_left {
    width: 55%;
}

#acd_right label {
    background-color: #466111;
}

#acd_right {
    width: 45%;
}

#opinion {
    position: fixed;
    overflow-y: auto;
    overflow-x: hidden;
    height: calc(100% - 85px);
    padding-bottom: 10px;
    border-left: 1px solid gray;
}

.accordion {
    margin: 10px 0px;
    padding: 0px 20px;
}

.accordion.detail {
    margin: 10px 0 10px 2%;
    padding: 0;
}

label {
    background-color: #9bbb59;
    color: #ffffff;
    font-size: 18px;
    padding: 2px 8px;
    display: block;
    margin: 0;
}

input[type="checkbox"].on_off {
    display: none;
}

input[type="checkbox"].on_off+ul {
    height: auto;
}

input[type="checkbox"].on_off:checked+ul {
    height: 0;
    overflow: hidden;
}

.accordion ul {
    -webkit-transition: all 0.5s;
    -moz-transition: all 0.5s;
    -ms-transition: all 0.5s;
    -o-transition: all 0.5s;
    transition: all 0.5s;
    padding: 0;
    list-style: none;
}

/*----------------
表全体
----------------*/
#table {
    font-size: 15px;
    margin: 0px auto 10px;
    width: 90%;
}

td {
    padding-top: 0;
    padding-bottom: 0;
}

#table input {
    display: none;
}

/*----------------
Result一覧表
----------------*/

.checked {
    background-color: #d1ff8c;
}

.memo {
    font-size: 12px;
}

.result_img {
    text-align: center;
    padding: 10px 0px;
}

.image {
    text-decoration: none;
    cursor: zoom-in;
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
その他取得データ
----------------*/
#dl_message {
    text-align: right;
}

/*----------------
レポート登録項目
----------------*/
#table_added th {
    background-color: #466111;
}

#table_added tr:hover {
    background-color: rgb(233, 233, 233);
}

#add_btn_wrapper {
    text-align: right ;
    margin-top: 20px;
}

#btn_del_all {
    text-align: left ;
    margin-top: 10px;
    margin-left: 10px;
    margin-bottom: 20px;
}

.add_count {
    background-color: white;
    color: rgb(49, 67, 107);
    border-radius: 40%;
    padding: 0em 0.7em;
    margin-right: 0.3em;
    text-align: center;
}

.un_btn .add_count{
    color: #a1a1bb;
}

#opinion input[type="text"] {
    border: solid 1px gray;
    width: 90%;
    padding: 2px;
}

#report_graph {
    justify-content: start;
    display: flex;
    align-items: flex-end;
    padding-top: 10px;
}

.message {
    font-size: 13px;
    padding-left: 15px;
}

#btn_reg input {
    margin: 0 5px;
}

#grid>>>button.minusBtn {
    width: 20px;
    height: 20px;
    font-weight: bold;
    border: 1px solid #ccc;
    color: #31436b;
    background: #fff;
    border-radius: 5px;
    padding: 0;
    margin: 0;
    line-height: normal;
    box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.29);
    cursor:pointer;
}

#grid>>>button.minusBtn:after {
  font-family: 'Material Icons';
  font-size: 18px;
  content: "\e15b";
}


/*----------------
quality_measurement
----------------*/
#quality_measurement {
    margin-bottom: 20px;
}

#quality_measurement label {
    background-color: transparent;
    color: #000066;
    font-weight: bold;
}

#quality_measurement label:hover {
    background: #aaaaaa;
}

/*----------------
見解
----------------*/
.opinion {
    align-items: flex-end;
}

#opinion li {
    padding-top: 10px;
}

.accordion textarea {
    width: 95%;
    margin: 0 10px 10px;
    padding: 5px;
}

#btn_reg {
    text-align: center;
}

.con {
    padding-left: 5px;
}

/*----------------
フッター
----------------*/
#footer {
    padding-top: 30px;
}

/*----------------
テスト詳細
----------------*/
.detail td {
    background-color: #f0f0f0;
}

.tbl21 {
    width: 160px;
    /*ラベルの幅 文字数に合わせる*/
}

.accordion tr {
    vertical-align: top;
}

/*----------------
新しいタブを開く
----------------*/
.new-window {
    width: 20px;
    height: 20px;
    vertical-align: middle;
}

.window {
    cursor: pointer;
}

/*---------------
ag-gridスタイル
---------------*/
/* ポップアップ */
#grid>>>.ag-popup-child {
    box-shadow: 0 3px 1px -2px rgba(0, 0, 0, 0.2), 0 2px 2px 0 rgba(0, 0, 0, 0.14), 0 1px 5px 0 rgba(0, 0, 0, 0.12);
    background-color: var(--ag-control-panel-background-color, #fafafa);
}

#grid>>>.ag-theme-fresh .ag-root-wrapper {
    position: relative;
    left: 11px;
}

#grid>>>.ag-theme-fresh .ag-header-cell::after,
.ag-theme-fresh .ag-header-group-cell::after {
    width: 0px;
}

#grid>>>.ag-theme-fresh .ag-header-cell,
.ag-theme-fresh .ag-header-group-cell {
    color: white;
    background-color: #466111;
}

#grid>>>.ag-drag-handle.ag-row-drag {
    margin-right: 2px !important;
}

#grid>>>.ag-theme-fresh .ag-cell{
    padding-left: 0 !important;
    padding-right: 0 !important;
}

#grid>>>.ag-header-cell-label.ag-header-cell-text {
    text-align: center !important;
}
#grid>>>.ag-theme-fresh .ag-ltr .ag-cell {
    border-right: none;
}

#grid>>>.ag-cell{
    color: #000066;
    line-height: 1.1;
}

#grid>>>.ag-theme-fresh .ag-row-odd {
    background-color: white;
}

</style>

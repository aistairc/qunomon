<template>
<div>
    <!--ヘッダータイトル-->
    <header id="head" :class="{ active: isActive }">
        <div id="title">
            <button @click="toggleSubmenu(isActive)" class="qq"><img :src="this.isActive ? this.icon2 : this.icon1" alt="Image" width="30" height="auto"></button>
            <h1 class="head_title">{{$t("common.title")}}</h1>
        </div>
    </header>
    <!-- サブメニュー（左カラム） -->

    <SubMenu :isActive="this.isActive" >
        <!--SubMenuのアイコンとメニューの間の言語項目は各コンポーネントで実施-->
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
    </SubMenu>


    <!-- ニュース（中央カラム） -->
    <div id="main" :class="{ active: isActive }">
        <div id="main_body">
            <div id="search_table">
                <div class="btnArea">
                    <mlcCreate :key="key" ref="mlcc" @createMLC="addMLComponents" @reset="modalReset"></mlcCreate>
                </div>
                <!--表-->
                <div id="table" align="center">
                    <VueGoodTable
                        ref="mlTable"
                        :columns="columns"
                        styleClass="vgt-table"
                        :rows="rows"
                        max-height="700px"
                        :fixed-header="true"
                        align="center"
                        :search-options="{enabled: true}"
                        :pagination-options="{enabled: true, mode: 'pages'}"
                        @on-row-click="onRowClick"
                    >
                        <template slot="table-row" slot-scope="props">
                            <!--EditOptions-->
                            <span v-if="props.column.field == 'edit_options'">
                                <template v-if="$i18n.locale === 'en'">
                                    <img src="~@/assets/edit.svg" alt="edit" title="edit" class="icon" @click="editMlComponent(props)"/>
                                    <img src="~@/assets/delete.svg" alt="delete" title="delete" class="icon" @click="deleteMlComponent(props)"/>
                                </template>
                                <template v-else>
                                    <img src="~@/assets/edit.svg" alt="編集" title="編集" class="icon" @click="editMlComponent(props)"/>
                                    <img src="~@/assets/delete.svg" alt="削除" title="削除" class="icon" @click="deleteMlComponent(props)"/>
                                </template>
                            </span>
                            <span v-else-if="props.column.field == 'test'">
                                <template v-if="$i18n.locale === 'en'">
                                    <img src="~@/assets/test.svg" alt="test" title="test" class="icon" @click="screenTransition(props)"/>

                                </template>
                                <template v-else>
                                    <img src="~@/assets/test.svg" alt="試験" title="試験" class="icon" @click="screenTransition(props)"/>
                                </template>
                            </span>
                        </template>
                    </VueGoodTable>
                </div>
            </div>
            <!-- フッタ -->
            <div id="footer">
                <address>Copyright © National Institute of Advanced Industrial Science and Technology （AIST）</address>
            </div>
        </div>
    </div>
</div>
</template>

<script>
import SubMenu from './SubMenu.vue';
import { subMenuMixin } from "../mixins/subMenuMixin";
import { urlParameterMixin } from '../mixins/urlParameterMixin';
import { AccountControlMixin } from '../mixins/AccountControlMixin';
import { csrfMixin } from '../mixins/csrfMixin';
import 'vue-good-table/dist/vue-good-table.css';
import mlcCreate from './MLComponentCreate';
import { VueGoodTable } from 'vue-good-table';

export default {
    mixins: [subMenuMixin, urlParameterMixin, AccountControlMixin, csrfMixin],
    data() {
        return {
            mlComponents: null,
            languagedata: null,
            key: 0,
            columns: [{
                //ヘッダーとなるlabelはメソッドから取得
                label: this.setTableLanguage("mlc_name"),
                field: "mlc_name",
                thClass: 'th1',
                width: "20%",
            },
                {
                    label: this.setTableLanguage("description"),
                    field: "description",
                    thClass: 'th2',
                    width: "30%",
                },
                {
                    label: this.setTableLanguage("domain"),
                    field: "domain",
                    thClass: 'th3',
                    width: "10%",
                },
                {
                    label: this.setTableLanguage("guideline_name"),
                    field: "guideline_name",
                    thClass: 'th5',
                    width: "20%",
                },
                {
                    label: this.setTableLanguage("scope_name"),
                    field: "scope_name",
                    thClass: 'th6',
                    width: "12%",
                },
                {
                    label: this.setTableLanguage("edit_options"),
                    field: "edit_options",
                    thClass: 'th7',
                    width: "5%",
                    sortable: false,
                },
                {
                    label: "Test",
                    field: "test",
                    thClass: 'th8',
                    width: "5%",
                    sortable: false,
                },
            ],
            rows: [],
            // ボタンが押されたらtrueにするフラグ
            del_exe_flag: false,
            edit_exe_flag: false,
            edit_key: 0
        }
    },
    mounted: function () {
        this.organizationIdCheck_method();
        this.organizationIdCheck = sessionStorage.getItem('organizationId');
        this.getMLComponents();
    },
    components: {
        SubMenu,
        VueGoodTable,
        mlcCreate,
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
                    case 'mlc_name':
                        return this.languagedata.ja.mlComponents.mlComponentsName;
                    case 'description':
                        return this.languagedata.ja.mlComponents.description;
                    case 'domain':
                        return this.languagedata.ja.mlComponents.domain;
                    case 'guideline_name':
                        return this.languagedata.ja.mlComponents.guidelineName;
                    case 'scope_name':
                        return this.languagedata.ja.mlComponents.scopeName;
                    case 'edit_options':
                        return this.languagedata.ja.mlComponents.editOptions;
                    default:
                }
            } else if (this.$i18n.locale == 'en') {
                switch (fieldName) {
                    case 'mlc_name':
                        return this.languagedata.en.mlComponents.mlComponentsName;
                    case 'description':
                        return this.languagedata.en.mlComponents.description;
                    case 'domain':
                        return this.languagedata.en.mlComponents.domain;
                    case 'guideline_name':
                        return this.languagedata.en.mlComponents.guidelineName;
                    case 'scope_name':
                        return this.languagedata.en.mlComponents.scopeName;
                    case 'edit_options':
                        return this.languagedata.en.mlComponents.editOptions;
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
        MLComponentCreate() {
            this.$router.push({
                name: 'MLComponentCreate'
            })
        },
        getMLComponents() {
            this.$axios.get(this.$backendURL + '/' + this.organizationIdCheck + '/mlComponents', {})
                .then((response) => {
                    this.mlComponents = response.data.MLComponents;
                    for (var mlc in this.mlComponents) {
                        this.rows.push({
                            id: this.mlComponents[mlc].Id,
                            mlc_name: this.mlComponents[mlc].Name,
                            description: this.mlComponents[mlc].Description,
                            domain: this.mlComponents[mlc].ProblemDomain,
                            guideline_name: this.mlComponents[mlc].GuidelineName,
                            scope_name: this.mlComponents[mlc].ScopeName,
                            scope_id: this.mlComponents[mlc].ScopeId,
                            guideline_reason: this.mlComponents[mlc].GuidelineReason,
                            scope_reason: this.mlComponents[mlc].ScopeReason,
                        })
                    }
                })
                .catch((error) => {
                    this.$router.push({
                        name: 'Information',
                        params: {
                            error
                        }
                    }).catch(error => {
                        // eslint-disable-next-line no-console
                        console.log(error)
                    })
                });
        },
        addMLComponents() {
            this.rows = [];
            this.getMLComponents();
        },
        modalReset() {
            this.key = this.key ? 0 : 1;
            this.edit_key = this.edit_key ? 0 : 1;
        },
        onRowClick(params) {
            if (params.event.target.parentElement.parentElement.tagName.includes("TBODY")){
                params.event.target.parentElement.classList.toggle("expanded");
            }else{
                params.event.target.parentElement.parentElement.classList.toggle("expanded");
            }
            // ボタンフラグをfalseに戻す
            this.del_exe_flag = false;
            this.edit_exe_flag = false;
        },
        screenTransition(params) {
            let mlComponentId = params.row.id;
            let scopeId = params.row.scope_id
            sessionStorage.setItem('mlComponentId', mlComponentId);
            sessionStorage.setItem('scopeId', scopeId);
            this.$router.push({
                name: 'TestDescriptions'
            });
            this.del_exe_flag = false;
            this.edit_exe_flag = false;
        },
        editMlComponent(params) {
            this.edit_exe_flag = true;
            this.$refs.mlcc.editShow(params.row.id,
                                 params.row.mlc_name,
                                 params.row.description,
                                 params.row.domain,
                                 params.row.guideline_name,
                                 params.row.scope_name,
                                 params.row.guideline_reason,
                                 params.row.scope_reason);
        },
        deleteMlComponent(params) {
            this.del_exe_flag = true;
            if (confirm(this.$t("confirm.delete"))) {
                const url = this.$backendURL +
                    '/' +
                    this.organizationIdCheck +
                    '/mlComponentsFront/' +
                    params.row.id
                //リクエスト時のオプションの定義
                const config = {
                    headers:{
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRF-TOKEN' : this.getCookie("csrf_access_token")
                    },
                    withCredentials:true,
                }
                this.$axios.delete(url, config)
                    .then((response) => {
                        this.result = response.data;
                        window.location.reload()
                    })
                    .catch((error) => {
                        this.$router.push({
                            name: 'Information',
                            params: {error}
                        })
                    })
            }
        },
    }
}
</script>

<style scoped>
/*---------------
表
----------------*/

#table>>>.vgt-input, .vgt-select {
    width: 100% !important;
    float: left;
}
#table>>>.vgt-inner-wrap .vgt-global-search {
    background: unset;
    border: unset;
    padding: unset;
    margin: unset;
}
#table {
    height: 90%;
    z-index: 10;
    background-color: #f0f0f0;
}

#table>>>.vgt-inner-wrap {
    border-radius: unset;
    box-shadow: unset;
    background: none;
}

#table>>>.vgt-table {
    text-align: center;
    border-collapse: separate;
    border-spacing: 0 5px;
    background-color: unset;
    border: none;
    width: 100%;
}

.vgt-wrap>>>.vgt-wrap__footer {
    padding: 0.5rem;
    border: none;
    background: unset;
}

#table>>>.vgt-fixed-header .vgt-table {
    position: absolute !important;
    z-index: 10 !important;
    width: 100% !important;
    overflow-x: auto !important;
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


/*---------------
	メイン
	----------------*/
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

.btnArea{
    width: 50%;
    float: right;
}
</style>
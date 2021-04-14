<template>
<div>
    <!--ヘッダータイトル-->
    <header id="head">
        <div id="title">
            <h1 class="head_title">{{$t("common.title")}}</h1>
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
        <ul id=" submenu_body">
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
                <div class="btn">
                    <mlcCreate :key="key" @createMLC="addMLComponents" @reset="modalReset"></mlcCreate>
                </div>
                <!--表-->
                <div id="table" align="center">
                    <VueGoodTable ref="mlTable" :columns="columns" styleClass="vgt-table" :rows="rows" max-height="350px" :fixed-header="true" align="center" :search-options="{enabled: true}" @on-row-click="onRowClick" >
                        <template slot="table-row" slot-scope="props">
                            <!--EditOptions-->
                            <span v-if="props.column.field == 'edit_options'">
                                <template v-if="$i18n.locale === 'en'">
                                    <img src="~@/assets/delete.svg" alt="delete" title="delete" class="icon" @click="deleteMlComponent(props)"/>
                                </template>
                                <template v-else>
                                    <img src="~@/assets/delete.svg" alt="削除" title="削除" class="icon" @click="deleteMlComponent(props)"/>
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
import {
    urlParameterMixin
} from '../mixins/urlParameterMixin';
import 'vue-good-table/dist/vue-good-table.css';
import mlcCreate from './MLComponentCreate';
import {
    VueGoodTable
} from 'vue-good-table';

export default {
    mixins: [urlParameterMixin],
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
                    width: "25%",
                },
                {
                    label: this.setTableLanguage("description"),
                    field: "description",
                    thClass: 'th2',
                    width: "25%",
                },
                {
                    label: this.setTableLanguage("domain"),
                    field: "domain",
                    thClass: 'th3',
                    width: "13%",
                },
                {
                    label: this.setTableLanguage("mlf_name"),
                    field: "mlf_name",
                    thClass: 'th4',
                    width: "25%",
                },
                {
                    label: this.setTableLanguage("edit_options"),
                    field: "edit_options",
                    thClass: 'th5',
                    width: "7%",
                    sortable: false,
                },
            ],
            rows: [],
            // 削除ボタンが押されたらtrueにするフラグ
            del_exe_flag: false
        }
    },
    mounted: function () {
        this.organizationIdCheck();
        this.organizationIdCheck = sessionStorage.getItem('organizationId');
        this.getMLComponents();
    },
    components: {
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
                    case 'mlf_name':
                        return this.languagedata.ja.mlComponents.mlFrameworkName;
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
                    case 'mlf_name':
                        return this.languagedata.en.mlComponents.mlFrameworkName;
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
                            mlf_name: this.mlComponents[mlc].MLFrameworkName,
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
        },
        onRowClick(params) {
            if (this.del_exe_flag == false) {
                // 削除ボタンが押されていない場合は通常の画面遷移
                this.screenTransion(params.row.id);
            }
            // 削除ボタンフラグをfalseに戻す
            this.del_exe_flag = false;
        },
        screenTransion(mlComponentId) {
            sessionStorage.setItem('mlComponentId', mlComponentId);
            this.$router.push({
                name: 'TestDescriptions'
            });
        },
        deleteMlComponent(params) {
            this.del_exe_flag = true;
            if (confirm(this.$t("confirm.delete"))) {
                const url = this.$backendURL +
                    '/' +
                    this.organizationIdCheck +
                    '/mlComponents/' +
                    params.row.id
                this.$axios.delete(url)
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
        }
    }
}
</script>

<style scoped>
/*---------------
表
----------------*/
#table>>>#search_table table tr:hover {
    background-color: rgb(233, 233, 233) !important;
}

#table>>>.vgt-input,
.vgt-select {
    width: 45% !important;
}

#table>>>.vgt-global-search {
    padding: 5px 2px !important;
    border: 1px solid #f0f0f0 !important;
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
    padding: .32em .0em .32em .68em !important;
    text-align: center !important;
}

#table>>>.vgt-table th.sortable:after,
#table>>>.vgt-table th.sortable::before {
    right: 0px !important;
}

#table>>>table.vgt-table {
    font-size: 16px !important;
    max-width: 880px !important;
    max-width: 1000px !important;
}

#table>>>table.vgt-table td {
    vertical-align: middle !important;
}

#table>>>.vgt-left-align {
    text-align: left !important;
    vertical-align: middle !important;
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
    position: relative;
    z-index: 0;
}

#search_table {
    margin-left: auto;
    margin-right: auto;
    margin-top: -17px;
    text-align: center;
    width: 905px;
}

.btn {
    text-align: right;
    padding: 10px 0px 5px;
}

#openModal {
    position: relative;
    top: 48px;
    right: 24px;
    z-index: 1;
}
</style>

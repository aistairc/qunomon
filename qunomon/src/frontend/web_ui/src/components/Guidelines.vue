<template>
    <div>
        <!--ヘッダータイトル-->
        <header id="head" :class="{ active: isActive }">
            <div id="title">
                <button @click="toggleSubmenu(isActive)" class="qq"><img :src="this.isActive ? this.icon2 : this.icon1" alt="Image" width="30" height="auto"></button>
                <h1 class="head_title">{{$t("common.titleGuidelines")}}</h1>
            </div>
        </header>
        <!-- サブメニュー（左カラム） -->

        <SubMenu :isActive="this.isActive">
            <!--SubMenuのアイコンとメニューの間の言語項目は各コンポーネントで実施-->
            <!--言語ボタン■-->
            <div id="btn_language">
                <template v-if="$i18n.locale === 'en'">
                    <a href="#" v-on:click.prevent="changeLanguage('ja', screenName)" class="btn_unselect">{{$t("common.lanJa")}}</a>
                    <a href="#" class="btn_select">{{$t("common.lanEn")}}</a>
                </template>
                <template v-else>
                    <a href="#" class="btn_select">{{$t("common.lanJa")}}</a>
                    <a href="#" v-on:click.prevent="changeLanguage('en', screenName)" class="btn_unselect">{{$t("common.lanEn")}}</a>
                </template>
            </div>
        </SubMenu>

        <!-- ニュース（中央カラム） -->
        <div id="main" :class="{ active: isActive }">
            <div id="main_body">
                <div id="search_table">
                    <div class="btnArea">
                        <div class="search_table_option">
                            <template v-if="$i18n.locale === 'en'">
                                <button type="button" value="Guideline Install" @click="installGuideline" v-bind:class="{'un_btn' : !aithub_linkage_mode}">Guideline Install</button>
                                <button type="button" value="Guideline Create" @click="guidelineCreate">Guideline Create</button>
                            </template>
                            <template v-else>
                                <button type="button" value="ガイドライン インストール" @click="installGuideline" v-bind:class="{'un_btn' : !aithub_linkage_mode}">ガイドライン インストール</button>
                                <button type="button" value="ガイドライン作成" @click="guidelineCreate">ガイドライン作成</button>
                            </template>
                        </div>
                    </div>
                    <!--表-->
                    <div id="table" align="center">
                        <VueGoodTable
                            ref="mlTable"
                            :columns="guideline_columns"
                            :rows="guideline_rows"
                            :fixed-header="false"
                            styleClass="vgt-table"
                            max-height="700px"
                            align="center"
                            :search-options="{enabled: true}"
                            :pagination-options="{enabled: true, mode: 'pages'}"
                            @on-row-click="onRowClick"
                        >
                            <template slot="table-row" slot-scope="props">
                                <template v-if="props.column.field == 'guideline_display_id'">
                                    <input type="radio" v-bind:value="props.row.guideline_display_id" name="radio" v-model="selected_guideline"/>
                                </template>
                                <template v-else-if="props.column.field == 'install'">
                                    <template v-if="props.row.install == true">
                                        <span>{{$t("guidelines.installed")}}</span>
                                        &nbsp;
                                        <img src="~@/assets/delete.svg" alt="delete" title="delete" class="icon" @click="deleteGuideline(props)">
                                    </template>
                                    <template v-else>
                                        <span>&nbsp;</span>
                                    </template>
                                </template>
                                <template v-else-if="props.column.field == 'aithub_status'">
                                    <template v-if="props.row.aithub_delete_flag == true">
                                        <span>{{$t("guidelines.aithub_deleted")}}</span>
                                    </template>
                                </template>
                                <template v-else-if="props.column.field == 'detail'">
                                <span v-if="$i18n.locale === 'en'">
                                    <img src="~@/assets/google_icon_detail.svg" alt="detail" title="detail" class="icon" @click="guidelineDetail(props)"/>
                                </span>
                                    <span v-else>
                                    <img src="~@/assets/google_icon_detail.svg" alt="詳細" title="詳細" class="icon" @click="guidelineDetail(props)"/>
                                </span>
                                </template>
                            </template>
                        </VueGoodTable>
                    </div>

                    <!-- button -->
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
import { GuidelinesMixin } from '../mixins/GuidelinesMixin';
import 'vue-good-table/dist/vue-good-table.css';
import { VueGoodTable } from 'vue-good-table';


export default {
    mixins: [subMenuMixin, urlParameterMixin, GuidelinesMixin, AccountControlMixin],
    data() {
        return {
            guideline_columns: [
                {
                    label: this.setGuidelinesTableLanguage("guideline_display_id"),
                    field: "guideline_display_id",
                    thClass: 'th1',
                    width: "4%",
                    sortable: false,
                },
                {
                    label: this.setGuidelinesTableLanguage("guideline_name"),
                    field: "guideline_name",
                    thClass: 'th2',
                    width: "10%",
                },
                {
                    label: this.setGuidelinesTableLanguage("description"),
                    field: "description",
                    thClass: 'th3',
                    width: "15%",
                },
                {
                    label: this.setGuidelinesTableLanguage("creator"),
                    field: "creator",
                    thClass: 'th4',
                    width: "10%",
                },
                {
                    label: this.setGuidelinesTableLanguage("publisher"),
                    field: "publisher",
                    thClass: 'th5',
                    width: "7%",
                },
                {
                    label: this.setGuidelinesTableLanguage("identifier"),
                    field: "identifier",
                    thClass: 'th6',
                    width: "15%",
                },
                {
                    label: this.setGuidelinesTableLanguage("install"),
                    field: "install",
                    thClass: 'th7',
                    width: "8%",
                    sortable: false,
                },
                {
                    label: this.setGuidelinesTableLanguage("aithub_status"),
                    field: "aithub_status",
                    thClass: 'th8',
                    width: "5%",
                    sortable: false,
                },
                {
                    label: this.setGuidelinesTableLanguage("detail"),
                    field: "detail",
                    thClass: 'th8',
                    width: "8%",
                    sortable: false,
                }
            ],
            guideline_rows: [],
            selected_row: null,
            selected_guideline: '',
            screenName: 'guidelines'
        }
    },
    mounted: async function () {
        await this.setAITHubLinkageMode();
        if (sessionStorage.getItem('aithub_linkage_mode') == '1') {
            await this.getGuidelineListFromAIThub();
            await this.getGuidelineListFromLocal();
            await this.setGuidelineRows_AITHubLinkageMode()
        } else {
            await this.getGuidelineListFromLocal();
            await this.setGuidelineRows_LocalMode();
        }
    },
    components: {
        SubMenu,
        VueGoodTable
    },
    methods: {
        //テーブルのヘッダーにタイトルを設定。
        //現在の選択言語がjaなら日本語のテーブルを、enなら英語のテーブルを設定。
        setGuidelinesTableLanguage(fieldName) {
            // mountよりも先に呼び出されるので、ここで言語設定を呼び出す。
            this.setLanguageData();
            this.languagedata = require('./languages/languages.json');
            if (this.$i18n.locale == 'ja') {
                switch (fieldName) {
                    case 'guideline_name':
                        return this.languagedata.ja.guidelines.guideline_name;
                    case 'description':
                        return this.languagedata.ja.guidelines.description;
                    case 'creator':
                        return this.languagedata.ja.guidelines.creator;
                    case 'publisher':
                        return this.languagedata.ja.guidelines.publisher;
                    case 'identifier':
                        return this.languagedata.ja.guidelines.identifier;
                    case 'install':
                        return this.languagedata.ja.guidelines.install;
                    case 'aithub_status':
                        return this.languagedata.ja.guidelines.aithub_status;
                    case 'detail':
                        return this.languagedata.ja.guidelines.detail;
                    default:
                }
            } else if (this.$i18n.locale == 'en') {
                switch (fieldName) {
                    case 'guideline_name':
                        return this.languagedata.en.guidelines.guideline_name;
                    case 'description':
                        return this.languagedata.en.guidelines.description;
                    case 'creator':
                        return this.languagedata.en.guidelines.creator;
                    case 'publisher':
                        return this.languagedata.en.guidelines.publisher;
                    case 'identifier':
                        return this.languagedata.en.guidelines.identifier;
                    case 'install':
                        return this.languagedata.en.guidelines.install;
                    case 'aithub_status':
                        return this.languagedata.en.guidelines.aithub_status;
                    case 'detail':
                        return this.languagedata.en.guidelines.detail;
                    default:
                }
            }
        },
        onRowClick(event){
            this.selected_row = event.row;
            this.selected_guideline = event.row.guideline_display_id;
            if (event.event.target.parentElement.parentElement.tagName.includes("TBODY")){
                event.event.target.parentElement.classList.toggle("expanded");
            }else{
                event.event.target.parentElement.parentElement.classList.toggle("expanded");
            }
        },
        installGuideline(){
            // 選択AITのエラーチェック
            if (this.selected_guideline.length == 0) {
                alert(this.$t("guidelines.guidelineUnselectedError"));
                return;
            }

            // インストール済みのエラーチェック
            if (this.selected_row.install == true) {
                alert(this.$t("guidelines.installedGuidelineError"));
                return;
            }

            // インストール実行
            if (confirm(this.$t("confirm.guidelineInstall"))) {
                this.installGuidelineCore(this.selected_row.guideline_aithub_id);
            }

        },
        guidelineDetail(param){
            this.selected_row = param.row;
            sessionStorage.setItem('guideline', JSON.stringify(this.selected_row));
            this.$router.push({
                name: 'GuidelineDetail'
            })
        },
        guidelineCreate(){
            this.$router.push({
                name: 'GuidelineCreate'
            })
        },
        deleteGuideline(params){
            if (confirm(this.$t("confirm.guidelineUninstall"))) {
                this.deleteGuidelineCore(params);
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
/*}*/
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
    padding-top: 2rem;
    margin: 0 auto;
    text-align: center;
    width: 90%;
}

.tittle {
    margin: 0 auto;
    font-size: 2rem;
    width: 90%;
    padding-top: 2rem;
    /*background: red;*/
}

.btnArea {
    width: 50%;
    float: right;
}
.search_table_option {
    display: flex;
    float: right;
}
.search_table_option button {
    background-color: #a9c7aa;
    color: black;
    float: right;
    border: none;
    height: 2rem;
    width: 10rem;
    margin-left: 1rem;
    text-align: center;
    text-decoration: none;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    border-radius: 5px;
    z-index: 10;
    &:hover {
        background: #43645b !important;
        color: white;
    }
    &.un_btn{
        background: silver;
        pointer-events: none;
    }
}
.btn_inline_left {
    float:left;
}

.btn_inline_right {
    float:left;
    margin-left: 50px;
}

.btn_create {
    float:right;
    margin-top: 10px;
}

</style>

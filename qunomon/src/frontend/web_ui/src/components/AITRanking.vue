<template>
<div>
    <!--ヘッダータイトル-->
    <header id="head">
        <div id="title" :class="{ active: this.isActive }">
            <button @click="toggleSubmenu(isActive)" class="qq"><img :src="this.isActive  ? this.icon2 : this.icon1" alt="Image" width="30" height="auto"></button>
            <h1 class="head_title">{{$t("common.titleAITRanking")}}</h1>
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
    <div id="main" :class="{ active: this.isActive  }">
        <div id="main_body">
            <div id="search_table">
                <div id="table" align="center">
                    <VueGoodTable 
                        ref="aitRankingListTable" 
                        :columns="aitRanking_columns" 
                        :rows="aitRows" 
                        :fixed-header="true"
                        max-height="43.75rem"
                        align="center"
                        :search-options="{ enabled: true }"
                        :pagination-options="{enabled: true, mode: 'pages'}"
                        @on-row-click="onRowClick"
                    >
                        <template slot="table-row" slot-scope="props">
                            <!--EditOptions-->

                            <template v-if="props.column.field == 'installed'">
                                <span v-if="props.row.install == true">
                                    <img src="~@/assets/AITSearch_complete_icon.svg" alt="complete" title="complete" class="icon"/>
                                </span>
                                <span v-else>
                                    <img src="~@/assets/AITSearch_incomplete_icon.svg" alt="not" title="not yet" class="icon"/>
                                </span>
                            </template>
                            <template v-else-if="props.column.field == 'install'">
                                <span v-if="$i18n.locale === 'en'">
                                    <img src="~@/assets/AITSearch_install_icon.svg" alt="install" title="install" class="icon" @click="aitInstall(props)"/>
                                </span>
                                <span v-else>
                                    <img src="~@/assets/AITSearch_install_icon.svg" alt="インストール" title="インストール" class="icon" @click="aitInstall(props)"/>
                                </span>
                            </template>
                            <template v-else-if="props.column.field == 'detail'">
                                <span v-if="$i18n.locale === 'en'">
                                    <img src="~@/assets/google_icon_detail.svg" alt="detail" title="detail" class="icon" @click="aitDetail(props)"/>
                                </span>
                                <span v-else>
                                    <img src="~@/assets/google_icon_detail.svg" alt="詳細" title="詳細" class="icon" @click="aitDetail(props)"/>
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
import { AITHubMixin } from '../mixins/AITHubMixin';
import { AccountControlMixin } from '../mixins/AccountControlMixin';
import 'vue-good-table/dist/vue-good-table.css';
import { VueGoodTable } from 'vue-good-table';

export default {
    mixins: [subMenuMixin, urlParameterMixin, AITHubMixin, AccountControlMixin],
    data() {
        return {
            aitRanking_columns: [
                {
                    label: this.setAITRankingTableLanguage("ait_name"),
                    field: "ait_name",
                    thClass: "th1",
                    width: "15%",
                },
                {
                    label: this.setAITRankingTableLanguage("description"),
                    field: "description",
                    thClass: "th2",
                    width: "20%",
                },
                {
                    label: this.setAITRankingTableLanguage("create_user_account"),
                    field: "create_user_account",
                    thClass: "th3",
                    width: "12%",
                },
                {
                    label: this.setAITRankingTableLanguage("create_user_name"),
                    field: "create_user_name",
                    thClass: "th4",
                    width: "12%",
                },
                {
                    label: this.setAITRankingTableLanguage("downloads"),
                    field: "downloads",
                    thClass: "th5",
                    width: "5%",
                },
                {
                    label: this.setAITRankingTableLanguage("views"),
                    field: "views",
                    thClass: "th6",
                    width: "5%",
                },
                {
                    label: this.setAITRankingTableLanguage("installed"),
                    field: "installed",
                    thClass: "th7",
                    width: "5%",
                },
                {
                    label: this.setAITRankingTableLanguage("install"),
                    field: "install",
                    thClass: "th8",
                    width: "5%",
                },
                {
                    label: this.setAITRankingTableLanguage("detail"),
                    field: "detail",
                    thClass: "th9",
                    width: "5%",
                    sortable: false,
                }
            ],
            selected_ait: '',
            selected_row: null,
            aitRows: [],
            screenName: 'aitRanking'
            
        }
    },
    mounted: async function () {
        await this.getAITListFromLocal(this.screenName);
        this.aitList_local = JSON.parse(sessionStorage.getItem('aitList_local'));
    },
    components: {
        SubMenu,
        VueGoodTable
    },
    methods: {
        //テーブルのヘッダーにタイトルを設定。
        //現在の選択言語がjaなら日本語のテーブルを、enなら英語のテーブルを設定。
        setAITRankingTableLanguage(fieldName) {
            // mountよりも先に呼び出されるので、ここで言語設定を呼び出す。
            this.setLanguageData()
            this.languagedata = require('./languages/languages.json');
            if (this.$i18n.locale == 'ja') {
                switch (fieldName) {
                    case 'ait_name':
                        return this.languagedata.ja.aitRanking.ait_name;
                    case 'description':
                        return this.languagedata.ja.aitRanking.description;
                    case 'create_user_account':
                        return this.languagedata.ja.aitRanking.create_user_account;
                    case 'create_user_name':
                        return this.languagedata.ja.aitRanking.create_user_name;
                    case 'downloads':
                        return this.languagedata.ja.aitRanking.downloads;
                    case 'views':
                        return this.languagedata.ja.aitRanking.views;
                    case 'installed':
                        return this.languagedata.ja.aitRanking.installed;
                    case 'install':
                        return this.languagedata.ja.aitRanking.install;
                    case 'detail':
                        return this.languagedata.ja.aitRanking.detail;
                    default:
                }
            } else if (this.$i18n.locale == 'en') {
                switch (fieldName) {
                    case 'ait_name':
                        return this.languagedata.en.aitRanking.ait_name;
                    case 'description':
                        return this.languagedata.en.aitRanking.description;
                    case 'create_user_account':
                        return this.languagedata.en.aitRanking.create_user_account;
                    case 'create_user_name':
                        return this.languagedata.en.aitRanking.create_user_name;
                    case 'downloads':
                        return this.languagedata.en.aitRanking.downloads;
                    case 'views':
                        return this.languagedata.en.aitRanking.views;
                    case 'installed':
                        return this.languagedata.en.aitRanking.installed;
                    case 'install':
                        return this.languagedata.en.aitRanking.install;
                    case 'detail':
                        return this.languagedata.en.aitRanking.detail;
                    default:
                }
            }
        },
        onRowClick(e){
            this.selected_ait = e.row.ait_id;
            this.selected_row = e.row;
            if (e.event.target.parentElement.parentElement.tagName.includes("TBODY")){
                e.event.target.parentElement.classList.toggle("expanded");
            } else {
                e.event.target.parentElement.parentElement.classList.toggle("expanded");
            }
        },
        aitInstall(params){
            // 選択AITのエラーチェック
            this.selected_ait = params.row.ait_id;
            this.selected_row = params.row;

            // インストール済みのエラーチェック
            if (this.selected_row.install == true) {
                alert(this.$t("aitRanking.installedAITError"));
                return;
            }

             // インストール実行
            if (confirm(this.$t("confirm.aitInstall"))) {
                this.aitInstallCore(this.selected_ait, 
                                    this.selected_row.create_user_account,
                                    this.selected_row.create_user_name);
            }
        },
        aitDetail(params){
            sessionStorage.setItem('aithub_id', params.row.ait_id);
            sessionStorage.setItem('beforeScreenName', this.screenName);
            sessionStorage.setItem('ait_local_installed_flag', params.row.install);

            this.$router.push({
                name: 'AITDetail'
            })
        }
    }
}
</script>


<style scoped>
/*---------------
表
----------------*/
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
#table>>>.vgt-input, .vgt-select {
    width: 100% !important;
    float: left;
}

#table>>>.vgt-inner-wrap .vgt-global-search{
    background: unset;
    border: unset;
    padding: unset;
    margin: unset;
    width: 50%;
    float: left;
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

#table>>>.vgt-table td {
    padding: unset;
    height: 2rem;
    vertical-align: middle;
}

#table>>>.vgt-table tbody tr td:nth-child(1) {
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

#table>>>.vgt-table .expanded td, th {
    white-space: normal;
    overflow: visible;
    text-overflow: unset;
    max-width: 10%;
}
</style>
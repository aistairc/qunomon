<template>
    <div>
        <!--ヘッダータイトル-->
        <header id="head" :class="{ active: this.isActive }">
            <div id="title">
                <button @click="toggleSubmenu(isActive)" class="qq"><img :src="this.isActive  ? this.icon2 : this.icon1" alt="Image" width="30" height="auto"></button>
                <h1 class="head_title">{{$t("common.titleAITDashboard")}}</h1>
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
                    <div class="btnArea">
                        <div class="search_table_option">
                            <template v-if="$i18n.locale === 'en'">
                                <button type="button" @click="aitUninstall">AIT Uninstall</button>
                                <template v-if="aithub_linkage_mode">
                                    <button type="button" @click="aitSearch">AIT Search</button>
                                </template>
                            </template>
                            <template v-else>
                                <button type="button" @click="aitUninstall">AITアンインストール</button>                        
                                <template v-if="aithub_linkage_mode">
                                    <button type="button" @click="aitSearch">AIT検索</button>
                                </template>
                            </template>
                        </div>
                    </div>
                    <!--表-->
                    <div id="table">
                        <vue-good-table
                            ref="aitDashboardTable"
                            :columns="aitDashboard_columns"
                            :rows="aitDashboard_rows"
                            :fixed-header="true"
                            max-height="700px"
                            align="center"
                            :search-options="{ enabled: true }"
                            :select-options="{ enabled: true, disableSelectInfo: true}"
                            :pagination-options="{enabled: true, mode: 'pages'}"
                            v-on:row-click="onRowClick"
                        >
                            <template v-slot:table-row="props">
                                <template v-if="props.column.field == 'using_TD'">
                                <span class="using_TD_True" v-if="props.row.using_TD == true">
                                    {{$t("aitDashboard.using_TD_True")}}
                                </span>
                                    <span v-else>
                                    {{$t("aitDashboard.using_TD_False")}}
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
                        </vue-good-table>
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
import { AITHubMixin } from '../mixins/AITHubMixin';
import { AccountControlMixin } from '../mixins/AccountControlMixin';
import { csrfMixin } from '../mixins/csrfMixin';
import 'vue-good-table-next/dist/vue-good-table-next.css';
import { VueGoodTable } from 'vue-good-table-next';

export default {
    mixins: [subMenuMixin, urlParameterMixin, AITHubMixin, AccountControlMixin, csrfMixin],
    data() {
        return {
            aitDashboard_columns: [
                {
                    //ヘッダーとなるlabelはメソッドから取得
                    label: this.setAITDashboardTableLanguage("ait_name"),
                    field: "ait_name",
                    thClass: "th2",
                    width: "20%",
                },
                {
                    label: this.setAITDashboardTableLanguage("description"),
                    field: "description",
                    thClass: "th3",
                    width: "35%",
                },
                {
                    label: this.setAITDashboardTableLanguage("create_user_account"),
                    field: "create_user_account",
                    thClass: "th4",
                    width: "20%",
                },
                {
                    label: this.setAITDashboardTableLanguage("using_TD"),
                    field: "using_TD",
                    thClass: "th5",
                    width: "15%",
                },
                {
                    label: this.setAITDashboardTableLanguage("detail"),
                    field: "detail",
                    thClass: "th6",
                    width: "8%",
                    sortable: false,
                }
            ],
            aitDashboard_rows: [],
            usingTDList: [],
            deleteList: [],
            screenName: 'aitDashboard'
        }
    },
    mounted: function () {
        this.setAITHubLinkageMode();
        this.getAITListFromLocal(this.screenName);

    },
    components: {
        SubMenu,
        VueGoodTable
    },
    methods: {
        //テーブルのヘッダーにタイトルを設定。
        //現在の選択言語がjaなら日本語のテーブルを、enなら英語のテーブルを設定。
        setAITDashboardTableLanguage(fieldName) {
            // mountよりも先に呼び出されるので、ここで言語設定を呼び出す。
            this.setLanguageData()
            this.languagedata = require('./languages/languages.json');
            if (this.$i18n.locale == 'ja') {
                switch (fieldName) {
                    case 'ait_name':
                        return this.languagedata.ja.aitDashboard.ait_name;
                    case 'description':
                        return this.languagedata.ja.aitDashboard.description;
                    case 'create_user_account':
                        return this.languagedata.ja.aitDashboard.create_user_account;
                    case 'using_TD':
                        return this.languagedata.ja.aitDashboard.using_TD;
                    case 'detail':
                        return this.languagedata.ja.aitDashboard.detail;
                    default:
                }
            } else if (this.$i18n.locale == 'en') {
                switch (fieldName) {
                    case 'ait_name':
                        return this.languagedata.en.aitDashboard.ait_name;
                    case 'description':
                        return this.languagedata.en.aitDashboard.description;
                    case 'create_user_account':
                        return this.languagedata.en.aitDashboard.create_user_account;
                    case 'using_TD':
                        return this.languagedata.en.aitDashboard.using_TD;
                    case 'detail':
                        return this.languagedata.en.aitDashboard.detail;
                    default:
                }
            }
        },
        aitUninstall(){
            var selectedRows = this.$refs['aitDashboardTable'].selectedRows;
            // 選択AITのエラーチェック
            if (selectedRows.length == 0) {
                alert(this.$t("aitDashboard.aitUnselectedError"));
                return;
            }

            // TD使用中のエラーチェック
            for (var row in selectedRows) {
                if(selectedRows[row].using_TD){
                    alert(this.$t("aitDashboard.usingTDError"));
                    return;
                }
            }

            // アンインストール実行
            if (confirm(this.$t("confirm.aitUninstall"))) {
                for (var i in selectedRows) {
                    var delete_ait_id = this.aitDashboard_rows[selectedRows[i].originalIndex].ait_id;
                    //リクエスト時のオプションの定義
                    const config = {
                        headers:{
                            'X-Requested-With': 'XMLHttpRequest',
                            'X-CSRF-TOKEN' : this.getCookie("csrf_access_token")
                        },
                        withCredentials:true,
                    }
                    this.$axios.delete(this.$backendURL + '/testRunnersFront' + '/' + delete_ait_id, config)
                        .then((response) => {
                            this.deleteList.push(response.data);
                            // 非同期処理の対応のため、ループの最後回のみ実行する
                            if (selectedRows.length == this.deleteList.length){
                                window.location.reload();
                            }
                        })
                        .catch((error) => {
                            this.$router.push({
                                name: 'Information',
                                query: {error: JSON.stringify({...error, response: error.response})}
                            })
                        });
                }
            }
        },
        aitSearch(){
            this.$router.push({
                name: 'AITSearch'
            })
        },
        aitDetail(params){
            sessionStorage.setItem('aithub_id', params.row.ait_id);
            sessionStorage.setItem('beforeScreenName', this.screenName);
            sessionStorage.setItem('ait_local_installed_flag', params.row.install);

            this.$router.push({
                name: 'AITDetail'
            })
        },
        onRowClick(event){
            if (event.event.target.parentElement.parentElement.tagName.includes("TBODY")){
                event.event.target.parentElement.classList.toggle("expanded");
            } else {
                event.event.target.parentElement.parentElement.classList.toggle("expanded");
            }
        },


    }
}
</script>

<style scoped>
/*---------------
表
----------------*/

#table :deep(.vgt-input, .vgt-select) {
    width: 100% !important;
    float: left;
}

#table :deep(.vgt-inner-wrap) .vgt-global-search{
    background: unset;
    border: unset;
    padding: unset;
    margin: unset;
}

#table {
    height: 90%;
    z-index: 10;
    background-color: var(--gray-thema);
}

#table :deep(.vgt-inner-wrap) {
    border-radius: unset;
    box-shadow: unset;
    background: none;
}
#table :deep(.vgt-table) {
    text-align: center;
    border-collapse: separate;
    border-spacing: 0 5px;
    background-color: unset;
    border: none;
    width: 100%;
}
.vgt-wrap :deep(.vgt-wrap__footer) {
    padding: 0.5rem;
    border: none;
    background: unset;
}

#table :deep(.vgt-fixed-header .vgt-table) {
    position: absolute !important;
    z-index: 10 !important;
    width: 100% !important;
    overflow-x: auto !important;
}
#table :deep(.vgt-table thead th) {
    color: white;
    background: var(--secondary-color);
    text-align: center;
    border: none;
    width: 1rem;
    height: 2.5rem;
    padding: unset;
    vertical-align: middle;
}
#table :deep(.vgt-table thead tr th:first-child) {
    border-top-left-radius: 5px;
}
#table :deep(.vgt-table thead tr th:last-child) {
    border-top-right-radius: 5px;
}
#table :deep(.vgt-table tbody) {
    font-size: 0.85rem;
}
#table :deep(.vgt-table tbody tr th) {
    background: none;
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
}
#table :deep(.vgt-table td) {
    padding: unset;
    height: 2rem;
    vertical-align: middle;
}

#table :deep(.vgt-table tbody tr td:nth-child(0)) {
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
}

#table :deep(.vgt-table tbody tr td:last-child) {

    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
}
#table :deep(.vgt-table tbody tr) {
    background-color: #fff; /* Set row background color */
    border: rgba(0, 0, 0, 0.2);
    box-shadow: 0 0 2px rgba(0, 0, 0, 0.1); /* Add a box shadow for depth */
    border-radius: 5px;
    height: 2rem;
    vertical-align: middle;
}

#table :deep(.vgt-table tbody) tr:hover{
    background: var(--primary-color-light) !important;
}


#table :deep(.vgt-checkbox-col) {
    width: 5% !important;
    border: none;
}
#table :deep(.vgt-table tr) td{
    border: none;
/* padding: 1rem; */
    text-align: center;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 140px;
}

#table :deep(.vgt-table .expanded td, th) {
    white-space: normal;
    overflow: visible;
    text-overflow: unset;
    max-width: 10%;
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
    /*margin-left: auto;*/
    /*margin-right: auto;*/
    /*margin-top: 10px;*/
    padding-top: 2rem;
    margin: 0 auto;
    text-align: center;
    width: 90%;
    /*background-color: red;*/
}



.btnArea{
    width: 50%;
    float: right;
}

.search_table_option {
    display: flex;
    float: right;
}
.search_table_option button {
    background-color: var(--primary-color-light);
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
        background-color: var(--primary-color);
        color: white;
    }
}

.using_TD_True {
    color: red;
}

.btn_inline_left {
    float:left;
}
.btn_inline_right {
    float:right;
    margin-right: 50px;
}
.btn_inline_right_2 {
    float:right;
    margin-right: 50px;
}

</style>
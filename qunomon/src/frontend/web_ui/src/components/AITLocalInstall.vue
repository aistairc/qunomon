<template>
    <div>
        <!--ヘッダータイトル-->
        <header id="head" :class="{ active: this.isActive }">
            <div id="title">
                <button @click="toggleSubmenu(isActive)" class="qq"><img :src="this.isActive ? this.icon2 : this.icon1" alt="Image" width="30" height="auto"></button>
                <h1 class="head_title">{{$t("common.titleAITLocalInstall")}}</h1>
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
        <div id="main" :class="{ active: this.isActive }">
            <div id="main_body">

                <div class="option-menu">
                    <div>
                        <label class="cardTitle">{{$t("aitLocalInstall.aitCreate")}}</label>
                        <table>
                            <tr>
                                <td>
                                    <label class="labelBtn" for="fileUpload">
                                        {{$t("aitLocalInstall.fileSelect")}}
                                        <input class="file_input" type="file" id="fileUpload" @change="fileSelected" />
                                    </label>
                                </td>
                                <td>
                                <span v-if="ait_file == null">
                                    {{$t("aitLocalInstall.fileUnselected")}}
                                </span>
                                    <span v-else>
                                    {{ait_file_name}}
                                </span>
                                </td>
                                <td>
                                    <template v-if="$i18n.locale === 'en'">
                                        <input type="button" value="AIT Create" class="uploadBTN"
                                               @click="aitCreate"/>
                                    </template>
                                    <template v-else>
                                        <input type="button" value="AIT登録" class="uploadBTN"
                                               @click="aitCreate"/>
                                    </template>
                                </td>
                            </tr>
                        </table>
                    </div>
                </div>

                <!--AIT一覧-->
                <div class="accordion">
                    <!--                <label>{{$t("aitLocalInstall.aitList")}}</label>-->
                    <div id="search_table">
                        <div id="table" align="center">
                            <vue-good-table
                                ref="aitListTable"
                                :columns="aitLocalInstall_columns"
                                :rows="aitLocalInstall_rows"
                                :fixed-header="true"
                                styleClass="vgt-table"
                                max-height="700px"
                                align="center"
                                :search-options="{enabled: true}"
                                :sort-options="{
                                    enabled: true,
                                    multipleColumns: true,
                                    initialSortBy: [
                                        {field: 'ait_name', type: 'asc'},
                                        {field: 'version', type: 'asc'}
                                    ]
                                }"
                                :pagination-options="{enabled: true, mode: 'pages'}"
                                v-on:row-click="onRowClick"
                            >
                                <template v-slot:table-row="props">
                                    <!--EditOptions-->
                                    <template v-if="props.column.field == 'status'">
                                        <span v-if="props.row.status == 'OK'">
                                            {{$t("aitLocalInstall.status_registered")}}
                                        </span>
                                            <span class="status_processing" v-else>
                                            {{$t("aitLocalInstall.status_processing")}}
                                        </span>
                                    </template>
                                    <template v-else-if="props.column.field == 'detail'">
                                        <router-link :to="{ name: 'AITDetail'}" class="icon">
                                            <template v-if="$i18n.locale === 'en'">
                                                <template v-if="props.row.status == 'OK'">
                                                    <img src="~@/assets/description.svg" alt="Detail" title="Detail" class="icon" @click="aitDetail(props)">
                                                </template>
                                            </template>
                                            <template v-else>
                                                <template v-if="props.row.status == 'OK'">
                                                    <img src="~@/assets/description.svg" alt="詳細" title="詳細" class="icon" @click="aitDetail(props)">
                                                </template>
                                            </template>
                                        </router-link>
                                    </template>
                                </template>
                            </vue-good-table>
                        </div>
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
import { AITLocalMixin } from '../mixins/AITLocalMixin';
import { AccountControlMixin } from '../mixins/AccountControlMixin';
import 'vue-good-table-next/dist/vue-good-table-next.css';
import { VueGoodTable } from 'vue-good-table-next';

export default {
    mixins: [subMenuMixin, AITLocalMixin, AccountControlMixin],
    data() {
        return {
            aitLocalInstall_columns: [
                {
                    label: this.setAITLocalInstallTableLanguage("ait_name"),
                    field: "ait_name",
                    thClass: "th2",
                    width: "20%",
                },
                {
                    label: this.setAITLocalInstallTableLanguage("description"),
                    field: "description",
                    thClass: "th3",
                    width: "20%",
                },
                {
                    label: this.setAITLocalInstallTableLanguage("version"),
                    field: "version",
                    thClass: "th4",
                    width: "10%",
                },
                {
                    label: this.setAITLocalInstallTableLanguage("create_user_account"),
                    field: "create_user_account",
                    thClass: "th5",
                    width: "20%",
                },
                {
                    label: this.setAITLocalInstallTableLanguage("create_user_name"),
                    field: "create_user_name",
                    thClass: "th6",
                    width: "10%",
                },
                {
                    label: this.setAITLocalInstallTableLanguage("status"),
                    field: "status",
                    thClass: "th7",
                    width: "10%",
                },
                {
                    label: this.setAITLocalInstallTableLanguage("detail"),
                    field: "detail",
                    thClass: "th8",
                    width: "10%",
                }
            ],
            selected_ait: '',
            selected_row: null,
            aitLocalInstall_rows: [],
            ait_file: null,
            ait_file_name: '',
            result: null,
            screenName: 'aitLocalInstall',
        }
    },
    mounted: function () {
        this.getAITLocalList();
    },
    components: {
        SubMenu,
        VueGoodTable
    },
    methods: {
        //テーブルのヘッダーにタイトルを設定。
        //現在の選択言語がjaなら日本語のテーブルを、enなら英語のテーブルを設定。
        setAITLocalInstallTableLanguage(fieldName) {
            // mountよりも先に呼び出されるので、ここで言語設定を呼び出す。
            this.setLanguageData()
            this.languagedata = require('./languages/languages.json');
            if (this.$i18n.locale == 'ja') {
                switch (fieldName) {
                    case 'ait_name':
                        return this.languagedata.ja.aitLocalInstall.ait_name;
                    case 'description':
                        return this.languagedata.ja.aitLocalInstall.description;
                    case 'version':
                        return this.languagedata.ja.aitLocalInstall.version;
                    case 'create_user_account':
                        return this.languagedata.ja.aitLocalInstall.create_user_account;
                    case 'create_user_name':
                        return this.languagedata.ja.aitLocalInstall.create_user_name;
                    case 'status':
                        return this.languagedata.ja.aitLocalInstall.status;
                    case 'detail':
                        return this.languagedata.ja.aitLocalInstall.detail;
                    default:
                }
            } else if (this.$i18n.locale == 'en') {
                switch (fieldName) {
                    case 'ait_name':
                        return this.languagedata.en.aitLocalInstall.ait_name;
                    case 'description':
                        return this.languagedata.en.aitLocalInstall.description;
                    case 'version':
                        return this.languagedata.en.aitLocalInstall.version;
                    case 'create_user_account':
                        return this.languagedata.en.aitLocalInstall.create_user_account;
                    case 'create_user_name':
                        return this.languagedata.en.aitLocalInstall.create_user_name;
                    case 'status':
                        return this.languagedata.en.aitLocalInstall.status;
                    case 'detail':
                        return this.languagedata.en.aitLocalInstall.detail;
                    default:
                }
            }
        },
        onRowClick(e){
            this.selected_ait = e.row.ait_id;
            this.selected_row = e.row;
            if (e.event.target.parentElement.parentElement.tagName.includes("TBODY")){
                e.event.target.parentElement.classList.toggle("expanded");
            }else{
                e.event.target.parentElement.parentElement.classList.toggle("expanded");
            }
        },
        fileSelected(e) {
            var selected_file = e.target.files[0];
            if (selected_file.name.indexOf('.zip') < 0) {
                this.ait_file = null;
                this.ait_file_name = '';
                alert(this.$t("aitLocalInstall.fileTypeError"));
                return;
            }

            this.ait_file = selected_file;
            this.ait_file_name = selected_file.name;
        },
        aitDetail(params) {
            sessionStorage.setItem('aithub_id', params.row.ait_id);
            sessionStorage.setItem('beforeScreenName', this.screenName);
            sessionStorage.setItem('ait_local_installed_flag', params.row.install);

            this.$router.push({
                name: 'AITDetail'
            })
        },
    }
}
</script>


<style scoped>
/*---------------
表
----------------*/
#table :deep(.vgt-input, .vgt-select) {
    width: 50% !important;
    float: left;

}
#table :deep(.vgt-inner-wrap .vgt-global-search) {
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
#table :deep(.vgt-table tbody tr) {
    background-color: #fff; /* Set row background color */
    border: rgba(0, 0, 0, 0.2);
    box-shadow: 0 0 2px rgba(0, 0, 0, 0.1); /* Add a box shadow for depth */
    border-radius: 5px;
    vertical-align: middle;
}
#table :deep(.vgt-table tbody tr td:nth-child(1)) {
    border-bottom-left-radius: 5px;
    border-top-left-radius: 5px;
}
#table :deep(.vgt-table tbody tr td:last-child) {
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
}

#table :deep(.vgt-table tbody) tr:hover{
    background: var(--primary-color-light) !important;
}
#table :deep(.vgt-table tr) td{
    border: none;
    text-align: center;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 140px;
    padding: unset;
    height: 2rem;
    vertical-align: middle;
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

input[type="text"]:focus,
select:focus,
textarea:focus {
    background-color: #d0e2be;
}

#search_table {
    padding-top: 2rem;
    margin: 0 auto;
    text-align: center;
    width: 100%;
}

.aitCreate {
    /*margin-top: 20px;*/
    max-width: 40%;
    background: white;
    border-radius: 5px;
    /*margin-bottom: 10px;*/
}

.accordion {
    margin: 0 auto;
    width: 90%;
    vertical-align: middle;
    text-align: center;
}
.option-menu {
    padding-top: 1rem;
    margin: 0 auto;
    width: 90%;
    vertical-align: middle;
    text-align: center;

}
.option-menu div{
    border: none;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Add a box shadow for depth */
    width: 100%;
    float:left;
    margin-top: 1rem;
    height: 6rem;
    background: white;
}
.option-menu div .cardTitle {
    background-color: var(--secondary-color);
    color: #ffffff;
    border-top-right-radius: 5px;
    border-top-left-radius: 5px;
    width: 100%;
    margin: 0;
    height: 2.5rem;
    font-size: 1rem;
    font-weight: bold;
    display: flex;
    flex-direction: column-reverse;
    justify-content: space-evenly;
}
.option-menu div table {
    width: 95%;
    margin: 0.5rem auto 0.8rem auto;
    vertical-align: middle;
    text-align: center;
    position: relative;
    border-collapse: separate;
    border-spacing: 0 5px;
    font-size: 0.85rem;
}
.option-menu div table td {
    height: 2rem;
}

.option-menu div table td:nth-child(1) {
    background-color: var(--primary-color-light);
    color: black;
    border-bottom-left-radius: 5px;
    border-top-left-radius: 5px;
    text-align: center;
    font-weight: bold;

    &:hover {
        background-color: var(--primary-color);
        color: white;
    }
}

.option-menu div table td:nth-child(2) {
    width: 50%;
    border: 1px solid;
    border-color: var(--primary-color-light);
    background-color: var(--gray-thema);
    border-bottom-right-radius: 5px;
    border-top-right-radius: 5px;
    text-align: left;
    padding-left: 0.5rem;
}
.option-menu div table td:nth-child(2) input {
    background-color: var(--gray-thema);
}
.option-menu div table td:last-child {
    padding-left: 1rem;
}

.tittle {
    margin: 0 auto;
    font-size: 2rem;
    width: 90%;
    /*background: red;*/
}


.file_label {
    background-color: #31436B;
    font-size: 15px;
}

.file_input {
    display: none;
}

.footer_btn {
    margin-top: 20px;
}

.btn_inline_left {
    float:left;
}

.btn_inline_right {
    float:left;
    margin-left: 550px;
}

.status_processing {
    color: red;
}

.eachTitle {
    font-size: 1.5rem;
    margin-left: 1rem;
}
.uploadBTN {
    border: none;
    width: 100%;
    height: 100%;
    text-align: center;
    border-radius: 5px;
    color: black;
    font-weight: bold;
    background-color: var(--primary-color-light);
    &:hover {
        color: white;
        background-color: var(--primary-color);
    }
}

.labelBtn {
    cursor: pointer;
    width: 100%;
}
</style>
<template>
<div>
    <!--ヘッダータイトル-->
    <header id="head">
        <div id="title" :class="{ active: this.isActive }">
            <button @click="toggleSubmenu(isActive)" class="qq"><img :src="this.isActive  ? this.icon2 : this.icon1" alt="Image" width="30" height="auto"></button>
            <h1 class="head_title">{{$t("common.titleAITSearch")}}</h1>
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
            <!--検索条件-->
            <div id="search_conditions">
                <div id="searchArea" align="center">
                    <label class="cardTitle">
                        <span>AIT Search Parameters</span>
                        <span>
                            <template v-if="$i18n.locale === 'en'">
                                <input type="button" value="Search" class="uploadBTN"
                                       @click="search" />
                            </template>
                            <template v-else>
                                <input type="button" value="検索" class="uploadBTN"
                                       @click="search" />
                            </template>
                        </span>
                    </label>
                    <table id="search_conditions_table">
                        <thead>
                            <tr>
                                <th class="search_conditions_th1"></th>
                                <th class="search_conditions_th2"><span>{{$t("aitSearch.titleSearchCategory")}}</span></th>
                                <th class="search_conditions_th3"><span>{{$t("aitSearch.titleSearchKeyword")}}</span></th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(searchCondition, index) in searchCondition_rows" :key="searchCondition.Id">
                                <td>
                                    <img src="~@/assets/AITSearch_delete_icon.svg" alt="delete" title="delete" class="icon" @click="deleteSearchCategory(index)"/>
                                </td>
                                <td>
                                    <select class="categories_select" v-model="searchCondition.selectedSearchCategory"
                                            @click="changeCategory">
                                        <option value=null style="color: gray">
                                            {{$t("common.defaultPulldown")}}
                                        </option>
                                        <option v-for="category in searchCondition.categories" 
                                                :key="category.param_name" 
                                                v-bind:value="category.param_name" 
                                                v-bind:disabled="selectedSearchCategories.has(category.param_name)" >
                                            {{ category.categoryname }} 
                                        </option>
                                    </select>
                                </td>
                                <td>
                                     <input type="text" class="keyword" placeholder="Search Table" v-model="searchCondition.keyword"/>
                                </td>
                            </tr>
                            <tr>
                                <td>
                                    <img src="~@/assets/AITSearch_add_icon.svg" alt="add" title="add" class="icon" @click="addSearchCategory"/>
                                </td>
                                <td>
                                    <select class="categories_select disable"  disabled>
                                        <option value=null style="color: gray" disabled>
                                            {{$t("common.defaultPulldown")}}
                                        </option>
                                    </select>
                                </td>
                                <td>
                                    <input type="text" class="keyword disable" placeholder="Serch Table" disabled/>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                    <!-- button -->

                </div>
            </div>

            <!--検索結果-->
            <div id="search_table">
                <div id="table" align="center">
                    <VueGoodTable 
                        ref="aitSearchListTable" 
                        :columns="aitSearch_columns" 
                        :rows="aitRows" 
                        :fixed-header="true"
                        max-height="43.75rem"
                        align="center" 
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
            aitSearch_columns: [
                {
                    label: this.setAITSearchTableLanguage("ait_name"),
                    field: "ait_name",
                    thClass: "th2",
                    width: "10%",
                },
                {
                    label: this.setAITSearchTableLanguage("description"),
                    field: "description",
                    thClass: "th3",
                    width: "25%",
                },
                {
                    label: this.setAITSearchTableLanguage("create_user_account"),
                    field: "create_user_account",
                    thClass: "th4",
                    width: "10%",
                },
                {
                    label: this.setAITSearchTableLanguage("create_user_name"),
                    field: "create_user_name",
                    thClass: "th5",
                    width: "10%",
                },
                {
                    label: this.setAITSearchTableLanguage("version"),
                    field: "version",
                    thClass: "th6",
                    width: "7%",
                },
                {
                    label: this.setAITSearchTableLanguage("downloads"),
                    field: "downloads",
                    thClass: "th7",
                    width: "7%",
                },
                {
                    label: this.setAITSearchTableLanguage("installed"),
                    field: "installed",
                    thClass: "th8",
                    width: "5%",
                },
                {
                    label: this.setAITSearchTableLanguage("install"),
                    field: "install",
                    thClass: "th9",
                    width: "5%",
                },
                {
                    label: this.setAITSearchTableLanguage("detail"),
                    field: "detail",
                    thClass: "th10",
                    width: "5%",
                }
                
            ],
            selected_ait: '',
            selected_row: null,
            aitRows: [],
            searchCondition_rows: [],
            selectedSearchCategories: new Map(),
            categories: [],
            screenName: 'aitSearch'
        }
    },
    mounted: async function () {
        await this.getSearchCategories();
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
        setAITSearchTableLanguage(fieldName) {
            // mountよりも先に呼び出されるので、ここで言語設定を呼び出す。
            this.setLanguageData()
            this.languagedata = require('./languages/languages.json');
            if (this.$i18n.locale == 'ja') {
                switch (fieldName) {
                    case 'ait_name':
                        return this.languagedata.ja.aitSearch.ait_name;
                    case 'description':
                        return this.languagedata.ja.aitSearch.description;
                    case 'create_user_account':
                        return this.languagedata.ja.aitSearch.create_user_account;
                    case 'create_user_name':
                        return this.languagedata.ja.aitSearch.create_user_name;
                    case 'version':
                        return this.languagedata.ja.aitSearch.version;
                    case 'downloads':
                        return this.languagedata.ja.aitSearch.downloads;
                    case 'installed':
                        return this.languagedata.ja.aitSearch.installed;
                    case 'install':
                        return this.languagedata.ja.aitSearch.install;
                    case 'detail':
                        return this.languagedata.ja.aitSearch.detail;
                    default:
                }
            } else if (this.$i18n.locale == 'en') {
                switch (fieldName) {
                    case 'ait_name':
                        return this.languagedata.en.aitSearch.ait_name;
                    case 'description':
                        return this.languagedata.en.aitSearch.description;
                    case 'create_user_account':
                        return this.languagedata.en.aitSearch.create_user_account;
                    case 'create_user_name':
                        return this.languagedata.en.aitSearch.create_user_name;
                    case 'version':
                        return this.languagedata.en.aitSearch.version;
                    case 'downloads':
                        return this.languagedata.en.aitSearch.downloads;
                    case 'installed':
                        return this.languagedata.en.aitSearch.installed;
                    case 'install':
                        return this.languagedata.en.aitSearch.install;
                    case 'detail':
                        return this.languagedata.en.aitSearch.detail;
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
        async getSearchCategories(){
            const url = this.$aithubURL + '/aits/categories';
            
            await this.$axios.get(url)
                .then((response) => {
                    this.categories = response.data.Categories;
                    this.searchCondition_rows.push({
                        categories: this.categories,
                        selectedSearchCategory: null,
                        keyword: ''
                    });
                })
                .catch((error) => {
                    this.signOutAitHubWhitErr();
                    this.triggerMessage('aithub_E02', error)
                })
        },
        deleteSearchCategory(index){
            this.searchCondition_rows.splice(index, 1);
        },
        addSearchCategory(){
            this.searchCondition_rows.push({
                categories: this.categories,
                selectedSearchCategory: null,
                keyword: ''
            });
        },
        search(){
            this.searchConditions = {};
            for (var row in this.searchCondition_rows) {
                if (!this.isCategorySelected(this.searchCondition_rows[row].selectedSearchCategory)) {
                    alert(this.$t("aitSearch.categoryRequiredError"));
                    return;
                }
                if (this.searchCondition_rows[row].keyword == '') {
                    alert(this.$t("aitSearch.keywordRequiredError"));
                    return;
                }
                for (var re in this.searchCondition_rows) {
                    if (row != re &&
                        this.searchCondition_rows[row].selectedSearchCategory == 
                        this.searchCondition_rows[re].selectedSearchCategory) {
                            alert(this.$t("aitSearch.categoryRepeatError"));
                            return; 
                    }
                }

                this.$set(this.searchConditions, 
                          this.searchCondition_rows[row].selectedSearchCategory, 
                          this.searchCondition_rows[row].keyword);
            }
            this.aitRows = [];
            this.getAITListFromAITHub(this.searchConditions, this.screenName);
        },
        aitInstall(params){
            // 選択AITのエラーチェック
            this.selected_ait = params.row.ait_id;
            this.selected_row = params.row;

            // インストール済みのエラーチェック
            if (this.selected_row.install == true) {
                alert(this.$t("aitSearch.installedAITError"));
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
        },
        changeCategory(){
            this.selectedSearchCategories = new Map();
            for (var row in this.searchCondition_rows) {
                if (this.isCategorySelected(this.searchCondition_rows[row].selectedSearchCategory)){
                    this.selectedSearchCategories.set(this.searchCondition_rows[row].selectedSearchCategory, true);
                } else {
                    this.selectedSearchCategories.set(this.searchCondition_rows[row].selectedSearchCategory, false);
                }
            }
        },
        isCategorySelected(selectedSearchCategory){
            if (selectedSearchCategory == null || selectedSearchCategory == 'null' || selectedSearchCategory == '') {
                return false;
            } else {
                return true;
            }
        }
    }
}
</script>


<style scoped>

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
/*---------------
表
----------------*/


#table>>>.vgt-input, .vgt-select {
    width: 100% !important;
    float: left;
}

#table>>>.vgt-inner-wrap .vgt-global-search{
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
#table>>>.vgt-table tbody tr th {
    background: none;
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
}
#table>>>.vgt-table tbody tr td {
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
/* padding: 1rem; */
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

#search_conditions {
    padding-top: 1rem;
    margin: 0 auto;
    width: 90%;
    vertical-align: middle;
    text-align: center;
    border-radius: 5px;

}
#search_conditions div{
    border: none;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Add a box shadow for depth */
    width: 100%;
    margin-top: 1rem;
    margin-right: 1rem;
    background: white;
}
#search_conditions .cardTitle {
    background-color: #dc722b;
    color: #ffffff;
    border-top-right-radius: 5px;
    border-top-left-radius: 5px;
    margin: 0;
    width: 100%;
    height: 2.5rem;
    font-size: 1rem;
    font-weight: bold;
    display: flex;
    justify-content: space-evenly;
    flex-wrap: nowrap;
    align-items: center;
    flex-direction: row;
}
#search_conditions .cardTitle .uploadBTN {
    border: none;
    width: 10rem;
    height: 2rem;
    text-align: center;
    border-radius: 5px;
    color: black;
    background-color: #a9c7aa;
    font-size: 0.85rem;
    font-weight: bold;
    &:hover {
        color: white;
        background-color: #43645b;
    }
}
#search_conditions_table {
    text-align: center;
    border-collapse: separate;
    border-spacing: 0 5px;
    background-color: unset;
    border: none;
    margin-top: 1rem;
    width: 95%;
}

#search_conditions_table thead {
    margin-top: 1rem;
    height: 2rem;
    background-color: #dc722b;
    font-weight: bold;
    font-size: 1rem;
    color: white;
}
.search_conditions_th1{
    width: 5%;
}
#search_conditions_table tbody tr {
    height: 2rem;
    background: #f0f0f0;
}
#search_conditions_table tbody td:nth-child(1){
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
    width: 5%;
}
.search_conditions_th2{
    width: 45%;
}
#search_conditions_table tbody td:nth-child(2){
    width: 45%;
}
.search_conditions_th3{
    width: 45%;
}
#search_conditions_table tbody td:last-child{
    width: 45%;
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
}
#search_conditions_table tbody select{
    width: 95%;
    height: 2rem;
}
#search_conditions_table tbody input {
    width: 100%;
}
#search_conditions_table tbody tr:hover{
    background: #a9c7aa !important;
}
.categories_select, .keyword {
    width: 100%;
    background: white;
    border-radius: 5px;
    border: 1px solid;
    border-color: #f0f0f0;
    min-height: 2rem;
}
</style>
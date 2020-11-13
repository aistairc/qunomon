<template>
<div>
    <!-- ヘッダ -->
    <header id="head">
        <div id="title">
            <h1 v-if="this.mlComponent">{{this.mlComponent.Name}}</h1>
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
            <li class="place">
                <router-link :to="{ name: 'Inventories' }" class="move_">{{$t("common.menuInventories")}}</router-link>
            </li>
            <li class="un_place">
                <router-link :to="{ name: 'TestDescriptions' }" class="move_">{{$t("common.menuTestDescriptions")}}</router-link>
            </li>

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

    <!-- ニュース（中央カラム） -->
    <div id="main">
        <div id="main_body">
            <div id="search_table">
                <!--検索-->
                <!--クリエイトボタン-->
                <div class="btn">
                    <inventoryCreate :key="inv_create_key" @createInventory="addInventories" @reset="modalReset('create')"></inventoryCreate>
                </div>
                <!--表-->
                <div id="table" align="center">
                    <inventoryEdit :key="inv_edit_key" ref="inv_edit" @createInventory="addInventories" @reset="modalReset('edit')"></inventoryEdit>
                    <VueGoodTable :columns="columns" :rows="rows" max-height="300px" :fixed-header="true" align="center" styleClass="vgt-table" :search-options="{enabled: true}">
                        <template slot="table-row" slot-scope="props">
                            <!--EditOptions-->
                            <span v-if="props.column.field == 'edit_options'">
                                <template v-if="$i18n.locale === 'en'">
                                    <img src="~@/assets/edit.svg" alt="edit" title="edit" class="icon" @click="inventoryEdit(props.row.edit_option)" />
                                    <img src="~@/assets/delete.svg" alt="delete" title="delete" class="icon" @click="inventoryDelete(props.row.edit_option)" />
                                </template>
                                <template v-else>
                                    <img src="~@/assets/edit.svg" alt="編集" title="編集" class="icon" @click="inventoryEdit(props.row.edit_option)" />
                                    <img src="~@/assets/delete.svg" alt="削除" title="削除" class="icon" @click="inventoryDelete(props.row.edit_option)" />
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
import {
    VueGoodTable
} from 'vue-good-table';
import {
    inventoryMixin
} from '../mixins/inventoryMixin';

// modalに必要なもののimportする
import inventoryCreate from './InventoryAppend';
import inventoryEdit from './InventoryEdit';

export default {
    components: {
        VueGoodTable,
        inventoryCreate,
        inventoryEdit,
    },
    mixins: [urlParameterMixin, inventoryMixin],
    data() {
        return {
            result: null,
            inventories: null,
            page: 1,
            perPage: 100,
            totalPage: 1,
            inv_create_key: 0,
            inv_edit_key: 0,
            languagedata: null,
            columns: [{
                    label: this.setTableLanguage("inv_name"),
                    field: "inv_name",
                    thClass: 'th1',
                    tdClass: 't_left',
                    width: "35%",
                },
                {
                    label: this.setTableLanguage("inv_data"),
                    field: "inv_data",
                    thClass: 'th2',
                    tdClass: 't_left',
                    width: "20%",
                },
                {
                    label: this.setTableLanguage("inv_upda"),
                    field: "inv_upda",
                    thClass: 'th3',
                    tdClass: 't_center',
                    width: "30%",
                },
                {
                    label: this.setTableLanguage("edit_options"),
                    field: "edit_options",
                    thClass: 'th4',
                    tdClass: 't_center',
                    width: "15%",
                    sortable: false,
                },
            ],
            rows: []
        }
    },
    mounted: function () {
        this.mlComponentIdCheck();
        this.organizationIdCheck = sessionStorage.getItem('organizationId');
        this.mlComponentId = sessionStorage.getItem('mlComponentId');
        this.getMLComponent();
        const url = this.$backendURL +
            '/' +
            this.organizationIdCheck +
            '/mlComponents/' +
            this.mlComponentId +
            '/inventories'
        this.$axios.get(url)
            .then((response) => {
                this.inventories = response.data;
                this.getInventory();
            })
            .catch((error) => {
                this.$router.push({
                    name: 'Information',
                    params: {
                        error
                    }
                })
            })
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
                    case 'inv_name':
                        return this.languagedata.ja.inventories.name;
                    case 'inv_data':
                        return this.languagedata.ja.inventories.dataType;
                    case 'inv_upda':
                        return this.languagedata.ja.inventories.updateTime;
                    case 'edit_options':
                        return this.languagedata.ja.inventories.editOptions;
                    default:
                }
            } else if (this.$i18n.locale == 'en') {
                switch (fieldName) {
                    case 'inv_name':
                        return this.languagedata.en.inventories.name;
                    case 'inv_data':
                        return this.languagedata.en.inventories.dataType;
                    case 'inv_upda':
                        return this.languagedata.en.inventories.updateTime;
                    case 'edit_options':
                        return this.languagedata.en.inventories.editOptions;
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
        inventoryDelete(inventoryId) {
            if (confirm("削除してよろしいですか？")) {
                const url = this.$backendURL +
                    '/' +
                    this.organizationIdCheck +
                    '/mlComponents/' +
                    this.mlComponentId +
                    '/inventories/' +
                    inventoryId
                this.$axios.delete(url)
                    .then((response) => {
                        this.result = response.data;
                        window.location.reload()
                    })
                    .catch((error) => {
                        if(error.response.data.Code == 'I45000'){
                            if(this.$i18n.locale == 'ja'){
                                alert("テストディスクリプションに登録されているため、削除できませんでした。");
                            }
                            else{
                                alert("Could not be deleted because it is registered in TestDescriptions.");
                            }
                        }
                        else{
                            this.$router.push({
                                name: 'Information',
                                params: {
                                    error
                                }
                            })
                        }
                    })
            }
        },
        inventoryEdit(inventoryId) {
            this.$refs.inv_edit.show(inventoryId);
        },
        postInventoryId(inventoryId) {
            this.$router.push({
                name: 'InventoryEdit',
                params: {
                    inventoryId: inventoryId
                }
            })
        },
        postHistory() {
            this.$router.push({
                name: 'InventoryAppend',
                params: {
                    history: this.$route.name
                }
            })
        },
        splitJoin(text) {
            return text.split(" ");
        },
        getInventory() {
            this.$axios.get(this.$backendURL + '/' + this.organizationIdCheck + '/mlComponents/' + this.mlComponentId + '/inventories')
                .then((response) => {
                    this.inventories = response.data.Inventories;
                    if (this.inventories != null) {
                        for (var inventory in this.inventories) {
                            this.rows.push({
                                inv_name: this.inventories[inventory].Name,
                                inv_data: this.inventories[inventory].DataType.Name,
                                inv_upda: this.makeUpdateTime(this.inventories[inventory].UpdateDatetime), //this.inventories[inventory].UpdateDatetime,
                                edit_option: this.inventories[inventory].Id,
                            })
                        }
                    }
                }).catch((error) => {
                    this.$router.push({
                        name: 'Information',
                        params: {
                            error,
                        }
                    })
                }).catch(error => {
                    //eslint-disable-next-line no-console
                    console.log(error)
                })
        },
        addInventories() {
            this.rows = [];
            this.getInventory();
        },
        makeUpdateTime(updateTime) {
            var moment = require('moment-timezone');
            var datetime_conv = moment.tz(updateTime, 'UTC');
            datetime_conv.tz(moment.tz.guess());

            var datetime = datetime_conv.format().slice(0,16);
            datetime = datetime.replace(/T/g, ' ');
            datetime = datetime.replace(/-/g, '/');
            return datetime;
        },
        modalReset(key) {
            switch (key) {
                case 'create':
                    this.inv_create_key = this.inv_create_key ? 0 : 1;
                    break;
                case 'edit':
                    this.inv_edit_key = this.inv_edit_key ? 0 : 1;
                    break
                default:

            }
        },
        signOut() {
            sessionStorage.removeItem('mlComponentId');
            sessionStorage.removeItem('organizationId');
            sessionStorage.removeItem('language');
            this.$router.push({
                name: 'SignIn'
            });
        }
    },
    computed: {
        totalPages: function () {
            return Math.max(Math.ceil(this.inventories.Inventories.length / this.perPage), 1)
        },
        paging: function () {
            return this.inventories.Inventories.slice((this.page - 1) * this.perPage, this.page * this.perPage);
        },
        processedList: function () {
            return this.paging
        }
    }
}
</script>

<style scoped>
/*---------------
表
----------------*/
#table>>>table tr:hover {
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
    right: 20px !important;
}

#table>>>table.vgt-table {
    font-size: 16px !important;
    max-width: 880px !important;
    max-width: 1000px !important;
}

#table>>>table.vgt-table td {
    padding: .35em .75em .35em .75em;
    vertical-align: middle !important;
}

#table>>>table.vgt-table .t_center {
    text-align: center;
}

#table>>>table.vgt-table .t_left {
    text-align: left;
}
#table>>>.vgt-left-align {
    vertical-align: middle !important;
}

.right {
    float: right;
}

/*---------------
	メイン
	----------------*/
input#openModal {
    position: relative;
    top: 40px;
    right: -390px;
    z-index: 1;
}

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
    margin-right: 50;
    text-align: center;
    width: 905px;
}

.btn {
    text-align: right;
    padding: 10px 0px 5px;
}

.icon {
    position: relative;
    left: 5px;
    margin-left: 7px;
    text-decoration: none;
    vertical-align: middle;
    cursor: pointer;
}

#openModal {
    position: relative;
    top: 48px;
    right: 24px;
    z-index: 1;
}
</style>

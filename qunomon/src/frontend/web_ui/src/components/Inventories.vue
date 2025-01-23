<template>
<div>
    <!-- ヘッダ -->
    <header id="head" :class="{ active: this.isActive }">
        <div id="title">
            <button @click="toggleSubmenu(isActive)" class="qq"><img :src="this.isActive ? this.icon2 : this.icon1" alt="Image" width="30" height="auto"></button>
            <h1 class="head_title" v-if="this.mlComponent">{{this.mlComponent.Name}}</h1>
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
    </SubMenuMLComponent>


    <!-- ニュース（中央カラム） -->
    <div id="main" :class="{ active: this.isActive }">
        <div id="main_body">
            <div id="search_table">
                <!--検索-->
                <!--クリエイトボタン-->
                <div class="btnArea">
                    <inventoryCreate :key="inv_create_key" @createInventory="addInventories" @reset="modalReset('create')"></inventoryCreate>
                    <inventoryEdit :key="inv_edit_key" ref="inv_edit" @createInventory="addInventories" @reset="modalReset('edit')"></inventoryEdit>
                </div>
                <!--表-->
                <div id="table" align="center">
                    <vue-good-table :columns="columns" :rows="rows" max-height="300px" :fixed-header="true" align="center" styleClass="vgt-table" :search-options="{enabled: true}">
                        <template v-slot:table-row="props">
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
import SubMenuMLComponent from './SubMenuMLComponent.vue';
import { subMenuMixin } from "../mixins/subMenuMixin";
import { urlParameterMixin } from '../mixins/urlParameterMixin';
import { AccountControlMixin } from '../mixins/AccountControlMixin';
import { csrfMixin } from '../mixins/csrfMixin';
import { inventoryMixin} from '../mixins/inventoryMixin';

import 'vue-good-table-next/dist/vue-good-table-next.css';
import { VueGoodTable} from 'vue-good-table-next';

// modalに必要なもののimportする
import inventoryCreate from './InventoryAppend.vue';
import inventoryEdit from './InventoryEdit.vue';

export default {
    components: {
        SubMenuMLComponent,
        VueGoodTable,
        inventoryCreate,
        inventoryEdit,
    },
    mixins: [subMenuMixin, urlParameterMixin, inventoryMixin, AccountControlMixin, csrfMixin],
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
                    query: {error: JSON.stringify({...error, response: error.response})}
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
            if (confirm(this.$t("confirm.delete"))) {
                const url = this.$backendURL +
                    '/' +
                    this.organizationIdCheck +
                    '/mlComponents/' +
                    this.mlComponentId +
                    '/inventoriesFront/' +
                    inventoryId
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
                        if(error.response.data.Code == 'I45000'){
                            alert(this.$t("inventories.alertMessage"));
                        }
                        else{
                            this.$router.push({
                                name: 'Information',
                                query: {error: JSON.stringify({...error, response: error.response})}
                            })
                        }
                    })
            }
        },
        inventoryEdit(inventoryId) {
            this.$refs.inv_edit.show(inventoryId);
        },
        postHistory() {
            this.$router.push({
                name: 'InventoryAppend',
                query: {history: this.$route.name}
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
                        query: {error: JSON.stringify({...error, response: error.response})}
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
#table :deep(.vgt-input, .vgt-select) {
    width: 100% !important;
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
}
#table :deep(.vgt-table .expanded td, th) {
    white-space: normal;
    overflow: visible;
    text-overflow: unset;
    max-width: 10%;
}

#table :deep(.vgt-table td) {
    padding: unset;
    height: 2rem;
    vertical-align: middle;
}


.right {
    float: right;
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
    //position: relative;
    z-index: 0;
}

#search_table {
    padding-top: 2rem;
    margin: 0 auto;
    text-align: center;
    width: 90%;
}

.icon {
    position: relative;
    left: 5px;
    margin-left: 7px;
    text-decoration: none;
    vertical-align: middle;
    cursor: pointer;
}


.btnArea{
    width: 50%;
//background: red;
    float: right;
}

</style>

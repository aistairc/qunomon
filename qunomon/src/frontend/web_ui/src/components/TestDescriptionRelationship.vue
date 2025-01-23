<template>
    <div id="app">
        <BModal v-model="showModal" name="TDReletionModal" class="modalContents" size="lg"  @hide="tableReroad" no-footer no-header>
            <div id="search_table">
                <div id="modal_description">
                    <div id="title_area">
                        <span class="modal_title">{{$t("testDescriptions.relTitle")}}</span>
                        <span class="modal_message">{{$t("testDescriptions.relTitleExp")}}</span>
                    </div>
                    <div id="btn_test">
                        <template v-if="$i18n.locale === 'en'">
                            <input v-bind:class="{ 'un_btn' : isActivated }" id="compare_btn" type="submit" value="Compare" class="uploadBTN" @click="compare">
                        </template>
                        <template v-else>
                            <input v-bind:class="{ 'un_btn' : isActivated }" id="compare_btn" type="submit" value="比較" class="uploadBTN" @click="compare">
                        </template>
                    </div>
                </div>

                <!--テーブル-->
                <div id="table" align="center">
                    <vue-good-table
                        ref="tdTable"
                        :columns="columns"
                        :rows="rows"
                        max-height="350px"
                        :fixed-header="true"
                        align="center"
                        styleClass="vgt-table"
                    >
                        <template v-slot:table-row="props">
                            <!--チェックボックス-->
                            <span v-if="props.column.field == 'checked'">
                                <input v-bind:value="td_test[props.row.originalIndex].Id" v-model="checkedItems" @change="onRowClick" type="checkbox" name="background">
                            </span>
                            <!--お気に入り-->
                            <span v-if="td_test[props.row.originalIndex].Star === false && props.column.field == 'star'">
                                <img src="~@/assets/unlike.svg" alt="unlike" title="unlike" class="icon status" @click="onStarChange(td_test[props.row.originalIndex])">
                            </span>
                            <span v-else-if="td_test[props.row.originalIndex].Star === true && props.column.field == 'star'">
                                <img src="~@/assets/like.svg" alt="like" title="like" class="icon status" @click="onStarChange(td_test[props.row.originalIndex])">
                            </span>
                            <!--Status-->
                            <span v-else-if="td_test[props.row.originalIndex].Result == 'OK' && props.column.field == 'status'">
                                <img src="~@/assets/check_green.svg" alt="OK" title="OK" class="icon status">
                            </span>
                            <span v-else-if="td_test[props.row.originalIndex].Result == 'NG' && props.column.field == 'status'">
                                <img src="~@/assets/clear_red.svg" alt="NG" title="NG" class="icon status">
                            </span>
                            <span v-else>
                                {{props.formattedRow[props.column.field]}}
                            </span>
                        </template>
                    </vue-good-table>
                </div>
                <!-- テーブル下コンテンツ -->

            </div>
            <div id="closeModal" class="closeModal" @click="postTDRelationshipCancel">
            ×
            </div>
        </BModal>
    </div>
</template>

<script>
    import { tdMixin } from '../mixins/testDescriptionMixin';
    import { urlParameterMixin } from '../mixins/urlParameterMixin';
    import { AccountControlMixin } from '../mixins/AccountControlMixin';
    import 'vue-good-table-next/dist/vue-good-table-next.css';
    import { VueGoodTable } from 'vue-good-table-next';
    import { BModal } from 'bootstrap-vue-next';
    
    export default {
        mixins: [urlParameterMixin, tdMixin, AccountControlMixin],
        mounted: function () {
            this.mlComponentIdCheck();
			this.organizationIdCheck = sessionStorage.getItem('organizationId');
            this.mlComponentId = sessionStorage.getItem('mlComponentId');
        },
        components: {
            VueGoodTable,
            BModal
        },
		data() {
			return{
                isActivated: true,
                testDescriptionId: null,
                test_description_anc: null,
                td_test : null,
                generateReport: null,
                selectStatus: '',
                starChecked: false,
                dateStart: '',
                dateEnd: '',
                checkedItems: [],
                TestDescriptions: null,
				columns: [
					{
                        label: this.setTableLanguage("checked"),
                        field: "checked",
                        width: "3%",
                        tdClass: "t_center",
                        sortable: false,
                    },
                    {
                        label: this.setTableLanguage("star"),
                        field: "star",
                        width: "4%",
                        tdClass: "t_center",
                        sortable: false,
                    },
                    {
						label: this.setTableLanguage("td_id"),
                        field: "td_id",
                        thClass: 'tdID',
						tdClass: 't_right',
                        width: "10%",
                        sortFn: this.sortNumber,
                        firstSortType: 'asc',
					},
					{
						label: this.setTableLanguage("td_p_id"),
                        field: "td_p_id",
                        thClass: 'tdID',
						tdClass: 't_right',
                        width: "10%",
                        sortFn: this.sortNumber,
                    },
                    {
						label: this.setTableLanguage("status"),
						field: "status",
						tdClass: 't_center',
                        width: "8%",
                        sortable: false,
					},
					{
						label: this.setTableLanguage("td_name"),
						field: "td_name",
						tdClass: 't_left',
						width: "40%",
                    },
                    {
						label: this.setTableLanguage("update_time"),
						field: "update_time",
						tdClass: 't_center',
                        width: "22%",
                        formatFn: this.formatFn,
                        sortFn: this.sortNumber,
                    }
				],
				rows: [],
                showModal: false
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
                        case 'checked':
                            return this.languagedata.ja.testDescriptions.checkbox;
                        case 'star':
                            return this.languagedata.ja.testDescriptions.tStar;
                        case 'td_id':
                            return this.languagedata.ja.testDescriptions.tdId;
                        case 'td_p_id':
                            return this.languagedata.ja.testDescriptions.tdPId;
                        case 'status':
                            return this.languagedata.ja.testDescriptions.tStatus;
                        case 'td_name':
                            return this.languagedata.ja.testDescriptions.tdName;
                        case 'update_time':
                            return this.languagedata.ja.testDescriptions.updateTime;
                        default:
                    }
                } else if (this.$i18n.locale == 'en') {
                    switch (fieldName) {
                        case 'checked':
                            return this.languagedata.en.testDescriptions.checkbox;
                        case 'star':
                            return this.languagedata.en.testDescriptions.tStar;
                        case 'td_id':
                            return this.languagedata.en.testDescriptions.tdId;
                        case 'td_p_id':
                            return this.languagedata.en.testDescriptions.tdPId;
                        case 'status':
                            return this.languagedata.en.testDescriptions.tStatus;
                        case 'td_name':
                            return this.languagedata.en.testDescriptions.tdName;
                        case 'update_time':
                            return this.languagedata.en.testDescriptions.updateTime;
                        default:
                    }
                }
            },
            sortNumber(x, y) {
                return (x < y ? -1 : (x > y ? 1 : 0));
            },
            formatFn: function(val) {
                var date = val.slice(0,16);
                date = date.replace(/T/g, ' ');
                date = date.replace(/-/g, '/');
                return date;
            },
            show(TestDescriptionId) {
                this.testDescriptionId = TestDescriptionId;
                this.showModal = true;
                const url = this.$backendURL
                        + '/'
                        + this.organizationIdCheck
                        + '/mlComponents/'
                        + this.mlComponentId
                        + '/testDescriptions/'
                        + this.testDescriptionId
                        + '/ancestors';
                this.$axios.get(url)
                .then((response) => {
                    this.test_description_anc = response.data;
                    this.td_test = this.test_description_anc.TestDescriptions;
                    this.getAncestors(this.td_test)
                })
                .catch((error) => {
                    this.$router.push({
                        name: 'Information',
                        query: {error: JSON.stringify({...error, response: error.response})}
                    })
                });
            },
			hide() {
				this.showModal = false;
			},
            getAncestors(val){
                for(var td in val){
                    if(val[td].Result=='OK' || val[td].Result=='NG'){
                        this.rows.push(
                            {
                                td_id: val[td].Id,
                                td_p_id: val[td].ParentID,
                                td_name: val[td].Name,
                                td_status: val[td].Result,
                                update_time: val[td].UpdateDatetime,
                            }
                        )
                    }
                }
            },
            onRowClick: function(){
                var checked = this.checkedItems.length;
                var tdTable = this.$refs.tdTable;
                
                // テーブルの行の情報全てをチェック
                var status = []
                for(var j=0;j<tdTable.rows.length;j++){
                    // 1行ずつの情報をループ
                    // Statusの情報を取得
                    var td_id = tdTable.rows[j].td_id;
                    if(this.checkedItems.includes(td_id) && !status.includes(tdTable.rows[j].td_status)){
                        status.push(tdTable.rows[j].td_status);
                    }
                }
                
                //全チェックボックスのNameを取得する
                var background = document.getElementsByName('background')
                
                //選択した行の背景色制御
                for(var l=0; l<background.length; l++){
                    if(background[l].checked){
                        background[l].parentNode.parentNode.parentNode.classList.add('checked')
                    }else {
                        background[l].parentNode.parentNode.parentNode.classList.remove('checked')
                    }
                }
                
                //ボタン活性
                if(checked == 0 || ((status.includes('ERR') || status.includes('NA')) && (status.includes('OK') || status.includes('NG')))){
                    //チェックがないとき、Statusが混ざっているとき（非活性）
                    document.getElementById('compare_btn').classList.add('un_btn');
                    //CompareとDownloadReportのボタン活性
                }else if (checked == 2) {
                    //親子関係がない時はCompare非活性
                    document.getElementById('compare_btn').classList.remove('un_btn');
                } else if(checked == 1 ){
                    document.getElementById('compare_btn').classList.add('un_btn');
                } else {
                    document.getElementById('compare_btn').classList.add('un_btn');
                }
            },
            postTDRelationshipCancel(){
                this.hide();                
            },
            compare: function(){
                sessionStorage.setItem('testDescriptionId1', this.checkedItems[0]);
                sessionStorage.setItem('testDescriptionId2', this.checkedItems[1]);
                this.$router.push({
                    name: 'TestDescriptionsCompare'
                })
            },
            onStarChange: function(testDescription){
                if(testDescription.Star === true){
                    this.setUnStar(testDescription.Id)
                }
                else{
                    this.setStar(testDescription.Id)
                }
                testDescription.Star = !testDescription.Star
            },
            tableReroad(){
                this.$emit("tableReroad");
                this.$emit('reset');
            },
        },
	}
</script>

<style scoped>
/*---------z----------テーブル-------------------*/

#table :deep(.vgt-inner-wrap .vgt-global-search) {
    background: unset;
    border: unset;
    padding: unset;
    margin: unset;
}
#table {
    display: inline-block;
    height: 90%;
    width: 100%;
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
#table input[type="checkbox"] {
    width: 15px;
    height: 15px;
    vertical-align: middle;
}

.checked{
  background-color: #d1ff8c;
}

/*-------------------モーダル-------------------*/

#search_table {
  width: 780;
}
#title_area{
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    width: 50%;
    padding-left: 0.5rem;
}
#btn_test {
    width: 50%;
}
#btn_test  .uploadBTN {
    border: none;
    height: 2rem;
    width: 30%;
    text-align: center;
    border-radius: 5px;
    color: black;
    background-color: var(--primary-color-light);
    font-size: 0.85rem;
    font-weight: bold;
    &:hover {
        color: white;
        background-color: var(--primary-color);
    }
    &.un_btn{
        background: silver;
        pointer-events: none;
    }
}

#modal_description {
  display: flex;
    justify-content: space-between;
    align-items: center;
  height: 2.5rem;
    background: var(--secondary-color);
    border-radius: 5px;
}

.modal_title {
  font-size: 1rem;
    font-weight: bold;
    color: white;
}

.modal_message {
  font-size: 0.85rem;
    color: #d1ff8c
}

.modalContents  :deep( .vm--modal) {
    text-align: center;
    position: absolute !important;
    width: auto !important;
    height: auto !important;
    max-height: 90% !important;
    background-color: var(--gray-thema);
    top: 50%  !important;
	left: 50% !important;
    transform:translate(-50%,-50%) !important;
    overflow: auto !important;
    border-radius: 5px;
}

</style>
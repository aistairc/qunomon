<template>
    <div>
        <!--ヘッダータイトル-->
        <header id="head" :class="{ active: this.isActive }">
            <div id="title">
                <button @click="toggleSubmenu(isActive)" class="qq"><img :src="this.isActive ? this.icon2 : this.icon1" alt="Image" width="30" height="auto"></button>
                <h1 class="head_title">{{$t("common.titleReportTemplate")}}</h1>
            </div>
        </header>

        <!-- サブメニュー（左カラム） -->
        <SubMenu :isActive="this.isActive">
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
        <div id="main" :class="{ active: this.isActive }">
            <div id="main_body">
                <div class="option-menu">
                    <div>
                        <label class="cardTitle">{{$t("reportTemplate.createReportTemplate")}}</label>
                        <table class="cardTable">
                            <tr>
                                <td>
                                    <label class="labelBtn">{{$t("reportTemplate.selectGuideline")}}</label>
                                </td>
                                <td>
                                    <select class="guidelines_select" v-model="create_selected_guideline">
                                        <option value=null style="color: gray">
                                            {{$t("common.defaultPulldown")}}
                                        </option>
                                        <option v-for="guideline in guidelines"
                                                :key="guideline.Id"
                                                v-bind:value="guideline.Id">
                                            {{ guideline.Name }}
                                        </option>
                                    </select>
                                </td>
                                <td >
                                    <template v-if="$i18n.locale === 'en'">
                                        <input type="button" value="Create" class="uploadBTN"
                                               @click="getTemplateWhitGuidelineId"/>
                                    </template>
                                    <template v-else>
                                        <input type="button" value="ひな形作成" class="uploadBTN"
                                               @click="getTemplateWhitGuidelineId"/>
                                    </template>
                                </td>
                            </tr>
                        </table>
                        <label class="cardTitle">{{$t("reportTemplate.installReportTemplate")}}</label>
                        <table class="cardTable">
                            <tr>
                                <td >
                                    {{$t("reportTemplate.selectGuideline")}}
                                </td>
                                <td >
                                    <select class="guidelines_select" v-model="install_selected_guideline">
                                        <option value=null style="color: gray">
                                            {{$t("common.defaultPulldown")}}
                                        </option>
                                        <option v-for="guideline in guidelines"
                                                :key="guideline.Id"
                                                v-bind:value="guideline.Id">
                                            {{ guideline.Name }}
                                        </option>
                                    </select>
                                </td>
                                <td >

                                </td>
                            </tr>
                            <tr>
                                <td >
                                    {{$t("reportTemplate.reportTemplateName")}}
                                </td>
                                <td >
                                    <input type="text" class="template_name" placeholder="Template Name" v-model="template_name"/>
                                </td>
                                <td ></td>
                            </tr>
                            <tr>
                                <td >
                                    <label  for="fileUpload">
                                        {{$t("reportTemplate.fileSelect")}}
                                        <input class="file_input" type="file" id="fileUpload" @change="fileSelected" />
                                    </label>
                                </td>
                                <td >
                                <span v-if="template_file == null">
                                    {{$t("reportTemplate.fileUnselected")}}
                                </span>
                                    <span v-else>
                                    {{template_file_name}}
                                </span>
                                </td>
                                <td >
                                    <template v-if="$i18n.locale === 'en'">
                                        <input type="button" value="Install" class="uploadBTN"
                                               @click="installReportTemplate"/>
                                    </template>
                                    <template v-else>
                                        <input type="button" value="インストール" class="uploadBTN"
                                               @click="installReportTemplate"/>
                                    </template>
                                </td>
                            </tr>
                        </table>
                    </div>
                </div>

                <!-- Download -->
                <div class="accordion">
                    <div id="table" align="center">
                        <VueGoodTable
                            ref="templateTable"
                            :columns="columns"
                            :rows="rows"
                            :fixed-header="false"
                            styleClass="vgt-table"
                            max-height="700px"
                            :search-options="{ enabled: true }"
                            :pagination-options="{enabled: true, mode: 'pages'}"
                            @on-row-click="onRowClick"
                        >
                            <template slot="table-row" slot-scope="props">
                                <!--EditOptions-->
                                <template v-if="props.column.field == 'download'">
                                    <span v-if="$i18n.locale === 'en'">
                                        <img src="~@/assets/google_icon_download.svg" alt="download" title="download" class="icon" @click="downloadReportTemplate(props)"/>
                                    </span>
                                    <span v-else>
                                        <img src="~@/assets/google_icon_download.svg" alt="ダウンロード数" title="ダウンロード数" class="icon" @click="downloadReportTemplate(props)"/>
                                    </span>
                                </template>
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
import 'vue-good-table/dist/vue-good-table.css';
import { VueGoodTable } from 'vue-good-table';
import { csrfMixin } from '../mixins/csrfMixin';

export default {
    mixins: [subMenuMixin, urlParameterMixin, AccountControlMixin, csrfMixin],
    data() {
        return {
            columns: [

                {
                    label: this.setTableLanguage("guidelineName"),
                    field: "guidelineName",
                    thClass: "th1",
                    width: "30%",
                },
                {
                    label: this.setTableLanguage("templateName"),
                    field: "templateName",
                    thClass: "th2",
                    width: "25%",
                },
                {
                    label: this.setTableLanguage("createDate"),
                    field: "createDate",
                    thClass: "th3",
                    width: "15%",
                },
                {
                    label: this.setTableLanguage("updateDate"),
                    field: "updateDate",
                    thClass: "th4",
                    width: "15%",
                },
                {
                    label: this.setTableLanguage("download"),
                    field: "download",
                    thClass: "th5",
                    width: "15%",
                },
            ],
            selected_template_id: '',
            selected_template_name: '',
            rows: [],
            guidelines: [],
            reportTemplates: [],
            guidelinesMap: new Map(),
            create_selected_guideline: null,
            install_selected_guideline: null,
            template_name: '',
            template_file: null,
            template_file_name: '',
            result: null
        }
    },
    mounted: function () {
        this.getGuidelines();
    },
    components: {
        SubMenu,
        VueGoodTable
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
                    case 'guidelineName':
                        return this.languagedata.ja.reportTemplate.guidelineName;
                    case 'templateName':
                        return this.languagedata.ja.reportTemplate.templateName;
                    case 'createDate':
                        return this.languagedata.ja.reportTemplate.createDate;
                    case 'updateDate':
                        return this.languagedata.ja.reportTemplate.updateDate;
                    case 'download':
                        return this.languagedata.ja.reportTemplate.download;
                    default:
                }
            } else if (this.$i18n.locale == 'en') {
                switch (fieldName) {
                    case 'guidelineName':
                        return this.languagedata.en.reportTemplate.guidelineName;
                    case 'templateName':
                        return this.languagedata.en.reportTemplate.templateName;
                    case 'createDate':
                        return this.languagedata.en.reportTemplate.createDate;
                    case 'updateDate':
                        return this.languagedata.en.reportTemplate.updateDate;
                    case 'download':
                        return this.languagedata.en.reportTemplate.download;
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
        onRowClick(e) {
            this.selected_template_id = e.row.templateId;
            this.selected_template_name = e.row.templateName;
            if (e.event.target.parentElement.parentElement.tagName.includes("TBODY")){
                e.event.target.parentElement.classList.toggle("expanded");
            }else{
                e.event.target.parentElement.parentElement.classList.toggle("expanded");
            }
        },
        getGuidelines() {
            this.$axios.get(this.$backendURL + '/guidelines')
                .then((response) => {
                    this.guidelines = response.data.Guidelines;
                    for (var i in this.guidelines) {
                        this.guidelinesMap.set(this.guidelines[i].Id, this.guidelines[i].Name);
                    }
                    this.getReportTemplates();
                })
                .catch((error) => {
                    this.$router.push({
                        name: 'Information',
                        params: {error}
                    })
                })
        },
        getReportTemplates() {
            this.$axios.get(this.$backendURL + '/reportTemplates')
                .then((response) => {
                    this.reportTemplates = response.data.ReportTemplates;
                    for (var i in this.reportTemplates) {
                        var rt = this.reportTemplates[i];
                        this.rows.push({
                            guidelineName: this.guidelinesMap.get(rt.GuidelineId),
                            templateName: rt.Name,
                            createDate: this.formatFn(rt.CreationDatetime),
                            updateDate: this.formatFn(rt.UpdateDatetime),
                            templateId: rt.Id,
                        });
                    }
                })
                .catch((error) => {
                    this.$router.push({
                        name: 'Information',
                        params: {error}
                    })
                })
        },
        getTemplateWhitGuidelineId(){
            if (!this.isGuidelineSelected(this.create_selected_guideline)) {
                alert(this.$t("reportTemplate.guidelineRequiredError"));
                return;
            }

            const url = this.$backendURL + '/reportTemplates/generateFront';
            const parms = {GuidelineId: '' + this.create_selected_guideline};
            //リクエスト時のオプションの定義
            const config = {
                headers:{
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRF-TOKEN' : this.getCookie("csrf_access_token")
                },
                withCredentials:true,
                responseType: 'blob'
            }
            this.$axios.post(url, parms, config)
                .then((response) => {
                    var zipName = this.guidelinesMap.get(this.create_selected_guideline);
                    const href = window.URL.createObjectURL(new Blob([response.data]));
                    const link = document.createElement('a');
                    link.href = href;
                    link.setAttribute('download', zipName + '.zip');
                    document.body.appendChild(link);
                    link.click()
                })
                .catch((error) => {
                    this.$router.push({
                        name: 'Information',
                        params: {error}
                    })
                })
        },
        downloadReportTemplate(params){
            this.selected_template_id = params.row.templateId
            if (this.selected_template_id == '') {
                alert(this.$t("reportTemplate.reportTemplateRequiredError"));
                return;
            }
            const url = this.$backendURL + '/reportTemplates/' + this.selected_template_id + '/zip';
            this.$axios.get(url, {responseType: 'blob'})
                .then((response) => {
                    var zipName = this.selected_template_name;
                    const href = window.URL.createObjectURL(new Blob([response.data]));
                    const link = document.createElement('a');
                    link.href = href;
                    link.setAttribute('download', zipName + '.zip');
                    document.body.appendChild(link);
                    link.click()
                })
                .catch((error) => {
                    this.$router.push({
                        name: 'Information',
                        params: {error}
                    })
                })
        },
        fileSelected(e){
            var selected_file = e.target.files[0];
            if (selected_file.name.indexOf('.zip') < 0) {
                this.template_file = null;
                this.template_file_name = '';
                alert(this.$t("reportTemplate.fileTypeError"));
                return;
            }

            this.template_file = selected_file;
            this.template_file_name = selected_file.name;
        },
        installReportTemplate(){
            if (!this.isGuidelineSelected(this.install_selected_guideline)) {
                alert(this.$t("reportTemplate.guidelineRequiredError"));
                return;
            }

            if (this.template_name == '') {
                alert(this.$t("reportTemplate.reportTemplateNameRequiredError"));
                return;
            }

            if (this.template_file == null) {
                alert(this.$t("reportTemplate.fileRequiredError"));
                return;
            }

            const url = this.$backendURL + '/reportTemplatesFront';
            let data = new FormData;
            data.append('GidelineId', '' + this.install_selected_guideline);
            data.append('Name', this.template_name);
            data.append('File', this.template_file);

            //リクエスト時のオプションの定義
            const config = {
                headers:{
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRF-TOKEN' : this.getCookie("csrf_access_token")
                },
                withCredentials:true,
            }

            this.$axios.post(url, data, config)
                .then((response) => {
                    this.result = response.data;
                    window.location.reload();
                })
                .catch((error) => {
                    this.$router.push({
                        name: 'Information',
                        params: {error}
                    })
                })
        },
        isGuidelineSelected(selectedGuideline){
            if (selectedGuideline == null || selectedGuideline == 'null' || selectedGuideline == '') {
                return false;
            } else {
                return true;
            }
        },
        formatFn(date){
            var datetime = '';
            if (date) {
                var moment = require('moment-timezone');
                var datetime_conv = moment.tz(date, 'UTC');
                datetime_conv.tz(moment.tz.guess());

                datetime = datetime_conv.format().slice(0,16);
                datetime = datetime.replace(/T/g, ' ');
                datetime = datetime.replace(/-/g, '/');
            }
            return datetime;
        },

    }
}
</script>


<style scoped>
/*---------------
表
----------------*/

#table>>>.vgt-input, .vgt-select {
    width: 50% !important;
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
#table>>>.vgt-table .expanded td {
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
    position: relative;
    z-index: 0;
}

input[type="text"]:focus,
select:focus {
    background-color: #a9c7aa;
}

.accordion {
    margin: 0 auto;
    width: 90%;
    padding-top: 5.75rem;
    vertical-align: middle;
    text-align: center;
    /*background-color: red;*/
}
.option-menu {
    padding-top: 1rem;
    margin: 0 auto;
    width: 90%;
    vertical-align: middle;
    text-align: center;
    height: 15rem;

}
.option-menu div{
    border: none;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Add a box shadow for depth */
    width: 100%;
    margin-top: 1rem;
    margin-right: 1rem;
    background: white;
}

.cardTable  {
    width: 95%;
    margin: auto;
    vertical-align: middle;
    text-align: center;
    position: relative;
    border-collapse: separate;
    border-spacing: 0 5px;
    font-size: 0.85rem;
}
.cardTable td {
    height: 2rem;
}

.cardTable td:nth-child(1) {

    width: 30%;
    border-bottom-left-radius: 5px;
    border-top-left-radius: 5px;
    text-align: center;
    background-color: #a9c7aa;
    color: black;
    font-weight: bold;
    &:hover {
        background-color: #43645b;
        color: white;
    }
}
.cardTable  td:nth-child(2) {
    width: 50%;
    border: 1px solid;
    border-color: #a9c7aa;
    background-color: #f0f0f0;
    border-bottom-right-radius: 5px;
    border-top-right-radius: 5px;
    text-align: left;
}
.cardTable td:nth-child(2) input {
    background-color: #f0f0f0;
}
.cardTable td:last-child {
    padding-left: 1rem;
}
.option-menu div .cardTitle {
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
    flex-direction: column-reverse;
    justify-content: space-evenly;
}
.cardTable .guidelines_select, input{
    height: 100%;
    width: 100%;
    border-bottom-right-radius: 5px;
    border-top-right-radius: 5px;
    border: none;
    cursor: pointer;
}
.uploadBTN {
    border: none;
    width: 100%;
    height: 100%;
    text-align: center;
    border-bottom-left-radius: 5px;
    border-top-left-radius: 5px;
    color: black;
    background-color: #a9c7aa;
    font-size: 0.85rem;
    font-weight: bold;
    &:hover {
        color: white;
        background-color: #43645b;
    }
}
.downloadBTN {
    color: white;
    width: 60%;
    background-color: #31436B;
    border-radius: 5px;
}


.btn_inline_left {
    float:left;
}

.btn_inline_right {
    float:right;
}

.template_name{
    height: 28px;
    width: 300px;
}

.file_label {
    background-color: #31436B;
    font-size: 15px;
}

.file_input {
    display: none;
}

.labelBtn {
    width: 100%;
}

</style>

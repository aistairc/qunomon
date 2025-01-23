<template>
<div id="app">
    <BModal v-model="showModal" name="rtSelectModal" id="rtSelectModal" class="modalContents" @hide="beforeClose" no-footer no-header>
        <div id="parent">
            <div class="part1">
                <div class="title_area">
                    <label>
                        <span class="rts_modal_subtitle">{{$t("reportTemplateSelect.title")}}</span>
                    </label>
                </div>
                <span class="rts_modal_descriptions">{{$t("reportTemplateSelect.descriptions1")}}</span>
                <br>
                <span class="rts_modal_descriptions">{{$t("reportTemplateSelect.descriptions2")}}</span>
                <div class="input">
                    <form class="formSelect">
                        <table>
                            <tr>
                                <td class="label">{{$t("reportTemplateSelect.select")}}<span class="error">&#042;</span></td>
                                <td>
                                    <select class="rt_select" v-model="select_reportTemplate_id">
                                        <option value="" hidden style="color:gray">--Please Select--</option>
                                        <option v-for="reportTemplate in reportTemplates" v-bind:value="reportTemplate.Id" :key="reportTemplate.Id">
                                            {{reportTemplate.Name}}
                                        </option>
                                    </select>
                                </td>
                            </tr>

                        </table>
                        <div id="btn_set">
                            <template v-if="$i18n.locale === 'en'">
                                <input type="button" value="Close" class="btn_left" @click="reportCancel">
                                <input type="button" value="Preview" class="btn_right" @click="selectReportTemplate">
                            </template>
                            <template v-else>
                                <input type="button" value="閉じる" class="btn_left" @click="reportCancel">
                                <input type="button" value="プレビュー" class="btn_right" @click="selectReportTemplate">
                            </template>
                        </div>
                    </form>
                </div>
                <hr>
                <div id="closeModal" class="closeModal" @click="reportCancel">
                    ×
                </div>
            </div>

            <div class="info_area">
                <div id="child1">
                    <!--セレクトエリア-->
                    <template v-if="previewer">
                        <div class="title_area2">
                            <label>
                                <span class="rts_modal_subtitle">{{$t("reportTemplateSelect.opinion")}}</span>
                            </label>
                        </div>
                        <div>
                            <textarea class="z-depth__" name="example" cols="70" rows="15" v-model="opinion" style="overflow:auto; width:100%;"></textarea>
                        </div>
                        <div id="btn_set2">
                            <template v-if="$i18n.locale === 'en'">
                                <input type="button" value="Close" class="btn_left" @click="reportCancel">
                                <input type="button" value="Create" class="btn_right" @click="downloadReport">
                            </template>
                            <template v-else>
                                <input type="button" value="閉じる" class="btn_left" @click="reportCancel">
                                <input type="button" value="作成" class="btn_right" @click="downloadReport">
                            </template>
                        </div>
                    </template>
                </div>
                <div id="child2">
                    <template v-if="previewer">
                        <div id="pdf_wrapper">
                            <VuePDF :pdf="pdf" :page="previewer.page_current" />
                        </div>
                        <div id="btn_set2">
                            <template v-if="$i18n.locale === 'en'">
                                <input type="button" value="Back" class="btn_left" @click="prevPage" :disabled="previewer.page_current <= 1">
                                {{ previewer.page_current }} / {{ previewer.page_end }}
                                <input type="button" value="Next" class="btn_right" @click="nextPage" :disabled="previewer.page_current === previewer.page_end">
                            </template>
                            <template v-else>
                                <input type="button" value="戻る" class="btn_left" @click="prevPage" :disabled="previewer.page_current <= 1">
                                {{ previewer.page_current }} / {{ previewer.page_end }}
                                <input type="button" value="次へ" class="btn_right" @click="nextPage" :disabled="previewer.page_current === previewer.page_end">
                            </template>
                        </div>
                    </template>
                </div>
            </div>
        </div>
    </BModal>
</div>
</template>

<script>
import { urlParameterMixin } from '../mixins/urlParameterMixin';
import { AccountControlMixin } from '../mixins/AccountControlMixin';
import { csrfMixin } from '../mixins/csrfMixin';
import { VuePDF, usePDF } from '@tato30/vue-pdf'
import { BModal } from 'bootstrap-vue-next';

export default {
    components: {
        VuePDF,
        BModal
    },
    data() {
        return {
            checkedItems_str: null,
            generateReport: null,
            reportTemplates: null,
            select_reportTemplate_id: 0,
            previewer: null,
            previewRequestData:
            {
                ReportOpinion: '',
            },
            opinion: '',
            pdf: null,
            pages: [],
            showModal: false
        }
    },
    mixins: [urlParameterMixin, AccountControlMixin, csrfMixin],
    mounted: function () {
        this.organizationId = sessionStorage.getItem('organizationId');
        this.mlComponentId = sessionStorage.getItem('mlComponentId');
    },
    methods: {
        show(checkedItems_str, reportTemplates) {
            this.checkedItems_str = checkedItems_str;
            this.reportTemplates = reportTemplates;
            this.showModal = true;
        },
        hide() {
            this.showModal = false;
        },
        /**
         * モーダルを閉じる前の処理
         */
        beforeClose() {
            this.previewer = null;
            this.$emit('reset');
            
            // モーダルを閉じる前にモーダルの大きさを元に戻す
            let elem_parent = document.getElementById("parent");
            if (elem_parent) {
                elem_parent.style.width = "";
            }
            
            let elem_child1 = document.getElementById("child1");
            if (elem_child1) {
                elem_child1.style.width = "";
            }
            
            let elem_child2 = document.getElementById("child2");
            if (elem_child2) {
                elem_child2.style.width = "";
            }
            
            let elem_modal = document.getElementById("rtSelectModal");
            if (elem_modal) {
                let modalDialog = elem_modal.getElementsByClassName("modal-dialog");
                if (modalDialog.length > 0) {
                    modalDialog[0].style.maxWidth = "";
                    modalDialog[0].style.width = "";
                }
            }
        },

        selectReportTemplate() {
            if (!confirm(this.$t("confirm.create"))) {
                this.hide();
            }
            
            this.resizeModalForReport();

            const url = this.$backendURL + '/'
                        + this.organizationId + '/mlComponents/'
                        + this.mlComponentId + '/testDescriptions/reportGeneratorFront'
            var request_param = null;
            if (this.select_reportTemplate_id == 0){
                 // レポートテンプレート無しの場合
                 request_param = {"Command": "Generate", "Destination": this.checkedItems_str}
            }
            else {
                // レポートテンプレート選択された場合
                request_param = {"Command": "Generate", "Destination": this.checkedItems_str,
                                 "Params": {"TargetReportTemplateId": this.select_reportTemplate_id}}
            }

            // レポート見解をセット
            if (sessionStorage.getItem('reportOpinion') != 'null') {
                this.opinion = sessionStorage.getItem('reportOpinion');
            }

            //リクエスト時のオプションの定義
            const config = {
                headers:{
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRF-TOKEN' : this.getCookie("csrf_access_token")
                },
                withCredentials:true,
            }

            // レポート生成
            this.$axios.post(url, request_param, config)
            .then((response) => {
                this.generateReport = response.data;
                this.previewer =  {
                    src: this.generateReport.OutParams.ReportUrl,
                    page_current: 1,
                    page_end: null,
                };
                // PDFの読み込み
                const { pdf, pages } = usePDF(this.previewer.src)
                this.pdf = pdf
                this.pages = pages
                this.previewer.page_end = pages
            })
            .catch((error) => {
                this.$router.push({
                    name: 'Information',
                    query: {error: JSON.stringify({...error, response: error.response})}
                })
            })
        },
        /**
         * テンプレート作成時にモーダルの大きさを変更する処理
         */
        resizeModalForReport() {
            let elem_parent = document.getElementById("parent");
            if (elem_parent) {
                elem_parent.style.width = "1200px";
            }
            
            let elem_child1 = document.getElementById("child1");
            if (elem_child1) {
                elem_child1.style.width = "600px";
            }
            
            let elem_child2 = document.getElementById("child2");
            if (elem_child2) {
                elem_child2.style.width = "600px";
            }
            
            let elem_modal = document.getElementById("rtSelectModal");
            if (elem_modal) {
                let modalDialog = elem_modal.getElementsByClassName("modal-dialog");
                if (modalDialog.length > 0) {
                    modalDialog[0].style.maxWidth = "1230px";
                    modalDialog[0].style.width = "1230px";
                }
            }
        },
        downloadReport(){
            if (!confirm(this.$t("confirm.create"))) {
                this.hide();
                return;
            }

            // レポート見解を登録
            var url = this.$backendURL + '/'
                        + this.organizationId + '/mlComponents/'
                        + this.mlComponentId + '/report_opinion_front'
            this.previewRequestData.ReportOpinion = this.opinion;
            //リクエスト時のオプションの定義
            const config = {
                headers:{
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRF-TOKEN' : this.getCookie("csrf_access_token")
                },
                withCredentials:true,
            }
            this.$axios.put(url, this.previewRequestData, config).then((response) => {
                this.result = response.data;

                // レポート見解登録が終了したら、レポートダウンロード
                url = this.$backendURL + '/'
                            + this.organizationId + '/mlComponents/'
                            + this.mlComponentId + '/testDescriptions/reportGeneratorFront'
                var request_param = null;
                if (this.select_reportTemplate_id == 0){
                    // レポートテンプレート無しの場合
                    request_param = {"Command": "Generate", "Destination": this.checkedItems_str}
                }
                else {
                    // レポートテンプレート選択された場合
                    request_param = {"Command": "Generate", "Destination": this.checkedItems_str,
                                    "Params": {"TargetReportTemplateId": this.select_reportTemplate_id}}
                }
                //リクエスト時のオプションの定義
                const config = {
                    headers:{
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRF-TOKEN' : this.getCookie("csrf_access_token")
                    },
                    withCredentials:true,
                }
                this.$axios.post(url, request_param, config)
                .then((response) => {
                    this.generateReport = response.data;
                    this.previewer =  {
                        src: this.generateReport.OutParams.ReportUrl,
                        page_current: 1,
                        page_end: null,
                    };
                    // PDFの読み込み
                    const { pdf, pages } = usePDF(this.previewer.src)
                    this.pdf = pdf
                    this.pages = pages
                    this.previewer.page_end = pages
                    const link = document.createElement('a');
                    link.href = this.generateReport.OutParams.ReportUrl;
                    link.click();
                })
                .catch((error) => {
                    this.$router.push({
                        name: 'Information',
                        query: {error: JSON.stringify({...error, response: error.response})}
                    })
                })

            })
            .catch((error) => {
                this.$router.push({
                    name: 'Information',
                    query: {error: JSON.stringify({...error, response: error.response})}
                })
            })
        },
        reportCancel() {
            if (confirm(this.$t("confirm.loseInformation"))) {
                this.hide();
            }
        },
        prevPage() {
            this.previewer.page_current -= 1;
        },
        nextPage() {
            this.previewer.page_current += 1;
        }
    },
    errorCaptured() {
        return false
    },
};
</script>

<style scoped>

.modalContents :deep(.vm--modal) {
    position: absolute !important;
    top: 5% !important;
    background-color: var(--gray-thema);
    border-radius: 5px;
}
.modalContents :deep(.vm--modal.preview) {
    left: 15% !important;
    width: auto !important;
    height: 92% !important;
    overflow-y: scroll !important;
}
.rts_modal_subtitle {
    font-weight: bold;
    font-size: 1rem;
    color: white;
}
.rts_modal_descriptions {
    font-size: 0.85rem;
    color: black;
    text-align: left;
}
.rts_modal_subtitle2 {
    font-size: 0.85rem;
    color: black;
    text-align: left;
    border-radius: 5px;
}
.title_area{
    background: var(--secondary-color);
    width: 100%;
    border-radius: 5px;
}
.title_area label {
    height: 2.5rem;
    font-weight: bold;
    font-size: 1rem;
    color: white;
    display: flex;
    align-items: center;
    padding-left: 0.5rem;
}
.title_area2{
    background: var(--secondary-color);
    width: 100%;
    border-radius: 5px;
}
.title_area2 label {
    height: 2.5rem;
    font-weight: bold;
    font-size: 1rem;
    color: white;
}
.info_area{
    width: 100%;
    display: flex;
}

#parent{
    display:flex;
    flex-direction: column
}
#child1 {
    display: inline-block;
    margin-right: 1rem;
    margin-left: 1rem;
    flex-grow: 1;
}
#child2 {
    display: inline-block;
    margin-left: 1rem;
    margin-right: 1rem;
    flex-grow: 1;
    height: 95%;
}
#pdf_wrapper {
    border: 1px solid #ccc;
}
.annotationLayer {
    overflow: auto;
}
.part1 table {
    text-align: center;
    border-collapse: separate;
    border-spacing: 0 5px;
    background-color: unset;
    border: none;
    width: 90%;
}
.part1 table tr {
    border-radius: 5px;

}
.part1 table tr td:nth-child(1){
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
    background: var(--primary-color) !important;
    min-height: 2rem;
    color: white;
}
.part1 table tr td:last-child{
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
    min-height: 2rem;
    color: white;
    background: white;
}
.part1 table tr td:last-child select {
    border: none;
    background: white;
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
    width: 100%;
    min-height: 2rem;
}
#child1 textarea {
    border-radius: 5px;
}
#btn_set2 {
    margin: 1rem;
    display: flex;
    justify-content: center;
}


</style>

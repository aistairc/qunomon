<template>
<div id="app">
    <modal name="rtSelectModal" class="modalContents">
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
                                        <option v-for="reportTemplate in reportTemplates" :key="reportTemplate.Id" v-bind:value="reportTemplate.Id">
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
                        <textarea class="z-depth__" name="example" cols="70" rows="15" v-model="opinion" style="overflow:auto;"></textarea>
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
                            <pdf
                                    :src="previewer.src"
                                    @num-pages="previewer.page_end = $event"
                                    :page="previewer.page_current"

                            ></pdf>
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
    </modal>
</div>
</template>

<script>
import { urlParameterMixin } from '../mixins/urlParameterMixin';
import { AccountControlMixin } from '../mixins/AccountControlMixin';
import { csrfMixin } from '../mixins/csrfMixin';
import pdf from 'vue-pdf';

export default {
    components: {
        pdf
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
            opinion: ''
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
            this.$modal.show('rtSelectModal');
        },
        hide() {
            this.previewer = null;
            this.$modal.hide('rtSelectModal');
            this.$emit('reset');
        },

        selectReportTemplate() {
            if (!confirm(this.$t("confirm.create"))) {
                this.hide();
            }
            const url = this.$backendURL + '/'
                        + this.organizationId + '/mlComponents/'
                        + this.mlComponentId + '/testDescriotions/reportGeneratorFront'
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

            // 画面サイズ変更
            var elem_parent = document.getElementById("parent");
            elem_parent.style.width = "1200px"
            var elem_child1 = document.getElementById("child1");
            elem_child1.style.width = "600px"
            var elem_child2 = document.getElementById("child2");
            elem_child2.style.width = "600px"
            var elem_modal = document.getElementsByClassName("vm--modal");
            if (!elem_modal.item(0).classList.contains("preview")) {
                elem_modal.item(0).classList.add("preview");
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
            })
            .catch((error) => {
                this.$router.push({
                    name: 'Information',
                    params: {error}
                })
            })
        },
        downloadReport(){
            if (!confirm(this.$t("confirm.create"))) {
                this.hide();
            }
            // レポート見解を登録
            var url = this.$backendURL + '/'
                        + this.organizationId + '/mlComponents/'
                        + this.mlComponentId + '/report_opinion'
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
                            + this.mlComponentId + '/testDescriotions/reportGeneratorFront'
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
                    const link = document.createElement('a');
                    link.href = this.generateReport.OutParams.ReportUrl;
                    link.click();
                })
                .catch((error) => {
                    this.$router.push({
                        name: 'Information',
                        params: {error}
                    })
                })

            })
            .catch((error) => {
                this.$router.push({
                    name: 'Information',
                    params: {error}
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

.modalContents>>>.vm--modal {
    position: absolute !important;
    top: 5% !important;
    background-color: #f0f0f0;
    border-radius: 5px;
}
.modalContents>>>.vm--modal.preview {
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
    background: #dc722b;
    width: 100%;
}
.title_area label {
    height: 2.5rem;
    font-weight: bold;
    font-size: 1rem;
    color: white;
}
.title_area2{
    background: #dc722b;
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
    background: #43645b !important;
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
    margin-bottom: 1rem;
}


</style>

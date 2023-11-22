<template>
    <div id="app">
        <div class="search_table_option">
            <template v-if="$i18n.locale === 'en'">
                <input type="submit" v-on:click="show" value="Create" id="openModal" class="btn_single_test">
            </template>
            <template v-else>
                <input type="submit" v-on:click="show" value="作成" id="openModal" class="btn_single_test">
            </template>
        </div>
        <modal name="mlcCreateModal" class="modalContents">
            <div class="subtitleArea">
                <span class="subtitle">{{$t("mlComponentCreate.title")}}</span>
                <span id="asterisk"><span class="error">&#042;</span> {{$t("common.require")}}</span>
            </div>
            <div class="error">
                <ui v-for="errorMessage in errorMessages" v-bind:key="errorMessage.text">
                    <li class="error_message">{{errorMessage}}</li>
                </ui>
            </div>
            <!--テキストボックス-->
            <div class="input">
                <form class="formCreate">
                    <div class="formDetail">
                        <label class="eachTitle">{{$t("mlComponentCreate.generalInformation")}}</label>
                        <table>
                            <tr>
                                <td class="label">{{$t("mlComponentCreate.name")}}<span class="error">&#042;</span></td>
                                <td>
                                    <template v-if="$i18n.locale === 'en'">
                                        <input class="defaultStyleInput" type="text" placeholder="Enter MLComponent Name" name="project_name" v-model="name">
                                    </template>
                                    <template v-else>
                                        <input class="defaultStyleInput" type="text" placeholder="MLコンポーネントを入力してください" name="project_name" v-model="name">
                                    </template>
                                </td>
                            </tr>
                            <tr>
                                <td class="label">{{$t("mlComponentCreate.description")}}<span class="error">&#042;</span></td>
                                <td><textarea class="defaultStyleInput" name="example" cols="30" rows="3" v-model="description"></textarea></td>
                            </tr>
                            <tr>
                                <td class="label">{{$t("mlComponentCreate.problemDomain")}}<span class="error">&#042;</span></td>
                                <td>
                                    <template v-if="$i18n.locale === 'en'">
                                        <input class="defaultStyleInput" type="text" placeholder="Enter ProblemDomain" name="project_detail" v-model="problem_domain">
                                    </template>
                                    <template v-else>
                                        <input class="defaultStyleInput" type="text" placeholder="問題領域を入力してください" name="project_detail" v-model="problem_domain">
                                    </template>
                                </td>
                            </tr>
                        </table>
                    </div>
                    <div class="formDetail">
                        <label class="eachTitle">{{$t("mlComponentCreate.guidelineInformation")}}</label>
                        <table>
                            <tr>
                                <td class="label">{{$t("mlComponentCreate.guidelineName")}}<span class="error">&#042;</span></td>
                                <td>
                                    <select class="defaultStyleSelect" v-model="select_guideline_id" v-on:change="setScopeList">
                                        <option value="" hidden>--Please Select--</option>
                                        <option v-for="guideline in guidelines" :key="guideline.Id" v-bind:value="guideline.Id">
                                            {{guideline.Name}}
                                        </option>
                                    </select>
                                </td>
                            </tr>
                            <tr>
                                <td class="label"><label class="labelTest">{{$t("mlComponentCreate.guidelineChoosingReason")}}</label></td>
                                <td><textarea class="defaultStyleInput" name="example" cols="30" rows="3" v-model="guideline_reason"></textarea></td>
                            </tr>
                        </table>

                    </div>
                    <div class="formDetail">
                        <label class="eachTitle">{{$t("mlComponentCreate.scopeInformation")}}</label>
                        <table>
                            <tr>
                                <td class="label">{{$t("mlComponentCreate.scopeName")}}<span class="error">&#042;</span></td>
                                <td>
                                    <select class="defaultStyleSelect" v-model="select_scope_id">
                                        <option value="" hidden>--Please Select--</option>
                                        <option v-for="scope in scopes" :key="scope.Id" v-bind:value="scope.Id">
                                            {{scope.Name}}
                                        </option>
                                    </select>
                                </td>
                            </tr>
                            <tr>
                                <td class="label"><label class="labelTest">{{$t("mlComponentCreate.scopeChoosingReason")}}</label></td>
                                <td><textarea class="defaultStyleInput" name="example" cols="30" rows="3" v-model="scope_reason"></textarea></td>
                            </tr>
                        </table>

                    </div>
                    <div id="btn_set">
                        <template v-if="$i18n.locale === 'en'">
                            <input type="button" value="Cancel" class="btn_left" @click="postMLComponentCancel">
                            <template v-if="edit_flag === true">
                                <input type="button" value="Update" class="btn_right" @click="putMLComponent">
                            </template>
                            <template v-else>
                                <input type="button" value="Create" class="btn_right" @click="postMLComponent">
                            </template>
                        </template>
                        <template v-else>
                            <input type="button" value="キャンセル" class="btn_left" @click="postMLComponentCancel">
                            <template v-if="edit_flag === true">
                                <input type="button" value="更新" class="btn_right" @click="putMLComponent">
                            </template>
                            <template v-else>
                                <input type="button" value="作成" class="btn_right" @click="postMLComponent">
                            </template>
                        </template>
                    </div>
                </form>
            </div>
            <div id="closeModal" class="closeModal" @click="postMLComponentCancel">
                ×
            </div>
        </modal>
    </div>
</template>

<script>
import { urlParameterMixin } from '../mixins/urlParameterMixin';
import { MLComponentMixin } from '../mixins/MLComponentMixin';
import { AccountControlMixin } from '../mixins/AccountControlMixin';
import { csrfMixin } from '../mixins/csrfMixin';

export default {
    data() {
        return {
            mlComponentId: null,
            edit_flag: false
        }
    },
    mixins: [urlParameterMixin, MLComponentMixin, AccountControlMixin, csrfMixin],
    mounted: function () {
        this.getGuidelines();
        this.getScopes();
    },
    methods: {
        show() {
            this.$modal.show('mlcCreateModal');
        },
        hide() {
            this.$modal.hide('mlcCreateModal');
            this.$emit('reset');
        },
        postMLComponent() {
            this.errorMessages = [];
            this.commonCheckMLComponent();
            this.organizationIdCheck_method();
            this.organizationIdCheck = sessionStorage.getItem('organizationId');
            if (this.errorMessages.length === 0) {
                this.dispErrorMessage = "";
                if (confirm(this.$t("confirm.create"))) {
                    this.setMLComponent();
                    const url = this.$backendURL +
                        '/' +
                        this.organizationIdCheck +
                        '/mlComponentsFront'
                    //リクエスト時のオプションの定義
                    const config = {
                        headers:{
                            'X-Requested-With': 'XMLHttpRequest',
                            'X-CSRF-TOKEN' : this.getCookie("csrf_access_token")
                        },
                        withCredentials:true,
                    }
                    this.$axios.post(url, this.requestData, config)
                        .then((response) => {
                            this.result = response.data;
                            this.$emit('createMLC');
                            this.hide();
                        })
                        .catch((error) => {
                            this.$router.push({
                                name: 'Information',
                                params: {
                                    error
                                }
                            })
                        })
                }
            } else {
                scrollTo(0, 0);
            }
        },
        postMLComponentCancel() {
            if (confirm(this.$t("confirm.loseInformation"))) {
                this.hide();
            }
        },
        editShow(inputMlcId,
                 inputMlcName,
                 inputDescription,
                 inputDomain,
                 inputGdName,
                 inputScName,
                 inputGuidelineReason,
                 inputScopeReason) {
            this.edit_flag = true;
            this.mlComponentId = inputMlcId;
            this.name = inputMlcName;
            this.description = inputDescription;
            this.problem_domain = inputDomain;
            // guidelineIdの設定
            for (var gd of this.guidelines) {
                if (inputGdName == gd.Name){
                    this.select_guideline_id = gd.Id;
                    break;
                }
            }
            // scopeIdの設定
            this.setScopeList();
            for (var sc of this.scopes) {
                if (inputScName == sc.Name){
                    this.select_scope_id = sc.Id;
                    break;
                }
            }
            this.guideline_reason = inputGuidelineReason;
            this.scope_reason = inputScopeReason;
            this.$modal.show('mlcCreateModal');
        },
        putMLComponent() {
            this.errorMessages = [];
            this.commonCheckMLComponent();
            this.organizationIdCheck_method();
            this.organizationIdCheck = sessionStorage.getItem('organizationId');
            if (this.errorMessages.length === 0) {
                this.dispErrorMessage = "";
                if (confirm(this.$t("confirm.edit"))) {
                    this.setMLComponent();
                    const url = this.$backendURL +
                        '/' +
                        this.organizationIdCheck +
                        '/mlComponents/' +
                        this.mlComponentId
                    //リクエスト時のオプションの定義
                    const config = {
                        headers:{
                            'X-Requested-With': 'XMLHttpRequest',
                            'X-CSRF-TOKEN' : this.getCookie("csrf_access_token")
                        },
                        withCredentials:true,
                    }
                    this.$axios.put(url, this.requestData, config)
                        .then((response) => {
                            this.result = response.data;
                            this.$emit('createMLC');
                            this.hide();
                        })
                        .catch((error) => {
                            this.$router.push({
                                name: 'Information',
                                params: {
                                    error
                                }
                            })
                        })
                }
            } else {
                scrollTo(0, 0);
            }
        },
        putMLComponentCancel() {
            if (confirm(this.$t("confirm.loseInformation"))) {
                this.hide();
            }
        },
    },
};
</script>

<style scoped>

.search_table_option {
    display: flex;
    float: right;
}
.search_table_option input {
    background-color: #a9c7aa;
    color: black;
    border: none;
    height: 2rem;
    width: 10rem;
    text-align: center;
    text-decoration: none;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    border-radius: 5px;
    z-index: 10;
}
.search_table_option input:hover {
    color: white;
    background: #43645b !important;
}

.modalContents>>>.vm--modal {
    position: absolute !important;
    top: 10% !important;
    /*left: 22% !important;*/
    width: 32% !important;
    height: 65% !important;
    /*padding: 15px 0px !important;*/
    background-color: #f0f0f0;
    border-radius: 10px;
    overflow-y: auto;
}

.subtitleArea {
    background-color: #dc722b;
    color: #ffffff;
    border-top-right-radius: 5px;
    border-top-left-radius: 5px;
    margin: 0;
    width: 100%;
    height: 2.5rem;
    font-weight: bold;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.subtitle {
    color: white;
    font-size: 1rem;
    font-weight: bold;
}
#asterisk {
    color: red;
    font-size: 0.85rem;
}
.formDetail {
    background: white !important;
    margin: 1rem 0;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Add a box shadow for depth */
}

.formDetail table {
    text-align: center;
    border-collapse: separate;
    border-spacing: 0 5px;
    background-color: unset;
    border: none;
    width: 100%;
    font-size: 0.85rem;
}
.formDetail table tr td{
    height: 2rem;
}
.formDetail table tr td input,
.formDetail table tr td select,
.formDetail table tr td textarea{
    width: 100%;
    height: 100%;
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
    background: #f0f0f0;
}

.formDetail table tr td:nth-child(1) {
    width: 40%;
    background: #43645b;
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
    font-weight: bold;
    color: white;
}
.formDetail table tr td:last-child {
    width: 60%;
    background: #f0f0f0;
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
}
.eachTitle {
    height: 2rem;
    display: flex;
    font-size: 1rem;
    font-weight: bold;
    color: white;
    text-align: center;
    width: 100%;
    background-color: #dc722b;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    align-items: center;
}
@media ( max-width: 767px ){
    .defaultStyleInput {
        border-radius: 5px;
        max-width: 2rem;
        min-height: 2rem;
        background: white;
    }
    .defaultStyleSelect {
        /*display: inline-block;*/
        font-size: 15px;
        padding: 4px;
        max-width: 2rem;
        border: none;
        border-radius: 5px;
        min-height: 2rem;
    }
}


</style>

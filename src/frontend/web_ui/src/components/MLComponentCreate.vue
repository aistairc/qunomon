<template>
<div id="app">
    <div class="btn">
        <template v-if="$i18n.locale === 'en'">
            <input type="submit" v-on:click="show" value="Create" id="openModal" class="btn_single">
        </template>
        <template v-else>
            <input type="submit" v-on:click="show" value="作成" id="openModal" class="btn_single">
        </template>
    </div>
    <modal name="mlcCreateModal" class="modalContents">
        <span class="mlc_modal_subtitle">{{$t("mlComponentCreate.general")}}</span>
        <div class="error">
            <ui v-for="errorMessage in errorMessages" v-bind:key="errorMessage.text">
                <li class="error_message">{{errorMessage}}</li>
            </ui>
        </div>
        <p id="asterisk"><span class="requiredAsterisk">&#042;</span> {{$t("common.require")}}</p>
        <!--テキストボックス-->
        <div class="input">
            <form class="formCreate">
                <dl>
                    <dt class="label">{{$t("mlComponentCreate.name")}}<span class="error">&#042;</span></dt>
                    <template v-if="$i18n.locale === 'en'">
                        <dd><input class="z-depth__" type="text" placeholder="Enter MLComponent Name" name="project_name" v-model="name"></dd>
                    </template>
                    <template v-else>
                        <dd><input class="z-depth__" type="text" placeholder="MLコンポーネントを入力してください" name="project_name" v-model="name"></dd>
                    </template>
                </dl>
                <dl>
                    <dt class="label">{{$t("mlComponentCreate.description")}}<span class="error">&#042;</span></dt>
                    <dd><textarea class="z-depth__" name="example" cols="50" rows="6" v-model="description"></textarea></dd>
                </dl>
                <dl>
                    <dt class="label">{{$t("mlComponentCreate.problemDomain")}}<span class="error">&#042;</span></dt>
                    <template v-if="$i18n.locale === 'en'">
                        <dd><input class="z-depth__" type="text" placeholder="Enter ProblemDomain" name="project_detail" v-model="problem_domain"></dd>
                    </template>
                    <template v-else>
                        <dd><input class="z-depth__" type="text" placeholder="問題領域を入力してください" name="project_detail" v-model="problem_domain"></dd>
                    </template>
                </dl>
                <dl>
                    <dt class="label">{{$t("mlComponentCreate.mlFrameworkName")}}<span class="error">&#042;</span></dt>
                    <dd>
                        <select class="select" v-model="select_ml_framework_id">
                            <option value="" hidden style="color:gray">--Please Select--</option>
                            <option v-for="framework in mlFrameworks" :key="framework.Id" v-bind:value="framework.Id">
                                {{framework.Name}}
                            </option>
                        </select>
                    </dd>
                </dl>
                <div id="btn_set">
                    <template v-if="$i18n.locale === 'en'">
                        <input type="button" value="Cancel" class="btn_left" @click="postMLComponentCancel">
                        <input type="button" value="Create" class="btn_right" @click="postMLComponent">
                    </template>
                    <template v-else>
                        <input type="button" value="キャンセル" class="btn_left" @click="postMLComponentCancel">
                        <input type="button" value="作成" class="btn_right" @click="postMLComponent">
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
import {
    urlParameterMixin
} from '../mixins/urlParameterMixin';
import {
    MLComponentMixin
} from '../mixins/MLComponentMixin';
export default {
    data() {
        return {}
    },
    mixins: [urlParameterMixin, MLComponentMixin],
    mounted: function () {
        this.organizationIdCheck();
        this.organizationId = sessionStorage.getItem('organizationId');
        this.getMLFrameworks();
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
            if (this.errorMessages.length === 0) {
                this.dispErrorMessage = "";
                if (confirm("作成してよろしいですか？")) {
                    this.setMLComponent();
                    const url = this.$backendURL +
                        '/' +
                        this.organizationId +
                        '/mlComponents'
                    this.$axios.post(url, this.requestData)
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
            if (confirm("入力した内容が失われますがよろしいですか？")) {
                this.hide();
            }
        }
    },
};
</script>

<style scoped>
.mlc_modal_subtitle {
    display: inline-block;
    font-size: 20px;
    color: #000066;
    margin-top: 30px;
    margin-bottom: 10px;
    text-align: left;
    width: 100%;
}

#openModal {
    position: relative;
    top: 52px;
    right: 24px;
    z-index: 1;
}

.modalContents>>>.vm--modal {
    text-align: left;
    position: absolute !important;
    top: 10% !important;
    left: 22% !important;
    width: 733px !important;
    height: auto !important;
    padding: 15px 30px !important;
    background-color: #f0f0f0;
}

.el-modal {
    visibility: hidden;
}

.el-modal[aria-hidden=false] {
    visibility: visible;
}

input[type="text"] {
    width: 300px;
}

dl {
    margin-right: 20px;
}

.modalContents dt {
    width: 200px;
    /*ラベルの幅 文字数に合わせる*/
    margin-left: 50px;
    /*ラベルの位置 テーブルやリストに合わせる*/
    float: left;
}

.modalContents span {
    margin-left: 20px;
}

.modalContents dl {
    margin-bottom: 20px;
}

.req {
    font-size: 100%
}

#asterisk {
    top: 95px;
    margin-left: 50px;
    font-size: 14px;
}

.requiredAsterisk {
    color: red;
    margin-left: 40px;
}

.error {
    border: 0px;
    padding: 0px;
    margin-left: 40px;
}

.error_message {
    word-break: break-all;
}

.modalContents .margin {
    text-align: left;
    margin-left: 50px;
    margin-bottom: 0px;
}

.modalWrapper {
    height: auto;
    width: 50%;
}
</style>

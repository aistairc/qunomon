<template>
    <div id="app">
        <div class="search_table_option">
            <template v-if="$i18n.locale === 'en'">
                <input type="submit" v-on:click="show" value="Create" id="openModal" class="btn_single_test" />
            </template>
            <template v-else>
                <input type="submit" v-on:click="show" value="作成" id="openModal" class="btn_single_test" />
            </template>
        </div>
        <modal name="inventoryCreateModal" class="modalContents">
            <div class="subtitleArea">
                <span class="subtitle">{{$t("inventoryAppend.mes")}}</span>
                <span id="asterisk"><span class="error">&#042;</span> {{$t("common.require")}}</span>
            </div>
            <div class="error">
                <ui v-for="errorMessage in errorMessages" v-bind:key="errorMessage.text">
                    <li class="error_message">{{ errorMessage }}</li>
                </ui>
            </div>

            <!--テキストボックス-->
            <div class="input">
                <form class="formCreate">
                    <div class="formDetail">
                        <dl>
                            <dt class="label">{{$t("inventoryAppend.name")}}<span class="error">&#042;</span></dt>
                            <dd>
                                <template v-if="$i18n.locale === 'en'">
                                    <dd><input class="defaultStyleInput" type="text" size="30" placeholder="Enter Inventory Name" name="project_name" v-model="name" /></dd>
                                </template>
                                <template v-else>
                                    <dd><input class="defaultStyleInput" type="text" size="30" placeholder="インベントリ名を入力してください" name="project_name" v-model="name"/></dd>
                                </template>
                            </dd>
                        </dl>
                        <dl>
                            <dt class="label">{{$t("inventoryAppend.filePath")}}<span class="error">&#042;</span></dt>
                            <dd>
                                <template v-if="$i18n.locale === 'en'">
                                    <dd><input class="defaultStyleInput" type="text" size="30" placeholder="Enter Path" name="file_path" v-model="filePath" /></dd>
                                </template>
                                <template v-else>
                                    <dd><input class="defaultStyleInput" type="text" size="30" placeholder="パスを入力してください" name="file_path" v-model="filePath" /></dd>
                                </template>
                            </dd>
                        </dl>
                        <dl>
                            <dt class="label">{{$t("inventoryAppend.dataType")}}<span class="error">&#042;</span></dt>
                            <dd>
                                <select class="defaultStyleSelect" v-model="selectedType">
                                    <option value="" hidden style="color: gray">
                                        {{$t("common.defaultPulldown")}}
                                    </option>
                                    <option v-for="dataType in dataTypes" :key="dataType.Id" v-bind:value="dataType.Id">
                                        {{ dataType.Name }}
                                    </option>
                                </select>
                            </dd>
                        </dl>
                        <dl>
                            <dt class="label">{{$t("inventoryAppend.format")}}<span class="error">&#042;</span></dt>
                            <dd>
                                <VueSelect  class="vueselect"
                                            :options="formats"
                                            v-model="selectedFormat"
                                            taggable
                                            >
                                </VueSelect>
                            </dd>
                        </dl>
                        <dl>
                            <dt class="label">{{$t("inventoryAppend.description")}}</dt>
                            <dd>
                                <textarea class="defaultStyleInput" name="example" cols="50" rows="6" v-model="description"></textarea>
                            </dd>
                        </dl>

                    </div>
                    <div id="btn_set">
                        <template v-if="$i18n.locale === 'en'">
                            <input type="button" value="Cancel" class="btn_left" @click="postInventoryCancel" />
                            <input type="button" value="Create" class="btn_right" @click="postInventory" />
                        </template>
                        <template v-else>
                            <input type="button" value="キャンセル" class="btn_left" @click="postInventoryCancel" />
                            <input type="button" value="作成" class="btn_right" @click="postInventory" />
                        </template>
                    </div>
                </form>
            </div>
            <div id="closeModal" class="closeModal" @click="postInventoryCancel">
                ×
            </div>
        </modal>
    </div>
</template>

<script>
import {
    inventoryMixin
} from "../mixins/inventoryMixin";
import {
    urlParameterMixin
} from "../mixins/urlParameterMixin";
import { csrfMixin } from '../mixins/csrfMixin';
import { VueSelect } from "vue-select";
import "vue-select/dist/vue-select.css";

export default {
    mixins: [inventoryMixin, urlParameterMixin, csrfMixin],
    mounted() {
        this.mlComponentIdCheck();
        this.organizationIdCheck = sessionStorage.getItem("organizationId");
        this.mlComponentId = sessionStorage.getItem("mlComponentId");
        this.getMLComponent();
        this.getDataTypes();
        this.getFormats();
    },
    components: {
        VueSelect
    },
    methods: {
        show() {
            this.clearInputInventory();
            this.$modal.show("inventoryCreateModal");
        },
        hide() {
            this.clearInputInventory();
            this.$modal.hide("inventoryCreateModal");
        },
        postInventory() {
            this.errorMessages = [];
            this.commonCheckInventory();
            if (this.errorMessages.length === 0) {
                if (confirm(this.$t("confirm.create"))) {
                    this.setInventory();
                    const url = this.$backendURL +
                        "/" +
                        this.organizationIdCheck +
                        "/mlComponents/" +
                        this.mlComponentId +
                        "/inventoriesFront"
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
                            this.$emit("createInventory");
                            this.hide();

                            this.result = response.data;
                            this.clearInputInventory();
                            if (this.$route.params.testDescriptionId) {
                                this.$router.push({
                                    name: this.$route.params.history,
                                    params: {
                                        testDescriptionId: this.$route.params.testDescriptionId,
                                        previousPageSettingData: this.$route.params.previousPageSettingData
                                    }
                                })
                            } else if (this.$route.params.history != null) {
                                this.$router.push({
                                    name: this.$route.params.history,
                                    params: {
                                        previousPageSettingData: this.$route.params.previousPageSettingData
                                    }
                                })
                            } else {
                                this.$router.push({
                                    name: 'Inventories'
                                })
                            }
                        })
                        .catch((error) => {
                            if (this.checkAndWarnInventoryError(error.response.data)){
                                return;
                            }

                            this.$router.push({
                                name: "Information",
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
        cancel() {
            if (this.$route.params.testDescriptionId != null) {
                this.$router.push({
                    name: this.$route.params.history,
                    params: {
                        testDescriptionId: this.$route.params.testDescriptionId,
                        previousPageSettingData: this.$route.params.previousPageSettingData,
                    },
                });
            } else if (this.$route.params.history != null) {
                this.$router.push({
                    name: this.$route.params.history,
                    params: {
                        previousPageSettingData: this.$route.params.previousPageSettingData,
                    },
                });
            } else {
                this.$router.push({
                    name: "Inventories",
                });
            }
        },
        postInventoryCancel() {
            if (confirm(this.$t("confirm.loseInformation"))) {
                this.hide();
            }
        },
        clearInputInventory(){
            this.name = "";
            this.filePath = "";
            this.selectDatatype = "";
            this.selectedFormat = "";
            this.description = "";
            this.errorMessages = [];
        }
    },
};
</script>

<style scoped>

.subtitleArea {
    background-color: #dc722b;
    color: #ffffff;
    border-top-right-radius: 5px;
    border-top-left-radius: 5px;
    margin: 0;
    width: 100%;
    height: 3rem;
    font-weight: bold;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}


.formDetail {
    background: white !important;
    margin: 1rem 0;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Add a box shadow for depth */

}
.formDetail dl {
    padding-top: 0.5rem;
    display: flex;
}
.formDetail dt {
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
    margin-left: 1rem;
    font-size: 0.85rem;
    font-weight: bold;
    flex-basis: 30%;
    background: #43645b;
    display: flex;
    flex-direction: row-reverse;
    align-items: center;
    justify-content: center;
    color: white;
}
.formDetail dd {
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
    margin-right: 1rem;
    flex-basis: 70%;
    margin-bottom: unset;
    height: 100%;
    text-align: left;
    width: 100%;
    border: 1px solid;
    min-height: 2rem;
    border-color: #43645b;
}
.formDetail dl dd textarea {
    width: 100%;
    height: 100%;
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
}


.modalContents>>>.vm--modal {
    position: absolute !important;
    top: 10% !important;
    /*left: 22% !important;*/
    width: 32% !important;
    height: 52% !important;
    /*padding: 15px 0px !important;*/
    background-color: #f0f0f0;
    border-radius: 10px;
    overflow-y: auto;
}




#btn_set {
    margin-bottom: 10px;
}

.vueselect {
    width: 100%;
    font-size: 0.85rem;
    cursor: pointer;
    border:none;
}
.search_table_option {
    display: flex;
    float: right;
}


.search_table_option input {
    background-color: #a9c7aa;
    color: black;
    border: none;
    height: 2rem;
    /*margin-right: 1rem;*/
    width: 10rem;
    text-align: center;
    text-decoration: none;
    /*display: inline-block;*/
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    border-radius: 5px;
    z-index: 10;
    /*margin-right: 1rem;*/
}

.search_table_option input:hover {
    color: white;
    background: #43645b !important;
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
.defaultStyleSelect {
    /*display: inline-block;*/
    font-size: 0.85rem;
    width: 100%;
    min-height: 2rem;
    cursor: pointer;
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
    border: none;
    background: unset;
}
.defaultStyleInput {
    font-size: 0.85rem;
    width: 100%;
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
    border: none;
}
</style>

<template>
<div>
    <BModal v-model="showModal" name="inventoryEditModal" class="modalContents" @hide="reset" no-footer no-header>
        <!--言語切り替えを実装する-->
        <div class="subtitleArea">
            <span class="subtitle">{{$t("inventoryEdit.mes")}}</span>
            <span id="asterisk" class="asterisk">&#042; {{$t("common.require")}}</span>
        </div>
        <div class="error">
            <ul v-for="errorMessage in errorMessages" v-bind:key="errorMessage.text">
                <li class="error_message">{{ errorMessage }}</li>
            </ul>
        </div>
        <!--テキストボックス-->
        <div class="input">
            <form class="formCreate">
                <div class="formDetail">
                    <dl>
                        <dt class="label">{{$t("inventoryEdit.name")}}<span class="error">&#042;</span></dt>
                        <dd>
                            <template v-if="$i18n.locale === 'en'">
                                <dd><input class="defaultStyleInput" type="text" size="30" placeholder="Enter Inventory Name" name="project_name" v-model="name" /></dd>
                            </template>
                            <template v-else>
                                <dd><input class="defaultStyleInput" type="text" size="30" placeholder="インベントリ名を入力してください" name="project_name" v-model="name" /></dd>
                            </template>
                        </dd>
                    </dl>
                    <dl>
                        <dt class="label"> {{$t("inventoryEdit.filePath")}}<span class="error">&#042;</span></dt>
                        <dd>
                            <template v-if="$i18n.locale === 'en'">
                                <dd><input  class="defaultStyleInput" type="text" size="50" placeholder="Enter Path" name="file_path" v-model="filePath" /></dd>
                            </template>
                            <template v-else>
                                <dd><input  class="defaultStyleInput" type="text" size="50" placeholder="パスを入力してください" name="file_path" v-model="filePath" /></dd>
                            </template>
                        </dd>
                    </dl>
                    <dl>
                        <dt class="label">{{$t("inventoryEdit.dataType")}}<span class="error">&#042;</span></dt>
                        <dd>
                            <select class="defaultStyleSelect" v-model="selectedType">
                                <option value="" hidden style="color: gray">
                                    {{$t("common.defaultPulldown")}}
                                </option>
                                <option v-for="dataType in dataTypes" v-bind:value="dataType.Id" :key="dataType.Id">
                                    {{ dataType.Name }}
                                </option>
                            </select>
                        </dd>
                    </dl>
                    <dl>
                        <dt class="label">{{$t("inventoryEdit.format")}}<span class="error">&#042;</span></dt>
                        <dd>
                            <multiselect :options="formats"
                                         v-model="selectedFormat"
                                         :taggable="true"
                                         >
                            </multiselect>
                        </dd>
                    </dl>
                    <dl>
                        <dt class="label">{{$t("inventoryEdit.description")}}</dt>
                        <dd>
                            <textarea class="defaultStyleInput" name="example" cols="50" rows="6" v-model="description"></textarea>
                        </dd>
                    </dl>
                </div>
                <div id="btn_set">
                    <template v-if="$i18n.locale === 'en'">
                        <input type="button" value="Cancel" class="btn_left" @click="postInventoryCancel" />
                        <input type="button" value="Update" class="btn_right" @click="postInventory" />
                    </template>
                    <template v-else>
                        <input type="button" value="キャンセル" class="btn_left" @click="postInventoryCancel" />
                        <input type="button" value="更新" class="btn_right" @click="postInventory" />
                    </template>
                </div>
            </form>
        </div>
        <div id="closeModal" class="closeModal" @click="postInventoryCancel">
            ×
        </div>
    </BModal>
</div>
</template>

<script>
import {
    inventoryMixin
} from '../mixins/inventoryMixin';
import {
    urlParameterMixin
} from '../mixins/urlParameterMixin';
import { csrfMixin } from '../mixins/csrfMixin';
import Multiselect from 'vue-multiselect';
import { BModal } from 'bootstrap-vue-next';

export default {
    mixins: [inventoryMixin, urlParameterMixin, csrfMixin],
    data() {
        return {
            targetInventory: null,
            inventoryId: null,
            showModal: false
        }
    },
    mounted() {
        this.mlComponentIdCheck();
        this.organizationIdCheck = sessionStorage.getItem('organizationId');
        this.mlComponentId = sessionStorage.getItem('mlComponentId');
        this.getMLComponent();
        this.getDataTypes();
        this.getFormats();
    },
    components: {
        Multiselect,
        BModal
    },
    methods: {
        show(inventoryId) {
            this.inventoryId = inventoryId;
            this.getInventory();
            this.showModal = true;
        },
        hide() {
            this.showModal = false;
        },
        reset() {
            this.$emit("reset");
        },
        postInventory() {
            this.errorMessages = [];
            this.commonCheckInventory();
            if (this.errorMessages.length === 0) {
                if (confirm(this.$t("confirm.edit"))) {
                    this.setInventory();
                    const url = this.$backendURL +
                        '/' +
                        this.organizationIdCheck +
                        '/mlComponents/' +
                        this.mlComponentId +
                        '/inventoriesFront/' +
                        this.inventoryId
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
                            this.$emit("createInventory");
                            this.hide();
                        })
                        .catch((error) => {
                            if (this.checkAndWarnInventoryError(error.response.data)){
                                return;
                            }

                            this.$router.push({
                                name: 'Information',
                                query: {error: JSON.stringify({...error, response: error.response})}
                            })
                        })
                }
            } else {
                scrollTo(0, 0);
            }
        },
        getInventory() {
            const url = this.$backendURL +
                '/' +
                this.organizationIdCheck +
                '/mlComponents/' +
                this.mlComponentId +
                '/inventories'
            this.$axios.get(url)
                .then((response) => {
                    for (var inventory of response.data.Inventories) {
                        if (inventory.Id == this.inventoryId) {
                            this.targetInventory = inventory;
                        }
                    }
                    this.name = this.targetInventory.Name;
                    this.filePath = this.targetInventory.FilePath;
                    this.selectedType = this.targetInventory.DataType.Id;
                    this.selectedFormat = this.targetInventory.Formats[0].Format;
                    this.description = this.targetInventory.Description;
                })  
                .catch((error) => {
                    /* eslint-disable no-console */
                    console.log(error)
                    this.$router.push({
                        name: 'Information'
                    })
                })
        },
        postInventoryCancel() {
            if (confirm(this.$t("confirm.loseInformation"))) {
                this.errorMessages = [];
                this.hide();
            }
        }
    }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style scoped>
.subtitleArea {
    background-color: var(--secondary-color);
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
.subtitle{
    color: #fff;
}
.asterisk {
    color: #ff0000;
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
    background: var(--primary-color);
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
    border-color: var(--primary-color);
}
.formDetail dl dd textarea {
    width: 100%;
    height: 100%;
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
}


.modalContents :deep(.vm--modal) {
    position: absolute !important;
    top: 10% !important;
    /*left: 22% !important;*/
    width: 32% !important;
    height: 52% !important;
    /*padding: 15px 0px !important;*/
    background-color: var(--gray-thema);
    border-radius: 10px;
    overflow-y: auto;
}


#btn_set {
    margin-bottom: 10px;
}

.search_table_option {
    display: flex;
    float: right;
}


.search_table_option input {
    background-color: var(--primary-color-light);
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
    background: var(--primary-color) !important;
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

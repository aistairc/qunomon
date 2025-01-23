<template>
    <div>
        <!--ヘッダータイトル-->
        <header id="head">
            <div id="title" :class="{ active: this.isActive }">
                <button @click="toggleSubmenu(isActive)" class="qq"><img :src="this.isActive ? this.icon2 : this.icon1" alt="Image" width="30" height="auto"></button>
                <h1 class="head_title">{{$t("common.titleGuidelineCreate")}}</h1>
            </div>
        </header>

        <!-- サブメニュー（左カラム） -->

        <SubMenu :isActive="this.isActive">
            <!--SubMenuのアイコンとメニューの間の言語項目は各コンポーネントで実施-->
            <!--言語ボタン■-->
            <div id="btn_language">
                <template v-if="$i18n.locale === 'en'">
                    <a href="#" v-on:click.prevent="changeLanguage('ja', screenName)" class="btn_unselect">{{$t("common.lanJa")}}</a>
                    <a href="#" class="btn_select">{{$t("common.lanEn")}}</a>
                </template>
                <template v-else>
                    <a href="#" class="btn_select">{{$t("common.lanJa")}}</a>
                    <a href="#" v-on:click.prevent="changeLanguage('en', screenName)" class="btn_unselect">{{$t("common.lanEn")}}</a>
                </template>
            </div>
        </SubMenu>


        <!-- ニュース（中央カラム） -->
        <div id="main" :class="{ active: this.isActive }">
            <div id="main_body">
                <div class="tittle">

                </div>
                <div class="accordion">
                        <div>
                            <p>{{$t("guidelineCreate.guidelineSample")}}</p>

                            <div class="error">
                                <ul v-for="errorMessage in errorMessages" v-bind:key="errorMessage">
                                    <li class="error_message">{{ errorMessage }}</li>
                                </ul>
                            </div>

                            <Vue3JsonEditor
                                v-model="json"
                                :show-btns="false"
                                :expandedOnStart="true"
                                :mode="'code'"
                                @json-change="onJsonChange"
                                @has-error="onHasError" />

                        </div>
                </div>
                <div v-if="jsonErrorMessage" class="json_error_message">{{ jsonErrorMessage }}</div>

                <!-- button -->
                <div class="btn_area">
                    <template v-if="$i18n.locale === 'en'">
                        <input type="button" value="Register" class="btn_left"
                               @click="guidelineCreate" />
                        <input type="button" value="Back" class="btn_left"
                               @click="guidelineBack" />
                    </template>
                    <template v-else>
                        <input type="button" value="登録" class="btn_right"
                               @click="guidelineCreate" />
                        <input type="button" value="戻る" class="btn_right"
                               @click="guidelineBack" />
                    </template>
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
import { GuidelinesMixin } from '../mixins/GuidelinesMixin';
import { AccountControlMixin } from '../mixins/AccountControlMixin';
import { csrfMixin } from '../mixins/csrfMixin';
import { Vue3JsonEditor } from 'vue3-json-editor'

export default {
    mixins: [subMenuMixin, urlParameterMixin, GuidelinesMixin, AccountControlMixin, csrfMixin],
    components: {
        SubMenu,
        Vue3JsonEditor
    },
    data() {
        return {
            screenName: 'guidelineCreate',
            json: {
                msg: 'demo of jsoneditor'
            },
            errorMessages : [],
            jsonErrorMessage: "",
        }
    },
    mounted: function () {
        this.setLanguageData();
        this.json = require('./guideline_sample/aiqm_guideline_schema.json');

        // エディタの高さを変える
        var editors = document.getElementsByClassName('jsoneditor-vue');
        for(var i = 0; i < editors.length; i++){
            editors[i].style.height = '700px';
        }
    },
    methods: {
        guidelineCreate(){
            this.errorMessages = [];
            // 入力値チェック
            this.guidelineValidationCheck(this.json, this.errorMessages);
            if (this.errorMessages.length === 0) {
                // 入力されたjsonデータを文字列にする
                const json_str = JSON.stringify(this.json, null, '    ');
                // ファイル形式にする
                const blob = new Blob([json_str],{type:"application/json"});
                const g_file = new File([blob], "guideline.json", { type: "application/json" });
                const fd = new FormData();
                fd.append("guideline_schema", g_file);
                fd.append("guideline_aithub_id", "");

                const url = this.$backendURL + '/guidelines/guideline_schema_file_front';
                //リクエスト時のオプションの定義
                const config = {
                    headers:{
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRF-TOKEN' : this.getCookie("csrf_access_token")
                    },
                    withCredentials:true,
                }
                this.$axios.post(url, fd, config)
                    .then((response) => {
                        this.result = response.data;
                        this.$router.push({
                            name: "Guidelines"
                        });
                    })
                    .catch((error) => {
                        this.$router.push({
                            name: 'Information',
                            query: {error: JSON.stringify({...error, response: error.response})}
                        })
                    })
            } else {
                scrollTo(0, 0);
            }
        },
        guidelineBack(){
            this.$router.push({
                name: "Guidelines"
            });
        },
        /**
         * JSONの値が変更された場合の処理
         * @param json JSONの値
         */
        onJsonChange(json){
            this.json = json;
            this.jsonErrorMessage = "";
        },
        /**
         * JSONの構文に誤りがある場合の処理
         */
        onHasError(){
            this.jsonErrorMessage = this.$t("guidelineCreate.errorMessage");
        }
    },
}
</script>


<style scoped>
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
    /*position: relative;*/
    z-index: 0;
}
.accordion {
    margin: 0 auto;
    padding-top: 2rem;
    width: 80%;
}
.tittle {
    margin: 0 auto;
    font-size: 2rem;
    width: 80%;
    /*background: red;*/
}

.btn_area {
    /*background-color: red;*/
    margin-top: 2rem;
    text-align: center;
}

/* JSONの構文に誤りがある場合のエラーメッセージ */
.json_error_message {
    text-align: center;
    word-break: break-all;
    color: #ff0000;
}

/*エラーメッセージ*/
.error_message {
    text-align: left;
    word-break: break-all;
    margin: 0px;
    color: #ff0000;
}

</style>
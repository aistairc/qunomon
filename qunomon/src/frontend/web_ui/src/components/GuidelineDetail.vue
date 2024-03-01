<template>
    <div>
        <!--ヘッダータイトル-->
        <header id="head" :class="{ active: this.isActive }">
            <div id="title">
                <button @click="toggleSubmenu(isActive)" class="qq"><img :src="this.isActive ? this.icon2 : this.icon1" alt="Image" width="30" height="auto"></button>
                <h1 class="head_title">{{$t("common.titleGuidelineDetail")}}</h1>
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
                <div class="accordion">
                    <template>
                        <div>
                            <p>{{$t("guidelineDetail.description")}}</p>
                            <vue-json-editor
                                v-model="json"
                                :show-btns="false"
                                :expandedOnStart="true"
                                :mode="'code'"
                            >
                            </vue-json-editor>
                        </div>
                    </template>
                </div>

                <!-- button -->
                <div class="btn_area">
                    <template v-if="$i18n.locale === 'en'">
                        <input type="button" value="Update" class="btn_left"
                               @click="guidelineUpdate" v-bind:disabled="!guideline_install_flag"
                               v-bind:class="{'un_btn' : !guideline_install_flag}"/>
                        <input type="button" value="Back" class="btn_left"
                               @click="guidelineBack" />
                    </template>
                    <template v-else>
                        <input type="button" value="更新" class="btn_right"
                               @click="guidelineUpdate" v-bind:disabled="!guideline_install_flag"
                               v-bind:class="{'un_btn' : !guideline_install_flag}"/>
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
import SubMenu from './SubMenu.vue'
import { subMenuMixin } from "../mixins/subMenuMixin";
import { urlParameterMixin } from '../mixins/urlParameterMixin';
import { GuidelinesMixin } from '../mixins/GuidelinesMixin';
import { AccountControlMixin } from '../mixins/AccountControlMixin';
import { csrfMixin } from '../mixins/csrfMixin';
import vueJsonEditor from 'vue-json-editor';

export default {
    mixins: [subMenuMixin, urlParameterMixin, GuidelinesMixin, AccountControlMixin, csrfMixin],
    data() {
        return {
            screenName: 'guidelineDetail',
            json: {
                msg: 'demo of jsoneditor'
            },
            errorMessages: [],
            guideline_install_flag: false,
            guideline_id: null
        }
    },
    mounted: async function () {
        this.setLanguageData();
        var guideline = JSON.parse(sessionStorage.getItem('guideline'));
        this.guideline_install_flag = guideline.install;
        var guideline_aithub_id = guideline.guideline_aithub_id;
        var guideline_local_id = guideline.guideline_local_id;
        this.guideline_id = '';
        if (this.guideline_install_flag) {
            this.guideline_id = guideline_local_id;
        } else {
            this.guideline_id = guideline_aithub_id;
        }
        await this.getGuidelineJsonData(this.guideline_id, this.guideline_install_flag);
        this.json = this.json_date;

        // エディタの高さを変える
        var editors = document.getElementsByClassName('jsoneditor-vue');
        for(var i = 0; i < editors.length; i++){
            // editors[i].style.height = '800px';
            editors[i].style.height = '700px';
        }

    },
    components: {
        SubMenu,
        vueJsonEditor
    },
    methods: {
        guidelineUpdate(){
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

                const url = this.$backendURL + '/guidelines/' + this.guideline_id + '/guideline_schema_file_front';
                //リクエスト時のオプションの定義
                const config = {
                    headers:{
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRF-TOKEN' : this.getCookie("csrf_access_token")
                    },
                    withCredentials:true,
                }
                this.$axios.put(url, fd, config)
                    .then((response) => {
                        this.result = response.data;
                        this.$router.push({
                            name: "Guidelines"
                        });
                    })
                    .catch((error) => {
                        this.$router.push({
                            name: 'Information',
                            params: {error}
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
    }
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
    width: 90%;
}
.tittle {
    margin: 0 auto;
    font-size: 2rem;
    width: 80%;
    /*background: red;*/
}

/*エラーメッセージ*/
.error_message {
    text-align: left;
    word-break: break-all;
    margin: 0px;
    color: #ff0000;
}
.btn_area {
    /*background-color: red;*/
    margin-top: 2rem;
    text-align: center;
}

</style>
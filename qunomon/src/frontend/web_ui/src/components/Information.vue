<template>
<div>
    <!--ヘッダータイトル-->
    <header id="head">
        <div id="title">
            <button @click="toggleSubmenu(isActive)" class="qq"><img :src="this.isActive ? this.icon2 : this.icon1" alt="Image" width="30" height="auto"></button>
            <h1 class="head_title">TF2-TestbedInformation</h1>
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
            <table class="error" v-if="error">
                <tbody v-if="error.response && error.response.data">
                    <tr>
                        <td class="td1">
                            <p class="error_message">{{$t("infomation.errorCode")}}:</p>
                        </td>
                        <td class="td2">
                            <p class="error_message">
                                <template  v-if="error.response.data.Result">
                                    {{error.response.data.Result.Code}}
                                </template>
                                <template v-else>
                                    {{error.response.data.Code}}
                                </template>
                            </p>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <p class="error_message">{{$t("infomation.errorMessage")}}:</p>
                        </td>
                        <td>
                            <p class="error_message">
                                <template  v-if="error.response.data.Result">
                                    {{error.response.data.Result.Message}}
                                </template>
                                <template v-else-if="error.response.data.Message">
                                    {{error.response.data.Message}}
                                </template>
                                <template v-else-if="error.response.data.message">
                                    {{error.response.data.message}}
                                </template>
                                <template v-else>
                                    {{$t("infomation.frontErrorMessage1")}}
                                    {{$t("infomation.frontErrorMessage2")}}
                                </template>
                            </p>
                        </td>
                    </tr>
                </tbody>
                <tbody v-else>
                    <tr>
                        <td colspan="2">
                            {{error}}
                        </td>
                    </tr>
                </tbody>
            </table>
            <table class="error" v-else>
                <tr>
                    <td>
                        {{$t("infomation.frontErrorMessage1")}}
                    </td>
                </tr>
                <tr>
                    <td>
                        {{$t("infomation.frontErrorMessage2")}}
                    </td>
                </tr>
            </table>

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
import { AccountControlMixin } from '../mixins/AccountControlMixin';

export default {
    components: {SubMenu},
    mixins: [subMenuMixin, AccountControlMixin],
    data() {
        return {
            error: this.$route.query.error === undefined ? undefined : JSON.parse(this.$route.query.error)
        }
    },
    mounted: function () {
        this.setLanguageData();
    },
    methods: {
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
        changeLanguage(lang) {
            sessionStorage.setItem('language', lang);
            this.$i18n.locale = lang;
        }
    }
}
</script>

<style scoped>
/*エラーメッセージ*/
.error {
    margin: 20px auto 0px auto;
    border: 0px;
    padding: 0px;
    width: 95%;
    font-size: 20px;
}

.error_message {
    text-align: left;
    word-break: break-all;
    margin: 0px;
}

.error tr {
    background: none;
}

.td1 {
    width: 170px;
}

.td2 {
    width: auto;
}

.error td {
    vertical-align: top;
}
</style>

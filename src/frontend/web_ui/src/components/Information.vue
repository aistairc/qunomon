<template>
<div>
    <!--ヘッダータイトル-->
    <header id="head">
        <div id="title">
            <h1 class="head_title">TF2-TestbedInfomation</h1>
        </div>
    </header>
    <!-- サブメニュー（左カラム） -->
    <div id="submenu">
        <div id="logo">
            <img src="~@/assets/logo.svg" alt="logo" class="logo">
        </div>
        <div id="header_set">
            <div id="company_name">
                <p class="company_name">{{$t("common.organizationName")}}</p>
                <p class="company_name2">産総研</p>
            </div>
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
        </div>
        <ul id=" submenu_body">
            <li class="mlcomponent un_place">
                <router-link :to="{ name: 'MLComponents'}" class="move_">{{$t("common.menuMLComponents")}}</router-link>
            </li>
            <li class="btn_logout">
                <a href="javascript:void(0);" @click="signOut()" class="btn_unselect">
                    <img src="~@/assets/logout.svg" alt="logout" class="icon">
                    {{$t("common.signOut")}}
                </a>
            </li>
        </ul>
    </div>
    <!-- ニュース（中央カラム） -->
    <div id="main">
        <div id="main_body">
            <table class="error" v-if="this.$route.params.error">
                <tbody v-if="this.$route.params.error.response.data">
                    <tr>
                        <td class="td1">
                            <p class="error_message">{{$t("infomation.errorCode")}}:</p>
                        </td>
                        <td class="td2">
                            <p class="error_message">{{this.$route.params.error.response.data.Code}}</p>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <p class="error_message">{{$t("infomation.errorMessage")}}:</p>
                        </td>
                        <td>
                            <p class="error_message">{{this.$route.params.error.response.data.Message}}</p>
                        </td>
                    </tr>
                </tbody>
                <tbody v-else>
                    <tr>
                        <td colspan="2">
                            {{this.$route.params.error}}
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
export default {
    data() {
        return {}
    },
    mounted: function () {
        this.setLanguageData()
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
        },
        signOut() {
            sessionStorage.removeItem('mlComponentId');
            sessionStorage.removeItem('organizationId');
            sessionStorage.removeItem('language');
            this.$router.push({
                name: 'SignIn'
            });
        },
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

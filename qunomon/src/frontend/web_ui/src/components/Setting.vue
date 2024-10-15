<template>
    <div>
        <!--ヘッダータイトル-->
        <header id="head" :class="{ active: this.isActive }">
            <div id="title">
                <button @click="toggleSubmenu(isActive)" class="qq"><img :src="this.isActive  ? this.icon2 : this.icon1" alt="Image" width="30" height="auto"></button>
                <h1 class="head_title">{{$t("common.titleSetting")}}</h1>
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
                <div class="option-menu">
                    <div>
                        <label class="cardTitle">{{$t("setting.title")}}</label>
                        <table>
                            <!-- AIT-HUB 使用可否 -->
                            <tr>
                                <td>{{$t("setting.aithubUsingStatus")}}</td>
                                <td>
                                    <template v-if=aithub_using_status>
                                        {{$t("setting.usingStatusOn")}}
                                    </template>
                                    <template v-else>
                                        {{$t("setting.usingStatusOff")}}
                                    </template>
                                </td>
                            </tr>
                            <!-- AIT-HUB 接続状態 -->
                            <tr>
                                <td>{{$t("setting.aithubNetworkStatus")}}</td>
                                <td>
                                    <template v-if=aithub_network_using_status>
                                        {{$t("setting.linkStatusOn")}}
                                    </template>
                                    <template v-else>
                                        {{$t("setting.linkStatusOff")}}
                                    </template>
                                </td>
                                <td>
                                    <template v-if="$i18n.locale === 'en'">
                                        <input type="button" value="AIT-HUB login" class="btn_status" @click="aithubNetworkCheck"/>
                                    </template>
                                    <template v-else>
                                        <input type="button" value="AIT-HUBログイン" class="btn_status" @click="aithubNetworkCheck"/>
                                    </template>
                                </td>
                                <td>
                                    <template v-if="$i18n.locale === 'en'">
                                        <input type="button" value="AIT-HUB logout" class="btn_status" @click="signOutAitHub()"/>
                                    </template>
                                    <template v-else>
                                        <input type="button" value="AIT-HUBログアウト" class="btn_status" @click="signOutAitHub()"/>
                                    </template>
                                </td>
                            </tr>
                            <!-- DB設定値（AIT-HUB使用／不使用） -->
                            <tr>
                                <td>{{$t("setting.aithubUsingPermission")}}</td>
                                <td>
                                    <template v-if=aithub_using_permission>
                                        <a href="#" class="btn_select_setting">{{$t("setting.permissionOn")}}</a>
                                        <a href="#" v-on:click.prevent="changeAITHubSetting('off')" class="btn_unselect_setting">{{$t("setting.permissionOff")}}</a>
                                    </template>
                                    <template v-else>
                                        <a href="#" v-on:click.prevent="changeAITHubSetting('on')" class="btn_unselect_setting">{{$t("setting.permissionOn")}}</a>
                                        <a href="#" class="btn_select_setting">{{$t("setting.permissionOff")}}</a>
                                    </template>
                                </td>
                            </tr>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import SubMenu from './SubMenu.vue';
import { subMenuMixin } from "../mixins/subMenuMixin";
import { urlParameterMixin } from '../mixins/urlParameterMixin';
import { AccountControlMixin } from '../mixins/AccountControlMixin';

export default {
    components: {SubMenu},
    mixins: [subMenuMixin, urlParameterMixin, AccountControlMixin],
    data() {
        return {
            aithub_using_status: false,
            aithub_network_using_status: false,
            aithub_using_permission: false
        }
    },
    mounted() {
        this.setLanguageData();
        this.triggerAithubUsing();
        setTimeout(() => {
            this.setAITHubLinkageMode();
            this.getSessionItems();
        }, 500); 
    },
    methods: {
        getSessionItems() {
            // alert('getSessionItems:' + sessionStorage.getItem('aithub_network_status'))
            // AIT-HUBを使用するか否かの最終決定フラグの判断
            if (sessionStorage.getItem('aithub_linkage_mode') == '1') {
                this.aithub_using_status = true;
            }
            // AIT-HUBとのネットワークが正常か異常かの判断
            if (sessionStorage.getItem('aithub_network_status') == '1') {
                this.aithub_network_using_status = true;
            }
            // DB設定値（AIT-HUB使用／不使用）の判断
            if (sessionStorage.getItem('aithub_setting_flag') == '1') {
                this.aithub_using_permission = true;
            }
        },
        //言語データ読み込み
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
            this.setLanguageData();
        },
        aithubNetworkCheck(){
            // 画面遷移時にはnginxのlocation /settingが実行されず、再描画するときに実行され認証サーバへのログイン画面がリダイレクトされる
            // 画面描画時にネットワークチェックが実行される
            window.location.reload();
        }
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
    position: relative;
    z-index: 0;
}


.option-menu {
    padding-top: 1rem;
    margin: 0 auto;
    width: 90%;
    vertical-align: middle;
    text-align: center;
    display: inline-block;
}
.option-menu div{
    border: none;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Add a box shadow for depth */
    margin: 1rem;
    height: 12rem;
    background: white;
    vertical-align: middle;
    text-align: center;
}

.option-menu div table {
    width: 95%;
    margin: auto;
    vertical-align: middle;
    position: relative;
    border-collapse: separate;
    border-spacing: 0 5px;
    font-size: 0.85rem;
}
.option-menu div table td {
    height: 2rem;
    text-align: center;
}

.option-menu div table td:nth-child(1) {
    background-color: #a9c7aa;
    color: black;
    border-bottom-left-radius: 5px;
    border-top-left-radius: 5px;
    text-align: center;
    font-weight: bold;
    &:hover {
        background-color: #43645b;
        color: white;
    }
}
.option-menu div table td:nth-child(2) {
    border: 1px solid;
    border-color: #a9c7aa;
    background-color: #f0f0f0;
    border-bottom-right-radius: 5px;
    border-top-right-radius: 5px;
    text-align: center;
}
.option-menu div table td:nth-child(2) input {
    background-color: #f0f0f0;
}
.option-menu div table td:nth-child(3), td:last-child {
    padding-left: 1rem;
}

.option-menu div .cardTitle {
    background-color: #dc722b;
    color: #ffffff;
    border-top-right-radius: 5px;
    border-top-left-radius: 5px;
    margin: 0;
    width: 100%;
    height: 2.5rem;
    font-size: 1rem;
    font-weight: bold;
    display: flex;
    flex-direction: column-reverse;
    justify-content: space-evenly;

}
.option-menu div table .guidelines_select, input{
    height: 100%;
    width: 100%;
    border-bottom-right-radius: 5px;
    border-top-right-radius: 5px;
    border: none;
}

.uploadBTN {
    color: white;
    border: none;
    width: 100%;
    height: 100%;
    text-align: center;
    border-radius: 5px;
    background-color: #31436B;
}

.btn_select_setting {
    text-align: left;
    display: inline-block;
    text-decoration: none;
    color: indianred;
    padding-right: 20px;
    border: none;
    font-size: 0.85rem;
    font-weight: bold;
    pointer-events: none;
    cursor: pointer;
}

.btn_unselect_setting {
    text-align: left;
    display: inline-block;
    color: #c0c0c0;
    padding-right: 20px;
    border: none;
    font-size: 0.85rem;
    cursor: pointer;
}

.btn_status {
    width: 100%;
    text-align: center;
    display: inline-block;
    text-decoration: none;
    font-size: 0.85rem;
    font-weight: bold;
    border-radius: 5px;
    /*box-shadow: 0px 2px 3px 3px rgba(0, 0, 0, 0.29);*/
    border: none;
    font-size: 0.85rem;
    color: black;
    background-color: #a9c7aa;
    &:hover {
        color: white;
        background-color: #43645b;
    }
}

</style>

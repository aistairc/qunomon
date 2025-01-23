<template>
    <div id="app">
        <div id="nav">
            <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
            <!--
            <router-link to="/">Home</router-link> |
            <router-link to="/about">About</router-link>
            -->
        </div>
        <Message ref="ref_message" />
        <router-view/>
        <div v-if="loading" class="loader-overlay">
            <div class="loader"></div>
        </div>
    </div>
</template>

<script>
import Message from './components/Message.vue';
import EventBus from './eventBus';

export default {
    data() {
        return {
            loading: false
        };
    },
    components: {
        Message
    },
    created() {
        // organizationIdを設定する
        sessionStorage.setItem('organizationId', this.postLoginData());
    },
    mounted() {
        // APP共通メソッド
        EventBus.on('show-message', this.showMessage);
        EventBus.on('set-aithub-using', this.setAithubUsing);

        // 遷移パターンの判断
        if (this.$route.query.err) {
            this.showMessage('aithub_E01');
        } else if (sessionStorage.hasOwnProperty('aithub_logout')) {
            sessionStorage.removeItem('aithub_logout');
            sessionStorage.setItem('aithub_network_status', 'logout')
            this.showMessage('aithub_logout');
        } else if (sessionStorage.hasOwnProperty('aithub_logout_whit_error')) {
            sessionStorage.removeItem('aithub_logout_whit_error');
            sessionStorage.setItem('aithub_network_status', 'logout')
            this.showMessage('aithub_logout_whit_error', );
        }

        // ログイン処理
        this.signIn();

        // AITHUB使用状態を設定する
        this.setAithubUsing();
    },
    methods: {
        postLoginData(){
            // TODO: ログイン処理
            return 'dep-a'
        },
        signIn(){
            // SESSION側でログインフラグが設定されない場合のみ初期処理を実施する
            if (!sessionStorage.hasOwnProperty('session_signIn_flag')) {
                // SESSIONにサインインフラグを設定する
                sessionStorage.setItem('session_signIn_flag', true);


                // // TODO アカウント実装時に再開する予定
                // const url = this.$backendURL + '/login';
                // var requestData = {
                //     AccountId: '',
                //     Password: ''
                // }
                // //リクエスト時のオプションの定義
                // const config = {
                //     headers:{
                //         'X-Requested-With': 'XMLHttpRequest',
                //         'X-CSRF-TOKEN' : this.getCookie("csrf_access_token")
                //     },
                //     withCredentials:true,
                // }
                // this.$axios.post(url, requestData, config)
                // .then(() => {
                //     // 正常処理
                    
                // })
                // .catch((error) => {
                //     // 異常時にorganizationIdをクリアする
                //     sessionStorage.removeItem('organizationId');

                //     // 異常処理
                //     this.$router.push({
                //         name: 'Information',
                //         query: {error: JSON.stringify({...error, response: error.response})}
                //     })
                // })
            }
        },
        setAithubUsing() {
            // ローディングスピナーが表示
            this.loading = true;

            // DB設定値（AIT-HUB使用／不使用）チェック
            const url = this.$backendURL + '/setting/' + 'aithub_linkage_flag';
            this.$axios.get(url)
            .then((response) => {
                // AIT-HUB使用フラグの設定
                if (response.data.Value == '1') {
                    sessionStorage.setItem('aithub_setting_flag', '1');

                    // AIT-HUBとの接続チェック（health-checkは認証無しで動くので、他のAPIにする）
                    var aithub_url = this.$aithubURL + '/health-check';
                    this.$axios.get(aithub_url)
                    .then((response) => {
                        // AWS版 response.status == 200
                        if (response.statusText == 'OK' ) {
                            // 接続OK
                            sessionStorage.setItem('aithub_network_status', '1');
                            // AIT-HUBを使用するか否かの最終決定フラグの設定
                            // (AITHUBへ接続OK、かつ、AIT-HUB使用フラグがOnの場合のみ使用可能に設定)
                            sessionStorage.setItem('aithub_linkage_mode', '1');
                        } else {
                            // 接続NG
                            if (sessionStorage.getItem('aithub_network_status') === '1') {
                                this.showMessage('aithub_E01');
                            }
                            sessionStorage.setItem('aithub_network_status', '0');
                            // AIT-HUBを使用するか否かの最終決定フラグの設定(AITHUBへ接続NGのため使用不可に設定)
                            sessionStorage.setItem('aithub_linkage_mode', '0');
                        }
                        //  ローディングスピナーが非表示
                        this.loading = false;
                    })
                    .catch((error) => {
                        // 接続NG
                        if (sessionStorage.getItem('aithub_network_status') === '1') {
                            this.showMessage('aithub_E01');
                        }
                        sessionStorage.setItem('aithub_network_status', '0');
                        // AIT-HUBを使用するか否かの最終決定フラグの設定(AITHUBネットワークエラーのため使用不可に設定)
                        sessionStorage.setItem('aithub_linkage_mode', '0');
                        //  ローディングスピナーが非表示
                        this.loading = false;
                        // eslint-disable-next-line no-console
                        console.log(error);
                    });

                } else {
                    sessionStorage.setItem('aithub_setting_flag', '0');
                    sessionStorage.setItem('aithub_network_status', '0');
                    sessionStorage.setItem('aithub_linkage_mode', '0');
                    this.loading = false;
                }
            })
            .catch((error) => {
                this.$router.push({
                    name: 'Information',
                    query: {error: JSON.stringify({...error, response: error.response}) }
                });
                //  ローディングスピナーが非表示
                this.loading = false;
            });
        },
        showMessage(messageCode, messageText) {
            this.$refs.ref_message.show(messageCode, messageText);
        }
    },
    watch: {
        '$route': {
            handler(to, from) {
                // eslint-disable-next-line no-console
                console.log(`Route changed from ${from.fullPath} to ${to.fullPath}`);
                // DB設定値（AIT-HUB使用）時、かつ、Setting画面以外の場合のみチェック
                if (sessionStorage.getItem('aithub_setting_flag') == '1' &&
                    to.fullPath !== '/Setting') {
                    this.setAithubUsing();
                }
            },
            deep: true
        }
    }
}
</script>


<style>

/*============================================
全般的なスタイル
============================================*/
* {
    margin:0; padding:0; 	/*全要素のマージン・パディングをリセット*/
    line-height:1.5;	/*全要素の行の高さを1.5倍にする*/
    /* 主要な色のカスタムプロパティ */
    --gray-thema: #f0f0f0;
    --primary-color: #43645b;
    --primary-color-light: #a9c7aa;
    --secondary-color: #dc722b;
    --text-color-black: #000066;
}
body {
    color:var(--text-color-black);		/*文字色*/
    background-color: var(--gray-thema);
    font-size: 1rem;
    font-family:Meiryo;			/*フォント*/
}
html, body {
    height: 100%;
    margin: 0;
}
.contents {
    min-height: 100%;
    margin-bottom: -50px;
}

/*----------------
文字
----------------*/
.title_2{
    font-size: 40px;
    color:var(--text-color-black);
}

.subtitle {
    font-size: 20px;
    color:var(--text-color-black);
}

.error {
    color:#ff0000;
}

/*----------------
影
----------------*/
/*影が大きい*/
.z-depth__3 {
    box-shadow: 0 13px 20px 3px rgba(0,0,0,.46);
}

/*影が小さい*/
.z-depth__ {
    box-shadow: 0px 2px 10px rgba(0,0,0,.46);
}


/*---------------
ヘッダー部
----------------*/
#head {
    height:3rem;
    background: var(--primary-color);	/*背景色*/
    color: #fff;		/*文字色*/
    width: 100%;
    align-items: center;
    font-size: 0;
    position: fixed;
    text-align: left;
    margin: 0;
    background-color: var(--primary-color);
}
#head .head_title {
    margin-left: 4rem;
}
#title h1{
    font-size: 25px;
    margin-block-start: 0.3em;
    margin-block-end: 0.3em;
}


.labelBtn {
    width: 100%;
}

/*============================================
サブメニュー（左カラム）
============================================*/
#submenu {
    top: 3rem;
    position: fixed;
    height: 100%;
    width: 12.5rem;			/*幅の指定*/
    display:inline;			/*IE6のマージン算出のバグ対策*/
    float:left;			/*サブメニューのカラムを左寄せにする*/
    transition: width 0.3s;
    background-color: #203e3b;
}
#submenu.active {
    width: 6.25rem;
    transition: width 0.3s;
    text-align: center;
    vertical-align: middle;
    #sidebar {
        width: 6.25rem;
        transition: width 0.3s;
    }
}

#submenu a {
    font-size: 1rem;
}
/*水平ライン*/
#submenu hr {
    border-top: #ffffff solid 1px;
    margin: 20px 0px;
}

/*ロゴ*/
#logo{
    text-align: center;
    margin: 5px auto;
}
.logo{
    margin: 0;
    padding: 0;
    vertical-align: top;
}
#signin_set .logo{
    width: 4em;
}
#submenu .logo{
    width: 50%;
    -webkit-filter: drop-shadow(0 0 5px rgba(0, 0, 0, .6));
}

/*会社名と言語切り替え*/
#header_set{
    padding: 0px;
    margin: 0px	5px 20px;
    font-size: 15px;
    color: #fff;
    text-align: center;
}

/*.company_name{*/
/*	text-align: left;*/
/*	margin: 0px 5px;*/
/*}*/
/*.company_name2{*/
/*	text-align: right;*/
/*	margin: 0px 5px 0px auto;*/
/*}*/
/*#company_name p{*/
/*	margin-block-start: 0px;*/
/*  margin-block-end: 0px;*/
/*}*/
#btn_language{
    margin: 5px 10px;
    text-align: center;
}
#btn_language a {
    font-size: 0.75rem;
}
#btn_set{
    text-align: center;
    font-weight: bold;
}
.btn_select {
    text-align: center;
    display: inline-block;
    text-decoration: none;
    color: indianred;		/*文字色*/
    margin:0px 5px;
    pointer-events: none;
    font-weight: bold;
}
.btn_unselect {
    text-align: center;
    display: inline-block;
    color: #c5c5c5;
    margin:0px 5px;
    border: none;
    text-decoration-line: none;
}

/*ログアウト*/
.btn_logout{
    position: absolute;
    bottom: 20px;
    left: 10px;
    margin: 0;
    padding: 0;
    color: var(--text-color-black);
}

/*サブメニューのボディ部分（余白調整・背景画像・背景色）*/
#submenu_body {
    padding-bottom:6px;
    margin: 0;
}

/*メニュー切り替え*/

.un_place, .place, .disable_place {
    font-size: 16px;
    list-style-type:none;		/*リストマーカー無しにする*/
    display:inline;			/*リスト項目をインライン表示にする*/
    width: 100%;
}

.mlcomponent {
    position: absolute;
    bottom: 45px;
    margin: 0;
    padding: 0;
    left: 0;
}

.move_{
    color: #fff;
    display:block;			/*リンクをブロック表示にする*/
    padding: 5px 15px;	/*サブメニュー項目のパディング*/
    text-decoration:none;		/*リンクの下線を無くす*/
}

.place a{
    display:block;			/*リンクをブロック表示にする*/
    padding: 5px 15px;	/*サブメニュー項目のパディング*/
    text-decoration:none;		/*リンクの下線を無くす*/
    background-color: var(--gray-thema);
    pointer-events: none;
    color: var(--text-color-black);
}

.un_place span{
    color: black;
    display:block;			/*リンクをブロック表示にする*/
    padding: 5px 2px;	/*サブメニュー項目のパディング*/
    text-decoration:none;		/*リンクの下線を無くす*/
}

.un_place a:hover{
    color: #b2b2c0;
    background-color: var(--gray-thema);
    opacity: 0.5;	/*リンクにマウスが乗ったら色を変える*/
}

.disable_place span{
    color: #a1a1bb;
    padding: 5px 15px;
}

/*============================================
メイン（中央カラム）
============================================*/
#main {
    top: 3rem;
    width: calc(100% - 12.5rem);
    float:right;
    transition: width 0.3s;
}
#main.active {
    width: calc(100% - 6.25rem);
    transition: width 0.3s;
}

#main_body {
    display: flex;
    flex-direction: column;
    min-height: calc(100vh - 3rem);
    background-color: var(--gray-thema);
}


/*============================================
フッタ
============================================*/
#footer {
    margin-top: auto;
    background: var(--gray-thema);
    margin-bottom: 10px;
    text-align: center;
}

address {
    font-style:normal;			 /*フォントスタイルを標準にする*/
    font-size:13px;			 /*フォントサイズを小さくする*/
}

/*----------------
単品ボタン
----------------*/
#btn_single{
    text-align: center;
}
.btn_single{
    background-color: var(--primary-color-light);
    color: black;
    border: none;
    height: 2rem;
    width: 10rem;
    margin-left: 1rem;
    text-align: center;
    text-decoration: none;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    border-radius: 5px;
    z-index: 10;
    &:hover {
        background-color: var(--primary-color) !important;
        color: white;
    }
    &.un_btn{
        background: silver;
        pointer-events: none;
    }
    &:active {
        box-shadow: inset 0 0 2px rgba(128, 128, 128, 0.1);
        transform: translateY(2px);
    }
}


/*ボタン*/
.btn {
    margin-bottom: 5px;
}

/*ボタン非活性*/
.un_btn {
    background-color: silver;
    pointer-events: none;
    box-shadow: 0px 2px 3px 1px rgba(0, 0, 0, 0.29);
}


/*----------------
表
----------------*/


/*スクロール*/


/*----------------
テキストエリア
----------------*/
input[type="text"]{
    border: none;
    background-color: #fff;	/*部品内の背景色*/
    padding: 4px;
}
input[type="text"]:hover{
    box-shadow: 0px 0px 5px rgba(0,0,0,.46);
}

textarea{
    background-color: #fff;	/*部品内の背景色*/
    border: none;
    padding: 0.4rem;
}

textarea:hover{
    box-shadow: 0px 0px 5px rgba(0,0,0,.46);
}

dt{
    float: left;
}
/*----------------
プルダウンリスト
----------------*/
.select{
    width: 200px;
    display: inline-block;
    font-size: 15px;
    padding:4px;
    border:none; /*枠線の種類 太さ 色*/
}
.select:hover{
    box-shadow: 0px 0px 5px rgba(0,0,0,.46);
}

/*----------------
吹き出し
----------------*/
.fukidashi {
    display: none;
    margin-left: 5px;
    position: fixed;
    padding: 16px;
    border-radius: 5px;
    background: #818181;
    color: #fff;
    font-weight: bold;
}
.fukidashi:after {
    content: "";
    position: absolute;
    top: 5%;
    left: -12px;
    border-top: 10px solid transparent;
    border-bottom: 10px solid transparent;
    border-right: 12px solid #818181;
}

/*----------------
個別に設定するもの
.fukidashi {
	width: 吹き出しの幅;
	margin-left: 20px;; 位置を調整したいとき
}

.吹き出しを付ける部品:hover + .fukidashi {
	display: inline;
}

.fukidashi:after {
	top: 3%;	矢印の位置
}

----------------*/

/*選択ボタン*/
#btn_set{
    margin-top: 20px;
    text-align: center;
}
.btn_right {
    width: 100px;
    padding: 8px 0px;
    text-align: center;
    display: inline-block;
    text-decoration: none;
    background-color: var(--primary-color-light);		/*アクセントカラー*/
    color: black;		/*文字色*/
    font-weight: bold;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Add a box shadow for depth */
    margin-left: 15px;
    display: inline-block;
    border: none;
    border-radius: 5px;
    font-size: 15px;
}
.btn_right:hover {
    background: var(--primary-color) !important;
    color: white;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.7); /* Add a box shadow for depth */
}
.btn_right:active {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.7); /* Add a box shadow for depth */
    transform: translateY(2px);
}
.btn_left {
    width: 100px;
    padding: 8px 0px;
    text-align: center;
    display: inline-block;
    text-decoration: none;
    background-color: var(--primary-color-light);		/*背景色*/
    color: black;		/*アクセントカラー*/
    font-weight: bold;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* Add a box shadow for depth */
    margin-right: 15px;
    display: inline-block;
    border: none;
    border-radius: 5px;
    font-size: 0.85rem;
}
.btn_left:hover {
    background-color: var(--primary-color) !important;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.7); /* Add a box shadow for depth */
    color: white;
}
.btn_left:active {
    box-shadow: inset 0 0 2px rgba(128, 128, 128, 0.7);
    transform: translateY(2px);
}

/* アイコン */
.icon{
    height: 24px;
    text-decoration: none;
    vertical-align:middle;
}
.icon:hover{
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.7);
}

/* ページング */
.page{
    margin-top: 10px;
}

/* モーダルCSS */
.modalArea {
    display: none;
    position: fixed;
    z-index: 10; /*サイトによってここの数値は調整 */
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}
.modalBg {
    width: 100%;
    height: 100%;
    background-color: rgba(30,30,30,0.9);
}
.modalWrapper {
    position: absolute;
    top: 50%;
    left: 50%;
    transform:translate(-50%,-50%);
    max-width: 1000px;
    padding: 30px 30px;
    background-color: var(--gray-thema);
    height: 90%;       /*モーダルウィンドウのサイズ*/
    width: auto;
    overflow: auto;
}
.closeModal {
    position: absolute;
    top: 0.1rem;
    right: 1.5rem;
    cursor: pointer;
    color: white;
    font-size: 2rem;
}

/* ローディングスピナーのスタイル */
.loader-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* 半透明の黒 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999; /* 高いz-indexで他の要素の上に表示 */
}

.loader {
  border: 16px solid #f3f3f3; /* Light grey */
  border-top: 16px solid #3498db; /* Blue */
  border-radius: 50%;
  width: 120px;
  height: 120px;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

</style>
<script setup>
</script>
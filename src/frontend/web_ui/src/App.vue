<template>
  <div id="app">
    <div id="nav">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
      <!--
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link>
      -->
    </div>
    <router-view/>
  </div>
</template>

<style>

/*============================================
全般的なスタイル
============================================*/
* {
	margin:0; padding:0; 	/*全要素のマージン・パディングをリセット*/
	line-height:1.5;	/*全要素の行の高さを1.5倍にする*/
}
body {
	color:#000066;		/*文字色*/
	background-color: #f0f0f0;
	font-size: 16px;
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
	color:#000066;
}

.subtitle {
	font-size: 20px;
	color:#000066; 
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
	height:55px;
	background: #9bbb59;	/*背景色*/
	color: #fff;		/*文字色*/
	width: 100%;
	align-items: center;
	font-size: 0;
	position: fixed;
	text-align: left;
	margin: 0px auto 0px 170px;
	padding-left: 20px;
}

#title h1{
	font-size: 25px;
	margin-block-start: 0.3em;
	margin-block-end: 0.3em;
}


/*============================================
サブメニュー（左カラム）
============================================*/
#submenu {
	position: fixed;
	height: 100%;
	background-color:#466111;
	width: 170px;			/*幅の指定*/
	display:inline;			/*IE6のマージン算出のバグ対策*/
	float:left;			/*サブメニューのカラムを左寄せにする*/
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
.company_name{
	text-align: left;
	margin: 0px 5px;
}
.company_name2{
	text-align: right;
	margin: 0px 5px 0px auto;
}
#company_name p{
	margin-block-start: 0px;
  margin-block-end: 0px;
}
#btn_language{
	margin: 5px 10px;
	text-align: center;
}
#btn_set{
	text-align: center;
}
.btn_select {
	text-align: center;
	display: inline-block;
	text-decoration: none;
	color: gray;		/*文字色*/
	margin:0px 5px;
	border: none;
	font-size: 14px;
	pointer-events: none;
}
.btn_unselect {
	text-align: center;
	display: inline-block;
	color: #f0f0f0;		/*アクセントカラー*/
	margin:0px 5px;
	border: none;
	font-size: 14px;
}

/*ログアウト*/
.btn_logout{
	position: absolute;
	bottom: 20px;
	left: 10px;
	margin: 0;
	padding: 0;
	color: #000066;
}

/*サブメニューのボディ部分（余白調整・背景画像・背景色）*/
#submenu_body {
	padding-bottom:6px;
}

/*メニュー切り替え*/

.un_place, .place {
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
	background-color: #f0f0f0;
	pointer-events: none;
	color: #000066;
}

.un_place a:hover{
	color: #b2b2c0;
	background-color: #f0f0f0;
  opacity: 0.5;	/*リンクにマウスが乗ったら色を変える*/
}
  
/*============================================
メイン（中央カラム）
============================================*/
#main {
	padding-top: 55px;
	width: 100%;
	float:right;
}

#main_body {
    display: flex;
    flex-direction: column;
	min-height: calc(100vh - 55px);
	margin-left: 170px;
	background-color: #f0f0f0;
}

  
/*============================================
フッタ
============================================*/
#footer {
  margin-top: auto;
  background: #f0f0f0;
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
	padding: 4px 15px;
	text-align: center;
	display: inline-block;
	text-decoration: none;
	background: #31436B;		/*アクセントカラー*/
	color: #fff;		/*文字色*/
	font-weight: bold;
	box-shadow: 0px 2px 3px 3px rgba(0, 0, 0, 0.29);
	display: inline-block;
	border: none;
	font-size: 15px;
	cursor: pointer;
}
.btn_single:hover {
	background-color:  #0e1629;
}
.btn_single:active {
	box-shadow: inset 0 0 2px rgba(128, 128, 128, 0.1);
	transform: translateY(2px);
}

/*ボタン*/
.btn {
	margin-bottom: 5px;
}

/*ボタン日活性*/
.un_btn {
	background-color: #a1a1bb;
	pointer-events: none;
	box-shadow: 0px 2px 3px 1px rgba(0, 0, 0, 0.29);
}


/*----------------
表
----------------*/
#search_table {
	margin-left: auto;
	margin-right: auto;
}

table {
  margin-left: 0px;
  table-layout:fixed;
  word-break : break-all;
}

tr{
	border: 1px solid gray;
	background: #fff;	/*部品内の背景色*/
}
th{
	background: #9bbb59;	/*メインカラー*/
	color:#fff;	/*文字色*/
}

td{
	padding-bottom: 5px;
	padding-top: 5px;
}

.t_left{
	text-align:left;
	padding-left: 5px;
}
.t_center{
	text-align:center;
}
.t_right{
	padding: 0px 10px;
	text-align:right;
}
.icon img{
	width: 25px;
	height: 25px;
}
.icon a {
	text-decoration: none;
}
#table p{
	margin-block-start: 0;
	margin-block-end: 0;
}

.checked{
  background-color: #d1ff8c;
}

/*スクロール*/

.table_column {
	display: block;
	overflow-y:auto;
	width: 100%;
}

/*個別に設定
#search_table {
	width: px;    スクロールを足した分の横幅
}

.table_frame {
	width: px;   テーブルの横幅

.table_column {
	height: px;   テーブルの縦幅
}


*/

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
	background: #31436B;		/*アクセントカラー*/
	color: #fff;		/*文字色*/
	font-weight: bold;
	box-shadow: 0px 2px 3px 3px rgba(0, 0, 0, 0.29);
	margin-left: 15px;
	display: inline-block;
	border: none;
	font-size: 15px;
}
.btn_right:hover {
	background-color: #000000;
	box-shadow: 0px 2px 10px 3px rgba(0, 0, 0, 0.29);
}
.btn_right:active {
	box-shadow: inset 0 0 2px rgba(128, 128, 128, 0.1);
	transform: translateY(2px);
}
.btn_left {
	width: 100px;
	padding: 8px 0px;
	text-align: center;
	display: inline-block;
	text-decoration: none;
	background: #fff;		/*背景色*/
	color: #31436B;		/*アクセントカラー*/
	font-weight: bold;
	box-shadow: 0px 2px 3px 3px rgba(0, 0, 0, 0.29);
	margin-right: 15px;
	display: inline-block;
	border: none;
	font-size: 15px;
}
.btn_left:hover {
	background-color: #f0f0f0;;
}
.btn_left:active {
	box-shadow: inset 0 0 2px rgba(128, 128, 128, 0.1);
	transform: translateY(2px);
}

/* アイコン */
.icon{
	text-decoration: none;
	vertical-align:middle;
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
	background-color: #f0f0f0;
	height: 90%;       /*モーダルウィンドウのサイズ*/
	width: auto;
	overflow: auto;
}
.closeModal {
	position: absolute;
	top: 0.5rem;
	right: 1rem;
	cursor: pointer;
}

</style>

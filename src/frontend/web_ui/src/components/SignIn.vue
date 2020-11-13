<template>
	<div>
		<div class="backGround"></div>
		<div id="sheet" class="login">
			<div id="signin_set">
				<img src="~@/assets/logo.svg" alt="logo" class="logo">
				<p class="form-title">Sign in</p>
			</div>
			<form action="post">
				<div class="email">
					<p class="id"><input placeholder="Enter Email Address" type="text" name="mail" /></p>
				</div>
				<div class="password">
					<p class="pass"><input placeholder="Enter Password" type="password" name="pass" /></p>
				</div>
			</form>

			<div id="btn_login">
				<button class="btn_login" @click="login()">Sign in</button>
			</div>
		</div>
	</div>
</template>

<script>
	export default{
		data() {
			return{
				emailAddress: null,
				password: null,
			}
		},
		methods: {
			login(){
					sessionStorage.setItem('organizationId', this.postLoginData())
					this.$router.push({
						name: 'MLComponents'
					})
			},
			postLoginData(){
					// TODO: ログイン処理
					return 'dep-a'
			}
		}
	}
</script>

<style scoped>
	/*============================================
	全般的なスタイル
	============================================*/
	* {
		margin:0; padding:0; 	/*全要素のマージン・パディングをリセット*/
	}
	body{
		color:#000066;		/*文字色*/
		font-size: 16px;
		font-family:Meiryo;			/*フォント*/
	}
	.backGround{
		position: absolute;
		height: 100%;
		width: 100%;
		background-image: url("~@/assets/background.jpg");
		background-size:cover;
	}
	#sheet{
		position: absolute;
		top: 50%;
		left: 75%;
		transform: translate(-50%,-50%);
		border-radius: 6px;
		background:#f0f0f0;	/*シート背景色（灰色）*/
		padding: 20px 0px;
		text-align: center;
		width: 400px;
		box-shadow: 0 13px 20px 3px rgba(0,0,0,.46);
	}

	/*============================================
	ロゴ、タイトル
	============================================*/

	#signin_set{
		display: flex;
		justify-content: center;
	}

	#signin_set p {
		display: inline;
		margin: auto 130px 0px 10px;
	}

	.label{
		text-align: left;
		margin-left: 50px ;
		margin-bottom: 0px;
	}

	.form-title{
		text-align: center;
		font-size: 30px;
	}

	/*============================================
	テキストエリア
	============================================*/
	.email, .password {
		padding:5px;
		margin-top:15px;
	}

	.id,.pass{
		margin-top: 0px;
		text-align: center;
	}

	input[type="text"],
	input[type="password"] {
		border: none;
		height: 25px;
		width: 300px;
		padding: 4px;
		font-size: 16px;
		background-color: #fff;	/*エリア背景色*/
	}

	input[type="text"]:hover,
	input[type="password"]:hover{
		box-shadow: 0px 0px 5px rgba(0,0,0,.46);
	}

	/*============================================
	ボタン
	============================================*/
	.btn_login {
		width: 100px;
		font-size: 15px;
		padding: 5px 0em;
		text-align: center;
		display: inline-block;
		text-decoration: none;
		background: #9bbb59;		/*ボタン色*/
		color: #fff;		/*文字色*/
		font-weight: bold;
		box-shadow: 0px 2px 2px rgba(0, 0, 0, 0.29);
		margin: 20px 0px 10px;
		border-style: none;
	}
	.btn_login:active {
		box-shadow: inset 0 0 2px rgba(128, 128, 128, 0.1);
		transform: translateY(2px);
	}
</style>
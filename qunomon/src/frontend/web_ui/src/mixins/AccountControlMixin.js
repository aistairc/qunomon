import { csrfMixin } from '../mixins/csrfMixin';

export const AccountControlMixin = {
    mixins: [csrfMixin],
    data(){
        return {
            userId: null,
            aithub_setting_flag: false, // DB設定値（AIT-HUB使用／不使用）
            aithub_network_status: false, // AIT-HUBとのネットワークが正常か異常か
            aithub_linkage_mode: false // AIT-HUBを使用するか否かの最終決定フラグ
        }
    },
    methods: {
        signIn(){

            // SESSION側でログインフラグが設定されない場合のみ初期処理を実施する
            if (!sessionStorage.hasOwnProperty('session_signIn_flag')) {
                // organizationIdを設定する
                sessionStorage.setItem('organizationId', this.postLoginData());
                // SESSIONにサインインフラグを設定する
                sessionStorage.setItem('session_signIn_flag', true);
                // AITHUB使用状態を設定する
                this.setAithubUsing();

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
                //         params: {error}
                //     })
                // })
            }
        },
        async setAithubUsing(){
            // DB設定値（AIT-HUB使用／不使用）チェック
            await this.checkAITHubSetting();
            // AIT-HUBとの接続状態チェック
            await this.checkAithubNetwork();
            if (this.aithub_setting_flag && this.aithub_network_status) {
                sessionStorage.setItem('aithub_linkage_mode', '1');
            }
            else {
                sessionStorage.setItem('aithub_linkage_mode', '0');
            }
        },
        setAITHubLinkageMode(){
            if (sessionStorage.getItem('aithub_linkage_mode') == '1') {
                this.aithub_linkage_mode = true;
            } else {
                this.aithub_linkage_mode = false;
            }
        },
        async checkAithubNetwork(){
            // AIT-HUBとの接続チェック（health-checkは認証無しで動くので、他のAPIにする）
            var url = this.$aithubURL + '/health-check';
            // var url = this.$aithubURL + '/aits/ranking';
            await this.$axios.get(url)
            .then((response) => {
                // AWS版 response.status == 200
                if (response.statusText == 'OK' ) {
                    // 接続OK
                    this.aithub_network_status = true;
                    sessionStorage.setItem('aithub_network_status', '1');
                }
                else {
                    this.aithub_network_status = false;
                    sessionStorage.setItem('aithub_network_status', '0');
                }
            })
            .catch(() => {
                this.aithub_network_status = false;
            })
        },
        async checkAITHubSetting() {
            const url = this.$backendURL + '/setting/' + 'aithub_linkage_flag';
            await this.$axios.get(url)
            .then((response) => {
                if (response.data.Value == '1') {
                    this.aithub_setting_flag = true;
                    sessionStorage.setItem('aithub_setting_flag', '1');
                } else {
                    this.aithub_setting_flag = false;
                    sessionStorage.setItem('aithub_setting_flag', '0');
                }
            })
            .catch((error) => {
                this.$router.push({
                    name: 'Information',
                    params: {error}
                })
            });
        },
        changeAITHubSetting(link_flag) {
            var aithub_linkage_flag = null
            if (link_flag == 'on') {
                aithub_linkage_flag = '1'
            } else {
                aithub_linkage_flag = '0'
            }
            const url = this.$backendURL + '/setting/' + 'aithub_linkage_flag';
            var requestData = {
                Value: aithub_linkage_flag
            }
            //リクエスト時のオプションの定義
            const config = {
                headers:{
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRF-TOKEN' : this.getCookie("csrf_access_token")
                },
                withCredentials:true,
            }
            this.$axios.put(url, requestData, config)
            .then(() => {
                if (aithub_linkage_flag == '1' && 
                    sessionStorage.getItem('aithub_network_status') == '1') {
                    sessionStorage.setItem('aithub_linkage_mode', '1');
                } else {
                    sessionStorage.setItem('aithub_linkage_mode', '0');
                }
                sessionStorage.setItem('aithub_setting_flag', aithub_linkage_flag)

                window.location.reload();
            })
            .catch((error) => {
                this.$router.push({
                    name: 'Information',
                    params: {error}
                })
            });

        },
        postLoginData(){
            // TODO: ログイン処理
            return 'dep-a'
        },
        signOutAitHub() {
            sessionStorage.clear();

            const url = '/Setting/logout';
            this.$axios.get(url)
            .then(() => {
                window.location.reload();
            })
            .catch((error) => {
                this.$router.push({
                    name: 'Information',
                    params: {error}
                })
            });

            this.$router.push({
                name: 'dummy'
            });
        }
    }
}
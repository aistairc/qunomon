import { csrfMixin } from '../mixins/csrfMixin';
import EventBus from '../eventBus';

export const AccountControlMixin = {
    mixins: [csrfMixin],
    data(){
        return {
            userId: null,
            aithub_linkage_mode: false // AIT-HUBを使用するか否かの最終決定フラグ
        }
    },
    methods: {
        setAITHubLinkageMode(){
            if (sessionStorage.getItem('aithub_linkage_mode') == '1') {
                this.aithub_linkage_mode = true;
            } else {
                this.aithub_linkage_mode = false;
            }
        },
        changeAITHubSetting(link_flag) {
            var aithub_linkage_flag = null
            if (link_flag == 'on') {
                aithub_linkage_flag = '1'
            } else {
                aithub_linkage_flag = '0'
            }
            const url = this.$backendURL + '/settingFront/' + 'aithub_linkage_flag';
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
                    query: {error:JSON.stringify({...error, response: error.response})}
                })
            });
        },
        signOutAitHub() {
            sessionStorage.setItem('aithub_network_status', '0');
            sessionStorage.setItem('aithub_linkage_mode', '0');

            const url = '/Setting/logout';
            this.$axios.get(url)
            .then(() => {
                sessionStorage.setItem('aithub_logout', '1')
                window.location.reload();
            })
            .catch((error) => {
                sessionStorage.setItem('aithub_logout_whit_error', error)
                // eslint-disable-next-line no-console
                console.log(error);
            });
            this.$router.push({ path: '/' }).catch(err => {
                if (err.name !== 'NavigationDuplicated') {
                    // eslint-disable-next-line no-console
                    console.error(err)
                }
            })
        },
        signOutAitHubWhitErr() {
            sessionStorage.setItem('aithub_network_status', '0');
            sessionStorage.setItem('aithub_linkage_mode', '0');
            const url = '/Setting/logout';
            this.$axios.get(url)
            .then(() => {
                window.location.reload();
            })
            .catch((error) => {
                // eslint-disable-next-line no-console
                console.log(error);
            });
            this.$router.push({ path: '/' }).catch(err => {
                if (err.name !== 'NavigationDuplicated') {
                    // eslint-disable-next-line no-console
                    console.error(err)
                }
            })
        },
        triggerMessage(messageCode, messageText) {
            EventBus.emit('show-message', messageCode, messageText);
        },
        triggerAithubUsing() {
            EventBus.emit('set-aithub-using');
        },
    }
}
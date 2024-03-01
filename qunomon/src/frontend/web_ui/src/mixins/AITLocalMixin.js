import { csrfMixin } from '../mixins/csrfMixin';

export const AITLocalMixin = {
    mixins: [csrfMixin],
    data(){
        return {
            languagedata: null,
            ait_local_list: []
        }
    },
    methods: {
        setLanguageData() {
            var lang = sessionStorage.getItem('language')
            if (lang === null) {
                this.$i18n.locale = 'en';
            } else {
                this.$i18n.locale = lang;
            }
        },
        changeLanguage(lang, screenName) {
            sessionStorage.setItem('language', lang);
            this.changeTableTitleLanguage(screenName);
        },
        changeTableTitleLanguage(screenName) {
            var columns = null;
            if (screenName == 'aitLocalInstall') {
                columns = this.aitLocalInstall_columns;
                for (var a in columns) {
                    columns[a].label = this.setAITLocalInstallTableLanguage(columns[a].field)
                }
            }
        },
        getAITLocalList(){
            var url = this.$backendURL + '/ait_local';
            
            this.$axios.get(url)
            .then((response) => {
                this.ait_local_list = response.data.AITLocalList;
                for (let i in this.ait_local_list) {
                    this.aitLocalInstall_rows.push({
                            ait_id: this.ait_local_list[i].Id,
                            ait_name: this.ait_local_list[i].Name,
                            description: this.ait_local_list[i].Description,
                            version: this.ait_local_list[i].Version,
                            create_user_account: this.ait_local_list[i].CreateUserAccount,
                            create_user_name: this.ait_local_list[i].CreateUserName,
                            status: this.ait_local_list[i].Status,
                            detail: '',
                            install: true
                        });
                }
            })
            .catch((error) => {
                this.$router.push({
                    name: 'Information',
                    params: {error}
                })
            })
        },
        aitCreate() {
            if (this.ait_file == null) {
               alert(this.$t("aitLocalInstall.fileRequiredError"));
               return;
           }

           const url = this.$backendURL + '/ait_local_front';
           let data = new FormData;
           data.append('ait_zip', this.ait_file);
           //リクエスト時のオプションの定義
           const config = {
                headers:{
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRF-TOKEN' : this.getCookie("csrf_access_token")
                },
                withCredentials:true,
            }

           this.$axios.post(url, data, config)
               .then((response) => {
                   this.result = response.data;
                   window.location.reload();
               })
               .catch((error) => {
                   this.$router.push({
                       name: 'Information',
                       params: {error}
                   })
               })
       },
    }
}
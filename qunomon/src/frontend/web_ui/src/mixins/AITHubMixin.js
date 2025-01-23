import { csrfMixin } from '../mixins/csrfMixin';

export const AITHubMixin = {
    mixins: [csrfMixin],
    data(){
        return {
            languagedata: null,
            aitList_local: [],
            aitList_AITHub: [],
            aitManifest: {},
            searchConditions: [],
            requestData: {},
            result: null
        }
    },
    methods: {
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
        changeLanguage(lang, screenName) {
            sessionStorage.setItem('language', lang);
            this.changeTableTitleLanguage(screenName);
        },
        changeTableTitleLanguage(screenName) {
            var columns = null;
            if (screenName == 'aitDashboard') {
                columns = this.aitDashboard_columns;
                for (var d in columns) {
                    columns[d].label = this.setAITDashboardTableLanguage(columns[d].field)
                }
            } else if(screenName == 'aitSearch') {
                columns = this.aitSearch_columns;
                for (var s in columns) {
                    columns[s].label = this.setAITSearchTableLanguage(columns[s].field)
                }
            } else if(screenName == 'aitRanking') {
                columns = this.aitRanking_columns;
                for (var r in columns) {
                    columns[r].label = this.setAITRankingTableLanguage(columns[r].field)
                }
            } else if (screenName == 'aitDetail') {
                this.setLanguageData();
            }
        },
        async getAITListFromLocal(screenName) {
            this.$axios.get(this.$backendURL + '/testRunners')
            .then((response) => {
                this.aitList_local = response.data.TestRunners;
                if (screenName == 'aitDashboard') {
                    for (let i in this.aitList_local) {
                        this.aitDashboard_rows.push({
                                ait_id: this.aitList_local[i].Id,
                                ait_name: this.aitList_local[i].Name,
                                description: this.aitList_local[i].Description,
                                create_user_account: this.aitList_local[i].CreateUserAccount,
                                using_TD: false,
                                install: true
                            });
                    }
                }
                sessionStorage.setItem('aitList_local', JSON.stringify(this.aitList_local));
            })
            .catch((error) => {
                this.$router.push({
                    name: 'Information',
                    query: {error:JSON.stringify({...error, response: error.response})}
                })
            })
            .finally(() => {
                // aitDashboard画面の場合
                if (screenName == 'aitDashboard') {
                    this.setAITDashboardRows();
                // aitDetail画面の場合    
                } else if (screenName == 'aitDetail') {
                    this.getAITDetail();
                // aitSearch または aitRanking画面の場合  
                } else if  (screenName == 'aitSearch' || screenName == 'aitRanking') {
                    this.getAITListFromAITHub([], screenName);
                } 
            });
        },
        setAITDashboardRows(){
            for (let row in this.aitDashboard_rows){
                const usingTd_url = this.$backendURL + '/testRunners'
                                    + '/' + this.aitDashboard_rows[row].ait_id
                                    + '/usingTD';
                this.$axios.get(usingTd_url)
                .then((response) => {
                    if (response.data.UsingTD.length > 0) {
                        this.usingTDList.push({
                            ait_id: response.data.UsingTD[0].TestRunnerID,
                            using_TD: true
                        });
                    } else {
                        this.usingTDList.push({
                            ait_id: null,
                            using_TD: false
                        });
                    }
                    // 非同期処理の対応のため、ループの最後回のみ実行する
                    if (this.aitDashboard_rows.length == this.usingTDList.length) {
                        for (var r in this.aitDashboard_rows) {
                            for (var u in this.usingTDList) {
                                if (this.aitDashboard_rows[r].ait_id == this.usingTDList[u].ait_id) {
                                    this.aitDashboard_rows[r].using_TD = this.usingTDList[u].using_TD;
                                    break;
                                }
                            }
                        }
                    }
                })
                .catch((error) => {
                    this.$router.push({
                        name: 'Information',
                        query: {error:JSON.stringify({...error, response: error.response})}
                    })
                });
            }
        },
        async getAITListFromAITHub(searchConditions, screenName){
            var url = '';
            if (screenName == 'aitSearch') {
                url = this.$aithubURL + '/aits/search';
            } else if (screenName == 'aitRanking') {
                url = this.$aithubURL + '/aits/ranking';
            }
            
            await this.$axios.get(url, { 'params' : searchConditions })
            .then((response) => {
                this.aitList_AITHub = response.data.AITs;
                this.setAITRows();
            })
            .catch((error) => {
                this.signOutAitHubWhitErr();
                this.triggerMessage('aithub_E02', error)
            })
        },
        setAITRows(){
            var aitList_local_key = '';
            var aitList_AITHub_key = '';
            var installFlag = false;
            var ait_id = null;
            for (let i in this.aitList_AITHub) {
                if (this.aitList_AITHub[i].status.type == 'OK'){
                    installFlag = false;
                    ait_id = this.aitList_AITHub[i].ait_id;

                    aitList_AITHub_key = this.aitList_AITHub[i].name +
                                         this.aitList_AITHub[i].create_user_account + 
                                         this.aitList_AITHub[i].version;
                    for (let j in this.aitList_local) {
                        aitList_local_key = this.aitList_local[j].Name + 
                                            this.aitList_local[j].CreateUserAccount + 
                                            this.aitList_local[j].Version;
                        if (aitList_AITHub_key == aitList_local_key) {
                            installFlag = true;
                            ait_id = this.aitList_local[j].Id;
                            break;
                        }
                    }

                    this.aitRows.push({
                        ait_id: ait_id,
                        ait_name: this.aitList_AITHub[i].name,
                        description: this.aitList_AITHub[i].description,
                        create_user_account: this.aitList_AITHub[i].create_user_account,
                        create_user_name: this.aitList_AITHub[i].create_user_name,
                        version: this.aitList_AITHub[i].version,
                        downloads: this.aitList_AITHub[i].downloads,
                        views: this.aitList_AITHub[i].views,
                        install: installFlag
                    });
                }
            }
        },
        async aitInstallCore(aithub_id, create_user_account, create_user_name){
            // token取得するまではawaitで後続処理は待機
            const aithub_url = this.$aithubURL + '/pull_authorization';
            await this.$axios.get(aithub_url)
            .then((response) => {
                if(response.data.Token !== undefined){
                    this.requestData.token = response.data.Token;
                }
                else{
                    this.$router.push({
                        name: 'Information',
                        query: {error: JSON.stringify(
                            {
                                response:{
                                    data:{
                                        Code: '',
                                        message: 'AitHub not login.'
                                    }
                                }
                            }
                        )}
                    })
                }
            })
            .catch((error) => {
                this.$router.push({
                    name: 'Information',
                    query: {error:JSON.stringify({...error, response: error.response})}
                })
            });

            const url = this.$aithubURL + '/aits/' + aithub_id + '/manifest';
            this.$axios.get(url)
            .then((response) => {
                this.aitManifest = response.data.AITManifest;

                for (var inv in this.aitManifest.inventories) {
                    if (this.aitManifest.inventories[inv].depends_on_parameter == null) {
                        delete this.aitManifest.inventories[inv].depends_on_parameter;
                    }
                }

                this.requestData.aitManifest = JSON.stringify(this.aitManifest);
                this.requestData.installAITFromAITHub = true;
                this.requestData.create_user_account = create_user_account;
                this.requestData.create_user_name = create_user_name;
                
                const url = this.$backendURL + '/testRunnersFront';
                //リクエスト時のオプションの定義
                const config = {
                    headers:{
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRF-TOKEN' : this.getCookie("csrf_access_token")
                    },
                    withCredentials:true,
                }
                this.$axios.post(url, this.requestData, config)
                .then((response) => {
                    this.result = response.data;
                    // installの判定に使用する項目だけ追加
                    if (this.aitList_local === undefined) {
                        this.aitList_local = [];
                    }
                    this.aitList_local.push({
                        Name: this.aitManifest.name,
                        CreateUserAccount: create_user_account,
                        Version: this.aitManifest.version
                    });
                    sessionStorage.setItem('aitList_local', JSON.stringify(this.aitList_local));
                    window.location.reload();
                })
                .catch((error) => {
                    this.$router.push({
                        name: 'Information',
                        query: {error:JSON.stringify({...error, response: error.response})}
                    })
                });
            })
            .catch((error) => {
                this.signOutAitHubWhitErr();
                this.triggerMessage('aithub_E02', error)
            });
        }
    }
}
import { csrfMixin } from '../mixins/csrfMixin';

export const GuidelinesMixin = {
    mixins: [csrfMixin],
    data(){
        return {
            languagedata: null,
            result: null,
            guidelineList_AITHub: [],
            guidelineList_Local: [],
            qdList_AITHub: [],
            scopeList_AITHub: [],
            scopeQDList_AITHub: [],
            qd_map: new Map(),
            local_gd_map : new Map(),
            json_date: null
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
            if (screenName == 'guidelines') {
                columns = this.guideline_columns;
                for (var g in columns) {
                    columns[g].label = this.setGuidelinesTableLanguage(columns[g].field)
                }
            } else if (screenName == 'guidelineDetail') {
                this.setLanguageData();
            } else if (screenName == 'guidelineCreate') {
                this.setLanguageData();
            }
        },
        async getGuidelineListFromAIThub(){
            const url = this.$aithubURL + '/guidelines'
            await this.$axios.get(url)
            .then((response) => {
                this.guidelineList_AITHub =  response.data.Guidelines;
            })
            .catch((error) => {
                this.errorTransition(error);
            })
        },
        async getGuidelineListFromLocal(){
            const url = this.$backendURL + '/guidelines'
            await this.$axios.get(url)
            .then((response) => {
                this.guidelineList_Local = response.data.Guidelines;
            })
            .catch((error) => {
                this.errorTransition(error);
            })
        },
        async setGuidelineRows_AITHubLinkageMode(){

            // ガイドラインの画面表示ID
            var guideline_display_id = 0;

            // インストール済みのローカルガイドラインを取得する
            for (let i_local in this.guidelineList_Local) {
                var aithub_delete_flag = true;
                var gd_local_aithub_id = this.guidelineList_Local[i_local].AithubGuidelineId;

                if (gd_local_aithub_id == null) {
                    aithub_delete_flag = false;
                } else {
                    for (let j_local in this.guidelineList_AITHub) {
                        var guideline_aithub = this.guidelineList_AITHub[j_local];
                        if (gd_local_aithub_id == guideline_aithub.Id) {
                            aithub_delete_flag = false;
                        }
                    }
                }
                
                this.local_gd_map.set(gd_local_aithub_id, this.guidelineList_Local[i_local]);

                this.guideline_rows.push({
                    guideline_display_id: guideline_display_id,
                    guideline_aithub_id: gd_local_aithub_id,
                    guideline_name: this.guidelineList_Local[i_local].Name,
                    description: this.guidelineList_Local[i_local].Description,
                    creator: this.guidelineList_Local[i_local].Creator,
                    publisher: this.guidelineList_Local[i_local].Publisher,
                    identifier: this.guidelineList_Local[i_local].Identifier,
                    publishDatetime: this.guidelineList_Local[i_local].PublishDatetime,
                    creationDatetime: this.guidelineList_Local[i_local].CreationDatetime,
                    updateDatetime: this.guidelineList_Local[i_local].UpdateDatetime,
                    install: true,
                    guideline_local_id: this.guidelineList_Local[i_local].Id,
                    aithub_delete_flag: aithub_delete_flag
                });
                
                if (aithub_delete_flag && this.guidelineList_Local[i_local].AIThubDeleteFlag != true) {
                    const url = this.$backendURL + '/guidelineFront/' + this.guidelineList_Local[i_local].Id;
                    //リクエスト時のオプションの定義
                    const config = {
                        headers:{
                            'X-Requested-With': 'XMLHttpRequest',
                            'X-CSRF-TOKEN' : this.getCookie("csrf_access_token")
                        },
                        withCredentials:true,
                    }
                    this.$axios.put(url, { AIThubDeleteFlag: true }, config)
                    .catch((error) => {
                        this.errorTransition(error);
                    })
                }
                guideline_display_id++;
            }

            // 未インストールのAITHUBガイドラインを取得する
            for (let i in this.guidelineList_AITHub) {
                var gd_aithub_id = this.guidelineList_AITHub[i].Id;

                if (this.local_gd_map.get(gd_aithub_id)) {
                    continue;
                }

                var gd_local_id = 0;
                var install_flag = false;

                for (let j in this.guidelineList_Local) {
                    if (gd_aithub_id == this.guidelineList_Local[j].AithubGuidelineId) {
                        gd_local_id = this.guidelineList_Local[j].Id;
                        install_flag = true;
                        break;
                    }
                }
                
                this.guideline_rows.push({
                        guideline_display_id: guideline_display_id,
                        guideline_aithub_id: gd_aithub_id,
                        guideline_name: this.guidelineList_AITHub[i].Name,
                        description: this.guidelineList_AITHub[i].Description,
                        creator: this.guidelineList_AITHub[i].Creator,
                        publisher: this.guidelineList_AITHub[i].Publisher,
                        identifier: this.guidelineList_AITHub[i].Identifier,
                        publishDatetime: this.guidelineList_AITHub[i].PublishDatetime,
                        creationDatetime: this.guidelineList_AITHub[i].CreationDatetime,
                        updateDatetime: this.guidelineList_AITHub[i].UpdateDatetime,
                        install: install_flag,
                        guideline_local_id: gd_local_id,
                        aithub_delete_flag: false
                    });

                guideline_display_id++;
            }
        },
        async setGuidelineRows_LocalMode(){
            for (let i in this.guidelineList_Local) {
                this.guideline_rows.push({
                    guideline_display_id: i,
                    guideline_aithub_id: this.guidelineList_Local[i].AithubGuidelineId,
                    guideline_name: this.guidelineList_Local[i].Name,
                    description: this.guidelineList_Local[i].Description,
                    creator: this.guidelineList_Local[i].Creator,
                    publisher: this.guidelineList_Local[i].Publisher,
                    identifier: this.guidelineList_Local[i].Identifier,
                    publishDatetime: this.guidelineList_Local[i].PublishDatetime,
                    creationDatetime: this.guidelineList_Local[i].CreationDatetime,
                    updateDatetime: this.guidelineList_Local[i].UpdateDatetime,
                    install: true,
                    guideline_local_id: this.guidelineList_Local[i].Id,
                    aithub_delete_flag: this.guidelineList_Local[i].AIThubDeleteFlag
                });
            }
        },
        installGuidelineCore(guideline_aithub_id){
            const url = this.$aithubURL + '/' + guideline_aithub_id +'/guideline_schema_file'
            this.$axios.get(url)
            .then((response) => {
                var guideline_schema_file = response.data.GuidelineSchemaFile;
                // 入力されたjsonデータを文字列にする
                const json_str = JSON.stringify(guideline_schema_file, null, '    ');
                // ファイル形式にする
                const blob = new Blob([json_str],{type:"application/json"});
                const g_file = new File([blob], "guideline.json", { type: "application/json" });
                const fd = new FormData();
                fd.append("guideline_schema", g_file);
                fd.append("guideline_aithub_id", guideline_aithub_id);

                const url = this.$backendURL + '/guidelines/guideline_schema_file_front';

                //リクエスト時のオプションの定義
                const config = {
                    headers:{
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRF-TOKEN' : this.getCookie("csrf_access_token")
                    },
                    withCredentials:true,
                }

                this.$axios.post(url, fd, config)
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
            })
            .catch((error) => {
                this.errorTransition(error);
            })
        },
        deleteGuidelineCore(params){
            const url = this.$backendURL + '/guidelineFront/' + params.row.guideline_local_id;
            //リクエスト時のオプションの定義
            const config = {
                headers:{
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRF-TOKEN' : this.getCookie("csrf_access_token")
                },
                withCredentials:true,
            }
            this.$axios.delete(url, config)
            .then((response) => {
                this.result = response.data;
                window.location.reload()
            })
            .catch((error) => {
                this.errorTransition(error);
            })
            
        },
        async getQDList(guideline_id, install_flag){
            var url = ''
            if (install_flag) {
                url = this.$backendURL + '/guidelines/' + guideline_id + '/quality_dimensions'
            } else {
                url = this.$aithubURL + '/' + guideline_id + '/quality_dimensions'
            }
            await this.$axios.get(url)
            .then((response) => {
                this.qdList_AITHub = response.data.QualityDimensions;
            })
            .catch((error) => {
                this.errorTransition(error);
            })
        },
        async getScopeList(guideline_id, install_flag){
            var url = ''
            if (install_flag) {
                url = this.$backendURL + '/guidelines/' + guideline_id + '/scopes'
            } else {
                url = this.$aithubURL + '/' + guideline_id + '/scopes'
            }
            await this.$axios.get(url)
            .then((response) => {
                this.scopeList_AITHub = response.data.Scopes;
            })
            .catch((error) => {
                this.errorTransition(error);
            })
        },
        async getScopeQDList(guideline_id, install_flag){
            var url = ''
            if (install_flag) {
                url = this.$backendURL + '/guidelines/' + guideline_id + '/scope_quality_dimensions'
            } else {
                url = this.$aithubURL + '/' + guideline_id + '/scope_quality_dimensions'
            }
            await this.$axios.get(url)
            .then((response) => {
                this.scopeQDList_AITHub = response.data.ScopeQualityDimensions;
            })
            .catch((error) => {
                this.errorTransition(error);
            })
        },
        async setQDRows(){
            for (let i in this.qdList_AITHub) {
                this.qd_rows.push({
                    qd_name: this.qdList_AITHub[i].Name,
                    qd_description: this.qdList_AITHub[i].Description,
                    qd_url: this.qdList_AITHub[i].Url
                })
                this.qd_map.set(this.qdList_AITHub[i].Id, this.qdList_AITHub[i].Name);
            }
        },
        async setScopeQDRows(){
            for (let i in this.scopeList_AITHub) {
                var scope_qd_list = [];
                for (let j  in this.scopeQDList_AITHub) {
                    if (this.scopeList_AITHub[i].Id == this.scopeQDList_AITHub[j].ScopeId) {
                        scope_qd_list.push(this.qd_map.get(this.scopeQDList_AITHub[j].QualityDimensionId));
                    }
                }

                this.scope_rows.push({
                    scope_name: this.scopeList_AITHub[i].Name,
                    scope_qds: scope_qd_list.join(' , ')
                })
            }

        },
        formatFnYMD(date){
            var datetime = '';
            if (date) {
                var moment = require('moment-timezone');
                var datetime_conv = moment.tz(date, 'UTC');
                datetime_conv.tz(moment.tz.guess());

                datetime = datetime_conv.format().slice(0,10);
                datetime = datetime.replace(/T/g, ' ');
                datetime = datetime.replace(/-/g, '/');
            }
            return datetime;
        },
        errorTransition(error){
            this.$router.push({
                name: 'Information',
                params: {error}
            })
        },
        async getGuidelineJsonData(guideline_id, install_flag){
            var url = '';
            if (install_flag) {
                url = this.$backendURL + '/guidelines/' + guideline_id + '/guideline_schema_file';
            } else {
                url = this.$aithubURL + '/' + guideline_id +'/guideline_schema_file';
            }
            await this.$axios.get(url)
            .then((response) => {
                this.json_date = response.data.GuidelineSchemaFile;
            })
            .catch((error) => {
                this.errorTransition(error);
            })
        },
        guidelineValidationCheck(jsonDate, errorMessages){

            // scopesとquality_dimensionsのIDチェック
            let scopes = jsonDate.guideline.scopes;
            // scope内に設定されたquality_dimensionsのIDのリスト
            let scope_qd_list = [];
            for(let a = 0; a < scopes.length; a++){
                if(typeof(scopes[a].quality_scopes) != "undefined"){
                    let qds = scopes[a].quality_scopes.quality_dimensions;
                    for(let b = 0; b < qds.length; b++){
                        scope_qd_list.push(qds[b]);
                    }
                }
            }
            let quality_dimensions = jsonDate.guideline.quality_dimensions;
            // quality_dimensions内に設定されたquality_dimensionsのIDのリスト
            let qd_list = [];
            for(let c = 0; c < quality_dimensions.length; c++){
                if(typeof(quality_dimensions[c].id) != "undefined"){
                    qd_list.push(quality_dimensions[c].id);
                }
            }
            // scope内に設定されたquality_dimensionsが、quality_dimensions内に存在しなければエラー
            if(scope_qd_list.length == 0){
                errorMessages.push("quality dimensions ID does not exist in scopes.")
            }
            else if(qd_list.length == 0){
                errorMessages.push("quality dimensions ID does not exist in quality dimensions.")
            }
            for(let d = 0; d < scope_qd_list.length; d++){
                if(!qd_list.includes(scope_qd_list[d])){
                    errorMessages.push("quality dimensions ID(" + scope_qd_list[d] + ") that exists in scopes does not exist in quality_dimensions.")
                }
            }

            // 必須
            if(scopes == null || scopes.length == 0){
                errorMessages.push("scopes does not exist");
            }
            else{
                for(let e = 0; e < scopes.length; e++){
                    if(typeof(scopes[e].name) != "string"){
                        // 必須
                        errorMessages.push("scopes.name " + scopes[e].name + " is not string");
                    }
                    let sds = scopes[e].scope_descriptors;
                    // 必須
                    if(sds == null || sds.length == 0){
                        errorMessages.push("scopes.scope_descriptors does not exist");
                    }
                    else{
                        for(let f = 0; f < sds.length; f++){
                            // 必須
                            if(typeof(sds[f].title) != "string"){
                                errorMessages.push("scopes.scope_descriptors.title " + sds[f].title + " is not string");
                            }
                            // 必須
                            if(typeof(sds[f].description) != "string"){
                                errorMessages.push("scopes.scope_descriptors.description " + sds[f].description + " is not string");
                            }
                        }
                    }
                    if(typeof(scopes[e].quality_scopes) == "undefined"){
                        errorMessages.push("scopes.quality_scopes does not exist");
                    }
                    else{
                        let qds = scopes[e].quality_scopes.quality_dimensions;
                        // 必須
                        if(qds == null || qds.length == 0){
                            errorMessages.push("scopes.quality_scopes.quality_dimensions does not exist");
                        }
                        else{
                            for(let g = 0; g < qds.length; g++){
                                // 必須
                                if(typeof(qds[g]) != "string"){
                                    errorMessages.push("scopes.quality_scopes " + qds[g] + " is not string");
                                }
                            }
                        }
                        let ext_quality_dimensions = scopes[e].quality_scopes.ext_quality_dimensions;
                        // 任意
                        if(ext_quality_dimensions != null){
                            for(let h = 0; h < ext_quality_dimensions.length; h++){
                                // 必須
                                if(typeof(ext_quality_dimensions[h]) != "string"){
                                    errorMessages.push("scopes.ext_quality_dimensions " + ext_quality_dimensions[h] + " is not string");
                                }
                            }
                        }
                    }
                }
            }
            // 任意
            let level_requirements_details = jsonDate.guideline.level_requirements;
            let level_requirements_details_list = [];
            if (level_requirements_details != null) {
                for(let lds = 0; lds < level_requirements_details.length; lds++){
                    var level_requirements_id_errFlag = false;
                    var level_requirements_description_errFlag = false;
                    // 必須
                    if(typeof(level_requirements_details[lds].id) != "string"){
                        errorMessages.push("level_requirements.id " + level_requirements_details[lds].id + " is not string");
                        level_requirements_id_errFlag = true;
                    }
                    // 必須
                    if(typeof(level_requirements_details[lds].description) != "string"){
                        errorMessages.push("level_requirements.description " + level_requirements_details[lds].description + " is not string");
                        level_requirements_description_errFlag = true;
                    }

                    // guideline直下のlevel_requirementsに設定されたIDのリスト
                    if(!level_requirements_id_errFlag && !level_requirements_description_errFlag){
                        level_requirements_details_list.push(level_requirements_details[lds].id);
                    }
                }
            }

            // 必須
            if(quality_dimensions == null || quality_dimensions.length == 0){
                errorMessages.push("quality_dimensions does not exist");
            }
            else{
                for(let i = 0; i < quality_dimensions.length; i++){
                    // 必須
                    if(typeof(quality_dimensions[i].id) != "string"){
                        errorMessages.push("quality_dimensions.id " + quality_dimensions[i].id + " is not string");
                    }
                    // 必須
                    if(typeof(quality_dimensions[i].name) != "string"){
                        errorMessages.push("quality_dimensions.name " + quality_dimensions[i].name + " is not string");
                    }
                    // 必須
                    if(typeof(quality_dimensions[i].description) != "string" ){
                        errorMessages.push("quality_dimensions.description " + quality_dimensions[i].description + " is not string");
                    }
                    // 任意
                    if(typeof(quality_dimensions[i].category) != "string" && typeof(quality_dimensions[i].category) != "undefined"){
                        errorMessages.push("quality_dimensions.category " + quality_dimensions[i].category + " is not string");
                    }
                    // 任意
                    if(typeof(quality_dimensions[i].external_reference) != "string" && typeof(quality_dimensions[i].external_reference) != "undefined"){
                        errorMessages.push("quality_dimensions.external_reference " + quality_dimensions[i].external_reference + " is not string");
                    }
                    let sub_dimensions = quality_dimensions[i].sub_dimensions;
                    // 任意
                    if(sub_dimensions != null){
                        for(let j = 0; j < sub_dimensions.length; j++){
                            // 必須
                            if(typeof(sub_dimensions[j]) != "string"){
                                errorMessages.push("quality_dimensions.sub_dimensions " + sub_dimensions[j] + " is not string");
                            }
                        }
                    }
                    let levels = quality_dimensions[i].levels;
                    // 必須
                    if(!(levels == null || levels.length == 0)){
                        for(let k = 0; k < levels.length; k++){
                            // 必須
                            if(typeof(levels[k].id) != "string"){
                                errorMessages.push("quality_dimensions.levels.id " + levels[k].id + " is not string");
                            }
                            // 任意
                            if(typeof(levels[k].name) != "string" && typeof(levels[k].name) != "undefined"){
                                errorMessages.push("quality_dimensions.levels.name " + levels[k].name + " is not string");
                            }
                            // 必須
                            if(typeof(levels[k].description) != "string"){
                                errorMessages.push("quality_dimensions.levels.description " + levels[k].description + " is not string");
                            }
                            // 必須
                            if(typeof(levels[k].level) != "number"){
                                errorMessages.push("quality_dimensions.levels.level " + levels[k].level + " is not number");
                            }
                            let level_requirements = levels[k].level_requirements;
                            // 任意
                            if(level_requirements != null){
                                for(let l = 0; l < level_requirements.length; l++){
                                    if(!level_requirements_details_list.includes(level_requirements[l])){
                                        errorMessages.push("level_requirements ID(" + level_requirements[l] + ")  does not exist in level_requirements.")
                                    }
                                }
                            }
                        }
                    }
                    let quality_inhibitors = quality_dimensions[i].quality_inhibitors;
                    // 任意
                    if(quality_inhibitors != null){
                        for(let m = 0; m < quality_inhibitors.length; m++){
                            // 必須
                            if(typeof(quality_inhibitors[m]) != "string"){
                                errorMessages.push("quality_dimensions.quality_inhibitors " + quality_inhibitors[m] + " is not string");
                            }
                        }
                    }
                    let measurements = quality_dimensions[i].measurements;
                    // 任意
                    if(measurements != null){
                        for(let n = 0; n < measurements.length; n++){
                            // 必須
                            if(typeof(measurements[n]) != "string"){
                                errorMessages.push("quality_dimensions.measurements " + measurements[n] + " is not string");
                            }
                        }
                    }
                }
            }
            let quality_inhibitor = jsonDate.guideline.quality_inhibitor;
            // 任意
            if(quality_inhibitor != null){
                // 必須
                if(typeof(quality_inhibitor.name) != "string"){
                    errorMessages.push("quality_inhibitor.name " + quality_inhibitor.name + " is not string");
                }
                // 必須
                if(typeof(quality_inhibitor.description) != "string"){
                    errorMessages.push("quality_inhibitor.description " + quality_inhibitor.description + " is not string");
                }
                // 任意
                let countermeasures = quality_inhibitor.countermeasures;
                if(countermeasures != null){
                    for(let o = 0; o < countermeasures.length; o++){
                        // 必須
                        if(typeof(countermeasures[o].id) != "string"){
                            errorMessages.push("quality_inhibitor.countermeasures.id " + quality_inhibitor[o].id + " is not string");
                        }
                        // 必須
                        if(typeof(countermeasures[o].description) != "string"){
                            errorMessages.push("quality_inhibitor.countermeasures.description " + quality_inhibitor[o].description + " is not string");
                        }
                    }
                }
            }
            let measurements = jsonDate.guideline.measurements;
            // 必須
            if(!(measurements == null || measurements.length == 0)){
                for(let p = 0; p < measurements.length; p++){
                    // 必須
                    if(typeof(measurements[p].id) != "string"){
                        errorMessages.push("measurements.id " + measurements[p].id + " is not string");
                    }
                    // 必須
                    if(typeof(measurements[p].name) != "string"){
                        errorMessages.push("measurements.name " + measurements[p].name + " is not string");
                    }
                    // 必須
                    if(typeof(measurements[p].type) != "string"){
                        errorMessages.push("measurements.type " + measurements[p].type + " is not string");
                    }
                    // 必須
                    if(typeof(measurements[p].description) != "string"){
                        errorMessages.push("measurements.description " + measurements[p].description + " is not string");
                    }
                    let sub_measurements = measurements.sub_measurements;
                    // 任意
                    if(sub_measurements != null){
                        for(let q = 0; q < sub_measurements.length; q++){
                            if(typeof(sub_measurements[q]) != "string"){
                                errorMessages.push("measurements.sub_measurements " + sub_measurements[q] + " is not string");
                            }
                        }
                    }
                }
            }
            let meta_info = jsonDate.guideline.meta_info;
            // 必須
            if(meta_info == null || meta_info.length == 0){
                errorMessages.push("meta_info does not exist");
            }
            else{
                for(let r = 0; r < meta_info.length; r++){
                    // 必須
                    if(typeof(meta_info[r].property) != "string"){
                        errorMessages.push("meta_info.property " + meta_info[r].property + " is not string");
                    }
                    // 必須
                    if(typeof(meta_info[r].content) != "string"){
                        errorMessages.push("meta_info.content " + meta_info[r].content + " is not string");
                    }
                    // 任意
                    if(typeof(meta_info[r].term) != "string" && typeof(meta_info[r].term) != "undefined"){
                        errorMessages.push("meta_info.content " + meta_info[r].term + " is not string");
                    }
                }
            }

        }
    }
}
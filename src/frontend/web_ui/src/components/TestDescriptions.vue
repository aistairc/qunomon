<template>
    <div>
        <!-- ヘッダ -->
        <header id="head">
            <div id="title">
                <h1 v-if="this.mlComponent">{{this.mlComponent.Name}}</h1>
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
            <ul id="submenu_body">
                <hr>
                <li class="un_place">
                    <router-link :to="{ name: 'Inventories'}" class="move_">{{$t("common.menuInventories")}}</router-link>
                </li>
                <li class="place">
                    <a href="#.htm">{{$t("common.menuTestDescriptions")}}</a>
                </li>
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
        <!-- 中央カラム -->
        <div id="main">
            <div id="main_body">
                <div id="search_table">
                    <!--検索-->
                    <div id="search">
                        <form action="post" class="search">
                            <p class="label search">
                                <span class="search">{{$t("testDescriptions.star")}}</span>
                                <input type="checkbox" class="star_check" v-model="starChecked">
                                <span class="search">{{$t("testDescriptions.status")}}</span>
                                    <select class="select" name="status" v-model="selectStatus">
                                        <option v-for="status in statuses" v-bind:value="status" :key="status">{{status}}</option>
                                    </select>
                                <span class="search">{{$t("testDescriptions.name")}}</span>
                                <template v-if="$i18n.locale === 'en'">
                                    <input class="name" type="text" placeholder="Test Name" name="example" v-model="searchName"/>
                                </template>
                                <template v-else>
                                    <input class="name" type="text" placeholder="テスト名称" name="example" v-model="searchName"/>
                                </template>
                                <span class="search">{{$t("testDescriptions.upDate")}}</span>
                                <input class="day" type="text" placeholder="yyyy/mm/dd" name="example" v-model="dateStart">
                                <span class="search" style="padding-left: 0;">～</span>
                                <input class="day day2" type="text" placeholder="yyyy/mm/dd" name="example" v-model="dateEnd">
                            </p>
                        </form>
                    </div>

                    <!--クリエイトボタン-->
                    <div class="btn">
                        <template v-if="$i18n.locale === 'en'">
                            <input type="submit" value="Create" @click="TestDescriptionCreate()" class="btn_single">
                        </template>
                        <template v-else>
                            <input type="submit" value="作成" @click="TestDescriptionCreate()" class="btn_single">
                        </template>
                    </div>

                    <!--テーブル-->
                    <div id="table" align="center" >
                        <TDRelation :key="rel_key" ref="rel" @reset="modalReset('modal')" @tableReroad="tableReroad"></TDRelation>
                        <table rules="rows" class="table_body">
                            <thead class="description_thead">
                                <tr class="t_center">
                                    <th class="th1"><input type="checkbox" v-model="allChecked" @click="onAllRowClick" name="checkbox_all"></th>
                                    <th class="th2"></th>
                                    <th @click="sortBy('Id')" :class="sortedClass('Id')" class="th3 sortable">{{$t("testDescriptions.tdId")}}</th>
                                    <th @click="sortBy('ParentID')" :class="sortedClass('ParentID')" class="th4 sortable">{{$t("testDescriptions.tdPId")}}</th>
                                    <th @click="sortBy('Result')" :class="sortedClass('Result')" class="th5 sortable">{{$t("testDescriptions.tStatus")}}</th>
                                    <th @click="sortBy('Name')" :class="sortedClass('Name')" class="th6 sortable">{{$t("testDescriptions.tdName")}}</th>
                                    <th @click="sortBy('UpdateDatetime')" :class="sortedClass('UpdateDatetime')" class="th7 sortable">{{$t("testDescriptions.updateTime")}}</th>
                                    <th class="th8">{{$t("testDescriptions.editOptions")}}</th>
                                </tr>
                            </thead>
                            <tbody v-if="td_test"  ref="tdTable">
                                <tr v-for="TestDescription in sorted" :key="TestDescription.Id">
                                    <td class="th1 t_center">
                                        <input type="checkbox" v-bind:value="TestDescription.Id" v-model="checkedItems" @click="onRowClick" name="checkbox">
                                    </td>
                                    <!--お気に入り-->
                                    <td class="th2 t_center">
                                        <span v-if="TestDescription.Star === false">
                                            <img src="~@/assets/unlike.svg" alt="unlike" title="unlike" class="icon status" @click="onStarChange(TestDescription)">
                                        </span>
                                        <span v-else-if="TestDescription.Star === true">
                                            <img src="~@/assets/like.svg" alt="like" title="like" class="icon status" @click="onStarChange(TestDescription)">
                                        </span>
                                    </td>
                                    <!--ID-->
                                    <td class="th3 t_right">
                                        {{TestDescription.Id}}
                                    </td>
                                    <!--P-ID-->
                                    <td class="th4 t_right">
                                        <template  v-if="TestDescription.ParentID">
                                            {{TestDescription.ParentID}}
                                        </template>
                                    </td>
                                    <!--Status-->
                                    <td class="th5 t_center">
                                        <span v-if="TestDescription.Result == 'OK'">
                                            <img src="~@/assets/check.svg" alt="OK" title="OK" class="icon status">
                                        </span>
                                        <span v-else-if="TestDescription.Result == 'NG'">
                                            <img src="~@/assets/clear.svg" alt="NG" title="NG" class="icon status">
                                        </span>
                                        <span v-else-if="TestDescription.Result == 'ERR'">
                                            <img src="~@/assets/warning.svg" alt="error" title="error" class="icon status">
                                        </span>
                                        <span v-else-if="TestDescription.Result == 'NA'">
                                            <img src="~@/assets/new.svg" alt="new" title="new" class="icon status">
                                        </span>
                                    </td>
                                    <td class="th6 t_left">
                                        <span class="test_name">{{TestDescription.Name}}</span>
                                        <span class="fukidashi" v-if="TestDescription.Opinion">
                                            <div style="text-align: center;">{{$t("testDescriptions.tdOpinion")}}</div>
                                            <hr>
                                            <span class="infomation-column">{{TestDescription.Opinion}}</span>
                                        </span>
                                    </td>
                                    <td class="th7 t_center">
                                        <font size="4">{{TestDescription.UpdateDatetime | formatFn}}</font>
                                    </td>
                                    <!--EditOptions-->
                                    <td class="th8 t_right">
                                        <template v-if="(TestDescription.Result === 'OK' || TestDescription.Result === 'NG') && TestDescription.ParentID != null" class="modal">
                                            <template v-if="$i18n.locale === 'en'">
                                                <img src="~@/assets/tree.svg" @click="TDRelation(TestDescription.Id)" alt="relationship" title="relationship" class="icon relationship">
                                            </template>
                                            <template v-else>
                                                <img src="~@/assets/tree.svg" @click="TDRelation(TestDescription.Id)" alt="関連" title="関連" class="icon relationship">
                                            </template>
                                        </template>
                                        <router-link :to="{ name: 'TestDescriptionEdit'}" class="icon" v-if="TestDescription.Result === 'ERR' || TestDescription.Result === 'NA'">
                                            <template v-if="$i18n.locale === 'en'">
                                                <img src="~@/assets/edit.svg" alt="edit" title="edit" class="icon" @click="postHistory_testDescriptionEdit($route.name,TestDescription.Id)">
                                            </template>
                                            <template v-else>
                                                <img src="~@/assets/edit.svg" alt="編集" title="編集" class="icon" @click="postHistory_testDescriptionEdit($route.name,TestDescription.Id)">
                                            </template>
                                        </router-link>
                                        <router-link :to="{ name: 'TestDescriptionCopy'}" class="icon" >
                                            <template v-if="$i18n.locale === 'en'">
                                                <img src="~@/assets/copy.svg" alt="copy" title="copy" class="icon" @click="postHistory_testDescriptionCopy($route.name,TestDescription.Id)"/>
                                            </template>
                                            <template v-else>
                                                <img src="~@/assets/copy.svg" alt="複製" title="複製" class="icon" @click="postHistory_testDescriptionCopy($route.name,TestDescription.Id)"/>
                                            </template>
                                        </router-link>
                                        <router-link :to="{ name: 'TestDescriptionsDetail'}" class="icon">
                                            <template v-if="$i18n.locale === 'en'">
                                                <img src="~@/assets/description.svg" alt="detail" title="detail" class="icon" @click="postTestDescriptionId_toDetail(TestDescription.Id)">
                                            </template>
                                            <template v-else>
                                                <img src="~@/assets/description.svg" alt="詳細" title="詳細" class="icon" @click="postTestDescriptionId_toDetail(TestDescription.Id)">
                                            </template>
                                        </router-link>
                                        <router-link :to="{ name: 'TestDescriptions'}" class="icon">
                                            <template v-if="$i18n.locale === 'en'">
                                                <img src="~@/assets/delete.svg" alt="delete" title="delete" class="icon" @click="postTestDescriptionId_toDelete(TestDescription.Id)">
                                            </template>
                                            <template v-else>
                                                <img src="~@/assets/delete.svg" alt="削除" title="削除" class="icon" @click="postTestDescriptionId_toDelete(TestDescription.Id)">
                                            </template>
                                        </router-link>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <!-- テーブル下コンテンツ -->
                    <div class="bottom_contents">
                        <div class="test">
                            <template v-if="$i18n.locale === 'en'">
                                <input type="submit" value="Run test" class="btn_single" @click="runTest" v-bind:class="{'un_btn' : isRunTest}">
                            </template>
                            <template v-else>
                                <input type="submit" value="テスト実行" class="btn_single" @click="runTest" v-bind:class="{'un_btn' : isRunTest}">
                            </template>
                            <div class="message_run">
                                {{$t("testDescriptions.annotationMessage1")}}
                                <img src="~@/assets/warning.svg" alt="error" title="error" class="icon status"> or <img src="~@/assets/new.svg" alt="new" title="new" class="icon status">
                                {{$t("testDescriptions.annotationMessage2")}}
                            </div>
                        </div>
                        <div id="status" v-if="test_descriptions" v-bind:class="{ 'status_disp' : isDisp }">
                            <p class="center result">{{$t("testDescriptions.result")}}</p>
                            <p class="center">{{$t("testDescriptions.status")}}:{{test_descriptions.Test.Status}}</p>
                            <p class="center">{{result}}</p>
                        </div>
                        <div id="btn_test">
                            <template v-if="$i18n.locale === 'en'">
                                <input type="submit" value="Compare" class="btn_single" @click="compare" v-bind:class="{'un_btn' : isCompare}">
                                <input type="submit" value="Download Report" class="btn_single" @click="downloadReport" v-bind:class="{'un_btn' : isDownloadReport}">
                            </template>
                            <template v-else>
                                <input type="submit" value="比較" class="btn_single" @click="compare" v-bind:class="{'un_btn' : isCompare}">
                                <input type="submit" value="レポートダウンロード" class="btn_single" @click="downloadReport" v-bind:class="{'un_btn' : isDownloadReport}">
                            </template>
                            <div class="message_con_repo">
                                {{$t("testDescriptions.annotationMessage1")}}
                                <img src="~@/assets/check.svg" alt="OK" title="OK" class="icon status"> or <img src="~@/assets/clear.svg" alt="NG" title="NG" class="icon status">
                                {{$t("testDescriptions.annotationMessage2")}}
                            </div>
                        </div>
                    </div>
                </div>
                <!-- フッタ -->
                <div id="footer">
                    <address>Copyright © National Institute of Advanced Industrial Science and Technology （AIST）</address>
                </div>
            </div>
        </div>
    </div>
</template>

<script scoped>
import { tdMixin } from '../mixins/testDescriptionMixin';
import { urlParameterMixin } from '../mixins/urlParameterMixin';
import TDRelation from './TestDescriptionRelationship';
    export default{
        components: {
            TDRelation,
        },
        mixins: [tdMixin, urlParameterMixin],
        data() {
            return{
                rel_key: 0,
                test_descriptions : null,
                generateReport: null,
                run_test: null,
                statuses: ['','OK','NG','ERR','NEW'],
                selectStatus: '',
                starChecked: false,
                searchName: '',
                dateStart: '',
                dateEnd: '',
                sort: {
                    key: 'Id',
                    isAsc: true
                },
                checkedItems: [],
                isPush: false,
                isDisp: true,
                isRunTest: true,
                isCompare: true,
                isDownloadReport: true,
                result: null,
                td_test: null,
                TestDescriptions: null,
            }
        },
        mounted: function () {
            this.setLanguageData()
            this.mlComponentIdCheck();
            this.organizationIdCheck = sessionStorage.getItem('organizationId');
            this.mlComponentId = sessionStorage.getItem('mlComponentId');
            this.getMLComponent();
            const url = this.$backendURL + '/'
                        + this.organizationIdCheck + '/mlComponents/'
                        + this.mlComponentId + '/testDescriotions';
            this.$axios.get(url)
            .then((response) => {
                this.test_descriptions = response.data;
                this.result = this.test_descriptions.Test.ResultDetail;
                this.td_test = this.test_descriptions.Test.TestDescriptions;
            })
            .catch((error) => {
                this.$router.push({
                    name: 'Information',
                    params: {error}
                })
            });
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
            //テーブルのヘッダーにタイトルを設定。
            //現在の選択言語がjaなら日本語のテーブルを、enなら英語のテーブルを設定。
            changeLanguage(lang) {
                sessionStorage.setItem('language', lang);
                this.$i18n.locale = lang;
            },
            downloadReport(){
                // チェックしたTDのIdを文字列に変換
                var checkedItems_str = [];
                for(var i=0;i<this.checkedItems.length;i++){
                    checkedItems_str.push(String(this.checkedItems[i]));
                }
                const url = this.$backendURL + '/'
                            + this.organizationIdCheck + '/mlComponents/'
                            + this.mlComponentId + '/testDescriotions/reportGenerator'
                this.$axios.post(url, {"Command": "Generate", "Destination": checkedItems_str})
                .then((response) => {
                    this.generateReport = response.data;
                    const link = document.createElement('a');
                    link.href = this.generateReport.OutParams.ReportUrl;
                    link.click();
                })
                .catch((error) => {
                    this.$router.push({
                        name: 'Information',
                        params: {error}
                    })
                })
            },
            runTest(){
                const that = this;
                this.isPush = true;
                this.isDisp = false;
                const url = this.$backendURL + '/'
                            + this.organizationIdCheck + '/mlComponents/'
                            + this.mlComponentId + '/testDescriotions/runners'
                this.$axios.post(url, {"Command": "AsyncStart", "TestDescriptionIds": this.checkedItems})
                .then((response) => {
                    this.run_test = response.data;
                    this.intervalId = setInterval(function () {
                        that.checkTestRunnerStatus();
                    }, 1000)
                })
                .catch((error) => {
                    this.isPush = false;
                    // eslint-disable-next-line no-console
                    console.log(error.response.data);
                    alert(error.response.data.Message);
                })
            },
            checkTestRunnerStatus(){
                const url = this.$backendURL + '/'
                            + this.organizationIdCheck + '/mlComponents/'
                            + this.mlComponentId + '/testDescriotions/run-status';
                this.$axios.get(url)
                    .then(response => {
                        // eslint-disable-next-line no-console
                        console.log(response.data.Result.Code + ': ' + response.data.Result.Message);
                        this.result = response.data.Job.ResultDetail;

                        /*
                        // デバッグ用コード
                        // (const data = response.data;)をコメントアウトして、
                        // インポートしているデバッグ用JSONの何れかのコメントアウトを外す。
                        */
                        // const data = runStatus;
                        // eslint-disable-next-line no-console
                        // console.log(data)

                        const data = response.data;
                        this.updateStatus(data);
                        if(data.Job.Status == 'DONE'){
                            this.isPush = false;
                            clearInterval(this.intervalId);
                            delete this.intervalId;
                            // eslint-disable-next-line no-console
                            console.log('status check roop fin')
                            const url = this.$backendURL + '/'
                                        + this.organizationIdCheck + '/mlComponents/'
                                        + this.mlComponentId + '/testDescriotions'
                            this.$axios.get(url)
                            .then((response) => {
                                this.test_descriptions = response.data;
                                this.td_test = this.test_descriptions.Test.TestDescriptions;
                            })
                        }
                    })
                    .catch((error) => {
                        // eslint-disable-next-line no-console
                        console.log(error.response.data);
                        alert(error.response.data.Message + '\nPlease push "Run Test" after waiting a moment or canceling the job.');
                        this.isPush = false;
                    })
            },
            updateStatus(data){
                this.test_descriptions.Test.Status = data.Job.Status;
                // その他、更新内容が増えればここに記載する。
            },
            sortedClass: function(key){
                return this.sort.key === key ? `sorted ${this.sort.isAsc ? 'asc' : 'desc'}` : '';
            },
            sortBy: function(key){
                if(this.sort.key == key) {
                    this.sort.isAsc = !this.sort.isAsc;
                } else {
                    this.sort.isAsc = true;
                }
                this.sort.key = key;
            },
            compare: function(){
                sessionStorage.setItem('testDescriptionId1', this.checkedItems[0]);
                sessionStorage.setItem('testDescriptionId2', this.checkedItems[1]);
                this.$router.push({
                    name: 'TestDescriptionsCompare'
                })
            },
            postTestDescriptionId_toDetail: function(testDescriptionId){
                this.setTestDescription(testDescriptionId);
                this.$router.push({
                    name: 'TestDescriptionsDetail'
                })
            },
            postTestDescriptionId_toDelete: function(testDescriptionId) {
                if (confirm(this.$t("confirm.delete"))) {
                    this.$axios.delete(this.$backendURL +
                            '/' +
                            this.organizationIdCheck +
                            '/mlComponents/' +
                            this.mlComponentId +
                            '/testDescriotions/' +
                            testDescriptionId
                    )
                    .then((response) => {
                        this.result = response.data;
                        window.location.reload()
                    })
                    .catch((error) => {
                        this.$router.push({
                            name: 'Information',
                            params: {error}
                        })
                    })
                }
            },
            postTestDescriptionId_toAncestors: function(testDescriptionId){
                this.$router.push({
                    name: 'TestDescriptionsRelationship',
                    params: {testDescriptionId: testDescriptionId}
                })
            },
            onStarChange: function(testDescription){
                if(testDescription.Star === true){
                    this.setUnStar(testDescription.Id)
                }
                else{
                    this.setStar(testDescription.Id)
                }
                testDescription.Star = !testDescription.Star
            },
            TestDescriptionCreate(){
				this.$router.push({
					name: 'TestDescriptionAppend'
				})
			},
			screenTransion(mlComponentId){
				sessionStorage.setItem('mlComponentId', mlComponentId);
				this.$router.push({
					name: 'TestDescriptions'
				});
            },
            onRowClick: function(){
                //チェックされている数を取得
                var checkbox = document.getElementsByName('checkbox');
                var checked = 0;
                var status = [];
                var my_id = [];
                var test_runner_ids = [];

                // 1行ずつの情報をループ
                for (var check of checkbox) {
                    if(check.checked) {
                        //親子関係、ボタン制御用に値を取得
                        checked++;
                        my_id.push(check.value)

                        //選択した行の背景色制御
                        check.parentNode.parentNode.classList.add('checked')

                        // チェックされているStatusの情報を取得
                        for(var TD1 of this.sorted){
                            var td_id = TD1.Id;
                            if(td_id == check.value && !status.includes(TD1.Result)){
                                status.push(TD1.Result);
                                break;
                            }
                        }
                    } else {
                        //選択されていない行の背景色制御
                        check.parentNode.parentNode.classList.remove('checked')
                    }
                }

                //親子関係の背景色制御
                if(checked == 1) {
                    var my_p_id = ''

                    //checkedItemのParentIDを引き出す
                    for(var TD2 of this.sorted){
                        if(TD2.ParentID){
                            if(my_id[0] == TD2.Id){
                                my_p_id = TD2.ParentID;
                                break;
                            }
                            
                        }
                    }

                    for(var TD3 of this.sorted){
                        //チェックされている行は除外
                        if(my_id[0] == TD3.Id){
                            continue;
                        }

                        //選択された行のIDと同じParentIDを持つもの
                        if(my_id[0] == TD3.ParentID){
                            for(var a of checkbox){
                                if(TD3.Id == a.value){
                                    a.parentNode.parentNode.classList.add('family');
                                    break;
                                }
                            }
                        }

                        if(my_p_id != '') {
                            //選択された行のParentIDをIDに持つもの
                            if(my_p_id == TD3.Id) {
                                for(var c of checkbox){
                                    if(TD3.Id == c.value){
                                        c.parentNode.parentNode.classList.add('family')
                                        break;
                                    }
                                }
                            }
                            //選択された行のParentIDをParentIDに持つもの
                            if(my_p_id == TD3.ParentID) {
                                for(var d of checkbox){
                                    if(TD3.Id == d.value){
                                        d.parentNode.parentNode.classList.add('family')
                                        break;
                                    }
                                }
                            }
                        }
                    }
                } else {
                    for(var e of checkbox){
                        e.parentNode.parentNode.classList.remove('family')
                    }
                }
                
                //ボタン活性
                if(checked == 0 || ((status.includes('ERR') || status.includes('NA')) && (status.includes('OK') || status.includes('NG')))){
                    //チェックがないとき、Statusが混ざっているとき（非活性）
                    this.isRunTest = true;
                    this.isCompare = true;
                    this.isDownloadReport = true;
                } else if (status.includes('ERR') || status.includes('NA')){
                    //RunTestのボタン活性
                    if (checked == 0 ){
                        this.isRunTest = true;
                        this.isCompare = true;
                        this.isDownloadReport = true;
                    } else {
                        this.isRunTest = false;
                        this.isCompare = true;
                        this.isDownloadReport = true;
                    }
                } else if (status.includes('OK') || status.includes('NG')) {
                    //CompareとDownloadReportのボタン活性
                    if (checked == 2) {

                        for(var td of this.td_test){
                            for(var my_td_id of my_id){
                                if (td.Id == my_td_id){
                                    test_runner_ids.push(td.TestRunnerId)
                                }
                            }
                        }

                        //同じTestRunnerのときは比較可能
                        if(test_runner_ids[0]==test_runner_ids[1]){
                            this.isCompare = false;
                        } else {
                            this.isCompare = true;
                        }
                        this.isRunTest = true;
                        this.isDownloadReport = false;
                    } else if(checked == 1 ){
                        this.isRunTest = true;
                        this.isCompare = true;
                        this.isDownloadReport = false;
                    } else {
                        this.isRunTest = true;
                        this.isCompare = true;
                        this.isDownloadReport = false;
                    }
                }
            },
            onAllRowClick: function(){
                //チェックされている数を取得
                var checkbox = document.getElementsByName('checkbox');
                var checked = 0;
                var status = [];
                var my_id = []

                // 1行ずつの情報をループ
                for (var check of checkbox) {
                    if(document.getElementsByName('checkbox_all')[0].checked) {
                        //親子関係、ボタン制御用に値を取得
                        checked++;
                        my_id.push(check.value)

                        //選択した行の背景色制御
                        check.parentNode.parentNode.classList.add('checked')

                        // チェックされているStatusの情報を取得
                        for(var TD1 of this.sorted){
                            var td_id = TD1.Id;
                            if(td_id == check.value && !status.includes(TD1.Result)){
                                status.push(TD1.Result);
                                break;
                            }
                        }
                    } else {
                        //選択されていない行の背景色制御
                        check.parentNode.parentNode.classList.remove('checked')
                    }
                }

                //ボタン活性
                if(checked == 0 || ((status.includes('ERR') || status.includes('NA')) && (status.includes('OK') || status.includes('NG')))){
                    //チェックがないとき、Statusが混ざっているとき（非活性）
                    this.isRunTest = true;
                    this.isCompare = true;
                    this.isDownloadReport = true;
                } else if (status.includes('ERR') || status.includes('NA')){
                    //RunTestのボタン活性
                    if (checked == 0 ){
                        this.isRunTest = true;
                        this.isCompare = true;
                        this.isDownloadReport = true;
                    } else {
                        this.isRunTest = false;
                        this.isCompare = true;
                        this.isDownloadReport = true;
                    }
                } else if (status.includes('OK') || status.includes('NG')) {
                    //CompareとDownloadReportのボタン活性
                    if (checked == 2) {
                        var my_p_id1 = '';
                        var my_p_id2 = '';
                        //選択された行のParentIDを取得
                        for(var TD4 of this.sorted){
                            if(TD4.ParentID) {
                                if (TD4.Id == my_id[0]) {
                                    my_p_id1 = TD4.ParentID;
                                } else if (TD4.Id == my_id[1]) {
                                    my_p_id2 = TD4.ParentID;
                                }
                            }
                        }
                        //親子関係がない時はCompare非活性
                        if(my_p_id1==my_p_id2 || my_id[0]==my_p_id2 || my_id[1]==my_p_id1){
                            this.isRunTest = true;
                            this.isCompare = false;
                            this.isDownloadReport = false;
                        } else {
                            this.isRunTest = true;
                            this.isCompare = true;
                            this.isDownloadReport = false;
                        }
                    } else if(checked == 1 ){
                        this.isRunTest = true;
                        this.isCompare = true;
                        this.isDownloadReport = false;
                    } else {
                        this.isRunTest = true;
                        this.isCompare = true;
                        this.isDownloadReport = false;
                    }
                }
            },
            modalReset() {
                this.rel_key = this.rel_key ? 0 : 1;
            },
            tableReroad(){
                const url = this.$backendURL + '/'
                            + this.organizationIdCheck + '/mlComponents/'
                            + this.mlComponentId + '/testDescriotions'
                this.$axios.get(url)
                .then((response) => {
                    this.test_descriptions = response.data;
                    this.td_test = this.test_descriptions.Test.TestDescriptions;
                })
            },
            TDRelation(TestDescriptionId){
                this.$refs.rel.show(TestDescriptionId);
            },
        },
        computed: {
            starMatched: function(){
                if(this.starChecked === false){
                    return this.td_test;
                }
                else{
                    return this.td_test.filter(function(el){
                        return el.Star === this.starChecked
                    },this)
                }
            },
            statusMatched: function(){
                if(this.selectStatus === '' && this.td_test){
                    return this.starMatched;
                }
                else if(this.selectStatus === 'NEW' && this.td_test){
                    return this.starMatched.filter(function(el){
                        return el.Result === 'NA'
                    },this)
                }
                else if(this.td_test){
                    return this.starMatched.filter(function(el){
                        return el.Result === this.selectStatus
                    },this)
                }
                else{
                    return [];
                }
            },
            nameMatched: function(){
                if(this.searchName == ''){
                    return this.statusMatched;
                } else {
                    return this.statusMatched.filter(function(el){
                        return el.Name.indexOf(this.searchName) > -1
                    },this)
                }
            },
            dateMached: function(){
                if(this.dateStart == '' && this.dateEnd == ''){
                    // this.getTestDescriptions(this.nameMatched);
                    
                    return this.nameMatched;
                }
                else if(this.dateEnd == ''){
                    var fil_start = this.nameMatched.filter(function(el){
                        return this.$options.filters.formatFn(el.UpdateDatetime) >= this.dateStart
                    },this)
                    // return this.getTestDescriptions(fil_start);
                    return fil_start;
                }
                else if(this.dateStart == ''){
                    var fil_end = this.nameMatched.filter(function(el){
                        return this.$options.filters.formatFn(el.UpdateDatetime) <= this.dateEnd +1
                    },this)

                    // return this.getTestDescriptions(fil_end);
                    return fil_end
                }
                else{
                    var fil_full = this.nameMatched.filter(function(el){
                        return this.$options.filters.formatFn(el.UpdateDatetime) >= this.dateStart
                        && this.$options.filters.formatFn(el.UpdateDatetime) <= this.dateEnd +1
                    },this)

                    // return this.getTestDescriptions(fil_full);
                    return fil_full
                }
            },
            sorted: function(){
                var list = this.dateMached.slice();
                if(this.sort.key){
                    if(this.sort.key == 'Id'){
                        list.sort((a, b) => {
                            return (a[this.sort.key] === b[this.sort.key] ? 0 : a[this.sort.key] > b[this.sort.key] ? 1 : -1) * (this.sort.isAsc ? 1 : -1)
                        });
                    } else if (this.sort.key == 'ParentID'){
                        var list_null = [];
                        var list_pId = [];
                        //ParentIDを持つものと持たないものに分ける
                        for (var l=0; l<list.length; l++) {
                            if(!list[l].ParentID){
                                list_null.push(list[l]);
                            } else {
                                list_pId.push(list[l])
                            }
                        }
                        //親を持つものを並び替えて、上部に表示する
                        if(list_pId.length > 0){
                            list_pId.sort((a, b) => {
                                return (a[this.sort.key] === b[this.sort.key] ? 0 : a[this.sort.key] > b[this.sort.key] ? 1 : -1) * (this.sort.isAsc ? 1 : -1)
                            });
                            list = list_pId.concat(list_null);
                        }
                        //親がいない場合はIDのソートを行う
                        else {
                            list.sort((a, b) => {
                                return (a.Id === b.Id ? 0 : a.Id > b.Id ? 1 : -1) * (this.sort.isAsc ? 1 : -1)
                            });
                        }
                    }
                    else{
                        list.sort((a, b) => {
                            a = a[this.sort.key].toLowerCase()
                            b = b[this.sort.key].toLowerCase()
                            return (a === b ? 0 : a > b ? 1 : -1) * (this.sort.isAsc ? 1 : -1)
                        });
                    }
                }
                return list;
            },
            totalPages: function(){
                return Math.max(Math.ceil(this.sorted.length / this.perPage) , 1)
            },
            allChecked: {
                get: function(){
                    return this.sorted ? this.checkedItems.length === this.sorted.length : false
                },
                set: function(value){
                    var selected = [];
                    if(value){
                        this.sorted.forEach(function(TestDescription){
                            selected.push(TestDescription.Id);
                        });
                    }
                    this.checkedItems = selected;
                }
            },
            processedList: function(){
                return this.paging
            }
        },
        filters: {
            formatFn: function(val){
                var moment = require('moment-timezone');
                var datetime_conv = moment.tz(val, 'UTC');
                datetime_conv.tz(moment.tz.guess());

                var datetime = datetime_conv.format().slice(0,16);
                datetime = datetime.replace(/T/g, ' ');
                datetime = datetime.replace(/-/g, '/');
                return datetime;
            },
        }
    }
</script>

<style scoped>
/*-------------------全体-------------------*/
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

/*--------------------メインコンテンツ-----------------------*/
/* テスト一覧 */
#main_body p {
  display: block;
  margin-block-start: 0;
  margin-block-end: 0;
}

#search {
  text-align: left;
  padding: 15px 0px 0px;
  float: left;
}
.star_check{
    margin-right: 10px;
    margin-left: 3px;
}

.select {
  font-size: 12px;
  width: 150px;
  margin-right: 10px;
  margin-left: 3px;
}
.name {
  font-size: 12px;
  margin-right: 10px;
  margin-left: 3px;
}
.day{
    margin-right: 3px;
  margin-left: 3px;
}
.select {
  font-size: 12px;
  width: 158px;
  margin-right: 10px;
}
.btn {
  text-align: right;
  padding: 10px 0px 5px;
}
.btn_single {
  margin: auto 5px;
}
input.day{
  width: 110px;
}
input.name{
  width: 100px;
}
#search select {
  width: 70px;
}
#search_table {
  width: 900px;
}
.search {
  display: inline-block;
}


/*-------------------テーブル-------------------*/

#table tr:hover {
    background-color: rgb(233, 233, 233);
}

.checked{
  background-color: #d1ff8c;
}

table{
    width: 100%;
}

.t_left{
	text-align:left;
	padding-left: 5px;
}
.t_center{
	text-align:center;
}
.t_right{
	padding-right: 5px;
	text-align:right;
}

.th1 {
  width: 3%;
}
.th2 {
  width: 3%;
}
.th3 {
  width: 4%;
}
th.th3 {
    text-align: left;
    padding-left: 0.5%;
}
.th4 {
  width: 6%;
}
th.th4 {
    text-align: left;
    padding-left: 0.5%;
}
.th5 {
  width: 11%;
}
.th6 {
  width: 40%;
}
.th7 {
  width: 20%;
}
.th8 {
  width: 14%;
}

#table input {
    width: 17px;
    height: 17px;
    vertical-align:middle;
}

/* ソートの矢印 */
.table_body th {
    position: relative;
}
.table_body th.sortable{
    cursor:pointer
}
.table_body th.sortable::before{
    content: "";
    position: absolute;
    height: 0;
    width: 0;
    right: 0;
    top: 50%;
    margin-bottom: -7px;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #cfd3e0;
}
.description_thead th.sortable::after{
    content: "";
    position: absolute;
    height: 0;
    width: 0;
    right: 0;
    top: 50%;
    margin-top: -7px;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-bottom: 5px solid #cfd3e0;
}
.description_thead th.sortable.sorted.desc::before{
    border-top: 5px solid #409eff;
}

.description_thead th.sortable.sorted.asc::after{
    border-bottom: 5px solid #409eff;
}

/*-------------------親子関係-------------------*/
.family {
  background-color:  #e7f5d4 !important;
}

.relationship{
    cursor: pointer;
}
/*-------------------テーブル下コンテンツ-------------------*/
#status {
  font-size: 13px;
  margin: 10px auto 0px 0px;
}
#btn_test {
  text-align: right;
  margin: 10px 0px 10px auto;
}
.result {
  font-size: 18px;
}
.bottom_contents {
  display: flex;
}
.test {
  margin: 10px 10px 0px 0px;
}

.message_run {
  font-size: 12px;
  text-align: center;
  padding-top: 5px;
}
.message_con_repo {
  font-size: 12px;
  text-align: right;
  padding-top: 5px;
}

.status_disp {
    display: none;
}

/* 吹き出し */
.test_name:hover + .fukidashi {
	display: inline;
}
.fukidashi {
  max-width: 300px;
  margin-left: 25px;
}

.fukidashi hr {
    margin-top: 5px;
    margin-bottom: 5px;
}
.fukidashi:after {
	top: 4%;
}


</style>
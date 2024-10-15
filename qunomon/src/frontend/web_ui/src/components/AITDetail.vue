<template>
<div>

    <!--ヘッダータイトル-->
    <header id="head" :class="{ active: this.isActive }">
        <div id="title">
            <button @click="toggleSubmenu(isActive)" class="qq"><img :src="this.isActive ? this.icon2 : this.icon1" alt="Image" width="30" height="auto"></button>
            <h1 class="head_title">{{$t("common.titleAITDetail")}}</h1>
        </div>
    </header>

    <!-- サブメニュー（左カラム） -->

    <SubMenu :isActive="this.isActive">
        <!--SubMenuのアイコンとメニューの間の言語項目は各コンポーネントで実施-->
        <!--言語ボタン■-->
        <div id="btn_language">
            <template v-if="$i18n.locale === 'en'">
                <a href="#" v-on:click.prevent="changeLanguage('ja', screenName)" class="btn_unselect">{{$t("common.lanJa")}}</a>
                <a href="#" class="btn_select">{{$t("common.lanEn")}}</a>
            </template>
            <template v-else>
                <a href="#" class="btn_select">{{$t("common.lanJa")}}</a>
                <a href="#" v-on:click.prevent="changeLanguage('en', screenName)" class="btn_unselect">{{$t("common.lanEn")}}</a>
            </template>
        </div>
    </SubMenu>


    <!-- ニュース（中央カラム） -->
    <div id="main" :class="{ active: isActive }">
        <div id="main_body">
            <div class="ait_install t_center">
                <div class="ait_install_btn">
                    <template v-if="$i18n.locale === 'en'">
                        <input type="button" value="AIT Install" class="btn_single btn_inline_left" 
                                @click="aitInstall" v-bind:disabled="ait_local_installed_flag == 'true'"
                                v-bind:class="{'un_btn' : ait_local_installed_flag == 'true'}" />
                    </template>
                    <template v-else>
                        <input type="button" value="AITインストール" class="btn_single btn_inline_left"  
                                @click="aitInstall" v-bind:disabled="ait_local_installed_flag == 'true'"
                                v-bind:class="{'un_btn' : ait_local_installed_flag == 'true'}" />
                    </template>
                </div>
                <div class="ait_install_text">
                    <span v-if="ait_local_installed_flag == 'true'">
                        {{$t("aitDetail.ait_installed")}}
                    </span>
                </div>
            </div>
            <div id="detailInfo">
                <div class="eachCard">
                    <label for="panel_ait_properties">
                        <span v-if="accordionOnOffFlag.ait_properties"><img class="icon" title="unfold" :src="lessInfo"></span>
                        <span v-else><img class="icon" :src="moreInfo"></span>
                        <span>{{$t("aitDetail.ait_properties")}}</span>
                    </label>
                    <input type="checkbox" id="panel_ait_properties" class="on_off" v-model="accordionOnOffFlag.ait_properties"/>
                    <ul>
                        <li>
                            <table class="dataTable" @click="$event.target.parentElement.classList.toggle('expanded')">
                                <tr>
                                    <td>{{$t("aitDetail.ait_name")}}</td>
                                    <td>{{ait_properties.ait_name}}</td>
                                </tr>
                                <tr>
                                    <td>{{$t("aitDetail.description")}}</td>
                                    <td>{{ait_properties.description}}</td>
                                </tr>
                                <tr>
                                    <td>{{$t("aitDetail.create_user_account")}}</td>
                                    <td>{{ait_properties.create_user_account}}</td>
                                </tr>
                                <tr>
                                    <td>{{$t("aitDetail.create_user_name")}}</td>
                                    <td>{{ait_properties.create_user_name}}</td>
                                </tr>
                                <tr>
                                    <td>{{$t("aitDetail.version")}}</td>
                                    <td>{{ait_properties.version}}</td>
                                </tr>
                                <tr>
                                    <td>{{$t("aitDetail.quality")}}</td>
                                    <td>
                                        <img v-if="ait_properties.quality" src="~@/assets/new_window.svg" alt="new-window" title="new-window" class="new-window">
                                        <a v-bind:href=cleanUrl(ait_properties.quality) target="_blank">{{cleanUrl(ait_properties.quality)}}</a>
                                    </td>
                                </tr>
                                <tr>
                                    <td valign="top">{{$t("aitDetail.references")}}</td>
                                    <td>
                                        <template v-for="(reference, index) in ait_properties.references">
                                            <div class="sub_accordion_level3" :key="index">
                                                <label v-bind:for="0 + index">
                                                    <span v-if="referencesOnOffFlag[index]"><img class="icon" title="unfold" :src="lessInfo"></span>
                                                    <span v-else><img class="icon" :src="moreInfo"></span>
                                                    {{$t("aitDetail.reference")}} - {{index + 1}}
                                                </label>
                                                <input type="checkbox" v-bind:id="0 + index" class="on_off" v-model="referencesOnOffFlag[index]"/>
                                                <ul>
                                                    <li>
                                                        <table class="dataTable" @click="$event.target.parentElement.classList.toggle('expanded')">
                                                            <tr>
                                                                <td>{{$t("aitDetail.reference_bib_info")}}</td>
                                                                <td>{{reference.bib_info}}</td>
                                                            </tr>
                                                            <tr>
                                                                <td>{{$t("aitDetail.reference_additional_info")}}</td>
                                                                <td>{{reference.additional_info}}</td>
                                                            </tr>
                                                            <tr>
                                                                <td>{{$t("aitDetail.reference_url")}}</td>
                                                                <td>
                                                                    <img v-if="reference.url" src="~@/assets/new_window.svg" alt="new-window" title="new-window" class="new-window">
                                                                    <a v-bind:href=cleanUrl(reference.url) target="_blank">{{cleanUrl(reference.url)}}</a>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </li>
                                                </ul>
                                            </div>
                                        </template>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="tbl_th">{{$t("aitDetail.keywords")}}</td>
                                    <td>{{ait_properties.keywords}}</td>
                                </tr>
                                <tr>
                                    <td class="tbl_th">{{$t("aitDetail.licenses")}}</td>
                                    <td>{{ait_properties.licenses}}</td>
                                </tr>
                            </table>
                        </li>
                    </ul>
                    <!-- inventories -->
                    <label for="panel_inventories">
                        <span v-if="accordionOnOffFlag.inventories"><img class="icon" title="unfold"  :src="lessInfo"></span>
                        <span v-else><img class="icon" :src="moreInfo"></span>
                        {{$t("aitDetail.inventories")}}
                    </label>
                    <input type="checkbox" id="panel_inventories" class="on_off" v-model="accordionOnOffFlag.inventories"/>
                    <ul>
                        <li>
                            <template v-for="(inventory, index_1) in inventories">
                                <div class="sub_accordion_level1" :key="index_1">
                                    <label v-bind:for="1000 + index_1">
                                        <span v-if="inventoriesOnOffFlag[index_1]"><img class="icon" title="unfold" :src="lessInfo"></span>
                                        <span v-else><img class="icon" :src="moreInfo"></span>
                                        {{$t("aitDetail.inventory")}} - {{index_1 + 1}}
                                    </label>
                                    <input type="checkbox" v-bind:id="1000 + index_1" class="on_off" v-model="inventoriesOnOffFlag[index_1]"/>
                                    <ul>
                                        <li>
                                            <table class="dataTable" @click="$event.target.parentElement.classList.toggle('expanded')">
                                                <tr>
                                                    <td>{{$t("aitDetail.inventory_name")}}</td>
                                                    <td>{{inventory.inventory_name}}</td>
                                                </tr>
                                                <tr>
                                                    <td>{{$t("aitDetail.inventory_type")}}</td>
                                                    <td>{{inventory.inventory_type}}</td>
                                                </tr>
                                                <tr>
                                                    <td>{{$t("aitDetail.inventory_description")}}</td>
                                                    <td>{{inventory.inventory_description}}</td>
                                                </tr>
                                                <tr>
                                                    <td>{{$t("aitDetail.inventory_depends_on_parameter")}}</td>
                                                    <td>{{inventory.inventory_depends_on_parameter}}</td>
                                                </tr>
                                                <tr>
                                                    <td valign="top">{{$t("aitDetail.requirements")}}</td>
                                                    <td>
                                                        <template v-for="(requirement, index_2) in inventory.inventory_requirements">
                                                            <div class="sub_accordion_level3" :key="index_2">
                                                                <label v-bind:for="1500 + index_1 + index_2">
                                                                    <span v-if="inventoryRequirementsOnOffFlag[index_1][index_2]"><img class="icon" title="unfold"  :src="lessInfo"></span>
                                                                    <span v-else><img class="icon" :src="moreInfo"></span>
                                                                    {{$t("aitDetail.requirement")}} - {{index_2 + 1}}
                                                                </label>
                                                                <input type="checkbox" v-bind:id="1500 + index_1 + index_2" class="on_off" v-model="inventoryRequirementsOnOffFlag[index_1][index_2]"/>
                                                                <ul>
                                                                    <li>
                                                                        <table class="dataTable" @click="$event.target.parentElement.classList.toggle('expanded')">
                                                                            <tr>
                                                                                <td>{{$t("aitDetail.inventory_format")}}</td>
                                                                                <td>{{requirement.inventory_format}}</td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td valign="top">{{$t("aitDetail.inventory_compatible_packages")}}</td>
                                                                                <td>
                                                                                    <template v-for="(compatible_package, index_3) in requirement.inventory_compatible_packages">
                                                                                        <div class="sub_accordion_level4" :key="index_3">
                                                                                            <label v-bind:for="2000 + index_2 + index_3">
                                                                                                <span v-if="inventoryCompatiblePackagesOnOffFlag[index_2][index_3]"><img class="icon" title="unfold"  :src="lessInfo"></span>
                                                                                                <span v-else><img class="icon" :src="moreInfo"></span>
                                                                                                {{$t("aitDetail.compatible_package")}} - {{index_3 + 1}}
                                                                                            </label>
                                                                                            <input type="checkbox" v-bind:id="2000 + index_2 + index_3" class="on_off" v-model="inventoryCompatiblePackagesOnOffFlag[index_2][index_3]"/>
                                                                                            <ul>
                                                                                                <li>
                                                                                                    <table class="dataTable" @click="$event.target.parentElement.classList.toggle('expanded')">
                                                                                                        <tr>
                                                                                                            <td>{{$t("aitDetail.inventory_compatible_package_name")}}</td>
                                                                                                            <td>{{compatible_package.name}}</td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td>{{$t("aitDetail.inventory_compatible_package_version")}}</td>
                                                                                                            <td>{{compatible_package.version}}</td>
                                                                                                        </tr>
                                                                                                        <tr>
                                                                                                            <td>{{$t("aitDetail.inventory_compatible_package_additional_info")}}</td>
                                                                                                            <td>{{compatible_package.additional_info}}</td>
                                                                                                        </tr>
                                                                                                    </table>
                                                                                                </li>
                                                                                            </ul>
                                                                                        </div>
                                                                                    </template>
                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td>{{$t("aitDetail.inventory_additional_info")}}</td>
                                                                                <td>
<!--                                                                                    <template v-for="(addi, index_4) in requirement.inventory_additional_info">-->

<!--                                                                                    {{addi.key}}&nbsp; : &nbsp;{{addi.value}}-->
<!--                                                                                    <br :key="index_4">-->
                                                                                    <table class="dataTable left_padding" >
                                                                                        <template v-for="(addi, index_4) in requirement.inventory_additional_info">
                                                                                            <tr :key="index_4">
                                                                                                <td>{{addi.key}}</td>
                                                                                                <td>{{addi.value}}</td>
                                                                                            </tr>

                                                                                        </template>
                                                                                    </table>

                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td>{{$t("aitDetail.inventory_min")}}</td>
                                                                                <td>{{requirement.inventory_min}}</td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td>{{$t("aitDetail.inventory_max")}}</td>
                                                                                <td>{{requirement.inventory_max}}</td>
                                                                            </tr>
                                                                        </table>
                                                                    </li>
                                                                </ul>
                                                            </div>
                                                        </template>
                                                    </td>
                                                </tr>
                                            </table>
                                        </li>
                                    </ul>
                                </div>
                            </template>
                        </li>
                    </ul>
                    <!-- parameters -->
                    <label for="panel_parameters">
                        <span v-if="accordionOnOffFlag.inventories"><img class="icon" title="unfold" :src="lessInfo"></span>
                        <span v-else><img class="icon" :src="moreInfo"></span>
                        {{$t("aitDetail.parameters")}}
                    </label>
                    <input type="checkbox" id="panel_parameters" class="on_off" v-model="accordionOnOffFlag.parameters"/>
                    <ul>
                        <li>
                            <template v-for="(parameter, index) in parameters">
                                <div class="sub_accordion_level1" :key="index">
                                    <label v-bind:for="3000 + index">
                                        <span v-if="parametersOnOffFlag[index]"><img class="icon" title="unfold"  :src="lessInfo"></span>
                                        <span v-else><img class="icon" :src="moreInfo"></span>
                                        {{$t("aitDetail.parameter")}} - {{index + 1}}
                                    </label>
                                    <input type="checkbox" v-bind:id="3000 + index" class="on_off" v-model="parametersOnOffFlag[index]"/>
                                    <ul>
                                        <li>
                                            <table class="dataTable" @click="$event.target.parentElement.classList.toggle('expanded')">
                                                <tr>
                                                    <td>{{$t("aitDetail.parameters_name")}}</td>
                                                    <td>{{parameter.parameter_name}}</td>
                                                </tr>
                                                <tr>
                                                    <td>{{$t("aitDetail.parameters_type")}}</td>
                                                    <td>{{parameter.parameter_type}}</td>
                                                </tr>
                                                <tr>
                                                    <td>{{$t("aitDetail.parameters_description")}}</td>
                                                    <td>{{parameter.parameter_description}}</td>
                                                </tr>
                                                <tr>
                                                    <td>{{$t("aitDetail.parameters_default_val")}}</td>
                                                    <td>{{parameter.parameter_default_val}}</td>
                                                </tr>
                                                <tr>
                                                    <td>{{$t("aitDetail.parameters_min")}}</td>
                                                    <td>{{parameter.parameter_min}}</td>
                                                </tr>
                                                <tr>
                                                    <td>{{$t("aitDetail.parameters_max")}}</td>
                                                    <td>{{parameter.parameter_max}}</td>
                                                </tr>
                                                <tr>
                                                    <td>{{$t("aitDetail.parameters_depends_on_parameter")}}</td>
                                                    <td>{{parameter.parameter_depends_on_parameter}}</td>
                                                </tr>
                                            </table>
                                        </li>
                                    </ul>
                                </div>
                            </template>
                        </li>
                    </ul>
                    <!-- report -->
                    <label for="panel_report">
                        <span v-if="accordionOnOffFlag.report"><img class="icon" title="unfold"  :src="lessInfo"></span>
                        <span v-else><img class="icon" :src="moreInfo"></span>
                        {{$t("aitDetail.report")}}
                    </label>
                    <input type="checkbox" id="panel_report" class="on_off" v-model="accordionOnOffFlag.report"/>
                    <ul>
                        <li>
                            <!-- measures -->
                            <div class="sub_accordion_level1">
                                <label for="panel_measures">
                                    <span v-if="accordionOnOffFlag.measures"><img class="icon" title="unfold" :src="lessInfo"></span>
                                    <span v-else><img class="icon" :src="moreInfo"></span>
                                    {{$t("aitDetail.measures")}}
                                </label>
                                <input type="checkbox" id="panel_measures" class="on_off" v-model="accordionOnOffFlag.measures"/>
                                <ul>
                                    <li>
                                        <template v-for="(measure, index) in measures">
                                            <div class="sub_accordion_level2" :key="index">
                                                <label v-bind:for="4000 + index">
                                                    <span v-if="measuresOnOffFlag[index]"><img class="icon" title="unfold" :src="lessInfo"></span>
                                                    <span v-else><img class="icon" :src="moreInfo"></span>
                                                    {{$t("aitDetail.measure")}} - {{index + 1}}
                                                </label>
                                                <input type="checkbox" v-bind:id="4000 + index" class="on_off" v-model="measuresOnOffFlag[index]"/>
                                                <ul>
                                                    <li>
                                                        <table class="dataTable" @click="$event.target.parentElement.classList.toggle('expanded')">
                                                            <tr>
                                                                <td>{{$t("aitDetail.measure_name")}}</td>
                                                                <td>{{measure.measure_name}}</td>
                                                            </tr>
                                                            <tr>
                                                                <td>{{$t("aitDetail.measure_description")}}</td>
                                                                <td>{{measure.measure_description}}</td>
                                                            </tr>
                                                        </table>
                                                    </li>
                                                </ul>
                                            </div>
                                        </template>
                                    </li>
                                </ul>
                            </div>

                            <!-- resources -->
                            <div class="sub_accordion_level1">
                                <label for="panel_resources">
                                    <span v-if="accordionOnOffFlag.resources"><img class="icon" title="unfold" :src="lessInfo"></span>
                                    <span v-else><img class="icon" :src="moreInfo"></span>
                                    {{$t("aitDetail.resources")}}
                                </label>
                                <input type="checkbox" id="panel_resources" class="on_off" v-model="accordionOnOffFlag.resources"/>
                                <ul>
                                    <li>
                                        <template v-for="(resource, index) in resources">
                                            <div class="sub_accordion_level2" :key="index">
                                                <label v-bind:for="5000 + index">
                                                    <span v-if="resourcesOnOffFlag[index]"><img class="icon" title="unfold" :src="lessInfo"></span>
                                                    <span v-else><img class="icon" :src="moreInfo"></span>
                                                    {{$t("aitDetail.resource")}} - {{index + 1}}
                                                </label>
                                                <input type="checkbox" v-bind:id="5000 + index" class="on_off" v-model="resourcesOnOffFlag[index]"/>
                                                <ul>
                                                    <li>
                                                        <table class="dataTable" @click="$event.target.parentElement.classList.toggle('expanded')">
                                                            <tr>
                                                                <td>{{$t("aitDetail.resource_name")}}</td>
                                                                <td>{{resource.resource_name}}</td>
                                                            </tr>
                                                            <tr>
                                                                <td>{{$t("aitDetail.resource_description")}}</td>
                                                                <td>{{resource.resource_description}}</td>
                                                            </tr>
                                                        </table>
                                                    </li>
                                                </ul>
                                            </div>
                                        </template>
                                    </li>
                                </ul>
                            </div>
                        </li>
                    </ul>
                    <!-- downloads -->
                    <label for="panel_downloads">
                        <span v-if="accordionOnOffFlag.downloads"><img class="icon" title="unfold" :src="lessInfo"></span>
                        <span v-else><img class="icon" :src="moreInfo"></span>
                        {{$t("aitDetail.downloads")}}
                    </label>
                    <input type="checkbox" id="panel_downloads" class="on_off" v-model="accordionOnOffFlag.downloads"/>
                    <ul>
                        <li>
                            <template v-for="(download, index) in downloads">
                                <div class="sub_accordion_level2" :key="index">
                                    <label v-bind:for="6000 + index">
                                        <span v-if="downloadsOnOffFlag[index]"><img class="icon" title="unfold" :src="lessInfo"></span>
                                        <span v-else><img class="icon" :src="moreInfo"></span>
                                        {{$t("aitDetail.download")}} - {{index + 1}}
                                    </label>
                                    <input type="checkbox" v-bind:id="6000 + index" class="on_off" v-model="downloadsOnOffFlag[index]"/>
                                    <ul>
                                        <li>
                                            <table class="dataTable" @click="$event.target.parentElement.classList.toggle('expanded')">
                                                <tr>
                                                    <td>{{$t("aitDetail.download_name")}}</td>
                                                    <td>{{download.download_name}}</td>
                                                </tr>
                                                <tr>
                                                    <td>{{$t("aitDetail.download_description")}}</td>
                                                    <td>{{download.download_description}}</td>
                                                </tr>
                                            </table>
                                        </li>
                                    </ul>
                                </div>
                            </template>
                        </li>
                    </ul>
                    <template v-if="ait_local_installed_flag == 'false'">
                        <!-- ait_hub_properties -->
                        <label for="panel_ait_hub_properties">
                            <span v-if="accordionOnOffFlag.ait_hub_properties"> <img class="icon" title="unfold" :src="lessInfo"></span>
                            <span v-else><img class="icon" :src="moreInfo"></span>
                            {{$t("aitDetail.ait_hub_properties")}}
                        </label>
                        <input type="checkbox" id="panel_ait_hub_properties" class="on_off" v-model="accordionOnOffFlag.ait_hub_properties"/>
                        <ul>
                            <li>
                                <table class="dataTable" @click="$event.target.parentElement.classList.toggle('expanded')">
                                    <tr>
                                        <td>{{$t("aitDetail.ait_hub_source_repository")}}</td>
                                        <td>
                                            <img src="~@/assets/new_window.svg" alt="new-window" title="new-window" class="new-window">
                                            <a v-bind:href=cleanUrl(ait_hub_properties.source_repository) target="_blank">{{cleanUrl(ait_hub_properties.source_repository)}}</a>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>{{$t("aitDetail.ait_hub_downloads")}}</td>
                                        <td>{{ait_hub_properties.downloads}}</td>
                                    </tr>
                                    <tr>
                                        <td>{{$t("aitDetail.ait_hub_views")}}</td>
                                        <td>{{ait_hub_properties.views}}</td>
                                    </tr>
                                </table>
                            </li>
                        </ul>

                    </template>
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

<script>
import SubMenu from './SubMenu.vue';
import { subMenuMixin } from "../mixins/subMenuMixin";
import { urlParameterMixin } from '../mixins/urlParameterMixin';
import { AITHubMixin } from '../mixins/AITHubMixin';
import { AccountControlMixin } from '../mixins/AccountControlMixin';
import moreInfo from "@/assets/google_icon_unfold_less.svg";
import lessInfo from "@/assets/google_icon_unfold_more.svg";

export default {
    components: {SubMenu},
    mixins: [subMenuMixin, urlParameterMixin, AITHubMixin, AccountControlMixin],
    data() {
        return {
            moreInfo:moreInfo,
            lessInfo:lessInfo,
            aithub_id: '',
            ait_install_flag: false,
            install_mode: '',
            ait_properties: {
                ait_name: '',
                description: '',
                create_user_account: '',
                create_user_name: '',
                version: '',
                quality: '',
                references: [],
                keywords: [],
                licenses: []
            },
            inventories: [],
            parameters: [],
            measures: [],
            resources: [],
            downloads: [],
            ait_hub_properties: {
                source_repository: '',
                downloads: '',
                views: ''
            },
            onOffAllFlag: false,
            accordionOnOffFlag: {
                ait_properties: false,
                inventories: false,
                parameters: false,
                report: false,
                measures: false,
                resources: false,
                downloads: false,
                ait_hub_properties: false,
            },
            referencesOnOffFlag: [],
            inventoriesOnOffFlag: [],
            inventoryRequirementsOnOffFlag: [],
            inventoryCompatiblePackagesOnOffFlag: [],
            parametersOnOffFlag: [],
            measuresOnOffFlag: [],
            resourcesOnOffFlag: [],
            downloadsOnOffFlag: [],
            screenName: 'aitDetail',
            beforeScreenName: ''
        }
    },
    mounted: function () {
        this.aithub_id = sessionStorage.getItem('aithub_id');
        this.ait_local_installed_flag = sessionStorage.getItem('ait_local_installed_flag');
        this.beforeScreenName = sessionStorage.getItem('beforeScreenName');
        this.setLanguageData();
        this.getAITListFromLocal(this.screenName);
    },
    methods: {
        getAITDetail(){
            if (this.ait_local_installed_flag == 'false') {
                // AITHubから情報取得
                const url = this.$aithubURL + '/aits/' + this.aithub_id;
                this.$axios.get(url)
                .then((response) => {
                    // install_mode：2(aithubから)を設定
                    this.install_mode = '2';
                    var ait_Detail = response.data.AITDetail;
                    var comma = ' , ';
                    var ait_hub_key = ait_Detail.name +
                                    ait_Detail.version +
                                    ait_Detail.create_user_account;
                    var ait_local_key = '';

                    // ait_install
                    for (var i in this.aitList_local) {
                        ait_local_key = this.aitList_local[i].Name +
                                        this.aitList_local[i].Version +
                                        this.aitList_local[i].CreateUserAccount;
                        if (ait_local_key == ait_hub_key) {
                            this.ait_install_flag = true;
                            break;
                        }
                    }

                    // ait_properties
                    this.ait_properties.ait_name = ait_Detail.name;
                    this.ait_properties.description = ait_Detail.description;
                    this.ait_properties.create_user_account = ait_Detail.create_user_account;
                    this.ait_properties.create_user_name = ait_Detail.create_user_name;
                    this.ait_properties.version = ait_Detail.version;
                    this.ait_properties.quality = ait_Detail.quality;
                    this.ait_properties.references = ait_Detail.references;
                    ait_Detail.references.forEach(() => {
                       this.referencesOnOffFlag.push(false);
                    });
                    this.ait_properties.keywords = ait_Detail.keywords.join(comma);
                    this.ait_properties.licenses = ait_Detail.licenses.join(comma);

                    // inventories
                    for (var inv in ait_Detail.inventories) {
                        var inventory = ait_Detail.inventories[inv];
                        var requirements = [];
                        for (var req in inventory.requirements) {
                            var requirement = inventory.requirements[req];
                            requirements.push({
                                inventory_format: requirement.format.join(comma),
                                inventory_compatible_packages: requirement.compatible_packages,
                                inventory_additional_info: requirement.additional_info,
                                inventory_min: requirement.min,
                                inventory_max: requirement.max
                            });
                            var inventoryCompatiblePackages = [];
                            requirement.compatible_packages.forEach(() => {
                                inventoryCompatiblePackages.push(false);
                            });
                            this.inventoryCompatiblePackagesOnOffFlag.push(inventoryCompatiblePackages);
                        }

                        var inventoryRequirements = [];
                        requirements.forEach(() => {
                            inventoryRequirements.push(false);
                        });
                        this.inventoryRequirementsOnOffFlag.push(inventoryRequirements);

                        this.inventories.push({
                            inventory_name: inventory.name,
                            inventory_type: inventory.type,
                            inventory_description: inventory.description,
                            inventory_requirements : requirements,
                            inventory_depends_on_parameter: inventory.depends_on_parameter,
                        });
                        this.inventoriesOnOffFlag.push(false);
                    }

                    // parameters
                    for (var par in ait_Detail.parameters) {
                        var parameter = ait_Detail.parameters[par];
                        this.parameters.push({
                            parameter_name: parameter.name,
                            parameter_type: parameter.type,
                            parameter_description: parameter.description,
                            parameter_default_val: parameter.default_val,
                            parameter_min: parameter.min,
                            parameter_max: parameter.max,
                            parameter_depends_on_parameter: parameter.depends_on_parameter
                        });
                        this.parametersOnOffFlag.push(false);
                    }

                    // measures resources downloads
                    for (var pro in ait_Detail.products) {
                        var product = ait_Detail.products[pro];
                        if (product.type == 'measure') {
                            this.measures.push({
                                measure_name: product.name,
                                measure_description: product.description
                            });
                            this.measuresOnOffFlag.push(false);
                        } else if (product.type == 'resource') {
                            this.resources.push({
                                resource_name: product.name,
                                resource_description: product.description
                            });
                            this.resourcesOnOffFlag.push(false);
                        } else if (product.type == 'download') {
                            this.downloads.push({
                                download_name: product.name,
                                download_description: product.description
                            });
                            this.downloadsOnOffFlag.push(false);
                        }
                    }

                    // ait_hub_properties
                    this.ait_hub_properties.source_repository = ait_Detail.source_repository;
                    this.ait_hub_properties.downloads = ait_Detail.downloads;
                    this.ait_hub_properties.views = ait_Detail.views;
                })
                .catch((error) => {
                    this.signOutAitHubWhitErr();
                    this.triggerMessage('aithub_E02', error)
                });

            } else {

                // QunomonのローカルDBから情報取得
                var ait_Detail = null;
                var comma = ' , ';

                for (var i in this.aitList_local) {
                    if (this.aithub_id == this.aitList_local[i].Id) {
                        ait_Detail = this.aitList_local[i];
                        break;
                    }
                }

                // インストール済みのAIT情報からinstall_modeを設定
                this.install_mode = ait_Detail.InstallMode;

                // ait_properties
                this.ait_properties.ait_name = ait_Detail.Name;
                this.ait_properties.description = ait_Detail.Description;
                this.ait_properties.create_user_account = ait_Detail.CreateUserAccount;
                this.ait_properties.create_user_name = ait_Detail.CreateUserName;
                this.ait_properties.version = ait_Detail.Version;
                this.ait_properties.quality = ait_Detail.Quality;
                this.ait_properties.references = [];
                for (var refe in ait_Detail.References) {
                    this.ait_properties.references.push({
                        bib_info: ait_Detail.References[refe].Bib_info,
                        additional_info: ait_Detail.References[refe].Additional_info,
                        url: ait_Detail.References[refe].Url,
                    });
                }

                ait_Detail.References.forEach(() => {
                    this.referencesOnOffFlag.push(false);
                });
                this.ait_properties.keywords = ait_Detail.Keywords;
                this.ait_properties.licenses = ait_Detail.Licenses;

                // inventories
                for (var inv in ait_Detail.TargetInventories) {
                    var inventory = ait_Detail.TargetInventories[inv];
                    var requirements = [];
                    var format_obj_list = [];
                    inventory.Formats.forEach(format => {
                        format_obj_list.push(format.Format);
                    });

                    var compatible_packages = [];
                    for (var cp in inventory.CompatiblePackages) {
                        compatible_packages.push({
                            name: inventory.CompatiblePackages[cp].Name,
                            version: inventory.CompatiblePackages[cp].Version,
                            additional_info: inventory.CompatiblePackages[cp].Additional_info,
                        });
                    }

                    var additional_info = [];
                    for (var addi in inventory.AdditionalInfo) {
                        additional_info.push({
                            key: inventory.AdditionalInfo[addi].Key,
                            value: inventory.AdditionalInfo[addi].Value
                        });
                    }

                    requirements.push({
                        inventory_format: format_obj_list.join(comma),
                        inventory_compatible_packages: compatible_packages,
                        inventory_additional_info: additional_info,
                        inventory_min: inventory.Min,
                        inventory_max: inventory.Max
                    });
                    var inventoryCompatiblePackages = [];
                    inventory.CompatiblePackages.forEach(() => {
                        inventoryCompatiblePackages.push(false);
                    });
                    this.inventoryCompatiblePackagesOnOffFlag.push(inventoryCompatiblePackages);

                    var inventoryRequirements = [];
                    requirements.forEach(() => {
                        inventoryRequirements.push(false);
                    });
                    this.inventoryRequirementsOnOffFlag.push(inventoryRequirements);

                    this.inventories.push({
                        inventory_name: inventory.Name,
                        inventory_type: inventory.DataType.Name,
                        inventory_description: inventory.Description,
                        inventory_requirements : requirements,
                        inventory_depends_on_parameter: inventory.depends_on_parameter,
                    });
                    this.inventoriesOnOffFlag.push(false);
                }

                // parameters
                for (var par in ait_Detail.ParamTemplates) {
                    var parameter = ait_Detail.ParamTemplates[par];
                    this.parameters.push({
                        parameter_name: parameter.Name,
                        parameter_type: parameter.Type,
                        parameter_description: parameter.Description,
                        parameter_default_val: parameter.DefaultVal,
                        parameter_min: parameter.Min,
                        parameter_max: parameter.Max,
                        parameter_depends_on_parameter: parameter.depends_on_parameter
                    });
                    this.parametersOnOffFlag.push(false);
                }

                // measures
                var measures = ait_Detail.Report.Measures
                for (var m in measures) {
                    var measure =  measures[m];
                    this.measures.push({
                        measure_name: measure.Name,
                        measure_description: measure.Description
                    });
                    this.measuresOnOffFlag.push(false);
                }


                // resources
                var resources = ait_Detail.Report.Resources
                for (var r in resources) {
                    var resource =  resources[r];
                    this.resources.push({
                        resource_name: resource.Name,
                        resource_description: resource.Description
                    });
                    this.resourcesOnOffFlag.push(false);
                }

                // downloads
                for (var d in ait_Detail.Downloads) {
                    var download = ait_Detail.Downloads[d];
                    this.downloads.push({
                        download_name: download.Name,
                        download_description: download.Description
                    });
                    this.downloadsOnOffFlag.push(false);
                }
            }
        },
        aitInstall(){
             // インストール実行
            if (confirm(this.$t("confirm.aitInstall"))) {
                this.aitInstallCore(this.aithub_id,
                                    this.ait_properties.create_user_account,
                                    this.ait_properties.create_user_name);
            }
        },
        onOffAllAccordion(){
            if (this.onOffAllFlag) {
                this.accordionOnOffFlag.ait_properties = true;
                this.accordionOnOffFlag.inventories = true;
                this.accordionOnOffFlag.parameters = true;
                this.accordionOnOffFlag.report = true;
                this.accordionOnOffFlag.downloads = true;
                this.accordionOnOffFlag.ait_hub_properties = true;
            } else {
                this.accordionOnOffFlag.ait_properties = false;
                this.accordionOnOffFlag.inventories = false;
                this.accordionOnOffFlag.parameters = false;
                this.accordionOnOffFlag.report = false;
                this.accordionOnOffFlag.downloads = false;
                this.accordionOnOffFlag.ait_hub_properties = false;
            }
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
#head .head_title {
    margin-left: 2rem;
}

#main {
    overflow: hidden;
}

#main #main_body {
    position: relative;
    z-index: 0;
    white-space: pre-line;
}

#detailInfo {
    margin: 60px auto;
    width: 90%;
    vertical-align: middle;
    text-align: center;
    padding-top: 2rem;
}

/* Float four columns side by side */

.eachCard ul {
    -webkit-transition: all 0.5s;
    -moz-transition: all 0.5s;
    -ms-transition: all 0.5s;
    -o-transition: all 0.5s;
    transition: all 0.5s;
    padding: 0;
    list-style: none;
}
/* Remove extra left and right margins, due to padding */
.cardRow {margin: 0 -5px;}

/* Clear floats after the columns */


/* Responsive columns */
@media screen and (max-width: 1000px) {
    .cardCol {
        width: 100%;
        display: block;
        margin-bottom: 20px;
    }
}

/* Style the counter cards */
.eachCard {
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
    text-align: center;
    vertical-align: middle;
    background-color: #f1f1f1;
    border-radius: 5px;
}

.eachCard label {
    background-color: #dc722b;
    color: #ffffff;
    padding: 2px 8px;
    height: 2.5rem;
    font-size: 1rem;
    font-weight: bold;
    border-radius: 5px;
    display: flex;
    align-items: center;
/* border-top-left-radius: 5px; */
/* border-top-right-radius: 5px; */
}


.eachCard table {
    border-spacing: 0 1rem;
    border-collapse: separate;
    border: none;
}

.dataTable {
    width: 100%;
    border-spacing: 0 5px;
    border-collapse: separate;
    border: none;
}
.dataTable td{
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
    max-width: 10rem;
    font-size: 0.85rem;
    height: 2rem;
    padding: unset;
    text-align: center;
    vertical-align: middle;
}
.dataTable .expanded td {
    white-space: normal;
    overflow: visible;
    text-overflow: unset;
    max-width: 10%;
    text-align: center;
    vertical-align: middle;
}
.dataTable td:nth-child(1) {
    text-align: center;
    width: 30%;
    font-weight: bold;
    color: black;
    background: #a9c7aa;
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
    &:hover {
        background-color: #43645b;
        color: white;
    }
}
.dataTable td:last-child{
    border: 1px solid;
    border-color: #a9c7aa;
    text-align: center;
    color: black;
    background: white;
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
}

.sub_accordion_level1 {
    padding-left: 4rem;
    padding-top: 1rem;
    text-align: center;
    vertical-align: middle;
}

.sub_accordion_level2{
    padding-left: 4rem;
    padding-top: 1rem;
    text-align: center;
    vertical-align: middle;
}
.sub_accordion_level2 label {
    padding-left: 1rem;

}
.sub_accordion_level3{
    padding-left: 4rem;
    padding-top: 1rem;
    text-align: center;
    vertical-align: middle;
}

.sub_accordion_level4{
    padding-left: 4rem;
    padding-top: 1rem;
    text-align: center;
    vertical-align: middle;
}

input[type="checkbox"].on_off {
    display: none;
}

input[type="checkbox"].on_off+ul {
    height: auto;
}

input[type="checkbox"].on_off:checked+ul{
    height: 0;
    overflow: hidden;
}
.left_padding {
    padding-left: 4rem;
}

.ait_install {
    position: fixed;
    width: 100%;
    background-color: #f0f0f0;
}

.ait_install_btn {
    margin: 15px 0px;
    padding-left: 30px;
    float:left;
}

.ait_install_text {
    margin: 20px 0px;
    padding-left: 30px;
    float:left;
    font: 15px;
}

</style>
<!-- サブメニュー（左カラム） -->
<template>
    <div id="sidebar-main">
        <aside>
            <b-sidebar
                id="sidebar"
                backdrop
                bg-variant="#f0f0f0"
                no-header
                sidebar-class="border-right"
                width="12.5rem"
            >

                <b-list-group flush>
                    <div id="submenu" :class="{'active': this.isActive}">
                        <div id="logo">
                            <img src="~@/assets/logo.svg" alt="logo" class="logo">
                        </div>
                        <slot></slot><!--ここに言語切替要素が入ってくる-->


                        <b-list-group-item to="MLComponents" variant="success" active-class="active" exact>
                            <span v-if="this.isActive" :title="$t('common.menuMLComponents')"><img :src="MLComponentIcon"  alt="Image" class="imageBtn" width="30" height="auto"></span>
                            <span v-else>{{$t("common.menuMLComponents")}}</span>
                        </b-list-group-item>
                        <b-list-group-item to="Guidelines" variant="success" active-class="active">
                            <span v-if="this.isActive" :title="$t('common.menuGuidelines')"><img :src="GuidelinesIcon" alt="Image" class="imageBtn" width="30" height="auto"></span>
                            <span v-else>{{$t("common.menuGuidelines")}}</span>
                        </b-list-group-item>
                        <b-list-group-item to="AITDashboard" variant="success" active-class="active">
                            <span v-if="this.isActive" :title="$t('')"><img :src="InstalledAITsIcon" alt="Image" class="imageBtn" width="30" height="auto"></span>
                            <span v-else>{{$t("common.menuAITDashboard")}}</span>
                        </b-list-group-item>
                        <template v-if="aithub_linkage_mode">
                            <b-list-group-item to="AITSearch" variant="success" active-class="active">
                                <span v-if="this.isActive" :title="$t('common.menuAITSearch')"><img :src="AITSearchIcon" alt="Image" class="imageBtn" width="30" height="auto"></span>
                                <span v-else>{{$t("common.menuAITSearch")}}</span>
                            </b-list-group-item>
                        </template>
                        <template v-if="aithub_linkage_mode">
                            <b-list-group-item to="AITRanking" variant="success" active-class="active">
                                <span v-if="this.isActive" :title="$t('common.menuAITRanking')"><img :src="AITRankingIcon" alt="Image" class="imageBtn" width="30" height="auto"></span>
                                <span v-else>{{$t("common.menuAITRanking")}}</span>
                            </b-list-group-item>
                        </template>
                        <b-list-group-item to="AITLocalInstall" variant="success" active-class="active">
                            <span v-if="this.isActive" :title="$t('common.menuAITLocalInstall')"><img :src="AITLocalInstallIcon" alt="Image" class="imageBtn" width="30" height="auto"></span>
                            <span v-else>{{$t("common.menuAITLocalInstall")}}</span>
                        </b-list-group-item>
                        <b-list-group-item to="ReportTemplate" variant="success" active-class="active">
                            <span v-if="this.isActive" :title="$t('common.menuReportTemplate')"><img :src="ReportTemplateIcon" alt="Image" class="imageBtn" width="30" height="auto"></span>
                            <span v-else>{{$t("common.menuReportTemplate")}}</span>
                        </b-list-group-item>
                    </div>
                </b-list-group>
            </b-sidebar>
        </aside>
    </div>
</template>

<script>
import { AccountControlMixin } from '../mixins/AccountControlMixin';
import { csrfMixin } from '../mixins/csrfMixin';
import pageMixin from "@/mixins/pageMixin";
import MLComponentIcon from '@/assets/MLComponents_icon.svg'
import GuidelinesIcon from '@/assets/Guidelines_icon.svg'
import InstalledAITsIcon from '@/assets/Installed_AITs_icon.svg'
import AITSearchIcon from '@/assets/AITSearching_icon.svg'
import AITRankingIcon from "@/assets/AITRanking_icon.svg";
import AITLocalInstallIcon from '@/assets/AITLocalInstall_icon.svg'
import ReportTemplateIcon from '@/assets/ReportTemplate_icon.svg'


export default {
    mixins: [AccountControlMixin, csrfMixin],
    data() {
        return{
            MLComponentIcon: MLComponentIcon,
            GuidelinesIcon: GuidelinesIcon,
            InstalledAITsIcon: InstalledAITsIcon,
            AITSearchIcon: AITSearchIcon,
            AITRankingIcon: AITRankingIcon,
            AITLocalInstallIcon: AITLocalInstallIcon,
            ReportTemplateIcon: ReportTemplateIcon,
            isActive: this.setIsActive_SubMenu()
        }
    },
    created: async function() {
        pageMixin.$on('classToggled', isActive => {
            this.isActive = isActive;
        })
        await this.setAithubUsing();
        await this.setAITHubLinkageMode();
    },
    mounted: async function () {
        await this.getCsrfToken();
    },
    methods: {
        setIsActive_SubMenu(){
            let checkIsActive = sessionStorage.getItem('isActive')
            if (checkIsActive === null){
                return false;
            }else{
                return checkIsActive !== "false";
            }
        },
    }
}
</script>

<style>
#sidebar-main, #sidebar{
    background-color: #f0f0f0;
}

#company_name {
    width: 100%;
}
#company_name table{
    width: 100%;
}
#company_name table td:nth-child(1){
    text-align: left;
}
#company_name table td:last-child{
    text-align: center;
}
/* SidebarをNavbarの下に配置 */
.b-sidebar,
.b-sidebar-backdrop {
    background-color: #f0f0f0;
    top: 3rem;
    padding-bottom: 56px;
}

.wrapper {
    position: relative;
    margin-top: 56px;
    min-height: calc(100vh - 56px);
    padding-bottom: 30px;
    background: #f0f0f0;

}

.list-group-item.list-group-item-success {
    color: #43645b;
    background-color: #a9c7aa;
}
.list-group-item.list-group-item-success.list-group-item-action:hover, .list-group-item-success.list-group-item-action:focus {
    color: #fff;
    background-color: rgba(255, 255, 255, 0.37);
}
.list-group-item.list-group-item-success.list-group-item-action.active {
    color: #fff;
    background-color: #43645b;
    border-color: #43645b;
}
.qq {
    background: unset;
    position: absolute;
    width: 30px;
    height: 30px;
    border: none;
    border-radius: 5px;
    cursor:pointer;
}
.qq:hover{
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.7);
}
.qq img {
    height: auto;
    width: 25px;
}
/* 横幅992px以上 */
@media (min-width: 992px) {
    /* メニューボタン非表示 */
    #menubtn,
    .b-sidebar-backdrop {
        display: none;
    }
    /* Sidebar常時表示 */
    .b-sidebar {
        display: block !important;
    }
}
</style>
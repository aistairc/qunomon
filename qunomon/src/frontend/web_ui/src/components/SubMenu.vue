<!-- サブメニュー（左カラム） -->
<template>
    <div id="sidebar-main">
        <aside>
            <BNavbar
                id="sidebar"
                width="12.5rem"
                container="'Breakpoint'"
            >

                <BListGroup flush>
                    <div id="submenu" :class="{'active': this.isActive}">
                        <div id="logo">
                            <img src="~@/assets/logo.svg" alt="logo" class="logo">
                        </div>
                        <slot></slot><!--ここに言語切替要素が入ってくる-->


                        <BListGroupItem 
                            :active="$route.path === '/mLcomponents'" 
                            to="MLComponents" 
                            variant="success" 
                            active-class="active"
                        >
                            <span v-if="this.isActive" :title="$t('common.menuMLComponents')"><img :src="MLComponentIcon"  alt="Image" class="imageBtn" width="30" height="auto"></span>
                            <span v-else>{{$t("common.menuMLComponents")}}</span>
                        </BListGroupItem>
                        <BListGroupItem to="Guidelines" variant="success" active-class="active" :active="$route.path === '/guidelines'">
                            <span v-if="this.isActive" :title="$t('common.menuGuidelines')"><img :src="GuidelinesIcon" alt="Image" class="imageBtn" width="30" height="auto"></span>
                            <span v-else>{{$t("common.menuGuidelines")}}</span>
                        </BListGroupItem>
                        <BListGroupItem to="AITDashboard" variant="success" active-class="active" :active="$route.path === '/AITDashboard'">
                            <span v-if="this.isActive" :title="$t('')"><img :src="InstalledAITsIcon" alt="Image" class="imageBtn" width="30" height="auto"></span>
                            <span v-else>{{$t("common.menuAITDashboard")}}</span>
                        </BListGroupItem>
                        <template v-if="aithub_linkage_mode">
                            <BListGroupItem to="AITSearch" variant="success" active-class="active" :active="$route.path === '/AITSearch'">
                                <span v-if="this.isActive" :title="$t('common.menuAITSearch')"><img :src="AITSearchIcon" alt="Image" class="imageBtn" width="30" height="auto"></span>
                                <span v-else>{{$t("common.menuAITSearch")}}</span>
                            </BListGroupItem>
                        </template>
                        <template v-if="aithub_linkage_mode">
                            <BListGroupItem to="AITRanking" variant="success" active-class="active" :active="$route.path === '/AITRanking'">
                                <span v-if="this.isActive" :title="$t('common.menuAITRanking')"><img :src="AITRankingIcon" alt="Image" class="imageBtn" width="30" height="auto"></span>
                                <span v-else>{{$t("common.menuAITRanking")}}</span>
                            </BListGroupItem>
                        </template>
                        <BListGroupItem to="AITLocalInstall" variant="success" active-class="active" :active="$route.path === '/AITLocalInstall'">
                            <span v-if="this.isActive" :title="$t('common.menuAITLocalInstall')"><img :src="AITLocalInstallIcon" alt="Image" class="imageBtn" width="30" height="auto"></span>
                            <span v-else>{{$t("common.menuAITLocalInstall")}}</span>
                        </BListGroupItem>
                        <BListGroupItem to="ReportTemplate" variant="success" active-class="active" :active="$route.path === '/ReportTemplate'">
                            <span v-if="this.isActive" :title="$t('common.menuReportTemplate')"><img :src="ReportTemplateIcon" alt="Image" class="imageBtn" width="30" height="auto"></span>
                            <span v-else>{{$t("common.menuReportTemplate")}}</span>
                        </BListGroupItem>
                        <BListGroupItem to="Setting" variant="success" active-class="active" :active="$route.path === '/setting'">
                            <span v-if="this.isActive" :title="$t('common.menuSetting')"><img :src="SettingIcon" alt="Image" class="imageBtn" width="30" height="auto"></span>
                            <span v-else>{{$t("common.menuSetting")}}</span>
                        </BListGroupItem>
                    </div>
                </BListGroup>
            </BNavbar>
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
import SettingIcon from '@/assets/Setting_icon.svg'
import { BNavbar, BListGroup, BListGroupItem } from 'bootstrap-vue-next'


export default {
    mixins: [AccountControlMixin, csrfMixin],
    components: {
        BNavbar,
        BListGroup,
        BListGroupItem
    },
    data() {
        return{
            MLComponentIcon: MLComponentIcon,
            GuidelinesIcon: GuidelinesIcon,
            InstalledAITsIcon: InstalledAITsIcon,
            AITSearchIcon: AITSearchIcon,
            AITRankingIcon: AITRankingIcon,
            AITLocalInstallIcon: AITLocalInstallIcon,
            ReportTemplateIcon: ReportTemplateIcon,
            SettingIcon: SettingIcon,
            isActive: this.setIsActive_SubMenu()
        }
    },
    created: async function() {
        pageMixin.on('classToggled', isActive => {
            this.isActive = isActive;
        })
    },
    mounted: async function () {
        await this.getCsrfToken();
        setTimeout(() => {
            this.setAITHubLinkageMode();
        }, 500); 
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
    },
    computed: {
        currentPath() {
            return this.$route.path;
        }
    }
}
</script>

<style>
#sidebar-main, #sidebar{
    background-color: var(--gray-thema);
    height: 3rem;
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
    background-color: var(--gray-thema);
    top: 3rem;
    padding-bottom: 56px;
}

.wrapper {
    position: relative;
    margin-top: 56px;
    min-height: calc(100vh - 56px);
    padding-bottom: 30px;
    background: var(--gray-thema);

}

.list-group-item.list-group-item-success {
    color: var(--primary-color);
    background-color: var(--primary-color-light);
}
.list-group-item.list-group-item-success.list-group-item-action:hover, .list-group-item-success.list-group-item-action:focus {
    color: #fff;
    background-color: rgba(255, 255, 255, 0.37);
}
.list-group-item.list-group-item-success.list-group-item-action.active {
    color: #fff;
    background-color: var(--primary-color);
    border-color: var(--primary-color);
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

/* アクティブなアイテムのスタイル */
.list-group-item.active {
    color: #fff !important;
    background-color: var(--primary-color) !important;
    border-color: var(--primary-color) !important;
}

/* ホバー時のスタイル */
.list-group-item:hover {
    color: #fff;
    background-color: rgba(67, 100, 91, 0.8) !important;
}

/* アクティブ状態のスタイルをより具体的に指定 */
.list-group-item.list-group-item-success.active,
.list-group-item.list-group-item-success.router-link-active {
  color: #fff !important;
  background-color: var(--primary-color) !important;
  border-color: var(--primary-color) !important;
}

/* ホバー時のスタイル */
.list-group-item.list-group-item-success:hover {
  color: #fff;
  background-color: rgba(67, 100, 91, 0.8) !important;
  cursor: pointer;
}
</style>
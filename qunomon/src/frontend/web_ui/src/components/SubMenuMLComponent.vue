<!-- サブメニュー（左カラム） -->
<template>
    <div id="sidebar-main">
        <aside>
            <BNavbar   
                id="sidebar-backdrop"
                width="12.5rem"
                container="'Breakpoint'"
            >
                <BListGroup flush>
                    <div id="submenu" :class="{'active': this.isActive}">
                        <div id="logo">
                            <img src="~@/assets/logo.svg" alt="logo" class="logo">
                        </div>

                        <slot name="language"></slot><!--ここに言語切替要素が入ってくる-->

                        <BListGroupItem to="test_descriptions" variant="success" active-class="active" exact :active="$route.path === '/test_descriptions'">
                            <span v-if="this.isActive" :title="$t('common.menuTestDescriptions')">
                                <img :src="TestDescriptionIcon" alt="Image" class="imageBtn" width="30" height="auto">
                            </span>
                            <span v-else>{{$t("common.menuTestDescriptions")}}</span>

                        </BListGroupItem>

                        <slot name="TestDescriptionDetail"></slot><!--ここにTestDescriptionDetail要素が入ってくる-->
                        <slot name="download"></slot><!--ここにdownload要素が入ってくる-->

                        <BListGroupItem to="Inventories" variant="success" active-class="active" :active="$route.path === '/Inventories'">
                            <span v-if="this.isActive" :title="$t('common.menuInventories')">
                                <img :src="InventoryIcon" alt="Image" class="imageBtn" width="30" height="auto">
                            </span>
                            <span v-else>{{$t("common.menuInventories")}}</span>

                        </BListGroupItem>
                        <li class="mlcomponent un_place">
                            <BListGroupItem to="MLComponents" variant="success" active-class="active" :active="$route.path === '/mLcomponents'">
                                <span v-if="this.isActive" :title="$t('common.menuMLComponents')">
                                    <img :src="MLComponentIcon" alt="Image" class="imageBtn" width="30" height="auto">
                                </span>
                                <span v-else>{{$t("common.menuMLComponents")}}</span>

                            </BListGroupItem>
                        </li>
                    </div>
                </BListGroup>
            </BNavbar>
        </aside>
    </div>
</template>

<script>
import { AccountControlMixin } from '../mixins/AccountControlMixin';
import { csrfMixin } from '../mixins/csrfMixin';
import MLComponentIcon from "@/assets/MLComponents_icon.svg";
import TestDescriptionIcon from "@/assets/TestDescription_icon.svg";
import InventoryIcon from "@/assets/Inventory_icon.svg";
import pageMixin from "@/mixins/pageMixin";
import { BNavbar, BListGroup, BListGroupItem } from 'bootstrap-vue-next'
export default {
    mixins: [AccountControlMixin, csrfMixin],
    components: {
        BNavbar,
        BListGroup,
        BListGroupItem
    },
    data() {
        return {
            MLComponentIcon: MLComponentIcon,
            TestDescriptionIcon: TestDescriptionIcon,
            InventoryIcon: InventoryIcon,
            tdDtl:'',
            isActive: this.setIsActive_SubMenu(),
        }
    },
    mounted: async function () {
        await this.getCsrfToken();
    },
    created() {
        pageMixin.on('classToggled', isActive => {
            this.isActive = isActive;
        })
    },
    methods: {
        setIsActive_SubMenu(){
            let checkIsActive = sessionStorage.getItem('isActive')
            if (checkIsActive === null){
                return false;
            }else{
                return checkIsActive !== "false";
            }
        }
    }
}
</script>

<style>


/* SidebarをNavbarの下に配置 */
.b-sidebar,
.b-sidebar-backdrop {
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
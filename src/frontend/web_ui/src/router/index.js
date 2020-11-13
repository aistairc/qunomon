import Vue from 'vue'
import Router from 'vue-router'
import SignIn from '@/components/SignIn'
import MLComponents from '@/components/MLComponents'
import Inventories from '@/components/Inventories'
import InventoryEdit from '@/components/InventoryEdit'
import TestDescriptions from '@/components/TestDescriptions'
import TestDescriptionsDetail from '@/components/TestDescriptionsDetail'
import TestDescriptionsDownload from '@/components/TestDescriptionsDownload'
import TestDescriptionsCompare from '@/components/TestDescriptionsCompare'
import TestDescriptionRelationship from '@/components/TestDescriptionRelationship'
import MLComponentCreate from '@/components/MLComponentCreate'
import TestDescriptionAppend from '@/components/TestDescriptionAppend'
import TestDescriptionEdit from '@/components/TestDescriptionEdit'
import InventoryAppend from '@/components/InventoryAppend'
import TestDescriptionCopy from '@/components/TestDescriptionCopy'
import Information from '@/components/Information'
import TestDescriptionAppend2 from '@/components/TestDescriptionAppend2'
import TestDescriptionEdit2 from '@/components/TestDescriptionEdit2'
import InventoryAdd from '@/components/InventoryAdd'


Vue.use(Router)
Vue.prototype.$backendURL = process.env.VUE_APP_BACKENDURL
Vue.prototype.$frontendURL = process.env.VUE_APP_FRONTENDURL

export default new Router({
  //  mode: 'history', // ルートのURLから自動で入る'#'を取り除く
   routes: [
     {
      path: '/',
      name: 'SignIn',
      component: SignIn
     },
     {
      path: '/mlcomponents',
      name: 'MLComponents',
      component: MLComponents
    },
    {
      path: '/inventories',
      name: 'Inventories',
      component: Inventories
    },
    {
      path: '/inventory_edit',
      name: 'InventoryEdit',
      component: InventoryEdit
    },
    {
      path: '/test_descriptions',
      name: 'TestDescriptions',
      component: TestDescriptions
    },
    {
      path: '/test_descriptions_detail',
      name: 'TestDescriptionsDetail',
      component: TestDescriptionsDetail
    },
    {
      path: '/test_descriptions_download',
      name: 'TestDescriptionsDownload',
      component: TestDescriptionsDownload
    },
    {
      path: '/test_descriptions_compare',
      name: 'TestDescriptionsCompare',
      component: TestDescriptionsCompare
    },
    {
      path: '/test_description_relationship',
      name: 'TestDescriptionRelationship',
      component: TestDescriptionRelationship
    },
    {
      path: '/ml_component_edit',
      name: 'MLComponentCreate',
      component: MLComponentCreate
    },
    {
      path: '/test_description_append',
      name: 'TestDescriptionAppend',
      component: TestDescriptionAppend
    },
    {
      path: '/test_description_edit',
      name: 'TestDescriptionEdit',
      component: TestDescriptionEdit
    },
    {
      path: '/test_description_copy',
      name: 'TestDescriptionCopy',
      component: TestDescriptionCopy
    },
    {
      path: '/inventory_append',
      name: 'InventoryAppend',
      component: InventoryAppend
    },
    {
      path: '/information',
      name: 'Information',
      component: Information
    },
    {
      path: '/test_description_append2',
      name: 'TestDescriptionAppend2',
      component: TestDescriptionAppend2
    },
    {
      path: '/test_description_edit2',
      name: 'TestDescriptionEdit2',
      component: TestDescriptionEdit2
    },
    {
      path: '/inventory_add',
      name: 'InventoryAdd',
      component: InventoryAdd
    },
   ]
})

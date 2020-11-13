import Vue from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import VueI18n from 'vue-i18n'
import VModal from 'vue-js-modal'

Vue.config.productionTip = false
Vue.use(VueI18n)
//JSONの読み込み
const data = require('./components/languages/languages.json');

const i18n = new VueI18n({
  locale: 'en',
  messages: data
})

Vue.prototype.$axios = axios;

Vue.use(VModal);

// API以外のJavaScript内でのエラーをハンドリングする予定（未検証）
Vue.config.errorHandler = (err, vm, info) => {
  // eslint-disable-next-line no-console
  console.log(err);
  // eslint-disable-next-line no-console
  console.log(vm);
  // eslint-disable-next-line no-console
  console.log(info);
  router.push({
    name: 'Information',
    params: {err, vm, info}
  })
}

new Vue({
  i18n,
  router,
  render: h => h(App)
}).$mount('#app')

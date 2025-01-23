import App from './App.vue'
import router from './router'
import axios from 'axios'
import { createI18n } from 'vue-i18n'
import { createApp } from 'vue'
import {createBootstrap} from 'bootstrap-vue-next'
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css';
import { configureCompat } from 'vue';

const app = createApp(App)

// vue3の変更で影響が大きい部分をオプトインでvue2のままにする
// OPTIONS_DATA_MERGE: dataのマージが浅いコピーになる挙動
configureCompat({
  MODE: 3,
  OPTIONS_DATA_MERGE: true
})

//JSONの読み込み
const data = require('./components/languages/languages.json');

const i18n = createI18n({
  locale: 'en',
  messages: data
})

app.config.globalProperties.$axios = axios;

app.config.globalProperties.$backendURL = process.env.VUE_APP_BACKENDURL
app.config.globalProperties.$frontendURL = process.env.VUE_APP_FRONTENDURL
app.config.globalProperties.$aithubURL = process.env.VUE_APP_AITHUBURL

app.use(createBootstrap());
app.use(i18n);
app.use(router);
app.mount('#app');

import Vue from 'vue'
import App from './App.vue'
import store from "@/store";
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import 'element-ui/lib/theme-chalk/base.css';
import router from './router'
import '@/style/index.scss' // 全局样式
import '@/router/beforce'
import '@/utils/StringUtils'
import '@/utils/ArrayUtils'
import VueCookies from 'vue-cookies'

Vue.config.productionTip = false

Vue.use(VueCookies)
Vue.use(ElementUI)

new Vue({
  el: '#app',
  render: h => h(App),
  router,
  store
})

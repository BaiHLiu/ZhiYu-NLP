import Vue from 'vue'
import router from "@/router/index";
import Antd from 'ant-design-vue'
import App from './App'
import 'ant-design-vue/dist/antd.css'

import Axios from 'axios'

Vue.prototype.$axios = Axios;  //在Vue的原型上添加$axios方法


Vue.config.productionTip = false

Vue.use(Antd)

new Vue({
    router,
    render: h => h(App),
}).$mount('#app')
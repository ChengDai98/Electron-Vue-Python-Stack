
import './assets/styles/index.scss';

import Vue from 'vue';
import App from './App.vue';
import router from './router/index';
import ViewUI from 'view-design';
import 'view-design/dist/styles/iview.css';
import * as echarts from 'echarts';

Vue.prototype.$echarts = echarts
Vue.use(ViewUI);
Vue.config.productionTip = false;

new Vue({
    el: '#app',
    router,
    components: { App },
    render: h => h(App)
})
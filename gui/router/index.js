import Vue from 'vue'
import Router from 'vue-router'
import Index from '../components/Index.vue'
import Resistence from '../components/Resistence.vue'
import Pressure from '../components/Pressure.vue'

Vue.use(Router)

export default new Router({
    mode: 'history',
    linkExactActiveClass: 'active',
    routes: [
        {
            path: '/index',
            name: 'Index',
            component: Index
        },
        {
            path: '/resistence',
            name: 'Resistence',
            component: Resistence
        },
        {
            path: '/pressure',
            name: 'Pressure',
            component: Pressure
        }
    ]
})
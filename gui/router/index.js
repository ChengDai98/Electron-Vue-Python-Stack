import Vue from 'vue'
import Router from 'vue-router'
import Microscope from '../components/Microscope.vue'
import Resistence from '../components/Resistence.vue'
import Pressure from '../components/Pressure.vue'

Vue.use(Router)

export default new Router({
    mode: 'history',
    linkExactActiveClass: 'active',
    routes: [
        {
            path: '/microscope',
            name: 'Microscope',
            component: Microscope
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
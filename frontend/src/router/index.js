import Vue from 'vue'
import VueRouter from 'vue-router'

import Home from '../views/Home.vue'
import Today from '../views/Today.vue';
import History from '../views/History.vue';
import Relax from '../views/Relax.vue';
import Shared from '../views/Shared.vue';
import LoginSignUp from '../views/LoginSignUp.vue';
import SchedulePage from '../views/SchedulePage.vue';

Vue.use(VueRouter)

const routes = [
    {
        path: '/login',
        name: 'Login',
        component: LoginSignUp,
    },
    {
        path: '/today',
        name: 'Today',
        component: Today
    },
    {
        path: '/shared',
        name: 'Shared',
        component: Shared,
    },
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/relax',
        name: 'Relax',
        component: Relax,
    },
    {
        path: '/history',
        name: 'History',
        component: History
    },
    {
        path: '/schedule/:scheduleId',
        name: 'Schedule',
        component: SchedulePage
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router

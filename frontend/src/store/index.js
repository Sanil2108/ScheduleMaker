import Vue from 'vue'
import Vuex from 'vuex'

import schedule from './schedule/index';
import users from './users/index';
import ui from './ui/index';

Vue.use(Vuex)

export default new Vuex.Store({
    state: {
    },
    mutations: {
    },
    actions: {
    },
    modules: {
        'schedule': schedule,
        'users': users,
        'ui': ui,
    }
})

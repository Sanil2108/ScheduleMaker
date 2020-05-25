export default {
    namespaced: true,
    state: {
        notification: null,
    },
    getters: {
        currentNotification(state) {
            return state.notification;
        },
    },
    mutations: {
        CREATE_NOTIFICATION(state, { message, type }) {
            state.notification = {
                text: message,
                type,
            }
        },
        CLEAR_NOTIFICATION(state) {
            state.notification = null;
        }
    },
    actions: {
        manageNewNotification({ commit }, { message, type }) {
            commit('CREATE_NOTIFICATION', { message, type });
            setTimeout(() => {
                commit('CLEAR_NOTIFICATION');
            }, 5000)
        },
        clearNotification({ commit }) {
            commit('CLEAR_NOTIFICATION');
        }
    }
}
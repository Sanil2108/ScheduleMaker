import * as axios from 'axios';

import {
    SIGN_UP_URL,
    LOGIN_URL
} from '../../networkConstants';

export default {
    namespaced: true,
    state: {
        user: {
        }
    },
    mutations: {
        SET_USER(state, user) {
            state.user = user;
            if (user) {
                axios.defaults.headers.common['Authorization'] = 'Basic ' + btoa(`${user.email}:${user.token}`);
            }
            else {
                axios.defaults.headers.common['Authorization'] = undefined;
            }
        },
    },
    getters: {
        user(state) {
            return state.user;
        },
        userName(state) {
            return state.user.name;
        },
        userEmail(state) {
            return state.user.email;
        },
        userToken(state) {
            return state.user.token;
        },
    },
    actions: {
        async validateCurrentUser({ commit, dispatch, getters }) {
            const email = getters.userEmail;
            const token = getters.userToken;
            const authHeaderValue = 'Basic ' + btoa(`${email}:${token}`)

            if (email == null || token == null) {
                return false;
            }

            return await new Promise((resolve, reject) => {
                axios.post(LOGIN_URL()).then((response) => {
                    resolve(true);
                }).catch((error) => {
                    resolve(false);
                })
            });
        },
        async signUpUser({ commit, dispatch }, { email, name, password }) {
            return await new Promise((resolve, reject) => {
                axios.post(SIGN_UP_URL(), {
                    email,
                    password,
                    name,
                }).then((response) => {
                    dispatch('ui/manageNewNotification', { message: 'Sign up successful', type: 'success' }, { root: true });
                    resolve({ status: response.status });
                }).catch((error) => {
                    if (error.response) {
                        dispatch('ui/manageNewNotification', { message: error.response.data, type: 'error' }, { root: true });
                        reject({
                            status: error.response.status,
                            message: error.response.data,
                        });
                    }
                    else {
                        dispatch('ui/manageNewNotification', { message: 'Unknown error', type: 'error' }, { root: true });
                        reject({
                            status: 400,
                            message: 'Unknown error',
                        });
                    }
                })
            });
        },
        async loginUser({ commit, dispatch }, { email, password }) {
            const authHeaderValue = 'Basic ' + btoa(`${email}:${password}`)

            return await new Promise((resolve, reject) => {
                axios.post(LOGIN_URL(), {}, { headers: { Authorization: authHeaderValue } }).then((response) => {
                    commit('SET_USER', { email, token: response.data.token, name: response.data.name });
                    dispatch('ui/manageNewNotification', { message: 'Login successful', type: 'success' }, { root: true });
                    dispatch('saveCurrentUserToLocalStorage');
                    resolve({ status: response.status });
                }).catch((error) => {
                    if (error.response) {
                        dispatch('ui/manageNewNotification', { message: error.response.data, type: 'error' }, { root: true });
                        reject({
                            status: error.response.status,
                            message: error.response.data,
                        });
                    }
                    else {
                        dispatch('ui/manageNewNotification', { message: 'Unknown error', type: 'error' }, { root: true });
                        reject({
                            status: 400,
                            message: 'Unknown error',
                        });
                    }
                })
            });
        },
        logoutUser({ commit, dispatch }) {
            commit('SET_USER', null);
            dispatch('saveCurrentUserToLocalStorage');
        },
        saveCurrentUserToLocalStorage({ getters }) {
            const user = getters.user;
            if (user) {
                localStorage.setItem('user', JSON.stringify({
                    email: user.email,
                    name: user.name,
                    token: user.token,
                }));
            }
            else {
                localStorage.removeItem('user');
            }
        },
        loadCurrentUserFromLocalStorage({ commit }) {
            if (localStorage.getItem('user')) {
                commit('SET_USER', JSON.parse(localStorage.getItem('user')));
            }
        }
    }
}
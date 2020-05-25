import * as axios from 'axios';

import {
    SCHEDULE_URL,
    SCHEDULES_BY_DATE,
    DELETE_SCHEDULE,
    CREATE_EVENT,
    DELETE_EVENT,
    CREATE_COMMENT,
    EDIT_EVENT as EDIT_EVENT_URL,
} from '../../networkConstants';

export default {
    namespaced: true,
    state: {
        allSchedules: [],
        uiEnabled: true,
    },
    mutations: {
        ENABLE_UI(state) {
            state.uiEnabled = true;
        },
        DISABLE_UI(state) {
            state.uiEnabled = false;
        },
        EDIT_EVENT(state, { scheduleId, eventId, updatedEvent }) {
            const schedule = state.allSchedules.find((element) => element.id === scheduleId);
            let event = schedule.event_set.find((element) => element.id === eventId );
            event = updatedEvent;
        },
        DELETE_EVENT(state, { scheduleId, eventId }) {
            const schedule = state.allSchedules.find((element) => element.id === scheduleId);
            schedule.event_set.splice(schedule.event_set.findIndex((element) => element.id === eventId), 1);
        },
        DELETE_SCHEDULE(state, scheduleId) {
            state.allSchedules.splice(state.allSchedules.findIndex((element) => element.id === scheduleId), 1);
        },
        CREATE_EVENT(state, { scheduleId, event }) {
            const schedule = state.allSchedules.find((element) => element.id === scheduleId);
            if (!schedule.event_set) {
                schedule.event_set = [];
            }

            schedule.event_set.push(event);
        },
        CREATE_SCHEDULE(state, schedule) {
            state.allSchedules.push(schedule);
        },
        UPDATE_SCHEDULE(state, { schedule, scheduleId }) {
            state.allSchedules[state.allSchedules.findIndex((schedule) => schedule.id === scheduleId)] = schedule;
        },
        CREATE_COMMENT(state, { scheduleId, comment }) {
            const schedule = state.allSchedules.find((element) => element.id === scheduleId);
            if (!schedule.comment_set) {
                schedule.comment_set = [];
            }

            schedule.comment_set.push(comment);
        },
        SET_ALL_SCHEDULES(state, schedules) {
            state.allSchedules = schedules;
        }
    },
    getters: {
        getAllComments(state) {
            return (schedule) => {
                return schedule.comment_set;
            }
        },

        isUIEnabled(state) {
            return state.uiEnabled;
        },

        scheduleByDate(state) {
            return (date) => {
                for (let schedule of state.allSchedules) {
                    const scheduleDate = schedule.date.split('-');
                    if (
                        date.getFullYear() === parseInt(scheduleDate[2]) &&
                        date.getMonth() + 1 === parseInt(scheduleDate[1]) &&
                        date.getDate() === parseInt(scheduleDate[0])
                    ) {
                        return schedule;
                    }
                }
                return null;
            }
        },
        getEventTime(state) {
            return (event) => {
                const startTime = event.start_time.split(':');
                const endTime = event.end_time.split(':');
                return {
                    start: `${startTime[0]}:${startTime[1]}:${startTime[2]}`,
                    end: `${endTime[0]}:${endTime[1]}:${endTime[2]}`,
                }
            }
        },
        getAllEventsBySchedule(state) {
            return (schedule) => {
                return schedule.event_set;
            }
        },
        getAllCategoriesBySchedule(state) {
            return (schedule) => {
                const categories = [];
                const category_names = [];
                for (let event of schedule.event_set) {
                    if (category_names.indexOf(event.category.name) === -1) {
                        categories.push(event.category);
                        category_names.push(event.category.name);
                    }
                }
                return categories;
            }
        },
    },
    actions: {
        startEditingEvent({ commit }) {
            commit('DISABLE_UI');
        },
        async completeEditingEvent({ commit, dispatch }, { eventId, scheduleId, event }) {
            commit('DISABLE_UI');

            await new Promise((resolve, reject) => {
                axios.patch(EDIT_EVENT_URL(scheduleId, eventId), event).then((response => {
                    dispatch('ui/manageNewNotification', { message: 'Event edited!', type: 'success' }, { root: true });
                    commit('EDIT_EVENT', { scheduleId, eventId, updatedEvent: response.data });
                    resolve();
                })).catch((error) => {
                    if (error.response) {
                        dispatch('ui/manageNewNotification', { message: error.response.data, type: 'error' }, { root: true });
                        reject();
                    }
                    else {
                        dispatch('ui/manageNewNotification', { message: 'Unknown error while editing event', type: 'error' }, { root: true });
                        reject();
                    }
                })
            });

            commit('ENABLE_UI');
        },
        cancelEditingEvent({ commit }) {
            commit('ENABLE_UI');
        },
        async createComment({ commit, dispatch }, { scheduleId, commentText }) {
            commit('DISABLE_UI');

            await new  Promise((resolve, reject) => {
                axios.post(CREATE_COMMENT(scheduleId), { comment_text: commentText }).then((response => {
                    dispatch('ui/manageNewNotification', { message: 'Comment created!', type: 'success' }, { root: true });
                    commit('CREATE_COMMENT', { scheduleId, comment: response.data });
                    resolve();
                })).catch((error) => {
                    if (error.response) {
                        dispatch('ui/manageNewNotification', { message: error.response.data, type: 'error' }, { root: true });
                        reject();
                    }
                    else {
                        dispatch('ui/manageNewNotification', { message: 'Unknown error while creating comment', type: 'error' }, { root: true });
                        reject();
                    }
                })
            });

            commit('ENABLE_UI');
        },
        async deleteEvent({ commit, dispatch }, { scheduleId, eventId }) {
            commit('DISABLE_UI');

            await new Promise((resolve, reject) => {
                axios.delete(DELETE_EVENT(scheduleId, eventId)).then((response) => {
                    dispatch('ui/manageNewNotification', { message: 'Event deleted successfully', type: 'success' }, { root: true });
                    commit('DELETE_EVENT', { scheduleId, eventId });
                    resolve();
                }).catch((error) => {
                    if (error.response) {
                        dispatch('ui/manageNewNotification', { message: error.response.data, type: 'error' }, { root: true });
                        reject();
                    }
                    else {
                        dispatch('ui/manageNewNotification', { message: 'Unknown error while deleting event', type: 'error' }, { root: true });
                        reject();
                    }
                });
            })
            commit('ENABLE_UI');
        },
        async deleteSchedule({ commit, dispatch }, scheduleId) {
            commit('DISABLE_UI');

            await new Promise((resolve, reject) => {
                axios.delete(DELETE_SCHEDULE(scheduleId)).then((response) => {
                    dispatch('ui/manageNewNotification', { message: 'Schedule deleted successfully', type: 'success' }, { root: true });
                    commit('DELETE_SCHEDULE', scheduleId);
                    resolve();
                }).catch((error) => {
                    if (error.response) {
                        dispatch('ui/manageNewNotification', { message: error.response.data, type: 'error' }, { root: true });
                        reject();
                    }
                    else {
                        dispatch('ui/manageNewNotification', { message: 'Unknown error while deleting schedule', type: 'error' }, { root: true });
                        reject();
                    }
                });
            });

            commit('ENABLE_UI');
        },
        async createEvent({ commit, dispatch }, { event, scheduleId }) {
            await new Promise((resolve, reject) => {
                axios.post(CREATE_EVENT(scheduleId), event).then((response) => {
                    dispatch('ui/manageNewNotification', { message: 'Event created successfully', type: 'success' }, { root: true });
                    commit('CREATE_EVENT', { scheduleId, event: response.data });
                    resolve();
                }).catch((error) => {
                    console.error(error);
                    if (error.response) {
                        dispatch('ui/manageNewNotification', { message: error.response.data, type: 'error' }, { root: true });
                        reject();
                    }
                    else {
                        dispatch('ui/manageNewNotification', { message: 'Unknown error', type: 'error' }, { root: true });
                        reject();
                    }
                });
            });
        },
        async getAllSchedules({ commit, dispatch }, dates) {
            await new Promise((resolve, reject) => {
                axios.get(SCHEDULES_BY_DATE(dates)).then((response) => {
                    commit('SET_ALL_SCHEDULES', response.data);
                    resolve();
                }).catch((error) => {
                    if (error.response) {
                        dispatch('ui/manageNewNotification', { message: error.response.data, type: 'error' }, { root: true });
                        reject();
                    }
                    else {
                        dispatch('ui/manageNewNotification', { message: 'Unknown error while fetching schedules', type: 'error' }, { root: true });
                        reject();
                    }
                });
            });
        },
        async updateSchedule({ commit, dispatch }, { sharedTo, publicEnabled, scheduleId }) {
            console.log(scheduleId, sharedTo, publicEnabled)
            await new Promise((resolve, reject) => {
                axios.patch(SCHEDULE_URL(scheduleId), { public: publicEnabled, shared_to: sharedTo }).then((response) => {
                    dispatch('ui/manageNewNotification', { message: 'Schedule sharing updated successfully', type: 'success' }, { root: true });
                    commit('UPDATE_SCHEDULE', { scheduleId, schedule: response.data });
                    resolve();
                }).catch((error) => {
                    if (error.response) {
                        dispatch('ui/manageNewNotification', { message: error.response.data, type: 'error' }, { root: true });
                        reject();
                    }
                    else {
                        dispatch('ui/manageNewNotification', { message: 'Unknown error. Please try again later.', type: 'error' }, { root: true });
                        reject();
                    }
                })
            })
        },
        async createSchedule({ commit, dispatch, getters, rootGetters }, schedule) {
            const existingSchedule = getters.scheduleByDate(schedule.date);

            if (!existingSchedule) {
                const dateNumber =(schedule.date.getDate() < 10) ? '0' + schedule.date.getDate() : schedule.date.getDate();
                const monthNumber =((schedule.date.getMonth() + 1) < 10) ? '0' + (schedule.date.getMonth() + 1) : (schedule.date.getMonth() + 1);
                const dateString = `${dateNumber}-${monthNumber}-${schedule.date.getFullYear()}`
                schedule.date = dateString;

                schedule.comment_set = [];
                schedule.event_set = [];

                // TODO:
                schedule.shared_to = [];

                await new Promise((resolve, reject) => {
                    axios.post(SCHEDULE_URL(), {
                        schedule,
                    }).then((response) => {
                        dispatch('ui/manageNewNotification', { message: 'Schedule created successfully', type: 'success' }, { root: true });
                        commit('CREATE_SCHEDULE', response.data);
                        resolve();
                    }).catch((error) => {
                        if (error.response) {
                            dispatch('ui/manageNewNotification', { message: error.response.data, type: 'error' }, { root: true });
                            reject();
                        }
                        else {
                            dispatch('ui/manageNewNotification', { message: 'Unknown error', type: 'error' }, { root: true });
                            reject();
                        }
                    });
                });

            }
        }
    }
}
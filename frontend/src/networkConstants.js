const ENVS = {
    PRODUCTION: 'prod',
    DEVELOPMENT: 'dev',
}

const ENVIRONMENT = ENVS.PRODUCTION;

const HOST = ENVIRONMENT === ENVS.DEVELOPMENT ? 'http://localhost:8000/' : 'http://3.7.175.185/schedulemaker/api/';
export const FRONT_END_URL = ENVIRONMENT === ENVS.DEVELOPMENT ? 'http://localhost:8080/' : 'http://schedule-maker-front-end.s3-website.ap-south-1.amazonaws.com/';

export const SIGN_UP_URL = () => (HOST + 'users/create/');
export const LOGIN_URL = () => (HOST + 'users/login/');
export const SCHEDULE_URL = (scheduleId = null) => (HOST + 'schedule/' + (scheduleId ? `${scheduleId}/` : ''));
export const SCHEDULES_BY_DATE = (dates) => (HOST + 'schedule/dates_list?dates=' + dates.join(','));
export const DELETE_SCHEDULE = (scheduleId) => (HOST + 'schedule/' + scheduleId + '/');
export const CREATE_EVENT = (scheduleId) => (HOST + 'schedule/' + scheduleId + '/events/');
export const DELETE_EVENT = (scheduleId, eventId) => (HOST + 'schedule/' + scheduleId + '/events/' + eventId);
export const CREATE_COMMENT = (scheduleId) => (HOST + 'schedule/' + scheduleId + '/comments/');
export const EDIT_EVENT = (scheduleId, eventId) => (HOST + 'schedule/' + scheduleId + '/events/' + eventId);
export const SCHEDULES_LIST = () => HOST + 'schedule/list/';

export const TESTING_SCHEDULE_URL = FRONT_END_URL + 'schedule/66/';
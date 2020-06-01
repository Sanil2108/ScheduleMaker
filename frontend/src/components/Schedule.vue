<template>
    <div style="margin-bottom: 4vh" class="schedule-container">
        <span v-if="scheduleExists" style="display: block" >
            <span style="display: flex; align-items: center; justify-content: space-between">
                <h1 class="schedule-heading">
                    Schedule for {{ dateTitle }}
                </h1>
                <span>
                    <div
                        :class="{ 'disabled': !uiEnabled }"
                        class="shadow-button"
                        style="float: right; margin-left: 5px"
                        @click="deleteSchedule(schedule.id)"
                    ><span class="material-icons" style="font-size: 2rem; display: block">delete</span></div>
                    <div
                        :class="{ 'disabled': !uiEnabled }"
                        class="shadow-button"
                        style="float: right"
                        @click="shareScheduleDialogOpen = true"
                    ><span class="material-icons" style="font-size: 2rem; display: block">share</span></div>
                </span>
            </span>
            <p class="owner-name" v-if="showOwner">
                by {{ schedule.owner }}
            </p>
            <category-list-view :categories="scheduleCategories" />
            <schedule-graph :categories="scheduleCategories" :schedule="schedule" />
            <event-list :schedule="schedule" v-if="fullSchedule" />
            <comment-list :schedule="schedule" v-if="fullSchedule"> </comment-list>
            <new-comment-card :schedule="schedule" v-if="fullSchedule" />
        </span>
        <span v-else>
            <div class="card empty-card">
                <span style="flex-grow: 1">
                    <h3 class="empty-heading heading-dark">No schedules here.</h3>
                    <div class="shadow-button-container">
                        <v-btn
                            v-show="showCreateScheduleButton"
                            outlined
                            @click="newScheduleDialogOpen = true"
                        >
                            Create one
                        </v-btn>
                    </div>
                </span>
            </div>
        </span>

        <new-schedule-dialog
            :open="newScheduleDialogOpen"
            :onClose="() => { newScheduleDialogOpen = false }"
            data-app
        >
        </new-schedule-dialog>

        <share-schedule-dialog
            v-if="schedule != null"
            :open="shareScheduleDialogOpen"
            :publicEnabled="schedule.public"
            :scheduleId="schedule.id"
            :sharedTo="schedule.shared_to"
            :onClose="() => { shareScheduleDialogOpen = false }"
        > </share-schedule-dialog>
    </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

import CategoryListView from './CategoryListView.vue';
import ScheduleGraph from './ScheduleGraph.vue';
import EventList from './EventList.vue';
import NewScheduleDialog from './NewScheduleDialog.vue';
import CommentList from './CommentList.vue';
import NewCommentCard from './NewCommentCard.vue';
import ScheduleShareDialog from './ScheduleShareDialog.vue';

export default {
    props: {
        schedule: {
            type: Object,
        },
        fullSchedule: {
            type: Boolean,
            default: true,
        },
        showOwner: {
            type: Boolean,
            default: false,
        },
        showCreateScheduleButton: {
            type: Boolean,
            default: true,
        }
    },
    data() {
        return {
            newScheduleDialogOpen: false,
            shareScheduleDialogOpen: false,
        }
    },
    components: {
        'event-list': EventList,
        'schedule-graph': ScheduleGraph,
        'category-list-view': CategoryListView,
        'new-schedule-dialog': NewScheduleDialog,
        'comment-list': CommentList,
        'new-comment-card': NewCommentCard,
        'share-schedule-dialog': ScheduleShareDialog,
    },
    computed: {
        ...mapGetters({
            getScheduleByDate: 'schedule/scheduleByDate',
            getAllCategoriesBySchedule: 'schedule/getAllCategoriesBySchedule',
            getAllEventsBySchedule: 'schedule/getAllEventsBySchedule',
            uiEnabled: 'schedule/isUIEnabled',
        }),
        scheduleExists() {
            return this.schedule !== null;
        },
        scheduleCategories() {
            return this.getAllCategoriesBySchedule(this.schedule);
        },
        dateTitle() {
            const date = this.dateStringToDateObject(this.schedule.date);

            const dayOffset = this.getDayOffset(new Date(), date);
            if (dayOffset === 0) {
                return 'Today';
            }
            else if (dayOffset === 1) {
                return 'Tomorrow';
            }
            else if (dayOffset === -1) {
                return 'Yesterday';
            }
            else {
                return `${this.getDateString(date.getDate())} ${this.getMonthString(date.getMonth())} ${date.getFullYear()}`
            }
        }
    },
    methods: {
        ...mapActions({
            'deleteSchedule': 'schedule/deleteSchedule'
        }),
        getDateString(day) {
            if (day === 1) {
                return `${day}st`;
            }
            else if (day === 2) {
                return `${day}nd`;
            }
            else if (day === 3) {
                return `${day}rd`;
            }
            else {
                return `${day}th`;
            }
        },
        getMonthString(month) {
            const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
            return monthNames[month - 1];
        },
        getDayOffset(firstDate, secondDate) {
            const firstDateClone = new Date(firstDate);
            const secondDateClone = new Date(secondDate);

            firstDateClone.setHours(0);
            firstDateClone.setMinutes(0);
            firstDateClone.setSeconds(0);
            firstDateClone.setMilliseconds(0);

            secondDateClone.setHours(0);
            secondDateClone.setMinutes(0);
            secondDateClone.setSeconds(0);
            secondDateClone.setMilliseconds(0);

            const oneDay = 24 * 60 * 60 * 1000; // hours * minutes * seconds * milliseconds
            const diffDays = Math.round((secondDate - firstDate) / oneDay);

            return diffDays;
        },
        dateStringToDateObject(dateString) {
            const dmy = dateString.split('-');
            const date = new Date();

            date.setDate(parseInt(dmy[0]));
            date.setMonth(parseInt(dmy[1]) - 1);
            date.setFullYear(parseInt(dmy[2]));

            return date;
        }
    },
    mounted() {
    }

}
</script>

<style lang="scss" scoped>
.owner-name {
    z-index: 100;
    color: white;
    margin: 0px 10px 5px;
    position: relative;
}

.empty-heading {
    margin-bottom: 10px;
    left: 50%;
    display: inline-block;
    text-align: center;
    align-self: center;
    transform: translateX(-50%);
}

.empty-card {
    height: 30vh;
    display: inline-flex;
    align-items: center;
}

.shadow-button--empty {
    color: #444;
    /* display: inline-block; */
    position: relative;

    &::after {
        border-radius: 0px !important;
        transition: all 0.4s;
        background: #e9e9e966 !important;
        position: absolute !important;
        height: 0px;
        width: 0px;
    }
}

.shadow-button-container {
    text-align: center;
}

.schedule-heading {
    display: inline-block;
}

</style>
<style>
.schedule-container .v-dialog__container {
    display: unset; 
}
</style>

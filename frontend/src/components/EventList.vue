<template>
    <div>
        <div class="events-heading-container">
            <span style="display: flex; align-items: center">
                <h2 class="events-heading">Events</h2>
                <div
                    :class="{ 'disabled': !uiEnabled }"
                    class="shadow-button"
                    style="margin-left: 5px"
                    @click="newEventDialogOpen = true"
                ><span class="material-icons" style="font-size: 2rem; display: block">add</span></div>
            </span>
            <div style="flex-grow:1" />
            <div class="sort-buttons-bar">
                <div @click="sortEventsByCategory" :class="{ 'button-enabled': currentSort == SORTED_BY_CATEGORY }">Category</div>
                <div @click="sortEventsByTime" :class="{ 'button-enabled': currentSort == SORTED_BY_TIME }">Time</div>
                <div @click="sortEventsByDuration" :class="{ 'button-enabled': currentSort == SORTED_BY_DURATION }">Duration</div>
            </div>
        </div>
        <transition-group name="flip-list">
            <event-card :schedule="schedule" v-for="event in localEvents" :key="event.id" :event="event" />
        </transition-group>

        <new-event-dialog :open="newEventDialogOpen" :schedule="schedule" :onClose="() => { newEventDialogOpen = false }" />
    </div>
</template>

<script>
import { mapGetters } from 'vuex';

import EventCard from './EventCard.vue';
import NewEventDialog from './NewEventDialog.vue';

export default {
    props: ['schedule'],
    data() {
        return {
            SORTED_BY_CATEGORY: 'sort_category',
            SORTED_BY_TIME: 'sort_time',
            SORTED_BY_DURATION: 'sort_duration',
            currentSort: 'sort_category',
            newEventDialogOpen: false,
            localEventsData: [],
        }
    },
    computed: {
        ...mapGetters({
            uiEnabled: 'schedule/isUIEnabled',
            getAllEventsBySchedule: 'schedule/getAllEventsBySchedule',
        }),
        scheduleEvents() {
            return this.getAllEventsBySchedule(this.schedule);
        },
        localEvents: {
            get() {
                if (this.localEventsData.length === this.scheduleEvents.length) {
                    return this.localEventsData
                }
                else {
                    this.localEvents = this.scheduleEvents
                    return this.scheduleEvents
                }
            },
            set(newValue) {
                this.localEventsData = newValue;
            }
        }
    },
    components: {
        'event-card': EventCard,
        'new-event-dialog': NewEventDialog,
    },
    methods: {
        sortEventsByTime() {
            this.localEvents.sort((a, b) => {
                const aTimeArray = a.start_time.split(':');
                const aTime = (parseInt(aTimeArray[0]) * 60 * 60) + (parseInt(aTimeArray[1]) * 60) + parseInt(aTimeArray[2]);

                const bTimeArray = b.start_time.split(':');
                const bTime = (parseInt(bTimeArray[0]) * 60 * 60) + (parseInt(bTimeArray[1]) * 60) + parseInt(bTimeArray[2]);

                return aTime - bTime;
            });

            this.currentSort = this.SORTED_BY_TIME;
        },
        sortEventsByDuration() {
            this.localEvents.sort((a, b) => {
                const aTimeStartArray = a.start_time.split(':');
                const aTimeEndArray = a.end_time.split(':');
                const aDuration = (parseInt(aTimeStartArray[0] - aTimeEndArray[0]) * 60 * 60) +
                (parseInt(aTimeStartArray[1] - aTimeEndArray[1]) * 60) + parseInt(aTimeStartArray[2] - aTimeEndArray[2]);

                const bTimeStartArray = b.start_time.split(':');
                const bTimeEndArray = b.end_time.split(':');
                const bDuration = (parseInt(bTimeStartArray[0] - bTimeEndArray[0]) * 60 * 60) +
                (parseInt(bTimeStartArray[1] - bTimeEndArray[1]) * 60) + parseInt(bTimeStartArray[2] - bTimeEndArray[2]);

                return aDuration - bDuration;
            });

            this.currentSort = this.SORTED_BY_DURATION;
        },
        sortEventsByCategory() {
            this.localEvents.sort((a, b) => {
                return a.category.name.charCodeAt(0) - b.category.name.charCodeAt(0);
            });

            this.currentSort = this.SORTED_BY_CATEGORY;
        }
    }
}
</script>
<style lang="scss" scoped>
.events-heading {
    display: inline-block;
}

.events-heading-container {
    display: flex;
}

.sort-buttons-bar {
    display: inline-flex;
    align-items: center;

    * {
        background: white;
        padding: 5px 15px;
        cursor: pointer;
        border-radius: 30px;
        margin: 4px;
        color: #424242;
        position: relative;
        box-shadow: 0px 3px 5px 2px #00000099;
        transition: all 0.5s;
    }

    *:not(.button-enabled):hover {
        box-shadow: 0px 5px 5px 3.5px #00000099;
        transform: translateY(-2px);
    }
}

.button-enabled {
    // box-shadow: inset 0px 3px 5px 2px #00000099;
    box-shadow: 0px 0px 0px 0px #00000099;
    background: #ddd;
}

.button-disabled {
}

.flip-list-move {
    transition: transform 0.5s;
}

</style>

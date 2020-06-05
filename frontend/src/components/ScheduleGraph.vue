<template>
    <div>
        <div class="card" style="margin-top: 1vh; height: 50vh" ref="parent-card">
            <perfect-scrollbar ref="timeFramesContainer">
                <div class="time-frame" v-for="label in timeFrameLabels" :key="label">
                    <div class="time-frame--label"> {{ label }} </div>
                </div>
                <div class="events_container">
                        <div
                            class="events_container--category"
                            v-for="(category, key) in categories"
                            :key="key"
                        >
                            <div
                                class="events_container--event card"
                                v-for="(event, key) in eventsElementAttributes[category.name]"
                                :key="key"
                                :style="{ left: event.left, width: event.width, backgroundColor: event.backgroundColor }"
                            >
                                <h4> {{ event.title }} </h4>
                            </div>
                        </div>
                </div>
            </perfect-scrollbar>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { PerfectScrollbar } from 'vue2-perfect-scrollbar'

export default {
    components: {
        'perfect-scrollbar': PerfectScrollbar
    },
    props: ['categories', 'schedule'],
    computed: {
        ...mapGetters({
            getEventTime: 'schedule/getEventTime',
            getAllEventsBySchedule: 'schedule/getAllEventsBySchedule',
        }),
        events() {
            return this.getAllEventsBySchedule(this.schedule);
        },
        eventsElementAttributes() {
            const eventElements = {};
            for (let i = 0; i < this.categories.length; i += 1) {
                eventElements[this.categories[i].name] = [];
            }

            for (let i = 0; i < this.events.length; i += 1) {
                const eventTime = this.getEventTime(this.events[i]);

                const eventStart = this.getTimeInHours(eventTime.start);
                const eventEnd = this.getTimeInHours(eventTime.end);

                eventElements[this.events[i].category.name].push({
                    title: this.events[i].title,
                    left: `${(eventStart / 24) * this.timeFramesContainerWidth }px`,
                    width: `${((eventEnd - eventStart) / 24) * this.timeFramesContainerWidth }px`,
                    backgroundColor: `${this.events[i].category.color}`,
                });
            }

            return eventElements;
        },
        timeFrameLabels() {
            const labels = [...Array(25).keys()];
            for (let i = 0; i < labels.length; i += 1) {
                labels[i] = ((labels[i] > 12) ? labels[i] - 12 : labels[i]) + " " + ((labels[i] > 12) ? "PM" : "AM");
            }
            return labels;
        },
        // timeFramesContainerWidth() {
        //     try {
        //         return 
        //     } catch {
        //         return 10;
        //     }
        // },
    },
    data() {
        return {
            timeFramesContainerWidth: 10
        }
    },
    mounted() {
        this.timeFramesContainerWidth =
            this.$refs.timeFramesContainer.$el.scrollWidth;

        this.$refs['parent-card'].addEventListener('mousewheel', (event) => {
            this.$refs.timeFramesContainer.$el.scrollLeft += event.deltaY;
            event.preventDefault();
        });
    },
    methods: {
        getTimeInHours(timeString) {
            const hms = timeString.split(':');
            return parseInt(hms[0]) + (hms[1] / 60) + (hms[2] / (60 * 60));
        }
    }
}
</script>

<style src="vue2-perfect-scrollbar/dist/vue2-perfect-scrollbar.css" />
<style lang="scss" scoped>
$TIME_FRAME_WIDTH: 50px;
$EVENTS_CONTAINER_HEIGHT: 60px;

h4 {
    white-space: pre-line;
    padding: 10px;
    text-overflow: ellipsis;
    white-space: nowrap;
    overflow: hidden;
    height: 80%;
    width: 100%;
}

.card {
    white-space: pre;
    box-shadow: 0px 0px 6px 3px #00000030;
    overflow: hidden;
}

.events_container {
    position: absolute;
    top: 0px;
    width: 100%;

    &--category {
        height: $EVENTS_CONTAINER_HEIGHT;
        width: 100%;
        position: relative;
        margin: 14px;
    }

    &--event {
        position: absolute;
        display: inline-block;
        height: 100%;
        border-radius: 10px;
        transition: all 0.4s;
        cursor: default;

        &:hover {
            min-width: fit-content !important;
            transform: scale(1.1);;
        }

        p {

        }
    }
}

.time-frame {
    height: 99%;
    opacity: 0.7;
    border-right: 1px solid #666666;
    display: inline-block;
    width: $TIME_FRAME_WIDTH;
    text-align: center;

    &--label {
        transform: translate(25px, -100%);
        top: 98%;
        position: relative;
        font-size: 0.8rem;
        background: white;
    }
}

.ps {
    height: 100%;
    border-radius: 20px;
}

</style>

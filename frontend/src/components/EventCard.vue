<template>
<div class="event-card-container" style="position: relative">
    <div
        class="card event-card"
        :style="{ backgroundColor }"
        :class="{ 'card--loading': loadingState }"
    >
        <h3> {{ event.title }} </h3>
        <div class="description-container">
            <p v-if="!editing" class="description"> {{ event.description }} </p>
            <v-textarea v-else
                :auto-grow="true"
                :autofocus="true"
                v-model="editingEvent.description"
                color="#ffffff"
                counter="100"
                placeholder="Description"
                ref="descriptionEditField"
                :error="descriptionTextFieldErred"
            >
            </v-textarea>
        </div>
        <div style="display: flex">
            <span class="material-icons">alarm</span>
            <span v-if="!editing">
                <p style="margin-left: 5px"> {{ eventTime.start }} - {{ eventTime.end }} </p>
            </span>
            <span v-else>
                <div
                    :class="{ 'highlighted': startTimePickerVisible, 'disabled': endTimePickerVisible }"
                    class="shadow-button shadow-button--text"
                    @click="toggleStartTimePickerVisible"
                > {{ eventTime.start }} </div> - 
                <div
                    :class="{ 'highlighted': endTimePickerVisible, 'disabled': startTimePickerVisible }"
                    class="shadow-button shadow-button--text"
                    @click="toggleEndTimePickerVisible"
                > {{ eventTime.end }} </div>
                <!-- <transition name="fadeAndSlide"> -->
                <v-time-picker
                    :header-color="event.category.color"
                    v-show="startTimePickerVisible"
                    v-model="editingEvent.start_time"
                ></v-time-picker>
                <!-- </transition> -->
                <!-- <transition name="fade"> -->
                    <v-time-picker :header-color="event.category.color" v-show="endTimePickerVisible" v-model="editingEvent.end_time"></v-time-picker>
                <!-- </transition> -->
            </span>
        </div>
        <div class="buttons-bar">
            <transition name="fade">
                <div
                    v-show="editing"
                    class="shadow-button"
                    @click="completeEditEvent"
                    :class="{ 'disabled': !editingEventValid }"
                ><span class="material-icons">check</span></div>
            </transition>
            <transition name="fade">
                <div v-show="editing" class="shadow-button" @click="cancelEditEvent"><span class="material-icons">close</span></div>
            </transition>
            <div :class="{ 'disabled': !uiEnabled }" class="shadow-button" @click="editEvent"><span class="material-icons">edit</span></div>
            <div :class="{ 'disabled': !uiEnabled }" class="shadow-button" @click="deleteEvent"><span class="material-icons">delete</span></div>
            <!-- <button-with-text text="Delete" icon="" /> -->
        </div>
    </div>
    <div class="loading-text" v-show="loadingState">
        <span class="material-icons">{{ currentStateIcon }}</span>
        <h3>{{ currentStateText }}</h3>
    </div>
</div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
    props: ['event', 'schedule'],
    data() {
        return {
            deleting: false,
            editing: false,
            updating: false,
            editingEvent: {
                description: '',
                start_time: undefined,
                end_time: undefined,
            },
            startTimePickerVisible: false,
            endTimePickerVisible: false,
        }
    },
    computed: {
        ...mapGetters({
            getEventTime: 'schedule/getEventTime',
            uiEnabled: 'schedule/isUIEnabled',
        }),
        eventTime() {
            const time24Hour = this.getEventTime(this.event);

            return {
                start: this.convert24HourTo12Hour(time24Hour.start),
                end: this.convert24HourTo12Hour(time24Hour.end),
            }
        },
        backgroundColor() {
            return this.event.category.color;
        },
        loadingState() {
            return this.deleting || this.updating;
        },
        currentStateIcon() {
            if (this.deleting) {
                return "delete";
            }
            else if (this.updating) {
                return "edit";
            }
        },
        currentStateText() {
            if (this.deleting) {
                return "Deleting";
            }
            else if (this.updating) {
                return "Editing";
            }
        },

        descriptionTextFieldErred() {
            return !this.editingEvent.description || this.editingEvent.description.length > 100;
        },
        editingEventValid() {
            return !this.descriptionTextFieldErred;
        }

    },
    methods: {
        convert24HourTo12Hour(time) {
            const hours = parseInt(time.split(':')[0]);
            let timeString = `${(hours > 12) ? hours - 12 : hours}:${time.split(':')[1]} `;
            if (hours >= 12) {
                timeString += 'PM';
            }
            else {
                timeString += 'AM';
            }
            return timeString;
        },

        ...mapActions({
            startEditingEventAction: 'schedule/startEditingEvent',
            cancelEditingEventAction: 'schedule/cancelEditingEvent',
            completeEditingEventAction: 'schedule/completeEditingEvent',
            deleteEventAction: 'schedule/deleteEvent',
        }),
        deleteEvent() {
            this.deleting = true;

            this.deleteEventAction({ eventId: this.event.id, scheduleId: this.schedule.id })
        },
        editEvent() {
            this.editing = true;

            this.editingEvent.description = this.event.description;

            this.startEditingEventAction();
        },
        async completeEditEvent() {
            this.editing = false;
            this.updating = true;

            await this.completeEditingEventAction({
                scheduleId: this.schedule.id,
                eventId: this.event.id,
                event: this.editingEvent,
            });

            this.updating = false;
        },
        cancelEditEvent() {
            this.editing = false;

            this.cancelEditingEventAction();
        },
        toggleStartTimePickerVisible() {
            if (!this.endTimePickerVisible) {
                this.startTimePickerVisible = !this.startTimePickerVisible;
            }

            if (this.startTimePickerVisible) {
                document.addEventListener('keydown', (event) => {
                    if (event.key === 'Escape') {
                        this.toggleStartTimePickerVisible();
                    }
                }, { once: true });
            }
        },
        toggleEndTimePickerVisible() {
            if (!this.startTimePickerVisible) {
                this.endTimePickerVisible = !this.endTimePickerVisible;
            }

            if (this.startTimePickerVisible) {
                document.addEventListener('keydown', (event) => {
                    if (event.key === 'Escape') {
                        this.toggleStartTimePickerVisible();
                    }
                }, { once: true });
            }
        }
    }
}
</script>

<style lang="scss" scoped>
.event-card {
    border-radius: 6px;
    margin-bottom: 20px;
    padding: 15px;
    color: white;
}

.event-card div.description-container {
    margin: 3px;
    width: 70%;
    min-height: 60px;
    display: block;
}

.loading-text {
    position: absolute;
    display: block;
    top: 50%;
    left: 50%;
    text-align: center;
    transform: translate(-50%, -50%);

    * {
        display: block;
        color: #fff;
    }

    span {
        font-size: 2.5rem;
        margin-bottom: 10px;
    }
}

.buttons-bar {
    position: absolute;
    top: 0px;
    right: 0px;
    margin: 10px;

    * {
        display: inline-block;
    }

    .material-icons {
        font-size: 2rem !important;
        display: block;
    }
}

p {
    font-size: 1.3rem;
    display: inline-block;
}

.material-icons {
    font-size: 1.5rem;
}

</style>

<style>
.event-card-container .v-input {
    padding: 0px !important;
}

.event-card-container textarea {
    color: white !important;
    font-size: 1.3rem !important;
    line-height: normal !important;
    height: auto;
}

.event-card-container .v-counter {
    color: white !important;
}

.event-card-container .v-input__slot::before {
    color: white !important;
    background-color: white !important;
}

.event-card-container .v-picker {
    position: absolute !important;
    z-index: 1000;
    border: 1px solid white !important;
    box-shadow: 0px 0px 6px 4px #00000033 !important;
}
</style>

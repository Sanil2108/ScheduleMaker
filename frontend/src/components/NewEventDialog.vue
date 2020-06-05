<template>
     <v-dialog
        v-model="open"
        max-width="600"
        persistent
    >
        <v-card>
            <v-card-title class="headline">Create a new event</v-card-title>
            
            <div class="form-container new-event-dialog-form">
                <v-form v-model="formValid">
                    
                    <div class="form-container__row">
                        <v-text-field
                            v-model="event.title"
                            label="Title"
                            :rules="[rules.required]"
                        ></v-text-field>
                    </div>

                    <div class="form-container__row">
                        <v-text-field
                            v-model="event.description"
                            label="Description"
                        ></v-text-field>
                    </div>

                    <div class="form-container__row">
                        <v-combobox
                            :items="allCategories"
                            color="white"
                            :search-input.sync="event.category.name"
                            hide-no-data
                            hide-selected
                            label="Category"
                            return-object
                            :rules="[rules.required]"
                        ></v-combobox>
                    </div>

                    <div class="form-container__row">
                        <span class="form-container__row__label">
                            Start time
                        </span>
                        <span style="position: absolute; right: 40px">
                            <div class="form-container__row__data-item">
                                <v-text-field
                                    v-model="startTime.hours"
                                    label="Hours"
                                    placeholder="HH"
                                    :rules="[rules.required, rules.hourValue]"
                                ></v-text-field>
                            </div>
                            <div class="form-container__row__data-item">
                                <v-text-field
                                    v-model="startTime.minutes"
                                    :rules="[rules.required, rules.minuteValue]"
                                    label="Minutes"
                                    placeholder="MM"
                                ></v-text-field>
                            </div>
                            <div class="form-container__row__data-item">
                                <v-select
                                    v-model="startTime.meridian"
                                    :items="['AM', 'PM']"
                                    :rules="[rules.required]"
                                ></v-select>
                            </div>
                        </span>
                    </div>

                    <div class="form-container__row">
                        <span class="form-container__row__label">
                            End time
                        </span>
                        <span style="position: absolute; right: 40px">
                            <div class="form-container__row__data-item">
                                <v-text-field
                                    v-model="endTime.hours"
                                    label="Hours"
                                    placeholder="HH"
                                    :rules="[rules.required, rules.hourValue]"
                                ></v-text-field>
                            </div>
                            <div class="form-container__row__data-item">
                                <v-text-field
                                    v-model="endTime.minutes"
                                    :rules="[rules.required, rules.minuteValue]"
                                    label="Minutes"
                                    placeholder="MM"
                                ></v-text-field>
                            </div>
                            <div class="form-container__row__data-item">
                                <v-select
                                    v-model="endTime.meridian"
                                    :items="['AM', 'PM']"
                                    :rules="[rules.required]"
                                ></v-select>
                            </div>
                        </span>
                    </div>
                </v-form>
            </div>

            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                    :text="true"
                    color=""
                    @click="onClose"
                >
                    Cancel
                </v-btn>

                <v-btn
                    :text="true"
                    color=""
                    :disabled="!formValid"
                    @click="onClickComplete"
                >
                    Complete!
                </v-btn>
            </v-card-actions>

        </v-card>
    </v-dialog>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
export default {
    props: ['open', 'onClose', 'schedule'],
    data() {
        return {
            startTimePickerVisible: false,
            endTimePickerVisible: false,
            event: {
                title: '',
                description: '',
                start_time: '',
                end_time: '',
                category: {
                    name: '',
                },
            },
            startTime: {
                hours: '',
                minutes: '',
                meridian: '',
            },
            endTime: {
                hours: '',
                minutes: '',
                meridian: '',
            },
            formValid: false,
            rules: {
                required: value => (value && value.length !== 0) ? true : 'Required',
                hourValue: value => {
                    if (!(parseInt(value) <= 12 && parseInt(value) >= 0 && value === parseFloat(value).toFixed(0))) {
                        return 'Invalid format';
                    }
                    return true;
                },
                minuteValue: value => {
                    if(!(parseInt(value) <= 59 && parseInt(value) >= 0 && value === parseFloat(value).toFixed(0))) {
                        return 'Invalid format';
                    }
                    return true;
                }
            }
        };
    },
    computed: {
        ...mapGetters({
            'getAllCategoriesBySchedule': 'schedule/getAllCategoriesBySchedule',
        }),
        allCategories() {
            return this.getAllCategoriesBySchedule(this.schedule).map((category) => category.name);
        },
    },
    methods: {
        ...mapActions({
            'createEvent': 'schedule/createEvent',
            'manageNewNotification': 'ui/manageNewNotification',
        }),
        endTimeAfterStartTime() {
            if (this.endTime.meridian === this.startTime.meridian) {
                if (this.endTime.hours === this.startTime.hours) {
                    return (parseInt(this.endTime.minutes) > parseInt(this.startTime.minutes));
                }
                else {
                    if (parseInt(this.endTime.hours) > parseInt(this.startTime.hours) ||
                        this.startTime.hours == 12) {
                        return true;
                    }
                    return false;
                }
            }
            else {
                return this.endTime.meridian === 'PM';
            }
        },
        setCategory(category) {
            this.event.category = category;
        },
        hideAllTimePickers() {
            this.startTimePickerVisible = false;
            this.endTimePickerVisible = false;
        },
        showStartTimePicker() {
            this.startTimePickerVisible = true;
            document.addEventListener('keydown', (event) => {
                if (event.key === 'Escape') {
                    this.hideAllTimePickers();
                }
            }, { once: true });
        },
        showEndTimePicker() {
            this.endTimePickerVisible = true;
            document.addEventListener('keydown', (event) => {
                if (event.key === 'Escape') {
                    this.hideAllTimePickers();
                }
            }, { once: true });
        },
        onClickComplete() {
            if (!this.endTimeAfterStartTime()) {
                this.manageNewNotification({ message: 'End time must be after start time', type: 'error' })
                return;
            }

            const startTimeHours = parseInt(this.startTime.hours) + ((this.startTime.meridian === 'PM' && parseInt(this.startTime.hours) < 12) ? 12 : 0);
            this.event.start_time = `${(startTimeHours < 10) ? '0' + startTimeHours : startTimeHours}:${(this.startTime.minutes < 10) ? '0' + this.startTime.minutes : this.startTime.minutes}`

            const endTimeHours = parseInt(this.endTime.hours) + ((this.endTime.meridian === 'PM' && parseInt(this.endTime.hours) < 12) ? 12 : 0);
            this.event.end_time = `${(endTimeHours < 10) ? '0' + endTimeHours : endTimeHours}:${(this.endTime.minutes < 10) ? '0' + this.endTime.minutes : this.endTime.minutes}`

            this.createEvent({ event: this.event, scheduleId: this.schedule.id });

            this.reset();
            this.onClose();
        },
        reset() {
            this.event= {
                title: '',
                description: '',
                start_time: '',
                end_time: '',
                category: {
                    name: '',
                },
            }
            this.startTime = {
                hours: '',
                minutes: '',
                meridian: '',
            }
            this.endTime = {
                hours: '',
                minutes: '',
                meridian: '',
            };
        }
    }
}
</script>

<style lang="scss" scoped>
.shadow-button--text {
    color: black;
}

.close-timer-icon {
    position: fixed;
    top: 10px;
    right: 10px;
    font-size: 2rem;
    display: block;
    width: auto;
    background: white;
    padding: 5px;
    cursor: pointer;
    border-radius: 30px;
    margin: 4px;
    color: #424242;
    box-shadow: 0px 3px 5px 2px #00000099;
    transition: all 0.5s;

    &:not(.button-enabled):hover {
        box-shadow: 0px 5px 5px 3.5px #00000099;
        transform: translateY(-2px);
    }
}


.form-container {
    margin: 20px 40px 10px;

    &__row {
        display: flex;
        align-items: center;
        height: 60px;
        

        &__label {
            display: inline-flex;
            align-items: center;

            .material-icons {
                margin-left: 3px;
                cursor: pointer;
                color: #00000077;
            }
        }

        &__data-item {
            display: inline-block;
        }
    }
}
</style>

<style>

.new-event-dialog-form .v-input {
    margin-right: 4px;
    width: 80px !important;
}

.new-event-dialog-form .v-messages__message {
    color: #f44336 !important;
}

.new-event-dialog-form .v-dialog {
    overflow: hidden !important;
    max-width: 25vw !important;
}
</style>
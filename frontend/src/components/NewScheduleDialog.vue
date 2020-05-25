<template>
     <v-dialog
        v-model="open"
        max-width="290"
        persistent
    >
        <v-card>
            <v-card-title class="headline">Create a new schedule</v-card-title>

            <div class="form-container new-schedule-dialog-form">
                <v-overflow-btn
                    auto-select-first
                    label="Select day"
                    class="my-2"
                    v-model="selectedDayTitle"
                    :items="dayTitles"
                    target="#dropdown-example"
                ></v-overflow-btn>

                <div class="form-container__row">
                    <span class="form-container__row__label">
                        Public
                        <v-tooltip top>
                            <template v-slot:activator="{ on }">
                                <span class="material-icons" v-on="on"> info </span>
                            </template>
                            <span>You schedule will be accessible by anyone who has a link to it</span>
                        </v-tooltip>
                    </span>
                    <div class="form-container__row__data-item">
                        <el-switch
                            v-model="publicEnabled"
                            active-color="#13ce66"
                            inactive-color="#ff4949">
                        </el-switch>
                    </div>
                </div>
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
                    @click="onClickComplete"
                >
                    Complete!
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
import { mapActions } from 'vuex';

export default {
    props: ['open', 'onClose'],
    data() {
        const tomorrow = new Date();
        const dayAfterTomorrow = new Date();

        tomorrow.setDate((new Date()).getDate() + 1);
        dayAfterTomorrow.setDate((new Date()).getDate() + 2);

        return {
            publicEnabled: true,
            shared_to: [],
            selectedDayTitle: 'Today',
            days: [
                {
                    title: 'Today',
                    date: new Date(),
                },
                {
                    title: 'Tomorrow',
                    date: tomorrow,
                },
                {
                    title: 'Day after tomorrow',
                    date: dayAfterTomorrow,
                }
            ]
        }
    },
    computed: {
        date() {
            return this.days.find((element) => { return element.title === this.selectedDayTitle });
        },
        dayTitles() {
            return this.days.map((day) => { return day.title; })
        }
    },
    methods: {
        ...mapActions({
            'createSchedule': 'schedule/createSchedule',
        }),
        onClickComplete() {
            const schedule = {
                date: this.days[this.dayTitles.indexOf(this.selectedDayTitle)].date,
                publicEnabled: this.publicEnabled,
            }

            this.createSchedule(schedule);

            // TODO: Dispatch an action to send an API request

            // TODO: Wait for the action to complete.
            // If failed or complete, show a notification

            this.onClose();
        },
        selectDay(day) {
            this.selectedDayTitle = day.title;
        }
    }
}
</script>

<style lang="scss" scoped>
.form-container {
    margin: 20px 40px 10px;

    &__row {
        display: inline-flex;
        align-items: center;
        

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
            position: absolute;
            right: 40px;
        }
    }
}

</style>
<style>

.new-schedule-dialog-form .v-dialog {
    max-width: 25vw !important;
}

/* .new-schedule-dialog-form .v-select__selections,
.new-schedule-dialog-form .v-label {
    padding-left: 16px !important;
}

.new-schedule-dialog-form .v-input__slot {
    margin: 0px;
}

.new-schedule-dialog-form .v-input {
    margin: 0px;
    padding: 0px;
}

.new-schedule-dialog-form .theme--light.v-messages {
    display: none;
} */

</style>

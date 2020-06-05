<template>
     <v-dialog
        v-model="open"
        max-width="550"
        persistent
    >
        <v-card>
            <v-card-title class="headline">Sharing</v-card-title>

            <div class="form-container share-schedule-dialog-form">
                <span class="schedule-link-container">
                    <p style="color: #444444; display: inline-block; margin-bottom: 4px"> Link </p>
                    <button class="copy-link-button"> Copy </button>
                    <v-text-field filled :disabled="true" style="cursor: pointer" :value="scheduleURL">" </v-text-field>
                </span>

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
                            v-model="localPublic"
                            active-color="#13ce66"
                            inactive-color="#ff4949">
                        </el-switch>
                    </div>
                </div>

                <div class="form-container__row" v-show="!localPublic">
                    <span class="form-container__row__label">
                        <v-form v-model="emailValid" style="width: 100%">
                            <v-text-field
                                icon
                                v-model="currentEmail"
                                label="Email address"
                                :rules="[rules.emailValidation, rules.noRepeat]"
                            >
                            </v-text-field>
                        </v-form>
                    </span>
                    <div class="form-container__row__data-item">
                        <v-btn
                            :text="true"
                            :disabled="!emailValid"
                            color=""
                            @click="addEmail"
                        >Add</v-btn>
                    </div>
                </div>

                <div style="margin-top: 6px" v-show="!localPublic">
                    <p class="email-chip" v-for="(email) in localSharedTo" :key="email" @click="removeEmail(email)">
                        {{ email }}
                    </p>
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
                    Update!
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
import { mapActions } from 'vuex';
import * as ClipboardJS from 'clipboard';
import {
    FRONT_END_URL
} from '../networkConstants';

const EMAIL_REGEX = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

export default {
    props: ['open', 'publicEnabled', 'sharedTo', 'scheduleId', 'onClose'],
    data() {
        return {
            localPublic: this.publicEnabled,
            localSharedTo: this.sharedTo,
            currentEmail: '',
            emailValid: false,
            rules: {
                emailValidation: value => (EMAIL_REGEX.test(String(value)) ? true : 'Email is not valid'),
                noRepeat: value => (value in this.localSharedTo) ? 'Already added' : true,
            },
            clipboard: null,
        }
    },
    computed: {
        scheduleURL() {
            return `${FRONT_END_URL}schedule/${this.scheduleId}/`;
        }
    },
    mounted() {
        this.$nextTick(() => {
            this.clipboard = new ClipboardJS('.copy-link-button', {
                text: function(trigger) {
                    return scheduleURL;
                }
            });
        })
    },
    beforeDestroy() {
        this.clipboard.destroy();
    },
    methods: {
        ...mapActions({
            'updateSchedule': 'schedule/updateSchedule',
        }),
        onClickComplete() {
            this.updateSchedule({ sharedTo: this.localSharedTo, publicEnabled: this.localPublic, scheduleId: this.scheduleId });

            this.onClose();
        },
        selectDay(day) {
            this.selectedDayTitle = day.title;
        },
        addEmail() {
            this.localSharedTo.push(this.currentEmail);
            this.currentEmail = '';
        },
        removeEmail(email) {
            this.localSharedTo.splice(this.localSharedTo.indexOf(email), 1);
        }
    }
}
</script>

<style lang="scss" scoped>
.copy-link-button {
    font-size: 0.8rem;
    cursor: pointer;
    display: inline-block;
    color: #444444;
    text-decoration: underline;
    float: right;
}

.email-chip {
    padding: 10px 20px;
    background: #444444dd;
    border-radius: 30px;
    margin: 4px;
    color: white;
    display: inline-block;
    cursor: pointer;
    position: relative;

    &::after {
        transition: all 0.15s;
        position: absolute;
        top: 50%;
        left: 50%;
        height: 0px;
        width: 0px;
        transform: translate(-50%, -50%);
        background: #f44336;
        content: '';
        display: inline-flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        border-radius: 30px;
        position: absolute;
        font-size: 1.5rem;
    }

    &:hover::after {
        content: '❌';
        height: 100%;
        width: 100%;
    }
}

.form-container {
    margin: 20px 40px 10px;

    &__row {
        margin-bottom: 5px;
        display: flex;
        width: 100%;
        align-items: center;

        &__label {
            display: inline-flex;
            align-items: center;
            width: 100%;

            .material-icons {
                margin-left: 3px;
                cursor: pointer;
                color: #00000077;
            }
        }

        &__data-item {
            display: inline-block;
            right: 40px;
        }
    }
}

</style>
<style>

.share-schedule-dialog-form .v-dialog {
    max-width: 25vw !important;
}

/* .share-schedule-dialog-form .v-select__selections,
.share-schedule-dialog-form .v-label {
    padding-left: 16px !important;
}

.share-schedule-dialog-form .v-input__slot {
    margin: 0px;
}

.share-schedule-dialog-form .v-input {
    margin: 0px;
    padding: 0px;
}

.share-schedule-dialog-form .theme--light.v-messages {
    display: none;
} */

</style>

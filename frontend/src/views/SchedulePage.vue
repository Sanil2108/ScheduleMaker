<template>
    <div class="root-card schedule-page-container">
        <schedule
            v-if="!scheduleLoading && currentSchedule != null"
            :schedule="currentSchedule"
            :showOwner="true"
        >
        </schedule>
        <v-progress-circular
            v-else
            :indeterminate="true"
            :size="64"
            :width="8"
            color="#ffffffaa"
        ></v-progress-circular>
    </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

import Schedule from '../components/Schedule.vue';
import { SCHEDULE_URL } from '../networkConstants';
import * as axios from 'axios';

export default {
    name: 'SchedulePage',
    components: {
        'schedule': Schedule,
    },
    data() {
        return {
            scheduleLoading: false,
            currentSchedule: null
        }
    },
    mounted() {
        this.loadSchedule();
    },
    methods: {
        ...mapActions({
            'manageNewNotification': 'ui/manageNewNotification',
        }),
        loadSchedule() {
            this.scheduleLoading = true;
            axios.get(SCHEDULE_URL(this.$route.params.scheduleId)).then((response) => {
                this.currentSchedule = response.data;
                this.scheduleLoading = false;
            }).catch((error) => {
                if (error.response) {
                    this.manageNewNotification({ message: error.response.data, type: 'error' });
                }
                else {
                    this.manageNewNotification({ message: 'Unknown error while retrieving schedule', type: 'error' });
                }
                this.scheduleLoading = false;
            })
        }
    }
}
</script>

<style lang="scss" scoped>
</style>
<style>
.schedule-page-container .v-progress-circular {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
</style>

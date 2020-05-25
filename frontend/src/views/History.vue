<template>
    <div class="history-page root-card">
        <v-tabs
            v-model="tab"
            background-color="transparent"
            class="elevation-2">
            <v-tabs-slider></v-tabs-slider>

            <v-tab
                v-for="(tabName, index) in tabNames"
                :key="index"
                :href="`#tab-${index}`"
            >
                {{ tabName }}
            </v-tab>

            <v-tab-item
                v-for="(tab, index) in tabNames"
                :key="index"
                :value="'tab-' + index"
            >
                <div class="schedule-container">
                    <schedule :schedule="getScheduleByDate(dates[index])"> </schedule>
                </div>
            </v-tab-item>
        </v-tabs>
    </div>
</template>

<script>
import Schedule from '../components/Schedule.vue';
import { mapGetters } from 'vuex';

export default {
    name: 'Home',
    components: {
        'schedule': Schedule
    },
    computed: {
        ...mapGetters({
            getScheduleByDate: 'schedule/scheduleByDate',
        }),
    },
    data() {
        const yesterday = new Date();
        const tomorrow = new Date();
        const dayAfterTomorrow = new Date();

        yesterday.setDate(new Date().getDate() - 1);
        tomorrow.setDate(new Date().getDate() + 1);
        dayAfterTomorrow.setDate(new Date().getDate() + 2);

        return {
            dates: [
                yesterday,
                new Date(),
                tomorrow,
                dayAfterTomorrow,
            ],
            tabs: 4,
            tabNames: [
                'Yesterday',
                'Today',
                'Tomorrow',
                'Day after tomorrow'
            ],
            tab: null,
        }
    }
}
</script>

<style lang="scss" scoped>
.schedule-container {
    padding: 20px;
}
</style>

<style>
.history-page .v-tab {
    color: white !important;
    letter-spacing: auto !important;
    text-transform: none !important;
    font-size: 1.2rem;
}

.history-page .v-tabs-slider {
    background-color: white !important;
}

.history-page .v-window {
    background-color: transparent !important;
}

.history-page .v-item-group {
    background-color: transparent !important;
}

.history-page .schedule-container {
    padding: 0px !important;
    transform: scale(0.99);
    margin-top: 10px;
}

.history-page .v-slide-group__prev.v-slide-group__prev--disabled {
    display: none !important;
}
</style>

<template>
    <div>
        <div class="root-card">
            <schedule
                :schedule="todaysSchedule"
            />
        </div>
    </div>
</template>

<script>

import Schedule from '../components/Schedule.vue';
import { mapGetters } from 'vuex';

export default {
    name: 'Today',
    components: {
        'schedule': Schedule,
    },
    computed: {
        ...mapGetters({
            getScheduleByDate: 'schedule/scheduleByDate',
        }),
        todaysSchedule() {
            return this.getScheduleByDate(new Date());
        },
    }
}
</script>

<style lang="scss" scoped>

h1 {
    display: inline-block;
    color: #fff;
    position: relative;
    font-size: 3rem;
    margin: 5px;
}

h2 {
    color: #fff;
    display: inline-block;
    font-size: 2rem;
    margin: 10px 0px;
    position: relative;
}
</style>

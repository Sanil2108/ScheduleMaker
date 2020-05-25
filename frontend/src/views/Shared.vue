<template>
    <div class="root-card">
        <span class="heading-container">
            <h1> Shared schedules </h1>
            <div
                class="shadow-button"
                style="float: right"
                :class="{ 'disabled': loadingSchedules }"
                @click="loadSharedSchedules"
            ><span class="material-icons" style="font-size: 2rem; display: block">refresh</span></div>
        </span>
        <router-link v-for="(item, index) in sharedSchedules" :key="index" :to="`/schedule/${item.id}`">
            <div class="card">
                <h2> Schedule for {{ item.date }} </h2>
                <p class="owner-p"> By {{ item.owner }} </p>
                <p> {{ item.event_set.length }} Events </p>
                <p> {{ item.comment_set.length }} Comments </p>
            </div>
        </router-link>
    </div>
</template>

<script>
import * as axios from 'axios';
import { mapActions } from 'vuex';

import {
    SCHEDULES_LIST as SCHEDULES_LIST_URL
} from '../networkConstants';

export default {
    name: 'Shared',
    data() {
        return {
            sharedSchedules: [],
            loadingSchedules: false,
        }
    },
    components: {

    },
    mounted() {
        this.loadSharedSchedules();
    },
    methods: {
        ...mapActions({
            'manageNewNotification': 'ui/manageNewNotification',
        }),
        loadSharedSchedules() {
            this.loadingSchedules = true;
            axios.get(SCHEDULES_LIST_URL()).then((response) => {
                this.sharedSchedules = response.data
                console.log(this.sharedSchedules);
                this.loadingSchedules = false;
            }).catch((error) => {
                if (error.response) {
                    this.manageNewNotification({ message: error.response.data, type: 'error' })
                }
                else {
                    this.manageNewNotification({ message: 'Unknown error when fetching shared schedules', type: 'error' })
                }
                this.loadingSchedules = false;
            })
        }
    }
}
</script>

<style lang="scss" scoped>
.heading-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.card {
    h1, h2, h3, h4 {
        color: #444444;
    }

    h2 {
        margin: 0px;
    }

    .owner-p {
        margin-bottom: 20px;
    }

    &:hover {
        transform: translateY(-2px) scale(1.03);
        box-shadow: 0px 0px 20px 8px #00000044
    }

    cursor: pointer;
    margin: 10px 0px 30px;
    color: #444444;
    padding: 20px 25px;
}
</style>

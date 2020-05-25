<template>
    <div class="root-card">
        <div class="home-card" :style="{ backgroundImage: `url('${backgroundImageForHomeCard}'` }">
            <h1 class="image-text"> Good {{ timeString }} </h1> <br>
            <h1 class="image-text"> {{ userName }} </h1>
        </div>
        <schedule
            :schedule="todaysSchedule"
            :showScheduleHeading="true"
            :fullSchedule="false"
        />
    </div>
</template>

<script>
import { mapGetters } from 'vuex';

import Schedule from '../components/Schedule.vue';

export default {
    name: 'Home',
    components: {
        'schedule': Schedule,
    },
    computed: {
        ...mapGetters({
            userName: 'users/userName',
            getScheduleByDate: 'schedule/scheduleByDate',
        }),
        todaysSchedule() {
            return this.getScheduleByDate(new Date());
        },
        backgroundImageForHomeCard() {
            const currentHour = (new Date()).getHours();
            if (currentHour < 6) {
                return 'https://cutewallpaper.org/21/firewatch-wallpaper-1080p/Firewatch-HD-Wallpaper-Background-12901-Wallur.jpg';
            }
            else if (currentHour < 12) {
                return 'https://c4.wallpaperflare.com/wallpaper/778/637/208/mountains-silhouette-minimal-sunset-wallpaper-preview.jpg';
            }
            else if (currentHour < 16) {
                return 'http://www.firewatchgame.com/screenshots/firewatch-e3-1.jpg';
            }
            else if (currentHour < 20) {
                return 'https://i.pinimg.com/originals/86/ff/b8/86ffb87572d657f335cd7cd828c70de3.jpg';
            }
            else {
                return 'https://cutewallpaper.org/21/firewatch-wallpaper-1080p/Firewatch-HD-Wallpaper-Background-12901-Wallur.jpg';
            }
        },
        timeString() {
            const currentHour = (new Date()).getHours();
            if (currentHour < 6) {
                return 'Night';
            }
            else if (currentHour < 12) {
                return 'Morning';
            }
            else if (currentHour < 16) {
                return 'Afternoon';
            }
            else if (currentHour < 20) {
                return 'Evening';
            }
            else {
                return 'Night';
            }
        }
    }
}
</script>

<style lang="scss" scoped>
$WIDTH: 50vw;
$LEFT_MARGIN: 25vw;

h1.image-text {
    display: inline-block;
    position: relative;
    top: 40%;
    font-size: 4rem;
}

.home-card {
    text-shadow: -1px 0 black, 0 1px black, 1px 0 black, 0 -1px black;
    text-align: center;
    border-radius: 20px;
    margin-bottom: 2vh;
    box-shadow: 0px 0px 10px 10px #00000044;
    background-color: #fff;
    height: 75vh;
    background-size: cover;
    background-position: center;
    position: relative;
}
</style>

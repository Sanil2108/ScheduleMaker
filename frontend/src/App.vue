<template>
    <div id="app">
        <parallax-background />
        <navigation-drawer v-if="showNavigationDrawer">
            <router-link
                v-for="item in NAVIGATION_DRAWER_ITEMS"
                :key="item.path"
                :to="item.path"
            >
                <div @click="changeNewRoute(item)" class="item">
                    <span>{{ item.text }}</span>
                </div>
            </router-link>
            <div style="height: 10vh" />
            <router-link to="/login">
                <div class="item" @click="logoutUser"><span> 🚪 Logout </span></div>
            </router-link>
        </navigation-drawer>
        <span v-else-if="!onLoginPage" class="login-redirect-button-container">
            <v-btn
                outlined
                @click="() => { $router.push('/login') }"
            >
                home
            </v-btn>
        </span>
        <div class="content-container">
            <transition :name="routeAnimationName()" mode="out-in">
                <router-view />
            </transition>
        </div>
        <transition name="snackbar-slide">
            <div v-show="notificationOpen" class="snackbar" :class="snackBarClass">
                <span class="material-icons">
                {{ notificationIcon }}
                </span>
                {{ (notification) ? notification.text : '' }}
                <v-btn
                    color="pink"
                    text
                    @click="closeNotification"
                >
                    Close
                </v-btn>
            </div>
        </transition>
    </div>
</template>

<script>
import * as axios from 'axios';
import { mapGetters, mapActions } from 'vuex';

import ParallaxBackground from "./components/ParallaxBackground.vue";
import NavigationDrawer from "./components/NavigationDrawer.vue";

export default {
    components: {
        "parallax-background": ParallaxBackground,
        "navigation-drawer": NavigationDrawer,
    },
    data() {
        return {
            newRoute: null,
            lastTransitionName: "",
            NAVIGATION_DRAWER_ITEMS: [
                {
                    text: "🏠 Home",
                    path: "/",
                },
                {
                    text: "📅 Today",
                    path: "/today",
                },
                {
                    text: "📜 History",
                    path: "/history",
                },
                {
                    text: "📱 Shared",
                    path: "/shared",
                },
                {
                    text: "🎧 Relax",
                    path: "/relax",
                },
            ],
        };
    },
    mounted() {
        this.$nextTick(() => {
            window.eventBus.$on('CHANGE_ROUTE', (newRoute) => { this.$router.push(newRoute) })
            window.eventBus.$on('RELOAD_SCHEDULES', this.getAllSchedules.bind(null, this.dates));
        });

        (async () => {
            await this.loadCurrentUserFromLocalStorage();

            if (this.user !== null && this.user !== undefined && Object.keys(this.user).length !== 0) {
                this.getAllSchedules(this.dates);
            }
            if (!this.onPublicPage && !await this.validateCurrentUser()) {
                this.$router.push('/login');
            }
            this.$nextTick(() => {
                window.eventBus.$emit('USER_LOADED');
            })
        })();
    },
    methods: {
        ...mapActions({
            closeNotification: 'ui/clearNotification',
            logoutUser: 'users/logoutUser',
            validateCurrentUser: 'users/validateCurrentUser',
            loadCurrentUserFromLocalStorage: 'users/loadCurrentUserFromLocalStorage',
            getAllSchedules: 'schedule/getAllSchedules',
        }),
        changeNewRoute(item) {
            this.newRoute = item;
        },
        routeAnimationName() {
            if (this.newRoute === null || this.animating) {
                return "slideDown";
            }
            const toRoute = JSON.parse(JSON.stringify(this.newRoute)).path;
            const fromRoute = this.$router.currentRoute.path;

            let transitionAnimationName = "";

            if (toRoute === fromRoute) {
                transitionAnimationName = this.lastTransitionName;
            } else {
                const transitionAnimationName =
                this.pathsArray.indexOf(toRoute) < this.pathsArray.indexOf(fromRoute)
                    ? "slideDown"
                    : "slideUp";
                this.lastTransitionName = transitionAnimationName;
            }

            return transitionAnimationName;
        },
    },
    computed: {
        dates() {
            const today = new Date();
            const yesterday = new Date();
            const tomorrow = new Date();
            const dayAfter = new Date();

            yesterday.setDate(yesterday.getDate() - 1);
            tomorrow.setDate(tomorrow.getDate() + 1);
            dayAfter.setDate(dayAfter.getDate() + 2);

            let dates = [yesterday, today, tomorrow, dayAfter];
            dates = dates.map((date) => {
                return `${(date.getDate() < 10) ? '0' + date.getDate() : date.getDate()}-${((date.getMonth() + 1) < 10) ? '0' + (date.getMonth() + 1) : (date.getMonth() + 1)}-${date.getFullYear()}`;
            });

            return dates;
        },
        onLoginPage() {
            return this.$route.path === '/login';
        },
        onPublicPage() {
            return this.onLoginPage || this.$route.path.match('/schedule/*') !== null;
        },
        showNavigationDrawer() {
            return this.user !== null && this.user !== undefined && Object.keys(this.user).length !== 0;
        },
        snackBarClass() {
            if (!this.notification) {
                return '';
            }

            switch(this.notification.type) {
                case 'error': return 'snackbar--error';
                case 'success': return 'snackbar--success';
            }
            return '';
        },
        notificationIcon() {
            if (!this.notification) {
                return '';
            }

            switch(this.notification.type) {
                case 'error': return 'error';
                case 'success': return 'check_circle';
            }
            return '';
        },
        pathsArray() {
            const pathsArray = [];
            this.NAVIGATION_DRAWER_ITEMS.forEach((item) => {
                pathsArray.push(item.path);
            });
            return pathsArray;
        },
        ...mapGetters({
            notification: 'ui/currentNotification',
            user: 'users/user',
        }),
        notificationOpen: {
            get: function() {
                return this.notification !== null;
            },
            set: function() {}
        }
    },
};
</script>

<style lang="scss">
$WIDTH: 50vw;
$LEFT_MARGIN: 25vw;

* {
    font-family: "Roboto", sans-serif;
}

html,
body {
    margin: 0;
    padding: 0;
}

#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #2c3e50;
}

.login-redirect-button-container {
    position: absolute;
    top: 10px;
    left: 10px;

    * {
        color: white !important;
    }
}

.snackbar {
    position: fixed;
    color: #fff;
    text-align: center;
    box-shadow: 0px 2px 8px 2.5px #00000088;
    border-radius: 7.5px;
    top: 0px;
    left: 50%;
    padding: 10px;
    display: flex;
    align-items: center;
    transform: translate(-50%, 20px);

    &-slide-enter-active {
        transition: all 0.5s;
    }

    &-slide-enter {
        transform: translate(-50%, -200%);
    }

    .material-icons {
        margin-right: 10px;
    }

    button {
        color: #fff !important;
        background-color: #33333322;
        margin-left: 40px;
    }

    &--error {
        background-color: #f44336;
    }

    &--success {
        background-color: #689f38;
    }
}

.content-container {
    padding-top: 8vh;
}

a {
    text-decoration: none;
    color: #333333;
}

h1 {
    display: inline-block;
    position: relative;
    font-size: 3rem;
    margin: 5px;
    color: #fff;
}

h2 {
    display: inline-block;
    margin: 15px 0px;
    font-size: 2rem;
    position: relative;
    color: #fff;
}

h3 {
    display: inline-block;
    font-size: 1.5rem;
    position: relative;
    color: #fff;
}

h4 {
    display: inline-block;
    font-size: 1.2rem;
    position: relative;
    color: #fff;
}

.heading-dark {
    color: #444444;
}

.shadow-button {
    background: transparent;
    color: white;
    cursor: pointer;
    border-radius: 10000px;
    padding: 6px;
    transition: all 0.4s ease-in;
    position: relative;

    &--text {
        border-radius: 0px;
        display: inline-block;
        &::after {
            border-radius: 0px !important;
        }
    }

    &:not(.disabled):hover::after {
        height: 100%;
        width: 100%;
    }

    &.disabled {
        color: #ffffff55;
        cursor: default;
    }

    &::after {
        content: "";
        position: absolute;
        display: inline-block;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        border-radius: 10000px;
        transition: all 0.4s;
        background: #e9e9e933;
        height: 0px;
        width: 0px;
    }

    .highlighted {
        background: #e9e9e933;
    }
}

.root-card {
    margin-left: $LEFT_MARGIN;
    width: $WIDTH;
    min-height: 100vh;
}

.card {
    border-radius: 20px;
    box-shadow: 0px 0px 10px 10px #00000044;
    background-color: #fff;
    width: $WIDTH;
    position: relative;
    transition: all 0.4s;

    &--loading {
        filter: blur(20px);
    }
}

div.item {
    margin: 3px 4px 3px 0px;
    border-radius: 7px;
    padding: 1px 5px;
    transition: all 0.5s;
    cursor: pointer;
    height: 1.7rem;

    &:hover {
        background-color: #33333333;
    }

    span {
        position: relative;
        top: 0.24rem;
    }
}

// Slide up
.slideUp-enter {
    transform: translateY(100%);
}

.slideUp-enter-active,
.slideUp-leave-active {
    transition: all 0.4s;
}

.slideUp-leave-to {
    transform: translateY(-100%);
}

// Slide down
.slideDown-enter {
    transform: translateY(-100%);
}

.slideDown-enter-active,
.slideDown-leave-active {
    transition: all 0.4s;
}

.slideDown-leave-to {
    transform: translateY(100%);
}

// Fade
.fade-enter,
.fade-leave-to {
    opacity: 0;
}

.fade-enter-active,
.fade-leave-active {
    transition: all 0.7s;
}

// Fade and slide
.fadeAndSlide-enter,
.fadeAndSlide-leave-to {
    opacity: 0.3;
    transform: translateY(100px);
}

.fadeAndSlide-enter-active,
.fadeAndSlide-leave-active {
    transition: all 2s;
}

// shrink
.shrink-enter,
.shrink-leave-to {
    // clip: rect(119px, 255px, 229px, 80px);
    // transform: scale(0);
    height: 0px;
}

.shrink-enter-active,
.shrink-leave-active {
    transition: all 1s;
}

</style>

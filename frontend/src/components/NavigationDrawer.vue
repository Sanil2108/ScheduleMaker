<template>
    <div class="navigation-drawer" ref="navigationDrawerRoot">
        <transition name="slide">
            <div class="navigation-drawer__items-container" v-show="navigationDrawerItemsVisible">
                <slot />
            </div>
        </transition>
    </div>
</template>

<script>
export default {
    data() {
        return {
            navigationDrawerItemsVisible: false,
        }
    },
    computed: {

    },
    mounted() {
        this.$refs.navigationDrawerRoot.addEventListener('mouseover', () => {this.navigationDrawerItemsVisible = true;})
        this.$refs.navigationDrawerRoot.addEventListener('mouseout', () => {this.navigationDrawerItemsVisible = false;})
    }
}
</script>

<style lang="scss" scoped>

.navigation-drawer {
    height: 100vh;
    width: 10vw;
    position: fixed;
    top: 0px;
    left: 0px;

    &__items-container {
        color: #37474f;
        text-align: start;
        background-color: #fff;
        width: 100%;
        top: 14vh;
        position: relative;
        border-radius: 0px 10px 10px 0px;
        box-shadow: 0px 0px 10px 10px #00000044;
        padding: 10px;
    }
}

.slide-enter {
    transform: translateX(-120%);
}

.slide-enter-active {
    transition: all 0.3s ease-in-out;
}

.slide-leave-active {
    transition: all 0.3s ease-in-out 0.75s;
}

.slide-leave-to {
    transform: translateX(-120%);
}

</style>
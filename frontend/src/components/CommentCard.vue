<template>
<div class="comment-card-container" style="position: relative">
    <transition name="fade" appear>
        <div class="card comment-card">
            <p style="margin-bottom: 4px; display: block; font-size: 0.8rem"> {{ comment.user }} says </p>
            <p> {{ comment.comment_text }} </p>
        </div>
    </transition>
</div>
</template>

<script>
export default {
    props: ['comment'],
    data() {
        return {};
    },
    computed: {},
    methods: {}
}
</script>

<style lang="scss" scoped>
.comment-card {
    border-radius: 6px;
    margin-bottom: 20px;
    padding: 15px;
}

p {
    font-size: 1.3rem;
    display: inline-block;
}

</style>

<style>
.event-card-container .v-input {
    padding: 0px !important;
}

.event-card-container textarea {
    color: white !important;
    font-size: 1.3rem !important;
    line-height: normal !important;
    height: auto;
}

.event-card-container .v-counter {
    color: white !important;
}

.event-card-container .v-input__slot::before {
    color: white !important;
    background-color: white !important;
}
</style>

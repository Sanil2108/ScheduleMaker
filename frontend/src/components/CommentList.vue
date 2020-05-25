<template>
    <div>
        <h2 class="comments-heading">Comments</h2>
        <comment-card v-for="comment in comments" :key="comment.id" :comment="comment" />
    </div>
</template>

<script>
import { mapGetters } from 'vuex';

import CommentCard from './CommentCard.vue';
import NewCommentCard from './NewCommentCard.vue';

export default {
    props: ['schedule'],
    data() {
        return {};
    },
    computed: {
        ...mapGetters({
            getAllComments: 'schedule/getAllComments'
        }),
        comments() {
            return this.getAllComments(this.schedule);
        }
    },
    components: {
        'comment-card': CommentCard,
        'new-comment-card': NewCommentCard,
    },
}
</script>
<style lang="scss" scoped>
.comments-heading {
    display: inline-block;
}
</style>

<template>
<div class="comment-card-container" style="position: relative">
    <div class="card comment-card">
        <!-- <h2> {{ comment.title }} </h2> -->
        <div class="description-container">
            <v-textarea
                :auto-grow="true"
                v-model="commentText"
                color="#ffffff"
                counter="100"
                placeholder="Write your comment here!"
                :rules="[]"
            >
            </v-textarea>
            <v-btn
                :loading="loading"
                outlined
                @click="onClickPostButton"
                :disabled="commentButtonDisabled"
            >
            Post!
            </v-btn>
        </div>
    </div>
</div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
    props: ['schedule'],
    data() {
        return {
            commentText: '',
            loading: false,
        }
    },
    computed: {
        ...mapGetters({

        }),
        commentButtonDisabled() {
            return this.commentText == null || this.commentText === '';
        },
        loadingState() {
            return this.deleting || this.updating;
        },
    },
    methods: {
        ...mapActions({
            createComment: 'schedule/createComment'
        }),
        async onClickPostButton() {
            this.loading = true;
            try {
                await this.createComment({ scheduleId: this.schedule.id, commentText: this.commentText });
                this.commentText = '';
            }
            finally {
                this.loading = false;
            }
        }
    }
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
.comment-card-container .v-input {
    padding: 0px !important;
}

.comment-card-container textarea {
    color: black !important;
    font-size: 1.3rem !important;
    line-height: normal !important;
    height: auto;
}

.comment-card-container .v-counter {
    color: white !important;
}

.comment-card-container .v-input__slot::before {
    color: white !important;
    background-color: white !important;
}
</style>

<template>
    <div>
        <div
            v-for="(item, key) in categories"
            :key="key"
            class="category_card card"
            :style="{ backgroundColor: item.color }"
        > {{ item.name }} </div>
    </div>
</template>

<script>
export default {
    props: ['categories']
}
</script>
<style scoped>
.category_card {
    border-radius: 5px;
    margin: 10px 5px;
    padding: 5px;
    color: white;
    font-size: 1.2rem;
    display: inline-block;
    width: auto;
}
</style>

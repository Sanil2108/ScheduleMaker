<template>
    <div class="root-card">
        <span class="heading-container">
            <h1> Relax </h1>
        </span>
        <div class="card">
            <span>
                <div style="font-size: 4rem; margin-bottom: 10px">🚧</div>
                <div style="font-size: 1.2rem;">Hey! Wait! Don't go out! It's unsafe! Wild Pokémon live in tall grass!</div>
                <div style="font-size: 1rem; color: #7e7e7e;"><i>We're hard at work trying to get you your first Pokemon!</i></div>
            </span>
        </div>
    </div>
</template>

<script>

export default {
    name: 'Relax',
    components: {

    }
}
</script>

<style lang="scss" scoped>
$WIDTH: 50vw;
$LEFT_MARGIN: 25vw;

h1 {
    display: inline-block;
    color: #fff;
    position: relative;
    font-size: 3rem;
    margin: 5px;

    &.home-heading {
        margin-left: $LEFT_MARGIN;
        margin-top: 25px;
    }
}

h2 {
    color: #fff;
    display: inline-block;
    font-size: 2rem;
    margin: 10px 0px;
    position: relative;
    margin-left: $LEFT_MARGIN;
}

.card {
    padding: 100px 30px;
    text-align: center;
}
</style>

<template>
    <div>
        <h1 class="home-heading"> Relax </h1><br>
        <h2> Today's schedule </h2>
        <div class="home-card">
            <div style="height: 40vh" />
        </div>
    </div>
</template>

<script>

export default {
    name: 'Home',
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

.home-card {
    border-radius: 20px;
    box-shadow: 0px 0px 10px 10px #00000044;
    background-color: #fff;
    width: $WIDTH;
    left: $LEFT_MARGIN;
    position: relative;
}
</style>

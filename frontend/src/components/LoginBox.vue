<template>
    <div class="login-box-container">
        <div class="login-container">
        </div>
    </div>
</template>

<script>
export default {
    
}
</script>

<style scoped>

    .login-box-container {
        height: 60vh;
        width: 20vw;
        display: inline-block;
        position: absolute;
        top: 50%;
        left: 50%;
        padding: 12px;
        transform: translate(-50%, -50%);
        background-color: transparent;
        border-radius: 25px;
        box-shadow: inset 0px 0px 0px 3px #646bb6d7;
        z-index: 10;
        transition: all 0.2s;
    }

    .login-container {
        height: 100%;
        width: 100%;
        background: #646bb6d7;
        border-radius: 20px;
        transition: all 0.2s;
    }

    .login-container:hover {
        /* transform: scale(1.03); */
    }

    .login-box-container:hover {
        /* transform: scale(1.03); */
    }

    .logo-container {
        position: absolute;
        background: red;
    }
</style>
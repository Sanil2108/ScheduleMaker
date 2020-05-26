<template>
    <div class="card-container login-card-container">
        <transition name="scaleAndSlideLeft" mode="out-in">
            <div class="card root-card" v-show="showLoginView">
                <img class="logo" src="interface.svg" />
                <p v-show="showTitle" class="title"> Schedule maker </p>
                    <perfect-scrollbar>
                        <h2> Login testing </h2>
                        <v-text-field
                            v-model="loginData.email"
                            label="Email"
                            :rules="[rules.required, rules.emailValidation]"
                        ></v-text-field>
                        <v-text-field
                            label="Password"
                            :append-icon="showPassword ? 'visibility' : 'visibility_off'"
                            :type="showPassword ? 'text' : 'password'"
                            @click:append="showPassword = !showPassword"
                            v-model="loginData.password"
                            :rules="[rules.required]"
                        ></v-text-field>

                        <v-btn
                            outlined
                            @click="loginButtonClick"
                            :loading="loading"
                            :disabled="loginButtonDisabled"
                        >
                            Login
                        </v-btn>
                        <v-btn
                            outlined
                            :disabled="loading"
                            @click="signUpViewButtonClick"
                            style="margin-bottom: 35px"
                        >
                            Sign up
                        </v-btn>
                    </perfect-scrollbar>
            </div>
        </transition>

        <transition name="scaleAndSlideRight" mode="out-in">
            <div class="card root-card" v-show="showSignUpView">
                <img class="logo" src="interface.svg" />
                <p v-show="showTitle" class="title"> Schedule maker </p>
                <perfect-scrollbar>
                    <h2> Sign up </h2>
                    <v-text-field
                        v-model="signUpData.email"
                        label="Email"
                        :rules="[rules.required, rules.emailValidation]"
                    ></v-text-field>
                    <v-text-field
                        v-model="signUpData.name"
                        label="Name"
                        :rules="[rules.required]"
                    ></v-text-field>
                    <v-text-field
                        v-model="signUpData.password"
                        label="Password"
                        :append-icon="showPassword ? 'visibility' : 'visibility_off'"
                        :type="showPassword ? 'text' : 'password'"
                        @click:append="showPassword = !showPassword"
                        :rules="[rules.required]"
                    ></v-text-field>
                    <v-text-field
                        v-model="signUpData.confirmPassword"
                        label="Confirm Password"
                        :append-icon="showPassword ? 'visibility' : 'visibility_off'"
                        :type="showPassword ? 'text' : 'password'"
                        @click:append="showPassword = !showPassword"
                        :rules="[rules.required, rules.matchPassword]"
                    ></v-text-field>

                    <v-btn
                        :disabled="signUpButtonDisabled"
                        outlined
                        :loading="loading"
                        @click="signUpButtonClick"
                    >
                        Sign up
                    </v-btn>
                    <v-btn
                        outlined
                        :disabled="loading"
                        @click="loginViewButtonClick"
                        style="margin-bottom: 35px"
                    >
                        Login
                    </v-btn>
                </perfect-scrollbar>
            </div>
        </transition>
    </div>
</template>

<script>
import { PerfectScrollbar } from 'vue2-perfect-scrollbar'
import { mapActions } from 'vuex';

const VIEWS= {
    LOGIN: 'login',
    SIGNUP: 'signup',
};

const EMAIL_REGEX = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

export default {
    name: 'LoginSignUp',
    components: {
        'perfect-scrollbar': PerfectScrollbar
    },
    data() {
        return {
            currentView: VIEWS.LOGIN,
            showPassword: false,
            showTitle: true,
            showForm: true,
            loading: false,
            loginData: {
                email: '',
                password: '',
            },
            signUpData: {
                email: '',
                name: '',
                password: '',
                confirmPassword: '',
            },
            rules: {
                required: value => (value.length !== 0) ? true : 'Required',
                matchPassword: value => (value === this.signUpData.password) ? true : `Passwords don't match`,
                emailValidation: value => (EMAIL_REGEX.test(String(value)) ? true : 'Email is not valid'),
            }
        }
    },
    computed: {
        signUpButtonDisabled() {
            return !(
                (this.rules.matchPassword(this.signUpData.confirmPassword) === true) &&
                (this.rules.emailValidation(this.signUpData.email) === true) &&
                (this.rules.required(this.signUpData.email) === true) &&
                (this.rules.required(this.signUpData.name) === true) &&
                (this.rules.required(this.signUpData.password) === true) &&
                (this.rules.required(this.signUpData.confirmPassword === true)));
        },
        loginButtonDisabled() {
            return !(
                (this.rules.emailValidation(this.loginData.email) === true) &&
                (this.rules.required(this.loginData.email) === true) &&
                (this.rules.required(this.loginData.password) === true));
        },
        showSignUpView() {
            return this.currentView === VIEWS.SIGNUP;
        },
        showLoginView() {
            return this.currentView === VIEWS.LOGIN;
        },
    },
    methods: {
        ...mapActions({
            sendSignUpRequest: 'users/signUpUser',
            sendLoginRequest: 'users/loginUser',
            logoutUser: 'users/logoutUser',
        }),

        signUpViewButtonClick() {
            this.currentView = VIEWS.SIGNUP;
        },
        loginViewButtonClick() {
            this.currentView = VIEWS.LOGIN;
        },
        async signUpButtonClick() {
            this.loading = true;
            try {
                const response = await this.sendSignUpRequest({ 
                    name: this.signUpData.name,
                    email: this.signUpData.email,
                    password: this.signUpData.password,
                });
            } finally {
                this.loading = false;
            }
        },
        async loginButtonClick() {
            this.loading = true;
            try {
                const response = await this.sendLoginRequest({ 
                    email: this.loginData.email,
                    password: this.loginData.password,
                });
                if (response.status === 200) {
                    window.eventBus.$emit('CHANGE_ROUTE', '/');
                }
            } finally {
                this.loading = false;
            }
        }
    },
    mounted() {
        this.logoutUser();
    }
}
</script>

<style lang="scss" scoped>
$LOGO_SIZE: 80px;
$LOGO_MARGIN: 40px;
$LOGO_TITLE_MARGIN: 80px;
$LEFT_MARGIN: 40px;

.card {
    max-height: 70vh;
    width: 20vw;
    position: absolute;
    top: 50vh;
    left: 50vw;
    transform: translate(-50%, -50%);
    margin-left: 0px;
    min-height: 0px;
}

.logo {
    height: $LOGO_SIZE;
    width: $LOGO_SIZE;
    position: absolute;
    top: 0px;
    left: 50%;
    transform: translate(-50%, -50%);
}

.title {
    font-weight: 500;
    font-size: 1.2rem;
    position: absolute;
    top: $LOGO_MARGIN;
    left: 50%;
    transform: translate(-50%, 0px);
    color: #343434;
    // margin-top: $LOGO_MARGIN;
}

h2 {
    color: #343434;
    margin: $LOGO_TITLE_MARGIN 0px 30px $LEFT_MARGIN;
}

// Scale and slide right
.scaleAndSlideRight-leave-active {
    animation: scaleAndSlideRightDisappear 0.5s;
}

.scaleAndSlideRight-enter-active {
    animation: scaleAndSlideRightAppear 0.5s;
    transform: translate(calc(0% + 50vw), -50%) scale(0.4);
}

@keyframes scaleAndSlideRightAppear {
    // 70% {
    //     transform: translate(calc(-50% + 30vw), -50%) scale(0.7);
    // }
    100% {
        transform: translate(-50%, -50%) scale(1);
    }
}

@keyframes scaleAndSlideRightDisappear {
    // 70% {
    //     transform: translate(calc(-50% + 30vw), -50%) scale(0.7);
    // }
    100% {
        transform: translate(calc(0% + 50vw), -50%) scale(0.4);
    }
}

// Scale and slide left
.scaleAndSlideLeft-leave-active {
    animation: scaleAndSlideLeftDisappear 0.5s;
}

.scaleAndSlideLeft-enter-active {
    animation: scaleAndSlideLeftAppear 0.5s;
    transform: translate(calc(-100% - 50vw), -50%) scale(0.4);
}

@keyframes scaleAndSlideLeftAppear {
    // 70% {
    //     transform: translate(calc(-50% - 30vw), -50%) scale(0.7);
    // }
    100% {
        transform: translate(-50%, -50%) scale(1);
    }
}

@keyframes scaleAndSlideLeftDisappear {
    // 70% {
    //     transform: translate(calc(-50% - 30vw), -50%) scale(0.7);
    // }
    100% {
        transform: translate(calc(-100% - 50vw), -50%) scale(0.4);
    }
}


</style>
<style lang="scss">
.login-card-container .v-input {
    margin: 0px 40px;
}

.login-card-container .v-btn {
    width: calc(100% - 80px);
    left: 40px;
    position: relative;
    margin: 7.5px 0px;
}

.login-card-container .v-input__slot {
    margin-bottom: 2px;
}

.login-card-container .v-text-field__details {
    margin-bottom: 15px;
}

.login-card-container .v-messages__message {
    color: #f44336 !important;
}

.login-card-container .ps {
    max-height: 70vh;
}

</style>
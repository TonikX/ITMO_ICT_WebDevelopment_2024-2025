<template>
    <div class="auth__container">
        <div class="auth__form">
            <h1 style="text-align: center;">Зарегистрироваться</h1>
            <form @submit.prevent="registerUser">
                <div class="form__group">
                    <label for="user.email">Email</label>
                    <input type="email" id="__email" v-model="user.email" required/>
                </div>
                <div class="form__group">
                    <label for="user.firstname">Firstname</label>
                    <input type="text" id="__firstname" v-model="user.firstname" required/>
                </div>
                <div class="form__group">
                    <label for="user.lastname">Lastname</label>
                    <input type="text" id="__lastname" v-model="user.lastname" required/>
                </div>
                <div class="form__group">
                    <label for="user.birth_date">Birth date</label>
                    <input type="date" id="__birth_date" v-model="user.birth_date" required/>
                </div>
                <div class="form__group">
                    <label for="user.phone">Phone</label>
                    <input type="tel" id="__phone" placeholder="+8 888 888 8888" pattern="\+[1-9]{1}\s[0-9]{3}\s[0-9]{3}\s[0-9]{4}" v-model="user.phone" required/>
                </div>
                <div class="form__group">
                    <label for="user.password">Password</label>
                    <input type="password" id="__password" v-model="user.password" required/>
                </div>
                <!-- <div class="form__group">
                    <label for="confirmPassword">Confirm Password</label>
                    <input type="password" id="__confirm__password" v-model="confirmPassword" required/>
                </div> -->
                <button type="submit" class="auth__button">Register</button>
            </form>
        </div> 
    </div>
</template>

<script>
    import axios from "axios";

    export default {
        name: 'Register',
        data() {
            return {
                user: {
                    email: '',
                    firstname: '',
                    lastname: '',
                    birth_date: '',
                    phone: '',
                    password: '',
                },
                confirmPassword : '',
            }
        },
        methods: {
            async registerUser() {
                console.log(this.user);
                try {
                    await axios.post('http://127.0.0.1:8000/auth/users/', this.user);
                    this.$router.push('/login');
                } catch (e) {
                    if (e.response) {
                        switch (e.response.status) {
                            case 401:
                                break;
                            default:
                        }
                    }
                }
            }
        },
    }
</script>

<style>
    @import '../assets/auth.css';
</style>
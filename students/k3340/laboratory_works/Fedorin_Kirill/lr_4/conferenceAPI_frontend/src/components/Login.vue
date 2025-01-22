<template>
    <div class="auth__container">
        <div class="auth__form">
            <h1 style="text-align: center;">Авторизация</h1>
            <label v-if="this.error_msg" style="color: red;">{{ this.error_msg }}</label>
            <form id="__auth__form" @submit.prevent="authUser">
                <div class="form__group">
                    <label for="email">Эл. почта</label>
                    <input type="email" id="__email" v-model="email" required>
                </div>
                <div class="form__group">
                    <label for="password">Пароль</label>
                    <input type="password" id="__password" v-model="password" required>
                </div>
                <button type="submit" class="auth__button">Войти</button>
            </form>
        </div>
    </div>
</template>

<script>
    import axios from "axios";
    export default {
        name: "Login",
        data() {
            return {
                email: "",
                password: "",
                error_msg: "",
            }
        },
        methods: {
            async authUser() {
                try {
                    console.log(this.email, this.password)
                    const response = await axios.post('http://127.0.0.1:8000/auth/token/login', {
                        password: this.password,
                        email: this.email,
                    });
                    console.log(response.data)
                    localStorage.setItem('token', response.data.auth_token);
                    axios.defaults.headers.common['Authorization'] = `Token ${response.data.auth_token}`;

                    const response_user = await axios.get('http://127.0.0.1:8000/auth/users/me/');
                    localStorage.setItem('user', JSON.stringify(response_user.data));
                    this.$router.push('/');
                } catch (e) {
                    if (e.response) {
                        switch (e.response.status) {
                            case 401:
                                console.log('delete token')
                                delete axios.defaults.headers.common["Authorization"];
                                break;
                            case 400:
                                this.error_msg = "Неверные логин или пароль. Проверьте пожалуйста данные для входа"
                            default:
                        }
                    }
                }
            }
        } 
    }
</script>

<style>
    @import '../assets/auth.css';
</style>
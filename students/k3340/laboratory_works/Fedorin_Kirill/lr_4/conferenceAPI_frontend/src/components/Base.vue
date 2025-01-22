<template>
    <header id="__header">
        <!-- <h2 style="text-align: center;">Science Conferences</h2> -->
        <div class="base__container">
            <nav class="nav__container">
                <div class="nav__list">
                    <div v-if="is_authorized">
                        <a href="/">Главная</a>
                        <a href="/conferences">Конференции</a>
                        <a id="__participation__btn" href="/participation">Участие</a>
                    </div>
                    <div v-if="!is_authorized">
                        <a href="/">Главная</a>
                        <a href="/conferences">Конференции</a>
                    </div>  
                    <div v-if="is_authorized">
                        <span class="user__name">Hello,{{ email }}</span>
                        <a id="__user__info" href="/logout">Выйти</a>
                    </div>
                    <div v-if="!is_authorized">
                        <a class="auth__btns" href="/login">Войти</a>
                        <a class="auth__btns" href="/register">Зарегистироваться</a>
                    </div>  
                </div>
            </nav>
        </div>
    </header>
</template>

<script>
    import axios from "axios";

    export default {
        name: "Base",
        data() {
            return {
                email: '',
                is_authorized: false,
            }
        },
        methods: {
            // refreshtoken () {
            //     axios.defaults.headers.common['Authorization'] = `Token ${localStorage.getItem('token')}`
            // },
            async fetchUserAuth () {
                try {
                    console.log(axios.defaults.headers.common['Authorization']);
                    const user = JSON.parse(localStorage.getItem('user'));
                    if (user) {
                        this.is_authorized = true;
                        axios.defaults.headers.common['Authorization'] = `Token ${localStorage.getItem('token')}`
                        this.email = user.email
                    }
                } catch (e) {
                    console.log('error in base')
                }
            }
        },
        mounted() {
            this.fetchUserAuth() 
        }
    }

    
</script>

<style>
    body {
        margin: 0;
        font-family: Arial, sans-serif;
    }

    #__header {
        background-color: #333;
        color: #fff;
        padding: 15px 0;
    }

    .base__container {
        width: 100%;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #333;
    }

    .nav__container {
        display: flex;
        width: 100%;
    }

    .nav__list {
        list-style: none;
        padding: 0;
        margin: 0;
        display: flex;
        justify-content: space-between;
        gap: 15px;
        width: 100%;
    }

    .nav__list div {
        margin-right: 5px;
    }


    .nav__list a {
        color: #fff;
        text-decoration: none;
        padding: 8px 15px;
        margin-left: 5px;
        border-radius: 4px;
        transition: background 0.3s;
    }

    .nav__list a:hover {
        background-color: #555;
    }

    .auth__btns {
        background-color: #444;
    }
</style>
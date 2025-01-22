<template>
    <h1 style="text-align: center;"> Вы успешно вышли из аккаунта </h1>
    <div id="__btn__div"><a class="button__home" href="/">Вернуться на главную</a></div>
    
</template>

<script>
    import axios from "axios";

    export default {
        name: 'Logout',
        methods: {
            async logout () {
                const token = localStorage.getItem('token');
                if (token) {
                    console.log(token)
                    try {
                        const response = await axios.post('http://127.0.0.1:8000/auth/token/logout/');
                        console.log(response.data)
                        console.log('aaa')
                    } catch (e) {
                        if (e.response) {
                            switch (e.response.status) {
                                case 401:
                                    break;
                                default:
                            }
                        }
                    } finally {
                        console.log('here delete all')
                        localStorage.removeItem('token');
                        localStorage.removeItem('user');
                        delete axios.defaults.headers.common["Authorization"];
                    }
                }
            }
        }, 
        mounted() {
            this.logout() 
        }
    }

    
</script>
    
<style>
    .button__home {
        display: inline-block; 
        padding: 10px 20px; 
        font-size: 16px;
        text-align: center; 
        text-decoration: none; 
        cursor: pointer; 
        border: none; 
        border-radius: 5px; 
        background-color: #3498db; 
        color: #ffffff; 
        transition: background-color 0.3s ease; 
    }

    .button__home:hover {
        background-color: #2980b9; 
    }

    #__btn__div {
        display: flex;
        justify-content: center;
        /* border: 1px solid; */
    }
</style>
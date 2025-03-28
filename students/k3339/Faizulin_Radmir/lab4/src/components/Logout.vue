<template>
    <h2>{{ username }}, are you sure you want to logout?</h2>
    <button @click="logout" class="btn">Yes</button>
</template>

<script>
    import api from '../services/api';
    import router from '../router';
    export default {
        data() {
            return {
                username: ''
            };
        },
        mounted() {
            const token = localStorage.getItem('token');
            if (!token) {
                router.push('/login');
                return;
            }
            console.log(token);
            api.get('auth/users/me/', {
                headers: {
                    Authorization: `Token ${token}`
                }
            })
            .then(response => {
                this.username = response.data.username;
                this.username = this.username.charAt(0).toUpperCase() + this.username.slice(1);
            })
            .catch(error => {
                console.error(error);
            })
        },
        methods: {
            logout() {
                localStorage.removeItem('token');
                this.$router.push('/login');
            }
        }
    }
</script>

<style scoped>

.btn {
  display: inline-block;
  padding: 10px 20px;
  font-size: 16px;
  font-weight: bold;
  text-align: center;
  color: #fff;
  background-color: red;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: black; /* Цвет фона кнопки при наведении */
}

</style>

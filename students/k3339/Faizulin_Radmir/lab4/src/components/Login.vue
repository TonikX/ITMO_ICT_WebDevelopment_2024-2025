<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="login">
      <label for="username">Username:</label>
      <input v-model="username" type="text" id="username" required>
      <h1></h1>
      <label for="password">Password:</label>
      <input v-model="password" type="password" id="password" required>
      <h1></h1>
      <button type="submit" class="btn">Login</button>
    </form>
    <router-link to="/registration" class="link">I don't have an account</router-link>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    login() {
      const credentials = {
        username: this.username,
        password: this.password,
      };

      api.post('/auth/token/login/', credentials)
        .then(response => {
          const token = response.data.auth_token;
          localStorage.setItem('token', token);
          this.$router.push('/books');
        })
        .catch(error => {
          console.error('Login failed:', error);
        });
    },
  },
};
</script>

<style scoped>
.link {
  color: #000;
  font-size: 17px;
}

form {
  margin-bottom: 20px;
}

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

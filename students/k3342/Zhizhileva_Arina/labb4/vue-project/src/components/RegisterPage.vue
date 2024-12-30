<template>
  <v-container class="register-container">
    <v-form @submit.prevent="registerUser">
      <v-text-field
        v-model="email"
        label="Email"
        type="email"
        required
      ></v-text-field>
      <v-text-field
        v-model="password"
        label="Password"
        type="password"
        required
      ></v-text-field>
      <v-text-field
        v-model="username"
        label="Username"
        required
      ></v-text-field>
      <v-btn type="submit" color="primary">Register</v-btn>
    </v-form>
  </v-container>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';

export default {
  name: 'RegisterPage',
  setup() {
    const email = ref('');
    const password = ref('');
    const username = ref('');

    const registerUser = async () => {
      try {
        const response = await axios.post('http://localhost:8000/api/register/', {
          email: email.value,
          password: password.value,
          username: username.value
        });
        console.log('Регистрация успешна:', response.data);
      } catch (error) {
        console.error('Ошибка регистрации:', error.response.data);
      }
    };

    return {
      email,
      password,
      username,
      registerUser
    };
  }
};
</script>

<style scoped>
.register-container {
  padding-top: 80px; /* Отступ сверху, чтобы не перекрывать шапкой */
}
</style>

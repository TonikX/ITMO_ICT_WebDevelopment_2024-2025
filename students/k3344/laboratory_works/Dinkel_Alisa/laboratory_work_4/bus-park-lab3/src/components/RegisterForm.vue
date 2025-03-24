<template>
  <div class="login-form">
    <form @submit.prevent="handleRegister" class="form-container">
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required class="form-input" />
      </div>

      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required class="form-input" />
      </div>

      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required class="form-input" />
      </div>

      <button type="submit" class="btn-submit">Зарегистрироваться</button>
    </form>
  </div>
</template>

<script>
import { registerUser, loginUser } from '@/api/auth';

export default {
  data() {
    return {
      username: '',
      password: '',
      email: ''
    };
  },
  methods: {
  async handleRegister() {
    try {
      const newUser = { username: this.username, password: this.password };
      const data = await registerUser(newUser);

      console.log('Registered successfully:', data);

      // После успешной регистрации сразу выполняем вход
      const credentials = { username: this.username, password: this.password };
      const loginResponse = await loginUser(credentials);

      console.log('Вход выполнен:', loginResponse);

      this.$router.push('/');
    } catch (error) {
      console.error('Registration failed:', error);
    }
  }
}
};
</script>

<style scoped>
/* Стили для формы регистрации */
.login-form {
  padding: 2rem;
}

.form-container {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 1rem;
}

.form-input {
  width: 100%;  /* Обеспечиваем одинаковую ширину для полей */
  padding: 0.75rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.btn-submit {
  width: 100%;  /* Обеспечиваем одинаковую ширину для кнопки */
  padding: 0.75rem;
  font-size: 1rem;
  color: white;
  background-color: #5b80a8;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-submit:hover {
  background-color: #99b6d6;
}
</style>

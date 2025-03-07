<template>
    <div>
      <h2>Register</h2>
      <form @submit.prevent="register">
        <div>
          <label for="username">Username:</label>
          <input v-model="username" type="text" id="username" required />
        </div>
        <div>
          <label for="email">Email:</label>
          <input v-model="email" type="email" id="email" required />
        </div>
        <div>
          <label for="password">Password:</label>
          <input v-model="password" type="password" id="password" required />
        </div>
        <div>
          <label for="passwordConfirmation">Confirm Password:</label>
          <input v-model="passwordConfirmation" type="password" id="passwordConfirmation" required />
        </div>
        <button type="submit">Register</button>
      </form>
      <p v-if="error" style="color:red;">{{ error }}</p>
      <p v-if="success" style="color:green;">Registration successful! Please log in.</p>
    </div>
  </template>
  
  <script>
  import api from '@/api'
  
  export default {
    name: 'RegisterView',
    data() {
      return {
        username: '',
        email: '',
        password: '',
        passwordConfirmation: '',
        error: '',
        success: false
      }
    },
    methods: {
      register() {
        if (this.password !== this.passwordConfirmation) {
          this.error = "Passwords do not match.";
          return;
        }
  
        api.post('/auth/users/', {
          username: this.username,
          email: this.email,
          password: this.password
        })
        .then(response => {
          this.success = true;
          this.error = '';
          this.$router.push('/login')
        })
        .catch(err => {
          console.error("Registration error:", err);
          this.error = "Registration failed. Please check your details.";
          this.success = false;
        });
      }
    }
  }
  </script>
  
  <style scoped>
  form {
    max-width: 400px;
    margin: auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  label {
    display: block;
    font-weight: bold;
  }
  
  input {
    width: 100%;
    padding: 8px;
    box-sizing: border-box;
  }
  </style>
  
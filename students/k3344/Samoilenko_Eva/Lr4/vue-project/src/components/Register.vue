<script setup>
import {ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/index.js";

const form = ref({
  username: '',
  email: '',
  password: ''
})

function register(){
  instance.post('/auth/users/', form.value).then(response => {
        if (response.status === 201){
          router.push('/login')
        }
      }
  ).catch(error => console.log(error))
}
</script>

<template>
  <div class="container">
    <div class="form-container">
      <h1>Register</h1>
      <form @submit.prevent="register">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            type="text"
            id="username"
            class="input-box"
            v-model="form.username"
            placeholder="Enter your username"
            required
          />
        </div>

        <div class="form-group">
          <label for="email">Email</label>
          <input
            type="email"
            id="email"
            class="input-box"
            v-model="form.email"
            placeholder="Enter your email"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            class="input-box"
            v-model="form.password"
            placeholder="Enter your password"
            required
          />
        </div>

        <button @click="register" class="btn">Register</button>
      </form>

      <p class="login-link">
        <router-link to="/login">Already have an account?</router-link>
      </p>
    </div>
  </div>
</template>

<style>
.form-container {
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  width: 100%;
  text-align: center;
}

h1 {
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
}

.input-box {
  border: 1px solid grey;
  border-radius: 4px;
  display: inline-block;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

button.btn {
  width: 100%;
  padding: 10px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 10px;
}

button.btn:hover {
  background-color: #45a049;
}

.login-link {
  margin-top: 15px;
  font-size: 14px;
  color: #555;
}

.login-link a {
  color: #007bff;
  text-decoration: none;
}
</style>

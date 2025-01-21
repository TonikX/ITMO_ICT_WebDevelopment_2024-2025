<script setup>
import {ref} from "vue";
import router from "@/router/index.js";
import {tokenStore} from "@/stores/token.js";
import axios from "axios";

const tokenStorage = tokenStore();
const form = ref({
  email: '',
  username: '',
  password: ''
});

async function register() {
  try {
    const response = await axios.post('/auth/users/', form.value);
    if (response.status === 201) {
      console.log("User registered:", response.data);
      await loginUser(form.value.username, form.value.password);
    }
  } catch (error) {
    console.error("Registration error:", error);
  }
}

async function loginUser(username, password) {
  try {
    const response = await axios.post('/auth/token/login/', {username, password});
    if (response.status === 200) {
      tokenStorage.setToken(response.data.auth_token);
      router.push('/rooms'); //TO CHANGE
    }
  } catch (error) {
    console.error("Login error after registration:", error);
  }
}

function goToLogin() {
  router.push("/login");
}
</script>

<template>
  <v-app>
    <v-container class="d-flex align-center justify-center fill-height">
      <div class="w-50 text-center">
        <h2>Регистрация</h2>
        <v-text-field label="Почта" v-model="form.email" required></v-text-field>
        <v-text-field label="Логин" v-model="form.username" required></v-text-field>
        <v-text-field label="Пароль" v-model="form.password" type="password" required></v-text-field>
        <div class="d-flex justify-center mt-4">
          <v-btn class="mx-2" @click="register">Зарегистрироваться</v-btn>
          <v-btn class="mx-2" @click="goToLogin">Войти</v-btn>
        </div>
      </div>
    </v-container>
  </v-app>
</template>

<style scoped>
</style>

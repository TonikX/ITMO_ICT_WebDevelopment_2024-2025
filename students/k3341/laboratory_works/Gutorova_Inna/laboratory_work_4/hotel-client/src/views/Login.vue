<script setup>
import {ref} from "vue";
import router from "@/router/index.js";
import {tokenStore} from "@/stores/token.js";
import axios from "axios";

const tokenStorage = tokenStore();
const form = ref({
  username: '',
  password: ''
});

async function login() {
  try {
    const response = await axios.post('/auth/token/login/', form.value);
    if (response.status === 200) {
      tokenStorage.setToken(response.data.auth_token);
      router.push('/clients');
    }
  } catch (error) {
    console.error("Login error:", error);
  }
}

function goToRegister() {
  router.push("/register");
}
</script>

<template>
  <v-app>
    <v-container class="d-flex align-center justify-center fill-height">
      <div class="w-50 text-center">
        <h2>Вход</h2>
        <v-text-field label="Логин" v-model="form.username" required></v-text-field>
        <v-text-field label="Пароль" v-model="form.password" type="password" required></v-text-field>
        <div class="d-flex justify-center mt-4">
          <v-btn class="mx-2" color="primary" @click="login">Войти</v-btn>
          <v-btn class="mx-2" color="secondary" @click="goToRegister">Зарегистрироваться</v-btn>
        </div>
      </div>
    </v-container>
  </v-app>
</template>

<style scoped>
</style>

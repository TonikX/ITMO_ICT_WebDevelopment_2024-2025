<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import {login} from "@/services/AuthService";

const router = useRouter();
const username = ref("");
const password = ref("");
const errorMessage = ref("");

const PerformLogin = async () => {
  try {
    await login(username.value, password.value);
    router.push("/");
  } catch (error: any) {
    errorMessage.value = "Invalid username or password!";
    console.error(error);
  }
};
</script>

<template>
  <div class="login-container">
    <h1>Login</h1>
    <input v-model="username" placeholder="Username" />
    <input v-model="password" type="password" placeholder="Password" />
    <button @click="PerformLogin">Login</button>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<style scoped>
.login-container {
  max-width: 300px;
  margin: auto;
  padding: 20px;
  text-align: center;
}
input {
  display: block;
  width: 100%;
  margin: 10px 0;
  padding: 8px;
}
button {
  width: 100%;
  padding: 8px;
  background-color: blue;
  color: white;
  border: none;
  cursor: pointer;
}
.error {
  color: red;
  margin-top: 10px;
}
</style>

<template>
  <v-container>
    <h1>Регистрация</h1>
    <v-form>
      <v-text-field v-model="email" label="Email" required></v-text-field>
      <v-text-field v-model="username" label="Username" required></v-text-field>
      <v-text-field v-model="password" label="Password" type="password" required></v-text-field>
      <v-text-field v-model="re_password" label="Repeat password" type="password" required></v-text-field>
      <v-text-field v-model="level" label="How many workouts you'd like to do?" required></v-text-field>

      <v-btn color="primary" @click="register">Зарегистрироваться</v-btn>
    </v-form>
    <p>
      Уже есть аккаунт? <v-btn text to="/login">Войти</v-btn>
    </p>
  </v-container>
</template>

<script setup>
import { useAppStore } from '@/stores/app';

const appStore = useAppStore();

const router = useRouter()

const email = ref('')
const username = ref('')
const imageUrl = ref('')
const password = ref('')
const re_password = ref('')
const level = ref('')

const register = async () => {
  await appStore.register(email.value, username.value, password.value, re_password.value, level.value);

  if (!appStore.errorMessage) {
    alert("Вы успешно зарегистрировались!");
    router.push('/dashboard');
  } else {
    alert(appStore.errorMessage);
  }
};
</script>

<style scoped>
h1 {
  margin: 24px 0;
}

p {
  margin-top: 12px;
}
</style>

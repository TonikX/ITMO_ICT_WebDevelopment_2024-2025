<template>
  <v-container>
    <h1>Войти в аккаунт</h1>
    <v-form>
      <v-text-field v-model="username" label="Username" required></v-text-field>
      <v-text-field v-model="password" label="Password" type="password" required></v-text-field>
      <v-btn color="primary" @click="login">Войти</v-btn>
    </v-form>
    <p>
      Нет аккаунта? <v-btn text to="/register">Зарегистрироваться</v-btn>
    </p>
  </v-container>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useAppStore } from '@/stores/app';
import { onMounted } from 'vue';

const appStore = useAppStore();

const router = useRouter();

const username = ref('');
const password = ref('');

const login = async () => {
  await appStore.login(username.value, password.value);
  if (!appStore.errorMessage) {
    router.push('/dashboard');
  } else {
    alert(appStore.errorMessage);
  }
}

onMounted(() => {
  if (appStore.isAuthenticated) {
    router.push('/dashboard');
  }
})
</script>

<style scoped>
/*@import url('../styles/custom-theme.css');*/
h1 {
  margin: 24px 0;
}

p {
  margin-top: 12px;
}
</style>

<template>
  <div class="home">
    <h1 v-if="!isAdmin">Погрузитесь в золотую эпоху кино</h1>

    <nav class="menu">
      <p v-if="isAdmin">
        <router-link to="/halls">Управление залами</router-link>
      </p>

      <p v-if="isAdmin">
        <router-link to="/movies">Управление фильмами</router-link>
      </p>

      <p v-if="isAdmin">
        <router-link to="/sessions">Управление сеансами</router-link>
      </p>

      <p v-if="!isAdmin">
        <router-link to="/session-board">Сейчас в прокате</router-link>
      </p>

      <p v-if="!isAdmin">
        <router-link to="/tickets">Мои билеты</router-link>
      </p>
    </nav>
  </div>
</template>

<script>
import {computed} from 'vue';
import {useAuthStore} from '@/stores/auth.js';

export default {
  name: 'Home',
  setup() {
    const authStore = useAuthStore();
    const isAdmin = computed(() => authStore.isAdmin);
    return {
      isAdmin,
    };
  },
};
</script>

<style>
.home {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #F5F5DC;
  font-family: 'Pacifico', cursive;
  color: #800020;
  padding: 20px;
  box-sizing: border-box;
}

h1 {
  font-size: 40px;
  margin-bottom: 30px;
}

.menu {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.menu p {
  margin: 15px 0;
}

.menu a {
  display: inline-block;
  background-color: #FFAA33;
  color: #fff;
  padding: 15px 30px;
  text-decoration: none;
  font-size: 20px;
  border-radius: 10px;
  transition: background-color 0.3s, transform 0.3s;
}

.menu a:hover {
  background-color: #800020;
  transform: scale(1.05);
}
</style>
<template>
  <div>
    <header>
      <nav>
        <router-link to="/" class="nav-button">Главная</router-link>
        <button @click="logout" class="nav-button">Выйти</button>
      </nav>
    </header>
  </div>
</template>

<script>

import authService from '@/api/authService';

export default {
  methods: {
    logout() {
      authService.logout();
      this.$router.push('/');
    },
  },
};
</script>

<style scoped>

header {
  background-color: #333;
  padding: 10px;
}

nav {
  display: flex;
  justify-content: space-between;
}

.nav-button {
  color: white;
  padding: 8px 16px;
  text-decoration: none;
  border: none;
  background: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.nav-button:hover {
  background-color: #444;
}

.nav-button:active {
  background-color: #555;
}
</style>

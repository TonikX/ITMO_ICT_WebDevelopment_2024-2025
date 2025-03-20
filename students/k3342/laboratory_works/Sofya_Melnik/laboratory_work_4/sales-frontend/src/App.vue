<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const goBack = () => {
  router.go(-1);
};
</script>

<template>
  <header>
    <div class="wrapper">
      <button @click="goBack" class="back-button">
        ← Назад
      </button>

      <nav>
        <RouterLink to="/signup">Регистрация</RouterLink>
        <RouterLink to="/login">Вход</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  background: linear-gradient(135deg, #007bff, #0056b3);
  padding: 15px 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.wrapper {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 900px;
  margin: auto;
}

.back-button {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s ease, transform 0.2s ease;
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.4);
  transform: scale(1.05);
}

nav a {
  text-decoration: none;
  color: white;
  font-weight: bold;
  margin: 0 10px;
  padding: 8px 12px;
  border-radius: 6px;
  transition: background 0.3s ease;
}

nav a:hover {
  background: rgba(255, 255, 255, 0.2);
}
</style>

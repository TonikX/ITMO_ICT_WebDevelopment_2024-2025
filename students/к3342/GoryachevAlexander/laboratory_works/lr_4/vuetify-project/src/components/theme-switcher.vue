<template>
  <button @click="toggleTheme">{{ currentTheme === 'dark' ? '🌞' : '🌚' }}</button>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const currentTheme = ref('light');

const applyTheme = (theme) => {
  document.documentElement.setAttribute('data-bs-theme', theme);
  localStorage.setItem('theme', theme);
  currentTheme.value = theme;
};

const toggleTheme = () => {
  const newTheme = currentTheme.value === 'light' ? 'dark' : 'light';
  applyTheme(newTheme);
};

onMounted(() => {
  const savedTheme = localStorage.getItem('theme') || 'light';
  applyTheme(savedTheme);
});
</script>

<style scoped>
button {
  cursor: pointer;
  padding: 8px 12px;
  border: none;
  border-radius: 8px;
  font-size: 1.2rem;
}
</style>

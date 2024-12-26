<script setup>
import WelcomeItem from './WelcomeItem.vue'
import DocumentationIcon from './icons/IconDocumentation.vue'
</script>

<template>
  <div class="welcome-container">
    <WelcomeItem>
      <template #icon>
        <DocumentationIcon class="icon" />
      </template>
      <template #heading>
        <h1 class="title">Навигационная страница</h1>
      </template>
    </WelcomeItem>
    <p class="description">
      Добро пожаловать! Выберите пункт меню, чтобы перейти к соответствующему разделу приложения.
    </p>
  </div>
</template>

<style scoped>

.welcome-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  min-height: 50vh;
  background-color: white;
  padding: 20px;
  box-sizing: border-box;
}

.title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #2c3643;
  margin: 20px 0;
}

.description {
  font-size: 1.2rem;
  color: #555;
  margin: 10px 0 30px;
  line-height: 1.6;
  max-width: 600px;
}


.icon {
  width: 80px;
  height: 80px;
  margin-bottom: 20px;
  fill: #2c3643;
}

.icon:hover {
  fill: #1d2a35;
}
</style>

<template>
  <div class="home-page">
    <Header />
    <div class="content">
      <div class="header-container">
        <h2 class="page-title">Добро пожаловать в систему управления школой</h2>
      </div>

      <div v-if="!isAuthenticated" class="buttons-container">
        <router-link to="/login" class="nav-button">Вход</router-link>
        <router-link to="/register" class="nav-button">Регистрация</router-link>
      </div>

      <div v-else class="buttons-container">
        <router-link to="/students" class="nav-button">Список студентов</router-link>
        <router-link to="/teachers" class="nav-button">Список учителей</router-link>
        <router-link to="/rooms" class="nav-button">Список кабинетов</router-link>
        <router-link to="/lessons" class="nav-button">Список уроков</router-link>
        <router-link to="/grades" class="nav-button">Оценки</router-link>
        <router-link to="/report" class="nav-button">Составление отчёта</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import Header from "@/components/Header.vue";

export default {
  components: {
    Header,
  },
  data() {
    return {
      isAuthenticated: !!localStorage.getItem("authToken"),
    };
  },
};
</script>

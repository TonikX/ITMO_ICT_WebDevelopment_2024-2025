<template>
  <header>
    <!-- Логотип приложения -->
    <img alt="CineLink Logo" class="logo" src="@/assets/images/smalllogo.png"/>

    <!-- Форма поиска фильмов -->
    <form aria-label="Search movies" class="search-form" role="search" @submit.prevent="performSearch">
      <input
          id="searchInput"
          v-model="searchQuery"
          aria-label="Search input"
          class="search-input"
          name="searchInput"
          placeholder="search"
          type="text"
      />
      <button
          id="searchButton"
          aria-label="Submit search"
          class="search-button"
          name="searchButton"
          type="submit"
      >
        <!-- Иконка поиска -->
        <svg class="search-icon">
          <use href="/icons/icons.svg#icon-search"></use>
        </svg>
      </button>
    </form>

    <!-- Основная навигация -->
    <nav aria-label="Main navigation" class="nav-links" role="navigation">
      <!-- Ссылки на основные страницы -->
      <router-link aria-label="Go to main page" class="nav-link" to="/">main</router-link>
      <router-link aria-label="Go to friends page" class="nav-link" to="/friends">friends</router-link>
      <router-link aria-label="Go to profile page" class="nav-link" to="/profile">profile</router-link>
      <!-- Кнопка выхода из аккаунта -->
      <svg id="logoutIcon" aria-label="Log out" class="logout-icon" role="button" tabindex="0" @click="logout">
        <use href="/icons/icons.svg#icon-logout"></use>
      </svg>
    </nav>
  </header>
</template>

<script>
import {useAuthStore} from "@/stores/auth";
import {useRouter} from "vue-router";
import {ref} from "vue";

export default {
  name: "AppHeader",
  setup() {
    const authStore = useAuthStore(); // Работа с состоянием аутентификации через Pinia
    const router = useRouter(); // Работа с маршрутизацией
    const searchQuery = ref(""); // Поле ввода текста для поиска

    // Обработка поиска фильмов
    const performSearch = () => {
      if (searchQuery.value.trim()) { // Если строка поиска не пуста
        router.push({path: "/search", query: {q: searchQuery.value.trim()}}); // Переход на страницу поиска
      }
    };

    // Обработка выхода из аккаунта
    const logout = () => {
      authStore.logout(); // Выход пользователя через Pinia
    };

    return {
      searchQuery,
      performSearch,
      logout,
    };
  },
};
</script>

<style scoped>
@import "@/assets/css/header.css"; /* Стили для хедера импортируются из отдельного файла */
</style>
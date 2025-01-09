<template>
  <div class="container us_panel">
    <header class="us_panel-header">
      <h1 id="welcomeHeader">Welcome, {{ username }}</h1>
      <p id="userIntro">Track your fitness progress and view your workout plans.</p>
    </header>

    <!-- Тренировки -->
    <SavedWorkouts v-if="userId" :userId="userId"/>

    <!-- Профиль -->
    <ProfileForm v-if="userId" :userId="userId" />

    <!-- Навигационные кнопки -->
    <nav role="navigation" aria-label="Main Navigation">
      <div class="navigation-buttons">
        <router-link to="/search" class="nav-button" aria-label="Go to workouts">
          Workouts
        </router-link>
        <router-link to="/blog" class="nav-button" aria-label="Go to Health & Nutrition Blog">
          Food Blog
        </router-link>
      </div>
    </nav>
  </div>
</template>

<script>
import { onMounted, ref } from 'vue'
import ProgressTracker from '../components/Acc/ProgressTracker.vue'
import SavedWorkouts from '../components/Acc/SavedWorkouts.vue'
import ProfileForm from '../components/Acc/ProfileForm.vue'
import instance from '@/AxiosInstance.js';
import { TokenStore } from '@/stores/TokenStore.js';
import WorkoutSearch from "@/views/WorkoutSearch.vue";

export default {
  components: {
    WorkoutSearch,
    ProgressTracker,
    SavedWorkouts,
    ProfileForm
  },
  setup() {
    const Token = TokenStore();
    const userId = ref(parseInt(localStorage.getItem('user_id')) || null);
    const username = ref(localStorage.getItem('username') || 'User');

    onMounted(() => {
      const token = Token.token;
      if (token) {
        // Проверяем, есть ли данные в localStorage
        if (!localStorage.getItem('user_id') || !localStorage.getItem('username')) {
          instance
            .get("/auth/users/me/", {
              headers: { Authorization: `Token ${token}` },
            })
            .then((response) => {
              userId.value = response.data.id;
              username.value = response.data.username;
              localStorage.setItem('user_id', userId.value);
              localStorage.setItem('username', username.value);
            })
            .catch((error) => {
              console.error("Ошибка при получении данных о пользователе:", error);
            });
        } else {
          userId.value = parseInt(localStorage.getItem('user_id'));
          username.value = localStorage.getItem('username');
        }
      } else {
        console.error("Токен отсутствует. Пожалуйста, выполните вход.");
      }
    });

    return {
      username,
      userId
    };
  },
}
</script>

<style>
:root {
    --background-color: #fbeaff;
    --text-color: #333;
    --card-background: #fff;
    --heading-color: #6a0dad;
    --button-background: #ff85c0;
    --button-border: #ff85c0;
    --circle-bg: #e6e6e6;
    --circle-main-weight: #ff99cc;
    --circle-main-workouts: #cc66ff;
    --circle-main-calories: #d1a3d6;
    --circle-text-color: #8c2e9e;
}

/* Альтернативная голубая тема */
.blue-theme {
    --background-color: #e0f7fa;
    --text-color: #333;
    --card-background: #ffffff;
    --heading-color: #00796b;
    --button-background: #00acc1;
    --button-border: #00acc1;
    --circle-bg: #b2ebf2;
    --circle-main-workouts: #0097a7;
    --circle-main-calories: #00796b;
    --circle-text-color: #00796b;
}

body {
    background-color: var(--background-color);
    color: var(--text-color);
    margin: 0;
    font-family: Arial, sans-serif;
    line-height: 1.6;
}

.us_panel {
    padding: 20px;
}
.us_panel-header {
    margin-bottom: 30px;
    text-align: center;
}


.card {
    width: 100%;
    max-width: 900px;
    margin: 5px auto;
    background-color: var(--card-background);
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-title, .card-workout-title, #profileInfo {
    font-size: 1.5rem;
    color: var(--heading-color);
    font-weight: bold;
}

.us_progress {
    margin-bottom: 30px;
}

.card-body {
    padding: 30px;
}

.circle-progress {
    width: 150px;
    height: 150px;
    position: relative;
    display: inline-block;
    margin: 20px;
    text-align: center;
}

.circle-progress svg {
    transform: rotate(-90deg);
    width: 100%;
    height: 100%;
}

.circle-progress text {
    font-size: 10px;
    font-weight: bold;
    text-anchor: middle;
    dominant-baseline: central;
    fill: var(--circle-text-color);
}

.circle-progress .bg-circle {
    stroke: var(--circle-bg);
}
.circle-progress .main-circle-weight {
    stroke: var(--circle-main-weight);
}
.circle-progress .main-circle-workouts {
    stroke: var(--circle-main-workouts);
}
.circle-progress .main-circle-calories {
    stroke: var(--circle-main-calories);
}

.circle-progress-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: var(--circle-text-color);
    font-size: 10px;
    font-weight: bold;
}

.circle-progress-text p {
    margin: 0;
    font-size: 10px;
}

.btn-custom {
    background-color: var(--button-background);
    border: none;
    color: white;
    font-size: 14px;
    padding: 5px 10px;
    border-radius: 5px;
    transition: background-color 0.3s ease;
}
.btn-custom:hover {
    background-color: #ff66b2;
}
.btn-primary {
    background-color: var(--button-background);
    border-color: var(--button-border);
}

.card-workout-title {
    color: var(--heading-color);
    font-weight: bold;
}

.list-group-item {
    padding: 15px;
    border: none;
}

.circle-progress p {
    font-size: 14px;
    color: var(--text-color);
    margin-top: 14px;
    word-wrap: break-word;
}

.navigation-buttons {
    margin-top: 20px;
    display: flex;
    justify-content: space-between;
}

.table th, .table td {
    border-top: 1px solid #f5f5f5;
    border-bottom: 1px solid #f5f5f5;
}

.table th {
    background-color: #f0f0f0;
    color: var(--circle-text-color);
}

.table td {
    color: var(--text-color);
}

.table {
    margin-top: 20px;
}

.icon-button {
    font-size: 2rem;
    padding: 15px;
    border: none;
    background: none;
    cursor: pointer;
    transition: transform 0.3s ease;
    color: #333;
}

.icon-button:hover {
    transform: scale(1.1);
    color: #000;
}

.theme-switcher {
    position: fixed;
    top: 10px;
    left: 10px;
    z-index: 1000;
    cursor: pointer;
}

.theme-switcher i {
    font-size: 2rem;
    color: #000;
    transition: color 0.3s ease;
}

.theme-switcher:hover i {
    color: #00796b;
}
</style>

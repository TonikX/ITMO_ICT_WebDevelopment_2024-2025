<template>
  <div v-if="isLoggedIn">
    <nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom">
      <div class="container">
        <!-- Логотип -->
        <router-link to="/" class="navbar-brand">
          <img
            src="@/assets/icons/bus-logo.svg"
            alt="Логотип"
            style="width: 40px; height: auto;"
          />
          Диспетчер Автопарка
        </router-link>

        <!-- Кнопка для мобильного меню -->
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Переключить навигацию"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <!-- Меню -->
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link to="/dashboard" class="nav-link" active-class="active">Главная</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/buses" class="nav-link" active-class="active">Автобусы</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/drivers" class="nav-link" active-class="active">Водители</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/routes" class="nav-link" active-class="active">Маршруты</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/schedules" class="nav-link" active-class="active">Расписания</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/incidents" class="nav-link" active-class="active">Инциденты</router-link>
            </li>
            <li class="nav-item">
              <button
                class="btn btn-outline-danger btn-sm"
                @click="logout"
              >
                Выйти
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'Navbar',
  data() {
    return {
      // Проверка, есть ли токен в localStorage
      isLoggedIn: !!localStorage.getItem('accessToken'),
    };
  },
  methods: {
    logout() {
      // Очистка данных пользователя и перенаправление на главную страницу
      localStorage.removeItem('accessToken');
      localStorage.removeItem('user');
      this.$router.push('/');  // Перенаправление на главную страницу
    },
  },
};
</script>

<style scoped>
.navbar-brand {
  font-weight: bold;
  font-size: 1.2rem;
}

.nav-link.active {
  font-weight: bold;
  color: #0d6efd !important; /* Цвет активной ссылки */
}

button {
  margin-left: 10px;
}
</style>

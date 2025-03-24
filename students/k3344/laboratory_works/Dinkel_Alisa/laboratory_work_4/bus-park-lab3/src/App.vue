<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Автобусный парк</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item"><router-link class="nav-link" to="/">Главная</router-link></li>
            <li v-if="isAuthenticated" class="nav-item"><router-link class="nav-link" to="/drivers">Водители</router-link></li>
            <li v-if="isAuthenticated" class="nav-item"><router-link class="nav-link" to="/routes">Маршруты</router-link></li>
            <li v-if="isAuthenticated" class="nav-item"><router-link class="nav-link" to="/buses">Автобусы</router-link></li>
            <li v-if="isAuthenticated" class="nav-item"><router-link class="nav-link" to="/schedule">Смены</router-link></li>
            <li v-if="isAuthenticated" class="nav-item"><router-link class="nav-link" to="/reports">Отчет</router-link></li>
          </ul>
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <button v-if="!isAuthenticated" class="btn btn-outline-light rounded-pill" @click="goToLogin">
                Вход
              </button>
              <button v-else class="btn btn-outline-danger rounded-pill" @click="logout">
                Выход
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <div class="container mt-4 d-flex justify-content-center">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import { logoutUser } from '@/api/auth';

export default {
  data() {
    return {
      isAuthenticated: localStorage.getItem('authToken') !== null,
    };
  },
  methods: {
    goToLogin() {
      this.$router.push('/login');
    },
    logout() {
      logoutUser()
        .then(() => {
          this.isAuthenticated = false;
          localStorage.removeItem('authToken');
          this.$router.push('/login');
        })
        .catch((error) => {
          console.error('Ошибка выхода:', error);
        });
    }
  },
  watch: {
    // Следим за изменением токена в localStorage
    // eslint-disable-next-line no-unused-vars
    '$route'(to, from) {
      this.isAuthenticated = localStorage.getItem('authToken') !== null;
    }
  }
};
</script>


<style scoped>
.btn-outline-light {
  border-color: #fff;
  color: #fff;
  background-color: transparent;
}

.btn-outline-light:hover {
  background-color: #fff;
  color: #000;
}

.btn-outline-danger {
  border-color: #dc3545;
  color: #dc3545;
  background-color: transparent;
}

.btn-outline-danger:hover {
  background-color: #dc3545;
  color: #fff;
}
</style>

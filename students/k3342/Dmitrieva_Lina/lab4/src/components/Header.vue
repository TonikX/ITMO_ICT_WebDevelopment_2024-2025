<template>
  <div class="header">
    <nav>
      <router-link to="/">Главная</router-link>
      <router-link to="/newspapers">Газеты</router-link>
      <router-link to="/printshops">Типографии</router-link>
      <router-link  to="/deliveries">Доставки</router-link>
      <router-link to="/distribution">Распределение</router-link>
      <router-link to="/reports">Отчеты</router-link>
      <router-link v-if="isAdmin" to="/employees">Сотрудники</router-link>
      <router-link to="/login" v-if="!isAuthenticated">Вход</router-link>
      <span v-if="isAuthenticated" class="user-info">Добро пожаловать, {{ username }}</span>
      <button v-if="isAuthenticated" @click="logout">Выйти</button>
    </nav>
  </div>
</template>

<script>
export default {
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem("token");
    },
    isAdmin() {
      return localStorage.getItem("role") === "admin";
    },
    isAdminOrEmployee() {
      const role = localStorage.getItem("role");
      return role === "admin" || role === "employee";
    },
    username() {
      return localStorage.getItem("username") || "Пользователь";
    },
  },
  methods: {
    logout() {
      localStorage.removeItem("token");
      localStorage.removeItem("role");
      localStorage.removeItem("username");
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
.header {
  background-color: #333;
  color: white;
  padding: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

nav {
  display: flex;
  align-items: center;
}

nav a {
  color: white;
  padding: 10px;
  text-decoration: none;
  margin-right: 20px;
}

nav a:hover {
  background-color: #555;
}

button {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  text-decoration: underline;
  font-size: 14px;
}

button:hover {
  color: #ccc;
}

.user-info {
  margin-right: 15px;
  font-size: 14px;
  color: #ddd;
}
</style>

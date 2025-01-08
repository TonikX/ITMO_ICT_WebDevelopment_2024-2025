<template>
  <header class="header">
    <nav class="nav-bar">
      <router-link to="/home" class="nav-link">Главная</router-link>
      <div v-if="isAuthenticated" class="user-info">
        <span>Приветствуем, вы вошли в систему!</span>
        <button @click="logout" class="auth-button">Выйти</button>
      </div>
    </nav>
  </header>
</template>

<script>
export default {
  data() {
    return {
      isAuthenticated: !!localStorage.getItem("authToken"),
      username: localStorage.getItem("username") || "",
    };
  },
  methods: {
    logout() {
      localStorage.removeItem("authToken");
      localStorage.removeItem("username");
      this.isAuthenticated = false;
      this.username = "";
      this.$router.push("/home");
      alert("Вы вышли из системы.");
    },
  },
};
</script>

<style scoped>
.header {
  background: linear-gradient(to top, #fcfdff, #d9dbde);
  padding: 15px 20px;
  margin-bottom: 20px;
  width: 100%;
  color: #333;
}

.nav-bar {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-link {
  color: #333;
  font-size: 16px;
  font-weight: 500;
  text-decoration: none;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-link:hover {
  background-color: #e3e3e3;
}

.auth-button {
  color: #333;
  font-size: 16px;
  padding: 8px 15px;
}

.auth-button:hover {
  background-color: #e3e3e3;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}
</style>

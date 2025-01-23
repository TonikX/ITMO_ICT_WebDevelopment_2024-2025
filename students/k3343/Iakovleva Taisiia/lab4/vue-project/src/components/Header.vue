<template>
    <header class="navbar">
      <nav>
        <ul class="nav-links">
          <li><router-link to="/workshops">Цехи</router-link></li>
          <li><router-link to="/cells">Ячейки</router-link></li>
          <li><router-link to="/employees">Сотрудники</router-link></li>
          <li><router-link to="/diets">Диеты</router-link></li>
          <li><router-link to="/chickens">Куры</router-link></li>
          <li><router-link to="/breeds">Породы</router-link></li>
          <li><router-link to="/reports">Отчеты по производительности</router-link></li>
          <!-- Кнопка для выхода -->
          <li><button @click="logout" class="btn-logout">Выйти</button></li>
        </ul>
      </nav>
    </header>
  </template>
  
  <script>
  export default {
    name: "Header",
    methods: {
      logout() {
        // Удаляем токен из localStorage
        localStorage.removeItem("authToken");
  
        // Перенаправляем на страницу логина
        this.$router.push("/login");
      },
    },
  };
  </script>
  
  <style scoped>
  .navbar {
    background-color: #085d88;
    color: white;
    padding: 10px 20px;
    display: flex;
    justify-content: center;
    width: 100%;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .nav-links {
    list-style-type: none;
    display: flex;
    gap: 20px;
    padding: 0;
    margin: 0;
  }
  
  .nav-links li {
    margin: 0;
  }
  
  .nav-links a {
    color: white;
    text-decoration: none;
    font-size: 16px;
    font-weight: bold;
  }
  
  .nav-links a:hover {
    text-decoration: underline;
  }
  
  .btn-logout {
    background-color: #dc3545; /* Красный для кнопки "Выйти" */
    color: white;
    padding: 6px 12px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
  }
  
  .btn-logout:hover {
    background-color: #b02a37;
  }
  </style>
  
<script setup>
import TheWelcome from '../components/TheWelcome.vue'
</script>

<template>
  <main class="main-container">
    <TheWelcome />

    <nav class="navigation">
      <ul>
        <li><router-link to="/login">Вход</router-link></li>
        <li><router-link to="/register">Регистрация</router-link></li>
        <li><router-link to="/drivers">Список водителей</router-link></li>
        <li><router-link to="/routes">Список маршрутов</router-link></li>
        <li><router-link to="/buses">Список автобусов</router-link></li>
        <li><router-link to="/driver-schedules">Расписание водителей</router-link></li>
        <li><router-link to="/assignment">Эксплуатация автобусов</router-link></li>
        <li><router-link to="/maintenances">Сервисное обслуживание</router-link></li>
      </ul>
    </nav>
  </main>
</template>

<style scoped>

.main-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  min-height: 70vh;
  background-color: white;
  padding: 20px;
  box-sizing: border-box;
}

.navigation {
  margin-top: 20px;
}

.navigation ul {
  list-style-type: none;
  padding: 0;
}

.navigation li {
  margin-bottom: 10px;
}

router-link {
  text-decoration: none;
  color: #2c3643;
  font-weight: bold;
  font-size: 1.2rem;
  padding: 10px 20px;
  border: 2px solid #2c3643;
  border-radius: 8px;
  transition: all 0.3s ease;
}

router-link:hover {
  background-color: #2c3643;
  color: #fff;
  border-color: #1d2a35;
}

@media (max-width: 768px) {
  router-link {
    font-size: 1rem;
    padding: 8px 15px;
  }
}
</style>

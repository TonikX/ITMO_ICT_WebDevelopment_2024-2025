<template>
  <div class="dashboard">
    <h1>Главная страница</h1>

    <!-- Проверка на аутентификацию -->
    <div v-if="isAuthenticated">
      <p>Добро пожаловать, {{ username }}!</p>
    </div>

    <!-- Если не аутентифицирован, перенаправить на страницу логина -->
    <div v-else>
      <p>Вы не авторизованы. <a href="/login">Войдите</a></p>
    </div>

    <!-- Кнопка выхода -->
    <button @click="logout" class="logout-btn">Выход</button>

    <div class="summary-cards" v-if="isAuthenticated">
      <div class="card">
        <h3>Количество рейсов</h3>
        <p>{{ flightCount }}</p>
      </div>
      <div class="card">
        <h3>Количество самолётов</h3>
        <p>{{ aircraftCount }}</p>
      </div>
      <div class="card">
        <h3>Количество сотрудников</h3>
        <p>{{ employeeCount }}</p>
      </div>
    </div>

    <div class="actions" v-if="isAuthenticated">
      <button @click="goToAddFlight">Управление рейсами</button>
      <button @click="goToSchedules">Просмотреть расписания</button>
      <button @click="goToManageAircrafts">Просмотреть самолёты</button>
      <button @click="goToManageCrew">Управление экипажами</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      flightCount: 0,
      aircraftCount: 0,
      employeeCount: 0,
      isAuthenticated: false, // Параметр для проверки аутентификации
      username: '',
    };
  },
  methods: {
    // Переходы на страницы
    goToAddFlight() {
      this.$router.push('/manage-flights');
    },
    goToSchedules() {
      this.$router.push('/manage-schedules');
    },
    goToManageAircrafts() {
      this.$router.push('/manage-aircrafts');
    },
    goToManageCrew() {
      this.$router.push('/manage-crew');
    },
    // Логика для выхода из аккаунта
    logout() {
      localStorage.removeItem('auth_token'); // Удаляем токен из localStorage
      this.$router.push('/login'); // Перенаправляем на страницу логина
    },
  },
  created() {
    const token = localStorage.getItem('auth_token');

    if (token) {
      // Если токен существует, считаем пользователя аутентифицированным
      this.isAuthenticated = true;

      // Загружаем информацию о пользователе с помощью запроса к серверу
      axios.get('/api/auth/current-user', {headers: {Authorization: `Token ${token}`}})
          .then(response => {
            this.username = response.data.username;
          })
          .catch(error => {
            console.error('Ошибка при получении данных пользователя:', error);
            // Если ошибка с токеном или пользователем, удаляем токен и перенаправляем
            localStorage.removeItem('auth_token');
            this.$router.push('/login');
          });

      // Загружаем данные после проверки аутентификации
      axios.get('/api/flights/count', {headers: {Authorization: `Token ${token}`}})
          .then(response => {
            this.flightCount = response.data.count;
          })
          .catch(error => {
            console.error('Ошибка при получении количества рейсов:', error);
          });

      axios.get('/api/aircrafts/count', {headers: {Authorization: `Token ${token}`}})
          .then(response => {
            this.aircraftCount = response.data.count;
          })
          .catch(error => {
            console.error('Ошибка при получении количества самолетов:', error);
          });

      axios.get('/api/employees/count', {headers: {Authorization: `Token ${token}`}})
          .then(response => {
            this.employeeCount = response.data.count;
          })
          .catch(error => {
            console.error('Ошибка при получении количества сотрудников:', error);
          });
    } else {
      // Если нет токена, перенаправляем на страницу логина
      this.$router.push('/login');
    }
  },
};
</script>

<style scoped>
.dashboard {
  padding: 20px;
  position: relative; /* Для позиционирования кнопки в правом верхнем углу */
}

.summary-cards {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
}

.card {
  background-color: #f4f4f4;
  padding: 20px;
  border-radius: 5px;
  width: 150px;
  height: 150px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border: 1px solid #ccc;
}

.card h3 {
  margin: 0;
  font-size: 18px;
  text-align: center;
}

.card p {
  font-size: 24px;
  font-weight: bold;
  margin-top: 10px;
  text-align: center;
}

.actions {
  display: flex;
  justify-content: center;
}

.actions button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  margin: 0 5px;
}

.actions button:hover {
  background-color: #0056b3;
}

.logout-btn {
  background-color: #ff4e4e;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  position: absolute;
  top: 20px;
  right: 20px; /* Фиксация кнопки в правом верхнем углу */
}

.logout-btn:hover {
  background-color: #d43333;
}
</style>

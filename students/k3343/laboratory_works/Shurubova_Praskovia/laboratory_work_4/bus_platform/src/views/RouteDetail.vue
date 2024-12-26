<template>
  <div class="form-container">
    <h1>{{ isEditMode ? 'Редактировать маршрут' : 'Добавить новый маршрут' }}</h1>
    <form @submit.prevent="submitRoute">
      <div class="form-group">
        <label for="route_num">Номер маршрута:</label>
        <input v-model.number="routeData.route_num" id="route_num" type="number" placeholder="Введите номер маршрута" required />
      </div>

      <div class="form-group">
        <label for="start_point">Начальный пункт:</label>
        <input v-model="routeData.start_point" id="start_point" type="text" placeholder="Введите начальный пункт" required />
      </div>

      <div class="form-group">
        <label for="end_point">Конечный пункт:</label>
        <input v-model="routeData.end_point" id="end_point" type="text" placeholder="Введите конечный пункт" required />
      </div>

      <div class="form-group">
        <label for="start_time">Время начала:</label>
        <input v-model="routeData.start_time" id="start_time" type="time" required />
      </div>

      <div class="form-group">
        <label for="end_time">Время окончания:</label>
        <input v-model="routeData.end_time" id="end_time" type="time" required />
      </div>

      <div class="form-group">
        <label for="interval">Интервал (мин.):</label>
        <input v-model.number="routeData.interval" id="interval" type="number" placeholder="Введите интервал" required />
      </div>

      <div class="form-group">
        <label for="duration">Длительность (мин.):</label>
        <input v-model.number="routeData.duration" id="duration" type="number" placeholder="Введите длительность" required />
      </div>

      <div class="form-buttons">
        <button type="submit">{{ isEditMode ? 'Сохранить изменения' : 'Добавить маршрут' }}</button>
        <router-link to="/routes" class="back-to-list-btn">
          Вернуться к списку маршрутов
        </router-link>
      </div>
    </form>
  </div>
</template>

<script>
import apiClient from '@/api/axios';

export default {
  data() {
    return {
      isEditMode: false,
      routeData: {
        route_num: null,
        start_point: '',
        end_point: '',
        start_time: '',
        end_time: '',
        interval: null,
        duration: null,
      },
    };
  },
  async created() {
    const routeId = this.$route.params.id;
    if (routeId) {
      this.isEditMode = true;
      try {
        const response = await apiClient.get(`/routes/${routeId}/`);
        this.routeData = response.data;
      } catch (error) {
        console.error('Ошибка при загрузке маршрута:', error);
        alert('Не удалось загрузить данные маршрута.');
      }
    }
  },
  methods: {
    async submitRoute() {
      try {
        if (this.isEditMode) {

          const routeId = this.$route.params.id;
          await apiClient.put(`/routes/${routeId}/update/`, this.routeData);
          alert('Маршрут обновлен!');
        } else {

          await apiClient.post('/routes/create/', this.routeData);
          alert('Маршрут добавлен!');
        }
        this.$router.push('/routes');
      } catch (error) {
        console.error('Ошибка при сохранении маршрута:', error);
        alert('Не удалось сохранить маршрут. Попробуйте позже.');
      }
    },
  },
};
</script>

<style scoped>

html, body {
  height: 100%;
  margin: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.form-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  max-width: 1500px;
  width: 100%;
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  text-align: left;
}

h1 {
  font-size: 24px;
  color: #2C3643;
  margin-bottom: 30px;
  text-align: center;
}

.form-group {
  margin-bottom: 20px;
  width: 100%;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-size: 16px;
  color: #333;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 2px solid #2C3643;
  font-size: 14px;
  color: #2C3643;
  box-sizing: border-box;
}

.form-group input::placeholder,
.form-group select::placeholder {
  color: #aaa;
}


button, .back-to-list-btn {
  padding: 10px 20px;
  border-radius: 6px;
  background-color: #8ABEE5;
  color: black;
  border: none;
  cursor: pointer;
  font-size: 16px;
  max-width: 300px;
  margin-top: 20px;
  text-align: center;
}

button:hover, .back-to-list-btn:hover {
  background-color: #2C3643;
  color: white;
}

.form-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}

.back-to-list-btn {
  text-decoration: none;
  display: inline-block;
}
</style>

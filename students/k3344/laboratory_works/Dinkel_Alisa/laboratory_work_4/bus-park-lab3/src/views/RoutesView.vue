<template>
  <div class="container">
    <h1 class="text-center mb-4">Маршруты</h1>

    <!-- Общая продолжительность маршрутов -->
    <div class="mb-4 text-center">
      <h4>Общая продолжительность маршрутов: {{ totalRouteDuration }} минут</h4>
    </div>

    <!-- Адаптивная таблица -->
    <div class="table-responsive">
      <table class="table table-striped table-hover">
        <thead class="table-dark">
          <tr>
            <th>Номер маршрута</th>
            <th>Начальная точка</th>
            <th>Конечная точка</th>
            <th>Время начала</th>
            <th>Время конца</th>
            <th>Интервал (мин)</th>
            <th>Продолжительность (мин)</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="route in routes" :key="route.id">
            <td>{{ route.route_number }}</td>
            <td>{{ route.start_point }}</td>
            <td>{{ route.end_point }}</td>
            <td>{{ route.start_time }}</td>
            <td>{{ route.end_time }}</td>
            <td>{{ route.interval_minutes || 'Нет данных' }}</td>
            <td>{{ route.duration_minutes || 'Нет данных' }}</td>
            <td>
              <div class="action-buttons">
                <button @click="editBus(bus.id)" class="btn btn-primary btn-sm mx-1 rounded shadow-sm">
                  Редактировать
                </button>
                <button @click="deleteBus(bus.id)" class="btn btn-danger btn-sm mx-1 rounded shadow-sm">
                  Удалить
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Форма для добавления или редактирования маршрута -->
    <div class="form-container card p-4 mt-4 shadow-sm">
      <h2 class="text-center">{{ isEditing ? 'Редактировать маршрут' : 'Добавить новый маршрут' }}</h2>
      <form @submit.prevent="submitRoute">
        <div class="mb-3">
          <label for="route_number" class="form-label">Номер маршрута</label>
          <input v-model="newRoute.route_number" type="text" id="route_number" class="form-control" required>
        </div>
        <div class="mb-3">
          <label for="start_point" class="form-label">Начальная точка</label>
          <input v-model="newRoute.start_point" type="text" id="start_point" class="form-control" required>
        </div>
        <div class="mb-3">
          <label for="end_point" class="form-label">Конечная точка</label>
          <input v-model="newRoute.end_point" type="text" id="end_point" class="form-control" required>
        </div>
        <div class="mb-3">
          <label for="start_time" class="form-label">Время начала</label>
          <input v-model="newRoute.start_time" type="time" id="start_time" class="form-control" required>
        </div>
        <div class="mb-3">
          <label for="end_time" class="form-label">Время конца</label>
          <input v-model="newRoute.end_time" type="time" id="end_time" class="form-control" required>
        </div>
        <div class="mb-3">
          <label for="interval_minutes" class="form-label">Интервал (мин)</label>
          <input v-model="newRoute.interval_minutes" type="number" id="interval_minutes" class="form-control">
        </div>
        <div class="mb-3">
          <label for="duration_minutes" class="form-label">Продолжительность (мин)</label>
          <input v-model="newRoute.duration_minutes" type="number" id="duration_minutes" class="form-control">
        </div>
        <button type="submit" class="btn btn-success w-100">
          {{ isEditing ? 'Обновить' : 'Добавить' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { getRoutes, addRoute, getRouteById, updateRoute, deleteRoute, getTotalRouteDuration } from '@/api/api';

export default {
  data() {
    return {
      routes: [], // Список маршрутов
      newRoute: {
        route_number: '',
        start_point: '',
        end_point: '',
        start_time: '',
        end_time: '',
        interval_minutes: '',
        duration_minutes: ''
      },
      isEditing: false, // Флаг для редактирования
      routeToEdit: null, // ID маршрута для редактирования
      totalRouteDuration: 0
    };
  },
  mounted() {
    this.loadRoutes(); // Загружаем маршруты при монтировании компонента
    this.loadTotalRouteDuration();
  },
  methods: {
    // Загрузка всех маршрутов
    loadRoutes() {
      getRoutes()
        .then(response => {
          this.routes = response.data;
          console.log('Загруженные маршруты:', this.routes); // Лог для проверки
        })
        .catch(error => {
          console.error('Ошибка при загрузке маршрутов:', error);
        });
    },

    // Добавление нового маршрута или обновление существующего
    submitRoute() {
      if (this.isEditing) {
        this.updateRouteData(); // Обновляем данные маршрута
      } else {
        this.submitNewRoute(); // Добавляем новый маршрут
      }
    },

    // Добавление нового маршрута
    submitNewRoute() {
      addRoute(this.newRoute)
        .then(() => {
          this.loadRoutes(); // Обновляем список маршрутов после добавления
          this.resetForm(); // Очищаем форму
        })
        .catch(error => {
          console.error('Ошибка при добавлении маршрута:', error.response ? error.response.data : error.message);
        });
    },

    // Редактирование маршрута
    editRoute(id) {
      getRouteById(id)
        .then(response => {
          this.newRoute = { ...response.data }; // Заполняем форму данными маршрута для редактирования
          this.isEditing = true; // Устанавливаем флаг редактирования
          this.routeToEdit = id; // Сохраняем ID маршрута для редактирования
        })
        .catch(error => {
          console.error('Ошибка при получении данных маршрута:', error);
        });
    },

    // Обновление данных маршрута
    updateRouteData() {
      updateRoute(this.routeToEdit, this.newRoute)
        .then(() => {
          this.loadRoutes(); // Обновляем список маршрутов после обновления
          this.resetForm(); // Очищаем форму
        })
        .catch(error => {
          console.error('Ошибка при обновлении данных маршрута:', error);
        });
    },

    // Удаление маршрута
    deleteRoute(id) {
      deleteRoute(id)
        .then(() => {
          this.loadRoutes(); // Обновляем список маршрутов после удаления
        })
        .catch(error => {
          console.error('Ошибка при удалении маршрута:', error);
        });
    },

    loadTotalRouteDuration() {
      getTotalRouteDuration()
        .then(response => {
          this.totalRouteDuration = response.data.total_route_duration || 0;
        })
        .catch(error => {
          console.error('Ошибка при загрузке общей продолжительности маршрутов:', error);
        });
    },

    // Сброс формы
    resetForm() {
      this.newRoute = {
        route_number: '',
        start_point: '',
        end_point: '',
        start_time: '',
        end_time: '',
        interval_minutes: '',
        duration_minutes: ''
      }; // Очистить форму
      this.isEditing = false; // Сбросить флаг редактирования
      this.routeToEdit = null; // Очистить данные редактируемого маршрута
    }
  }
};
</script>

<style scoped>
.container {
  margin-top: 20px;
}

.form-container {
  margin-top: 30px;
}

table {
  margin-bottom: 30px;
}

.btn {
  transition: all 0.2s ease-in-out;
}

.btn:hover {
  transform: scale(1.05);
}
</style>

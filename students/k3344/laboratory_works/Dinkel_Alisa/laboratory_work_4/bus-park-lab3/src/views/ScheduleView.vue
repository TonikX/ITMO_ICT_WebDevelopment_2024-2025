<template>
  <div class="container">
    <h1 class="text-center mb-4">Смены</h1>

    <!-- Адаптивная таблица -->
    <div class="table-responsive">
      <table class="table table-striped table-hover">
        <thead class="table-dark">
          <tr>
            <th>Водитель</th>
            <th>Автобус</th>
            <th>Маршрут</th>
            <th>Дата смены</th>
            <th>Время начала</th>
            <th>Время конца</th>
            <th>Статус</th>
            <th>Причина</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="shift in shifts" :key="shift.id">
            <td>{{ getDriverName(shift.driver) }}</td>
            <td>{{ getBusNumber(shift.bus) }}</td>
            <td>{{ getRouteNumber(shift.route) }}</td>
            <td>{{ shift.shift_date }}</td>
            <td>{{ shift.start_time }}</td>
            <td>{{ shift.end_time }}</td>
            <td>{{ getStatusLabel(shift.status) }}</td>
            <td>{{ shift.reason || '—' }}</td> <!-- Показываем причину, если она есть -->
            <td>
              <div class="action-buttons">
                <button @click="editShift(shift.id)" class="btn btn-primary btn-sm mx-1 rounded shadow-sm">
                  Редактировать
                </button>
                <button @click="deleteShift(shift.id)" class="btn btn-danger btn-sm mx-1 rounded shadow-sm">
                  Удалить
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Форма для добавления или редактирования смены -->
    <div class="form-container card p-4 mt-4 shadow-sm">
      <h2 class="text-center">{{ isEditing ? 'Редактировать смену' : 'Добавить новую смену' }}</h2>
      <form @submit.prevent="submitShift">
        <div class="mb-3">
          <label for="driver" class="form-label">Водитель</label>
          <select v-model="newShift.driver" id="driver" class="form-select" required>
            <option disabled value="">Выберите водителя</option>
            <option v-for="driver in drivers" :key="driver.id" :value="driver.id">
              {{ driver.full_name }}
            </option>
          </select>
        </div>
        <div class="mb-3">
          <label for="bus" class="form-label">Автобус</label>
          <select v-model="newShift.bus" id="bus" class="form-select" required>
            <option disabled value="">Выберите автобус</option>
            <option v-for="bus in buses" :key="bus.id" :value="bus.id">
              {{ bus.registration_number }}
            </option>
          </select>
        </div>
        <div class="mb-3">
          <label for="route" class="form-label">Маршрут</label>
          <select v-model="newShift.route" id="route" class="form-select" required>
            <option disabled value="">Выберите маршрут</option>
            <option v-for="route in routes" :key="route.id" :value="route.id">
              {{ route.route_number }}
            </option>
          </select>
        </div>
        <div class="mb-3">
          <label for="shift_date" class="form-label">Дата смены</label>
          <input v-model="newShift.shift_date" type="date" id="shift_date" class="form-control" required>
        </div>
        <div class="mb-3">
          <label for="start_time" class="form-label">Время начала</label>
          <input v-model="newShift.start_time" type="time" id="start_time" class="form-control" required>
        </div>
        <div class="mb-3">
          <label for="end_time" class="form-label">Время конца</label>
          <input v-model="newShift.end_time" type="time" id="end_time" class="form-control" required>
        </div>
        <div class="mb-3">
          <label for="status" class="form-label">Статус</label>
          <select v-model="newShift.status" id="status" class="form-control" required>
            <option value="Active">Отработано</option>
            <option value="Breakdown">Поломка автобуса</option>
            <option value="No Driver">Нет водителя</option>
          </select>
        </div>
        <div class="mb-3">
          <label for="reason" class="form-label">Причина</label>
          <textarea v-model="newShift.reason" id="reason" class="form-control"></textarea>
        </div>
        <button type="submit" class="btn btn-success w-100">
          {{ isEditing ? 'Обновить' : 'Добавить' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { getShifts, addShift, getShiftById, updateShift, deleteShift, getDrivers, getBuses, getRoutes } from '@/api/api';

export default {
  data() {
    return {
      shifts: [], // Список смен
      drivers: [], // Список водителей
      buses: [], // Список автобусов
      routes: [], // Список маршрутов
      newShift: {
        driver: '',
        bus: '',
        route: '',
        shift_date: '',
        start_time: '',
        end_time: '',
        status: 'Active',
        reason: ''
      },
      isEditing: false, // Флаг для редактирования
      shiftToEdit: null // ID смены для редактирования
    };
  },
  mounted() {
    this.loadShifts(); // Загружаем смены при монтировании компонента
    this.loadDrivers(); // Загружаем водителей
    this.loadBuses(); // Загружаем автобусы
    this.loadRoutes(); // Загружаем маршруты
  },
  methods: {
    loadShifts() {
      getShifts()
        .then(response => {
          this.shifts = response.data;
        })
        .catch(error => {
          console.error('Ошибка при загрузке смен:', error);
        });
    },
    loadDrivers() {
      getDrivers()
        .then(response => {
          this.drivers = response.data;
        })
        .catch(error => {
          console.error('Ошибка при загрузке водителей:', error);
        });
    },
    loadBuses() {
      getBuses()
        .then(response => {
          this.buses = response.data;
        })
        .catch(error => {
          console.error('Ошибка при загрузке автобусов:', error);
        });
    },
    loadRoutes() {
      getRoutes()
        .then(response => {
          this.routes = response.data;
        })
        .catch(error => {
          console.error('Ошибка при загрузке маршрутов:', error);
        });
    },
    submitShift() {
      if (this.isEditing) {
        this.updateShiftData(); // Обновляем данные смены
      } else {
        this.submitNewShift(); // Добавляем новую смену
      }
    },
    submitNewShift() {
      addShift(this.newShift)
        .then(() => {
          this.loadShifts(); // Обновляем список смен после добавления
          this.resetForm(); // Очищаем форму
        })
        .catch(error => {
          console.error('Ошибка при добавлении смены:', error.response ? error.response.data : error.message);
        });
    },

    editShift(id) {
      getShiftById(id)
        .then(response => {
          this.newShift = { ...response.data }; // Заполняем форму данными смены для редактирования
          this.isEditing = true; // Устанавливаем флаг редактирования
          this.shiftToEdit = id; // Сохраняем ID смены для редактирования
        })
        .catch(error => {
          console.error('Ошибка при получении данных смены:', error);
        });
    },
    updateShiftData() {
      updateShift(this.shiftToEdit, this.newShift)
        .then(() => {
          this.loadShifts(); // Обновляем список смен после обновления
          this.resetForm(); // Очищаем форму
        })
        .catch(error => {
          console.error('Ошибка при обновлении данных смены:', error);
        });
    },
    deleteShift(id) {
      deleteShift(id)
        .then(() => {
          this.loadShifts(); // Обновляем список смен после удаления
        })
        .catch(error => {
          console.error('Ошибка при удалении смены:', error);
        });
    },
    getDriverName(driverId) {
      const driver = this.drivers.find(d => d.id === driverId);
      return driver ? driver.full_name : 'Неизвестный водитель';
    },
    getBusNumber(busId) {
      const bus = this.buses.find(b => b.id === busId);
      return bus ? bus.registration_number : 'Неизвестный автобус';
    },
    getRouteNumber(routeId) {
      const route = this.routes.find(r => r.id === routeId);
      return route ? route.route_number : 'Неизвестный маршрут';
    },
    getStatusLabel(status) {
      const statusMap = {
        'Active': 'Отработано',
        'Breakdown': 'Поломка автобуса',
        'No Driver': 'Нет водителя'
      };
      return statusMap[status] || status; // Если вдруг появится неизвестный статус, вернем его как есть
    },
    resetForm() {
      this.newShift = {
        driver: '',
        bus: '',
        route: '',
        shift_date: '',
        start_time: '',
        end_time: '',
        status: 'Active',
        reason: ''
      };
      this.isEditing = false;
      this.shiftToEdit = null;
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

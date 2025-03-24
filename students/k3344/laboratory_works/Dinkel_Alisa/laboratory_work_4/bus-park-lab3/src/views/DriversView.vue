<template>
  <div class="container">
    <h1 class="text-center mb-4">Водители</h1>

  <!-- Раздел для отображения количества водителей по категориям -->
    <h3 class="text-center">Количество водителей по категориям</h3>
    <table class="table table-bordered">
      <thead class="table-dark">
        <tr>
          <th>Класс водителя</th>
          <th>Количество</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="category in driverCategoryCount" :key="category.driver_class">
          <td>{{ category.driver_class }}</td>
          <td>{{ category.count }}</td>
        </tr>
      </tbody>
    </table>

    <!-- Адаптивная таблица с водителями -->
    <h3 class="text-center">Список водителей</h3>
    <div class="table-responsive">
      <table class="table table-striped table-hover">
        <thead class="table-dark">
          <tr>
            <th>ID</th>
            <th>ФИО</th>
            <th>Класс</th>
            <th>Стаж</th>
            <th>Оклад</th>
            <th>Паспортные данные</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="driver in drivers" :key="driver.id">
            <td>{{ driver.id }}</td>
            <td>{{ driver.full_name }}</td>
            <td>{{ driver.driver_class }}</td>
            <td>{{ driver.experience }} лет</td>
            <td>{{ driver.salary }} руб.</td>
            <td>{{ driver.passport_number }}</td>
            <td>
              <div class="action-buttons">
                <button @click="editDriver(driver.id)" class="btn btn-primary btn-sm mx-1 rounded shadow-sm">
                  Редактировать
                </button>
                <button @click="deleteDriver(driver.id)" class="btn btn-danger btn-sm mx-1 rounded shadow-sm">
                  Удалить
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Форма для добавления или редактирования водителя -->
    <div class="form-container card p-4 mt-4 shadow-sm">
      <h2 class="text-center">{{ isEditing ? 'Редактировать водителя' : 'Добавить нового водителя' }}</h2>
      <form @submit.prevent="submitDriver">
        <div class="mb-3">
          <label for="full_name" class="form-label">ФИО</label>
          <input v-model="newDriver.full_name" type="text" id="full_name" class="form-control" required>
        </div>
        <div class="mb-3">
          <label for="driver_class" class="form-label">Класс</label>
          <select v-model="newDriver.driver_class" id="driver_class" class="form-select" required>
            <option disabled value="">Выберите класс</option>
            <option value="I">I класс</option>
            <option value="II">II класс</option>
            <option value="III">III класс</option>
          </select>
        </div>
        <div class="mb-3">
          <label for="experience" class="form-label">Стаж</label>
          <input v-model="newDriver.experience" type="number" id="experience" class="form-control" required>
        </div>
        <div class="mb-3">
          <label for="passport_number" class="form-label">Паспортные данные</label>
          <input v-model="newDriver.passport_number" type="text" id="passport_number" class="form-control" required>
        </div>
        <button type="submit" class="btn btn-success w-100">
          {{ isEditing ? 'Обновить' : 'Добавить' }}
        </button>
      </form>
    </div>
  </div>
</template>


<script>
import { getDrivers, addDriver, getDriverById, updateDriver, deleteDriver, getDriverCategoryCount } from '@/api/api';

export default {
  data() {
    return {
      drivers: [], // Список водителей
      driverCategoryCount: [], // Данные о количестве водителей по категориям
      newDriver: {
        full_name: '',
        driver_class: '',
        experience: '',
        passport_number: '',
      },
      isEditing: false,
      driverToEdit: null,
    };
  },
  mounted() {
    this.loadDrivers();
    this.loadDriverCategoryCount(); // Загружаем данные о категориях
  },
  methods: {
    // Загрузка всех водителей
    loadDrivers() {
      getDrivers()
        .then(response => {
          this.drivers = response.data;
        })
        .catch(error => {
          console.error('Ошибка при загрузке водителей:', error);
        });
    },

    // Загрузка данных о количестве водителей по категориям
    loadDriverCategoryCount() {
      getDriverCategoryCount()
        .then(response => {
          this.driverCategoryCount = response.data.drivers_by_category; // Сохраняем данные в массив
        })
        .catch(error => {
          console.error('Ошибка при загрузке данных о категориях водителей:', error);
        });
    },

    // Добавление нового водителя или обновление существующего
    submitDriver() {
      if (this.isEditing) {
        this.updateDriverData(); // Обновляем данные водителя
      } else {
        this.submitNewDriver(); // Добавляем нового водителя
      }
    },

    // Добавление нового водителя
    submitNewDriver() {
      addDriver(this.newDriver)
        .then(() => {
          this.loadDrivers(); // Обновляем список водителей после добавления
          this.resetForm(); // Очищаем форму
        })
        .catch(error => {
          console.error('Ошибка при добавлении водителя:', error);
        });
    },

    // Редактирование водителя
    editDriver(id) {
      getDriverById(id)
        .then(response => {
          this.newDriver = { ...response.data }; // Заполняем форму данными водителя для редактирования
          this.isEditing = true; // Устанавливаем флаг редактирования
          this.driverToEdit = id; // Сохраняем ID водителя для редактирования
        })
        .catch(error => {
          console.error('Ошибка при получении данных водителя:', error);
        });
    },

    // Обновление данных водителя
    updateDriverData() {
      updateDriver(this.driverToEdit, this.newDriver)
        .then(() => {
          this.loadDrivers(); // Обновляем список водителей после обновления
          this.resetForm(); // Очищаем форму
        })
        .catch(error => {
          console.error('Ошибка при обновлении данных водителя:', error);
        });
    },

    // Удаление водителя
    deleteDriver(id) {
      deleteDriver(id)
        .then(() => {
          this.loadDrivers(); // Обновляем список водителей после удаления
        })
        .catch(error => {
          console.error('Ошибка при удалении водителя:', error);
        });
    },

    // Сброс формы
    resetForm() {
      this.newDriver = { full_name: '', driver_class: '', experience: '', passport_number: '' }; // Очистить форму
      this.isEditing = false; // Сбросить флаг редактирования
      this.driverToEdit = null; // Очистить данные редактируемого водителя
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

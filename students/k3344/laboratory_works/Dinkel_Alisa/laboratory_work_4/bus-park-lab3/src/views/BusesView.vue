<template>
  <div class="container">
    <h1 class="text-center mb-4">Автобусы</h1>

    <!-- Адаптивная таблица -->
    <div class="table-responsive">
      <table class="table table-striped table-hover">
        <thead class="table-dark">
          <tr>
            <th>ID</th>
            <th>Рег. номер</th>
            <th>Категория</th>
            <th>Вместимость</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="bus in buses" :key="bus.id">
            <td>{{ bus.id }}</td>
            <td>{{ bus.registration_number }}</td>
            <td>{{ getCategoryName(bus.category) }}</td>
            <td>{{ bus.capacity }} мест</td>
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

    <!-- Форма для добавления или редактирования автобуса -->
    <div class="form-container card p-4 mt-4 shadow-sm">
      <h2 class="text-center">{{ isEditing ? 'Редактировать автобус' : 'Добавить новый автобус' }}</h2>
      <form @submit.prevent="submitBus">
        <div class="mb-3">
          <label for="registration_number" class="form-label">Рег. номер</label>
          <input v-model="newBus.registration_number" type="text" id="registration_number" class="form-control" required>
        </div>
        <div class="mb-3">
          <label for="category" class="form-label">Категория</label>
          <select v-model="newBus.category" id="category" class="form-select" required>
            <option disabled value="">Выберите категорию</option>
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }} ({{ category.capacity }} мест)
            </option>
          </select>
        </div>
        <button type="submit" class="btn btn-success w-100">
          {{ isEditing ? 'Обновить' : 'Добавить' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import { getBuses, addBus, getBusById, updateBus, deleteBus } from '@/api/api';
import { getBusCategories } from '@/api/api';

export default {
  data() {
    return {
      buses: [], // Список автобусов
      categories: [], // Список категорий автобусов
      newBus: {
        registration_number: '',
        category: '',
      },
      isEditing: false, // Флаг для редактирования
      busToEdit: null, // Данные автобуса, который редактируем
    };
  },
  mounted() {
    this.loadBuses(); // Загружаем автобусы при монтировании компонента
    this.loadCategories(); // Загружаем категории автобусов
  },
  methods: {
    // Загрузка всех автобусов
    loadBuses() {
      getBuses()
        .then(response => {
          this.buses = response.data;
          console.log('Загруженные автобусы:', this.buses); // Лог для проверки
        })
        .catch(error => {
          console.error('Ошибка при загрузке автобусов:', error);
        });
    },

    // Загрузка категорий автобусов
    loadCategories() {
      getBusCategories()
        .then(response => {
          this.categories = response.data;
          console.log('Загруженные категории:', this.categories); // Лог для проверки
        })
        .catch(error => {
          console.error('Ошибка при загрузке категорий:', error);
        });
    },

    // Добавление нового автобуса или обновление существующего
    submitBus() {
      if (this.isEditing) {
        this.updateBusData(); // Обновляем данные автобуса
      } else {
        this.submitNewBus(); // Добавляем новый автобус
      }
    },

    // Добавление нового автобуса
    submitNewBus() {
      addBus(this.newBus)
        .then(() => {
          this.loadBuses(); // Обновляем список автобусов после добавления
          this.resetForm(); // Очищаем форму
        })
        .catch(error => {
          console.error('Ошибка при добавлении автобуса:', error.response ? error.response.data : error.message);
        });
    },

    // Редактирование автобуса
    editBus(id) {
      getBusById(id)
        .then(response => {
          this.newBus = { ...response.data }; // Заполняем форму данными автобуса для редактирования
          this.isEditing = true; // Устанавливаем флаг редактирования
          this.busToEdit = id; // Сохраняем ID автобуса для редактирования
        })
        .catch(error => {
          console.error('Ошибка при получении данных автобуса:', error);
        });
    },

    // Обновление данных автобуса
    updateBusData() {
      updateBus(this.busToEdit, this.newBus)
        .then(() => {
          this.loadBuses(); // Обновляем список автобусов после обновления
          this.resetForm(); // Очищаем форму
        })
        .catch(error => {
          console.error('Ошибка при обновлении данных автобуса:', error);
        });
    },

    // Удаление автобуса
    deleteBus(id) {
      deleteBus(id)
        .then(() => {
          this.loadBuses(); // Обновляем список автобусов после удаления
        })
        .catch(error => {
          console.error('Ошибка при удалении автобуса:', error);
        });
    },

    // Метод для получения названия категории по ID
    getCategoryName(categoryId) {
      const category = this.categories.find(cat => cat.id === categoryId);
      return category ? category.name : 'Неизвестная категория';
    },

    // Сброс формы
    resetForm() {
      this.newBus = { registration_number: '', category: '' }; // Очистить форму
      this.isEditing = false; // Сбросить флаг редактирования
      this.busToEdit = null; // Очистить данные редактируемого автобуса
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

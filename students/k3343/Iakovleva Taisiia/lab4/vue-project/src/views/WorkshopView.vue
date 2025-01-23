<template>
  <div>
    <Header />
    <h3 class="table-header">Список цехов</h3>
    <div class="table-container">
    <table class="styled-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Название</th>
          <th>Вместимость</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="workshop in workshops" :key="workshop.id">
          <td>{{ workshop.id }}</td>
          <td>{{ workshop.title }}</td>
          <td>{{ workshop.capacity }}</td>
          <td>
            <button @click="deleteWorkshop(workshop.id)" class="btn btn-danger">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
</template>

<script>
import Header from '@/components/Header.vue';
import apiClient from '@/api/axios';

export default {
  components: {
    Header,
  },
  data() {
    return {
      workshops: [],
      showAddForm: false,
      selectedWorkshop: null,
      formData: {
        title: '',
        capacity: '',
      },
    };
  },
  async created() {
    await this.loadWorkshops();
  },
  methods: {
    async loadWorkshops() {
      try {
        const response = await apiClient.get('/manufactory/workshops');
        this.workshops = response.data;
      } catch (error) {
        console.error('Ошибка при загрузке цехов:', error);
        alert('Не удалось загрузить цехи.');
      }
    },
    async deleteWorkshop(id) {
      try {
        if (confirm('Вы уверены, что хотите удалить этот цех?')) {
          await apiClient.delete(`/manufactory/workshops/${id}/`);
          this.workshops = this.workshops.filter((workshop) => workshop.id !== id);
        }
      } catch (error) {
        console.error('Ошибка при удалении цеха:', error);
        alert('Не удалось удалить цех.');
      }
    },
  },
};
</script>

<style scoped>
.table-container {
  padding: 20px; /* Отступы вокруг таблицы */
  margin: 0 auto; /* Центрирование таблицы */
  max-width: 1200px; /* Ограничение ширины */
  box-sizing: border-box; /* Учёт padding в ширине */
}

.styled-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 16px;
  background-color: #ffffff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

.styled-table th,
.styled-table td {
  padding: 12px 15px;
  border: 1px solid #ddd;
  text-align: center;
}

.styled-table th {
  background-color: #085d88;
  color: #ffffff;
  font-weight: bold;
}

.styled-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.styled-table tr:hover {
  background-color: #eef7fc;
}

.table-header {
  font-size: 26px;
  margin: 20px auto;
  text-align: center;
  font-weight: bold;
  color: #4a4a4a;
}

.table-controls {
  display: flex;
  justify-content: flex-start; /* Кнопка слева */
  margin-bottom: 20px;
}

.btn {
  padding: 8px 16px;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: #04b922;
  color: #ffffff;
}

.btn-primary:hover {
  background-color: #01720a;
}

.btn-warning {
  background-color: #ffc107;
  color: black;
}

.btn-warning:hover {
  background-color: #e0a800;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
}

.btn-danger:hover {
  background-color: #b02a37;
}

.main-content {
  padding: 20px; /* Отступы вокруг основного содержимого */
  margin: 0 auto;
  max-width: 1200px; /* Ограничение ширины */
  background-color: #f8f9fa;
}

@media (max-width: 768px) {
  .styled-table th,
  .styled-table td {
    padding: 10px;
    font-size: 14px;
  }

  .btn {
    font-size: 14px;
    padding: 8px 16px;
  }

  .table-header {
    font-size: 20px;
  }
}

</style>

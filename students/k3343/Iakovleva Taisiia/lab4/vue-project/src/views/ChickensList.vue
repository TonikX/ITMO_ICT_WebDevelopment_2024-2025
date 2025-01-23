<template>
  <div>
    <Header />
    <h3 class="table-header">Список кур</h3>
    <div class="table-container">

    <div class="table-controls">
      <button @click="showAddForm = true" class="btn btn-primary">Добавить курицу</button>
    </div>

    <!-- Таблица для отображения списка кур -->
    <table class="styled-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Порода</th>
          <th>Вес</th>
          <th>Возраст</th>
          <th>Яичная продуктивность (в месяц)</th>
          <th>Цех</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="chicken in chickens" :key="chicken.id">
          <td>{{ chicken.id }}</td>
          <td>{{ chicken.breed.name }}</td>
          <td>{{ chicken.weight }}</td>
          <td>{{ chicken.age }}</td>
          <td>{{ chicken.egg_performance_month }}</td>
          <td>{{ chicken.cell.workshop.title }}</td>
          <td>
            <button @click="editChicken(chicken)" class="btn btn-warning">Редактировать</button>
            <button @click="deleteChicken(chicken.id)" class="btn btn-danger">Удалить</button>
          </td>
        </tr>
        <tr v-if="!chickens.length">
          <td colspan="7">Нет данных о курах.</td>
        </tr>
      </tbody>
    </table>
  </div>

    <!-- Форма добавления/редактирования курицы -->
    <div v-if="showAddForm || selectedChicken" class="form-modal">
      <div class="modal-overlay">
        <div class="modal-content">
          <h2>{{ selectedChicken ? 'Редактировать курицу' : 'Добавить курицу' }}</h2>
          <form @submit.prevent="saveChicken">
            <div class="form-group">
              <label for="breed" class="form-label">Порода:</label>
              <select v-model="formData.breed" id="breed" class="form-control">
                <option v-for="breed in breeds" :key="breed.id" :value="breed.id">
                  {{ breed.name }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label for="weight" class="form-label">Вес:</label>
              <input v-model="formData.weight" type="number" id="weight" class="form-control" required />
            </div>

            <div class="form-group">
              <label for="age" class="form-label">Возраст:</label>
              <input v-model="formData.age" type="number" id="age" class="form-control" required />
            </div>

            <div class="form-group">
              <label for="egg_performance_month" class="form-label">Яичная продуктивность (в месяц):</label>
              <input v-model="formData.egg_performance_month" type="number" id="egg_performance_month" class="form-control" required />
            </div>

            <div class="form-group">
              <label for="cell" class="form-label">Цех:</label>
              <select v-model="formData.cell" id="cell" class="form-control">
                <option v-for="cell in cells" :key="cell.cell_code" :value="cell.cell_code">
                  {{ cell.workshop.title }} - {{ cell.cell_code }}
                </option>
              </select>
            </div>

            <div class="form-actions">
              <button type="submit" class="btn btn-primary">
                {{ selectedChicken ? "Сохранить изменения" : "Добавить" }}
              </button>
              <button type="button" @click="cancelEdit" class="btn btn-secondary">Отмена</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from "@/components/Header.vue";
import apiClient from "@/api/axios";

export default {
  components: {
    Header,
  },
  data() {
    return {
      chickens: [],
      breeds: [],
      cells: [],
      showAddForm: false,
      selectedChicken: null,
      formData: {
        breed: null,
        weight: "",
        age: "",
        egg_performance_month: "",
        cell: null,
      },
    };
  },
  async created() {
    await this.loadChickens();
    await this.loadBreeds();
    await this.loadCells();
  },
  methods: {
    async loadChickens() {
      try {
        const response = await apiClient.get("/manufactory/chicken/");
        this.chickens = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке кур:", error);
        alert("Не удалось загрузить кур.");
      }
    },
    async loadBreeds() {
      try {
        const response = await apiClient.get("/manufactory/breeds/");
        this.breeds = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке пород:", error);
        alert("Не удалось загрузить породы.");
      }
    },
    async loadCells() {
      try {
        const response = await apiClient.get("/manufactory/cells/");
        console.log("Данные ячеек:", response.data); // Убедитесь, что есть id
        this.cells = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке ячеек:", error);
        alert("Не удалось загрузить ячейки.");
      }
    },
    async saveChicken() {
      console.log("Данные для отправки:", this.formData); // Логирование данных
      try {
        if (this.selectedChicken) {
          await apiClient.put(`/manufactory/chicken/${this.selectedChicken.id}/`, this.formData);
          alert("Изменения сохранены.");
        } else {
          await apiClient.post("/manufactory/chicken/", this.formData);
          alert("Курица добавлена.");
        }
        await this.loadChickens();
        this.cancelEdit();
      } catch (error) {
        console.log(this.formData);
        console.error("Ошибка при сохранении курицы:", error);
        alert("Не удалось сохранить изменения.");
      }
    },
    async deleteChicken(id) {
      try {
        if (confirm("Вы уверены, что хотите удалить эту курицу?")) {
          await apiClient.delete(`/manufactory/chicken/${id}/`);
          this.chickens = this.chickens.filter((chicken) => chicken.id !== id);
        }
      } catch (error) {
        console.error("Ошибка при удалении курицы:", error);
        alert("Не удалось удалить курицу.");
      }
    },
    editChicken(chicken) {
      this.selectedChicken = chicken;
      this.formData = {
        weight: chicken.weight,
        age: chicken.age,
        breed: chicken.breed.id, 
        egg_performance_month: chicken.egg_performance_month,
        cell: chicken.cell_code
      };
      console.log("Данные формы при редактировании:", this.formData);

    },
    cancelEdit() {
      this.selectedChicken = null;
      this.showAddForm = false;
      this.formData = {
        breed: null,
        weight: "",
        age: "",
        egg_performance_month: "",
        cell: null,
      };
    },
  },
};
</script>

<style scoped>
  .table-header {
  text-align: center;
  font-size: 26px;
  font-weight: bold;
  margin: 30px 0;
  color: #4a4a4a;
}

.table-controls {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}

.table-container {
  overflow-x: auto;
  margin: 0 auto;
  max-width: 1200px;
}

.styled-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 16px;
  background-color: #ffffff;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

.styled-table th, .styled-table td {
  padding: 12px 20px;
  border: 1px solid #e0e0e0;
  text-align: center;
}

.styled-table th {
  background-color: #086f99;
  color: #ffffff;
  font-weight: bold;
}

.styled-table tr:nth-child(even) {
  background-color: #f8f8f8;
}

.styled-table tr:hover {
  background-color: #eef7fc;
}

.btn {
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background-color: #28a745;
  color: #ffffff;
}

.btn-primary:hover {
  background-color: #218838;
}

.btn-warning {
  background-color: #ffc107;
  color: #212529;
}

.btn-warning:hover {
  background-color: #e0a800;
}

.btn-danger {
  background-color: #dc3545;
  color: #ffffff;
}

.btn-danger:hover {
  background-color: #c82333;
}

.form-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
}

.modal-content {
  background-color: #ffffff;
  padding: 25px 30px;
  border-radius: 10px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  max-width: 600px;
  width: 100%;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #333333;
}

.form-group input, .form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #cccccc;
  border-radius: 5px;
  font-size: 16px;
  box-sizing: border-box;
}

.form-group input:focus, .form-group select:focus {
  outline: none;
  border-color: #086f99;
  box-shadow: 0 0 4px rgba(8, 111, 153, 0.5);
}

.form-actions {
  display: flex;
  justify-content: space-between;
  gap: 15px;
  margin-top: 20px;
}

@media (max-width: 768px) {
  .styled-table th, .styled-table td {
    padding: 10px;
    font-size: 14px;
  }

  .btn {
    font-size: 14px;
    padding: 8px 16px;
  }

  .modal-content {
    padding: 20px;
  }

  .form-group input, .form-group select {
    padding: 8px;
    font-size: 14px;
  }
}
  </style>
  
<template>
    <div>
      <Header />
      <h3 class="table-header">Список диет</h3>
      <div class="table-container">
      <div class="table-controls">
        <button @click="showAddForm = true" class="btn btn-primary">Добавить диету</button>
      </div>
  
      <!-- Таблица для отображения списка диет -->
      <table class="styled-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Описание</th>
            <th>Сезон</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="diet in diets" :key="diet.id">
            <td>{{ diet.id }}</td>
            <td>{{ diet.description }}</td>
            <td>{{ diet.season }}</td>
            <td>
              <button @click="editDiet(diet)" class="btn btn-warning">Редактировать</button>
              <button @click="deleteDiet(diet.id)" class="btn btn-danger">Удалить</button>
            </td>
          </tr>
          <tr v-if="!diets.length">
            <td colspan="4">Нет данных о диетах.</td>
          </tr>
        </tbody>
      </table>
    </div>
  
      <!-- Форма добавления/редактирования диеты -->
      <div v-if="showAddForm || selectedDiet" class="form-modal">
        <div class="modal-overlay">
          <div class="modal-content">
            <h2>{{ selectedDiet ? 'Редактировать диету' : 'Добавить диету' }}</h2>
            <form @submit.prevent="saveDiet">
              <div class="form-group">
                <label for="description" class="form-label">Описание:</label>
                <textarea
                  v-model="formData.description"
                  id="description"
                  class="form-control"
                  rows="3"
                  required
                ></textarea>
              </div>
  
              <div class="form-group">
                <label for="season" class="form-label">Сезон:</label>
                <input v-model="formData.season" type="text" id="season" class="form-control" required />
              </div>
  
              <div class="form-actions">
                <button type="submit" class="btn btn-primary">
                  {{ selectedDiet ? "Сохранить изменения" : "Добавить" }}
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
        diets: [],
        showAddForm: false,
        selectedDiet: null,
        formData: {
          description: "",
          season: "",
        },
      };
    },
    async created() {
      await this.loadDiets();
    },
    methods: {
      async loadDiets() {
        try {
          const response = await apiClient.get("/manufactory/diets/");
          this.diets = response.data;
        } catch (error) {
          console.error("Ошибка при загрузке диет:", error);
          alert("Не удалось загрузить диеты.");
        }
      },
      async saveDiet() {
        try {
          console.log(this.selectedDiet)
          if (this.selectedDiet) {
            // Если редактируется существующая диета
            await apiClient.put(`/manufactory/diets/${this.selectedDiet.id}`, {
              description: this.formData.description,
              season: this.formData.season,
            });
            alert("Изменения сохранены.");
          } else {
            // Если создаётся новая диета
            await apiClient.post("/manufactory/diets/", {
              description: this.formData.description,
              season: this.formData.season,
            });
            alert("Диета добавлена.");
          }
          await this.loadDiets();
          this.cancelEdit();
        } catch (error) {
          console.error("Ошибка при сохранении диеты:", error);
          alert("Не удалось сохранить изменения.");
        }
      },
      async deleteDiet(id) {
        try {
          if (confirm("Вы уверены, что хотите удалить эту диету?")) {
            await apiClient.delete(`/manufactory/diets/${id}`);
            this.diets = this.diets.filter((diet) => diet.id !== id);
          }
        } catch (error) {
          console.error("Ошибка при удалении диеты:", error);
          alert("Не удалось удалить диету.");
        }
      },
      editDiet(diet) {
        this.selectedDiet = diet;
        this.formData = { ...diet };
      },
      cancelEdit() {
        this.selectedDiet = null;
        this.showAddForm = false;
        this.formData = {
          description: "",
          season: "",
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
  
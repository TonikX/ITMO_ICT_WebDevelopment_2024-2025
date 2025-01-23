<template>
    <div class="page-container">
      <Header />
      <h3 class="table-header">Список пород</h3>
      <div class="table-container">
      <div class="table-controls">
        <button @click="showAddForm = true" class="btn btn-primary">Добавить породу</button>
      </div>
  
      
        <table class="styled-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Название</th>
              <th>Средняя яйценоскость</th>
              <th>Средний вес</th>
              <th>Номер рациона</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="breed in breeds" :key="breed.id">
              <td>{{ breed.id }}</td>
              <td>{{ breed.name }}</td>
              <td>{{ breed.egg_performance_avg }}</td>
              <td>{{ breed.weight_avg }}</td>
              <td>{{ breed.diet_number.description }}</td>
              <td>
                <button @click="editBreed(breed)" class="btn btn-warning">Редактировать</button>
                <button @click="deleteBreed(breed.id)" class="btn btn-danger">Удалить</button>
              </td>
            </tr>
            <tr v-if="!breeds.length">
              <td colspan="6">Нет доступных пород.</td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <div v-if="showAddForm || selectedBreed" class="form-modal">
        <div class="modal-overlay">
          <div class="modal-content">
            <h2>{{ selectedBreed ? "Редактировать породу" : "Добавить породу" }}</h2>
            <form @submit.prevent="saveBreed">
              <div class="form-group">
                <label for="name">Название:</label>
                <input v-model="formData.name" type="text" id="name" class="form-control" required />
              </div>
  
              <div class="form-group">
                <label for="egg_performance_avg">Средняя яйценоскость:</label>
                <input v-model="formData.egg_performance_avg" type="number" id="egg_performance_avg" class="form-control" required />
              </div>
  
              <div class="form-group">
                <label for="weight_avg">Средний вес:</label>
                <input v-model="formData.weight_avg" type="number" step="0.1" id="weight_avg" class="form-control" required />
              </div>
  
              <div class="form-group">
                <label for="diet_number">Рацион:</label>
                <select v-model="formData.diet_number" id="diet_number" class="form-control">
                  <option v-for="diet in diets" :key="diet.id" :value="diet.id">
                    {{ diet.description }}
                  </option>
                </select>
              </div>
  
              <div class="form-actions">
                <button type="submit" class="btn btn-primary">
                  {{ selectedBreed ? "Сохранить изменения" : "Добавить" }}
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
        breeds: [],
        diets: [],
        showAddForm: false,
        selectedBreed: null,
        formData: {
          name: "",
          egg_performance_avg: 0,
          weight_avg: 0.0,
          diet_number: null,
        },
      };
    },
    async created() {
      await this.loadBreeds();
      await this.loadDiets();
    },
    methods: {
      async loadBreeds() {
        try {
          const response = await apiClient.get("/manufactory/breeds/");
          this.breeds = response.data;
        } catch (error) {
          console.error("Ошибка при загрузке пород:", error);
          alert("Не удалось загрузить породы.");
        }
      },
      async loadDiets() {
        try {
          const response = await apiClient.get("/manufactory/diets/");
          this.diets = response.data;
        } catch (error) {
          console.error("Ошибка при загрузке рационов:", error);
          alert("Не удалось загрузить рационы.");
        }
      },
      async saveBreed() {
        try {
          console.log(this.selectedBreed)
          if (this.selectedBreed) {
            await apiClient.put(`/manufactory/breeds/${this.selectedBreed.id}/`, this.formData);
            alert("Изменения сохранены.");
          } else {
            await apiClient.post("/manufactory/breeds/", this.formData);
            alert("Порода добавлена.");
          }
          await this.loadBreeds();
          this.cancelEdit();
        } catch (error) {
          console.error("Ошибка при сохранении породы:", error);
          alert("Не удалось сохранить изменения.");
        }
      },
      async deleteBreed(id) {
        try {
          if (confirm("Вы уверены, что хотите удалить эту породу?")) {
            await apiClient.delete(`/manufactory/breeds/${id}/`);
            this.breeds = this.breeds.filter((breed) => breed.id !== id);
          }
        } catch (error) {
          console.error("Ошибка при удалении породы:", error);
          alert("Не удалось удалить породу.");
        }
      },
      editBreed(breed) {
        this.selectedBreed = breed;
        this.formData = {
          name: breed.name,
          egg_performance_avg: breed.egg_performance_avg,
          weight_avg: breed.weight_avg,
          diet_number: breed.diet_number.id,
        };
      },
      cancelEdit() {
        this.selectedBreed = null;
        this.showAddForm = false;
        this.formData = {
          name: "",
          egg_performance_avg: 0,
          weight_avg: 0.0,
          diet_number: null,
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
  
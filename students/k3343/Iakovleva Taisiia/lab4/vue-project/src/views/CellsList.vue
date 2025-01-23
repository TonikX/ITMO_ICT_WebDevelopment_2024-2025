<template>
    <div>
      <Header />
      <h3 class="table-header">Список ячеек</h3>
      <div class="table-container">
      <div class="table-controls">
        <button @click="showAddForm = true" class="btn btn-primary">Добавить ячейку</button>
      </div>
  
      <table class="styled-table">
        <thead>
          <tr>
            <th>Код ячейки</th>
            <th>Ряд</th>
            <th>Колонка</th>
            <th>Цех</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="cell in cells" :key="cell.cell_code">
            <td>{{ cell.cell_code }}</td>
            <td>{{ cell.row }}</td>
            <td>{{ cell.column }}</td>
            <td>{{ cell.workshop.title }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  
      <div v-if="showAddForm || selectedCell" class="form-modal">
        <div class="modal-overlay">
          <div class="modal-content">
            <h2>{{ selectedCell ? 'Редактировать ячейку' : 'Добавить ячейку' }}</h2>
            <form @submit.prevent="saveCell">
              <div class="form-group">
                <label for="cell_code">Код ячейки:</label>
                <input v-model="formData.cell_code" type="text" id="cell_code" class="form-control" required />
              </div>
  
              <div class="form-group">
                <label for="row">Ряд:</label>
                <input v-model="formData.row" type="number" id="row" class="form-control" required />
              </div>
  
              <div class="form-group">
                <label for="column">Колонка:</label>
                <input v-model="formData.column" type="number" id="column" class="form-control" required />
              </div>
  
              <div class="form-group">
                <label for="workshop">Цех:</label>
                <select v-model="formData.workshop" id="workshop" class="form-control">
                  <option v-for="workshop in workshops" :key="workshop.id" :value="workshop.id">
                    {{ workshop.title }}
                  </option>
                </select>
              </div>
  
              <div class="form-actions">
                <button type="submit" class="btn btn-primary">
                  {{ selectedCell ? "Сохранить изменения" : "Добавить" }}
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
  import Header from '@/components/Header.vue';
  import apiClient from '@/api/axios';
  
  export default {
    components: {
    Header,
    },
    data() {
      return {
        cells: [],
        workshops: [],
        showAddForm: false,
        selectedCell: null,
        formData: {
          cell_code: '',
          row: '',
          column: '',
          workshop: null,
        },
      };
    },
    async created() {
      await this.loadCells();
      await this.loadWorkshops();
    },
    methods: {
      async loadCells() {
        try {
          const response = await apiClient.get('/manufactory/cells');
          this.cells = response.data;
        } catch (error) {
          console.error('Ошибка при загрузке ячеек:', error);
          alert('Не удалось загрузить ячейки.');
        }
      },
      async loadWorkshops() {
        try {
          const response = await apiClient.get('/manufactory/workshops');
          this.workshops = response.data;
        } catch (error) {
          console.error('Ошибка при загрузке цехов:', error);
          alert('Не удалось загрузить цехи.');
        }
      },
      async saveCell() {
        try {
          const payload = {
            cell_code: this.formData.cell_code,
            row: Number(this.formData.row),
            column: Number(this.formData.column),
            workshop: Number(this.formData.workshop), 
          };
          console.log(payload)
          if (this.selectedCell) {
            await apiClient.put(`/manufactory/cells/${this.selectedCell.cell_code}/`, payload);
            alert('Изменения сохранены.');
          } else {
            await apiClient.post('/manufactory/cells/', payload);
            alert('Ячейка добавлена.');
          }

          await this.loadCells(); // Перезагрузка данных
          this.cancelEdit(); // Очистка формы
        } catch (error) {
          console.error('Ошибка при сохранении ячейки:', error);
          alert('Не удалось сохранить изменения.');
        }
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
<template>
  <!-- Используем классы Bootstrap для стилизации модального окна -->
  <div class="modal fade show d-block" tabindex="-1" role="dialog" aria-labelledby="addDriverModalLabel" aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="addDriverModalLabel">Добавить водителя</h5>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <div class="form-group">
              <label for="name">Имя</label>
              <input type="text" id="name" class="form-control" v-model="newDriver.name" required />
            </div>
            <div class="form-group">
              <label for="passport_number">Паспортный номер</label>
              <input type="text" id="passport_number" class="form-control" v-model="newDriver.passport_number" required />
            </div>
            <div class="form-group">
              <label for="driver_class">Класс водителя</label>
              <select id="driver_class" class="form-control" v-model="newDriver.driver_class" required>
                <option value="MB">Minibus driver</option>
                <option value="NB">Normal Bus driver</option>
                <option value="DD">Double-Decker driver</option>
                <option value="EB">Electric Bus driver</option>
              </select>
            </div>
            <div class="form-group">
              <label for="experience_years">Опыт (лет)</label>
              <input type="number" id="experience_years" class="form-control" v-model="newDriver.experience_years" required />
            </div>
            <div class="form-group">
              <label for="salary">Зарплата</label>
              <input type="number" id="salary" class="form-control" v-model="newDriver.salary" required />
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="closeModal">Закрыть</button>
          <button type="submit" class="btn btn-primary" @click="handleSubmit">Добавить водителя</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      newDriver: {
        name: '',
        passport_number: '',
        driver_class: '',
        experience_years: null,
        salary: null,
      },
    };
  },
  methods: {
    handleSubmit() {
      this.$emit('add-driver', this.newDriver); // Отправляем событие для добавления водителя
      this.newDriver = { name: '', passport_number: '', driver_class: '', experience_years: null, salary: null }; // Очищаем форму
    },
    closeModal() {
      this.$emit('close'); // Отправляем событие для закрытия модального окна
    },
  },
};
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-dialog {
  max-width: 500px;
  width: 100%;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 5px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

button {
  margin-top: 10px;
}
</style>

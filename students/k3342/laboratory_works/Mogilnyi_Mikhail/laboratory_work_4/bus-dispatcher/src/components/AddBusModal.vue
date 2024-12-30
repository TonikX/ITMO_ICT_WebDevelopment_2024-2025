<template>
  <!-- Используем классы Bootstrap для стилизации модального окна -->
  <div class="modal fade show d-block" tabindex="-1" role="dialog" aria-labelledby="addBusModalLabel" aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="addBusModalLabel">Добавить автобус</h5>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <div class="form-group">
              <label for="registration_number">Регистрационный номер</label>
              <input type="text" id="registration_number" class="form-control" v-model="newBus.registration_number" required />
            </div>
            <div class="form-group">
              <label for="bus_type">Класс</label>
              <select id="bus_type" class="form-control" v-model="newBus.bus_type" required>
                <option v-for="(name, code) in busTypeChoices" :key="code" :value="code">
                  {{ name }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label for="capacity">Вместимость</label>
              <input type="number" id="capacity" class="form-control" v-model="newBus.capacity" required />
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="closeModal">Закрыть</button>
          <button type="submit" class="btn btn-primary" @click="handleSubmit">Добавить автобус</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    busTypeChoices: Object,
    newBus: Object,
  },
  methods: {
    handleSubmit() {
      this.$emit('add-bus', this.newBus); // Отправляем событие для добавления автобуса
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

button {
  margin-top: 10px;
}
</style>

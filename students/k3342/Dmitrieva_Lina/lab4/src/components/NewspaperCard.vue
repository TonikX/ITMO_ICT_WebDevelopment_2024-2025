<template>
  <div class="newspaper-card">
    <h3>{{ newspaper.name }}</h3>
    <p>Индекс: {{ newspaper.index }}</p>
    <p>Редактор: {{ newspaper.editor_first_name }} {{ newspaper.editor_last_name }}</p>
    <p>Цена: {{ newspaper.price }} руб.</p>

    <!-- Кнопки для редактирования и удаления (только для администратора или сотрудника) -->
    <div v-if="isAdminOrEmployee" class="admin-buttons">
      <button @click="$emit('edit', newspaper)">Редактировать</button>
      <button @click="$emit('delete', newspaper.id)" class="delete-button">Удалить</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    newspaper: Object,
  },
  computed: {
    isAdminOrEmployee() {
      const role = localStorage.getItem("role");
      return role === "admin" || role === "employee";
    },
  },
  methods: {
    goToDetails() {
      this.$router.push({ name: "Details", params: { type: "newspaper", id: this.newspaper.id } });
    },
  },
};
</script>

<style scoped>
.newspaper-card {
  background-color: white;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.details-button,
.edit-button,
.delete-button {
  margin: 10px 5px 0;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.details-button {
  background-color: #4caf50;
  color: white;
}

.edit-button {
  background-color: #ffa500;
  color: white;
}

.delete-button {
  background-color: #f44336;
  color: white;
}

.details-button:hover {
  background-color: #45a049;
}

.edit-button:hover {
  background-color: #ff9900;
}

.delete-button:hover {
  background-color: #e53935;
}

.admin-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-start;
  gap: 10px;
}
</style>

<template>
  <div class="delivery-card">
    <h3>Газета: {{ delivery.newspaper.name }}</h3>
    <p>Типография: {{ delivery.printshop.name }}</p>
    <p>Почтовое отделение: {{ delivery.post_office.address }}</p>
    <p>Количество: {{ delivery.quantity }}</p>
    <p>Дата доставки: {{ delivery.delivery_date }}</p>
    <p>Статус: {{ delivery.status ? 'Доставлено' : 'Не доставлено' }}</p>
    <button v-if="isAdminOrEmployee" @click="editDelivery">Редактировать</button>
  </div>
</template>

<script>
export default {
  props: {
    delivery: Object,
  },
  computed: {
    isAdminOrEmployee() {
      const role = localStorage.getItem("role");
      return role === "admin" || role === "employee";
    },
  },
  methods: {
    editDelivery() {
      this.$emit("edit", this.delivery);
    },
  },
};
</script>

<style scoped>
.delivery-card {
  border: 1px solid #ddd;
  padding: 10px;
  margin: 10px;
  flex: 1 1 calc(33.333% - 20px);
  box-sizing: border-box;
}

button {
  background-color: #4CAF50;
  color: white;
  padding: 10px;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>

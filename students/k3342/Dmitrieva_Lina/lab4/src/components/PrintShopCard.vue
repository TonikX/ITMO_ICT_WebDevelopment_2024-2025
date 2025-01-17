<template>
  <div class="printshop-card">
    <h3>{{ printShop.name }}</h3>
    <p>Адрес: {{ printShop.address }}</p>
    <button @click="goToDetails">Подробнее</button>
    <div v-if="canEdit">
      <button @click="editPrintShop">Редактировать</button>
      <button @click="deletePrintShop">Удалить</button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    printShop: Object,
    canEdit: Boolean,
  },
  methods: {
    goToDetails() {
      this.$router.push({ name: "Details", params: { type: "printshop", id: this.printShop.id } });
    },
    editPrintShop() {
      this.$emit("edit", this.printShop);
    },
    deletePrintShop() {
      this.$emit("delete", this.printShop.id);
    },
  },
};
</script>

<style scoped>
.printshop-card {
  border: 1px solid #ddd;
  padding: 10px;
  margin: 10px;
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

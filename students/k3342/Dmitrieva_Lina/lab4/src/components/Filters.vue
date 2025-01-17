<template>
  <div class="filters">
    <select v-model="selectedField">
      <option value="name">Название</option>
      <option value="price">Минимальная цена</option>
      <option value="editor">Редактор</option>
    </select>
    <input
      v-model="searchValue"
      type="text"
      :placeholder="placeholderText"
    />
    <button @click="applyFilter">Поиск</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedField: "name", // Поле для фильтрации (по умолчанию "Название")
      searchValue: "", // Значение для фильтрации
    };
  },
  computed: {
    placeholderText() {
      switch (this.selectedField) {
        case "name":
          return "Введите название газеты";
        case "price":
          return "Введите минимальную цену";
        case "editor":
          return "Введите имя редактора";
        default:
          return "Введите значение";
      }
    },
  },
  methods: {
    applyFilter() {
      const value = this.selectedField === "price" ? parseFloat(this.searchValue) || 0 : this.searchValue.trim();
      this.$emit("search", { field: this.selectedField, value });
    },
  },
};
</script>

<style scoped>
.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 20px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.filter-field {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 300px;
}

.filter-field label {
  font-weight: bold;
  margin-bottom: 5px;
}

.filter-field input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

.search-button {
  background-color: #4caf50;
  color: white;
  padding: 15px 25px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 10px;
}

.search-button:hover {
  background-color: #45a049;
}

@media (max-width: 768px) {
  .filter-field {
    max-width: 100%;
  }
}
</style>

<template>
  <div>
    <Header />
    <Filters @search="filterNewspapers" />
    <div class="newspaper-list">
      <NewspaperCard
        v-for="newspaper in filteredNewspapers"
        :key="newspaper.id"
        :newspaper="newspaper"
        @edit="isAdminOrEmployee ? openEditForm(newspaper) : null"
        @delete="isAdminOrEmployee ? deleteNewspaper(newspaper.id) : null"
      />
    </div>
    <button v-if="isAdminOrEmployee" @click="openForm">Добавить газету</button>
    <NewspaperForm
      v-if="isFormVisible"
      :newspaper="selectedNewspaper"
      @save="saveNewspaper"
      @cancel="closeForm"
    />
  </div>
</template>

<script>
import { getNewspapers, addNewspaper, updateNewspaper, deleteNewspaper } from "../api/api";
import Header from "../components/Header.vue";
import Filters from "../components/Filters.vue";
import NewspaperCard from "../components/NewspaperCard.vue";
import NewspaperForm from "../components/NewspaperForm.vue";

export default {
  components: {
    Header,
    Filters,
    NewspaperCard,
    NewspaperForm,
  },
  data() {
    return {
      newspapers: [],
      searchQuery: { field: "name", value: "" },
      isFormVisible: false,
      selectedNewspaper: null,
    };
  },
  computed: {
    filteredNewspapers() {
      const { field, value } = this.searchQuery;

      return this.newspapers.filter((n) => {
        if (field === "name") {
          return n.name.toLowerCase().includes(value.toLowerCase());
        } else if (field === "price") {
          return n.price >= value;
        } else if (field === "editor") {
          const fullName = `${n.editor_first_name} ${n.editor_last_name}`.toLowerCase();
          return fullName.includes(value.toLowerCase());
        }
        return true;
      });
    },
    isAdminOrEmployee() {
      const role = localStorage.getItem("role");
      return role === "admin" || role === "employee";
    },
  },
  methods: {
    async fetchNewspapers() {
      try {
        const response = await getNewspapers();
        this.newspapers = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке данных о газетах:", error);
      }
    },
    filterNewspapers({ field, value }) {
      this.searchQuery = { field, value };
    },
    openForm() {
      this.selectedNewspaper = null;
      this.isFormVisible = true;
    },
    openEditForm(newspaper) {
      this.selectedNewspaper = newspaper;
      this.isFormVisible = true;
    },
    closeForm() {
      this.isFormVisible = false;
      this.selectedNewspaper = null;
    },
    async saveNewspaper(newspaper) {
      try {
        if (newspaper.id) {
          await updateNewspaper(newspaper.id, newspaper);
          const index = this.newspapers.findIndex((n) => n.id === newspaper.id);
          this.newspapers.splice(index, 1, newspaper);
        } else {
          const response = await addNewspaper(newspaper);
          this.newspapers.push(response.data);
        }
        this.closeForm();
      } catch (error) {
        console.error("Ошибка при сохранении газеты:", error);
      }
    },
    async deleteNewspaper(id) {
      try {
        if (confirm("Вы уверены, что хотите удалить эту газету?")) {
          await deleteNewspaper(id);
          this.newspapers = this.newspapers.filter((n) => n.id !== id);
        }
      } catch (error) {
        console.error("Ошибка при удалении газеты:", error);
      }
    },
  },
  mounted() {
    this.fetchNewspapers();
  },
};
</script>

<style scoped>
.newspapers-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.newspaper-list {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.add-button {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 10px 15px;
  cursor: pointer;
  font-size: 16px;
  border-radius: 5px;
  margin: 20px 0;
}

.add-button:hover {
  background-color: #45a049;
}
</style>

<template>
  <div class="printshops-page">
    <Header />
    <Filters @search="filterPrintShops" />
    <div class="printshop-list">
      <PrintShopCard
        v-for="printShop in filteredPrintShops"
        :key="printShop.id"
        :printShop="printShop"
        :canEdit="isAdminOrEmployee"
        @edit="openEditForm(printShop)"
        @delete="deletePrintShop(printShop.id)"
      />
    </div>
    <PrintShopForm
      v-if="isFormVisible"
      :printShop="selectedPrintShop"
      @save="savePrintShop"
      @cancel="closeForm"
    />
    <button v-if="isAdminOrEmployee" @click="openForm" class="add-button">Добавить типографию</button>
  </div>
</template>

<script>
import { getPrintShops, addPrintShop, updatePrintShop, deletePrintShop } from "../api/api";
import PrintShopCard from "../components/PrintShopCard.vue";
import PrintShopForm from "../components/PrintShopForm.vue";
import Header from "@/components/Header.vue";

export default {
  components: {
    Header,
    PrintShopCard,
    PrintShopForm,
  },
  data() {
    return {
      printShops: [],
      searchQuery: "",
      isFormVisible: false,
      selectedPrintShop: null,
    };
  },
  computed: {
    filteredPrintShops() {
      return this.printShops.filter(
        (p) => p.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
    isAdminOrEmployee() {
      const role = localStorage.getItem("role");
      return role === "admin" || role === "employee";
    },
  },
  methods: {
    async fetchPrintShops() {
      try {
        const response = await getPrintShops();
        this.printShops = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке типографий:", error);
      }
    },
    async createPrintShop(printShop) {
      try {
        const response = await addPrintShop(printShop);
        this.printShops.push(response.data);
      } catch (error) {
        console.error("Ошибка при создании типографии:", error);
      }
    },
    async editPrintShop(printShop) {
      try {
        const response = await updatePrintShop(printShop.id, printShop);
        const index = this.printShops.findIndex((p) => p.id === printShop.id);
        this.printShops[index] = response.data;
      } catch (error) {
        console.error("Ошибка при обновлении типографии:", error);
      }
    },
    async deletePrintShop(id) {
      try {
        await deletePrintShop(id);
        this.printShops = this.printShops.filter((p) => p.id !== id);
      } catch (error) {
        console.error("Ошибка при удалении типографии:", error);
      }
    },
    filterPrintShops(query) {
      this.searchQuery = query;
    },
    openForm() {
      this.selectedPrintShop = null;
      this.isFormVisible = true;
    },
    openEditForm(printShop) {
      this.selectedPrintShop = printShop;
      this.isFormVisible = true;
    },
    closeForm() {
      this.isFormVisible = false;
      this.selectedPrintShop = null;
    },
    savePrintShop(printShop) {
      if (printShop.id) {
        this.editPrintShop(printShop);
      } else {
        this.createPrintShop(printShop);
      }
      this.closeForm();
    },
  },
  mounted() {
    this.fetchPrintShops();
  },
};
</script>

<style scoped>
.printshops-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  min-height: 100vh;
  padding: 20px;
  box-sizing: border-box;
}

.printshop-list {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  width: 100%;
  margin-top: 20px;
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
  align-self: flex-start;
}

.add-button:hover {
  background-color: #45a049;
}
</style>

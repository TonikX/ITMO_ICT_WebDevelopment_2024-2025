<template>
  <div class="reports-page">
    <Header />
    <h2>Отчеты</h2>

    <!-- Фильтры и выпадающий список для выбора аналитики -->
    <div class="filters">
      <div>
        <label for="report-type">Выберите тип аналитики:</label>
        <select v-model="selectedReport" id="report-type">
          <option value="">Выберите запрос</option>
          <option value="newspaper_addresses">Адреса типографий для газеты</option>
          <option value="editor_of_largest_circulation">Редактор с наибольшим тиражом</option>
          <option value="post_offices_for_expensive_newspapers">Почтовые отделения для дорогих газет</option>
          <option value="newspapers_with_low_quantity">Газеты с малым количеством</option>
        </select>
        <button @click="fetchReportData">Показать</button>
      </div>

      <!-- Фильтры для дополнительных параметров -->
      <div v-if="selectedReport === 'newspaper_addresses'">
        <label for="newspaper">Газета:</label>
        <select v-model="selectedNewspaper" id="newspaper">
          <option value="">Выберите газету</option>
          <option v-for="newspaper in newspapers" :key="newspaper.id" :value="newspaper.name">
            {{ newspaper.name }}
          </option>
        </select>
      </div>

      <div v-if="selectedReport === 'editor_of_largest_circulation'">
        <label for="printshop">Типография:</label>
        <select v-model="selectedPrintShop" id="printshop">
          <option value="">Выберите типографию</option>
          <option v-for="printShop in printShops" :key="printShop.id" :value="printShop.id">
            {{ printShop.name }}
          </option>
        </select>
      </div>

      <div v-if="selectedReport === 'post_offices_for_expensive_newspapers'">
        <label for="price">Минимальная цена:</label>
        <input v-model="priceFilter" id="price" type="number" placeholder="Введите минимальную цену" />
      </div>

      <div v-if="selectedReport === 'newspapers_with_low_quantity'">
        <label for="quantity">Минимальное количество:</label>
        <input v-model="quantityFilter" id="quantity" type="number" placeholder="Введите минимальное количество" />
      </div>
    </div>

    <!-- Результаты -->
    <div class="results">
      <h3>Результаты:</h3>
      <div v-if="results.length">
        <table>
          <thead>
            <tr>
              <th v-for="column in columns" :key="column">{{ column }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, index) in results" :key="index">
              <td v-for="value in row" :key="value">{{ value }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else>
        <p>Нет данных для отображения.</p>
      </div>
    </div>
  </div>
</template>

<script>
import Header from "@/components/Header.vue";
import { getNewspapers, getPrintShops, fetchReport } from "../api/api";

export default {
  components: { Header },
  data() {
    return {
      newspapers: [],
      printShops: [],
      selectedReport: "",
      selectedNewspaper: "",
      selectedPrintShop: "",
      priceFilter: "",
      quantityFilter: "",
      results: [],
      columns: [],
    };
  },
  methods: {
    async fetchData() {
      try {
        const [newspapersResponse, printShopsResponse] = await Promise.all([getNewspapers(), getPrintShops()]);
        this.newspapers = newspapersResponse.data;
        this.printShops = printShopsResponse.data;
      } catch (error) {
        console.error("Ошибка при загрузке данных:", error);
      }
    },
    async fetchReportData() {
      if (!this.selectedReport) {
        alert("Пожалуйста, выберите тип аналитики.");
        return;
      }

      let params = {};
      if (this.selectedReport === "newspaper_addresses" && this.selectedNewspaper) {
        params.name = this.selectedNewspaper;
      } else if (this.selectedReport === "editor_of_largest_circulation" && this.selectedPrintShop) {
        params.printshop_id = this.selectedPrintShop;
      } else if (this.selectedReport === "post_offices_for_expensive_newspapers" && this.priceFilter) {
        params.price = this.priceFilter;
      } else if (this.selectedReport === "newspapers_with_low_quantity" && this.quantityFilter) {
        params.quantity = this.quantityFilter;
      } else {
        alert("Заполните все необходимые поля.");
        return;
      }

      try {
        const response = await fetchReport(this.selectedReport, { params });
        this.results = this.formatResults(response.data);
        this.columns = this.getColumnsForReport(this.selectedReport);
      } catch (error) {
        console.error("Ошибка при загрузке отчета:", error);
      }
    },
    formatResults(data) {
      // Форматируем результаты для отображения в таблице
      if (this.selectedReport === "newspaper_addresses") {
        return data.addresses.map((address) => ({ Адрес: address }));
      } else if (this.selectedReport === "editor_of_largest_circulation") {
        return [{ Редактор: data.editor }];
      } else if (this.selectedReport === "post_offices_for_expensive_newspapers") {
        return data.post_offices.map((office) => ({ Адрес: office }));
      } else if (this.selectedReport === "newspapers_with_low_quantity") {
        return data.distributions.map((dist) => ({
          Газета: dist.newspaper__name,
          "Номер отделения": dist.post_office__number,
        }));
      }
    },
    getColumnsForReport(reportType) {
      if (reportType === "newspaper_addresses") {
        return ["Адрес"];
      } else if (reportType === "editor_of_largest_circulation") {
        return ["Редактор"];
      } else if (reportType === "post_offices_for_expensive_newspapers") {
        return ["Адрес"];
      } else if (reportType === "newspapers_with_low_quantity") {
        return ["Газета", "Номер отделения"];
      }
    },
  },
  mounted() {
    this.fetchData();
  },
};
</script>

<style scoped>
.reports-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.filters {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.results table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.results th,
.results td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
</style>

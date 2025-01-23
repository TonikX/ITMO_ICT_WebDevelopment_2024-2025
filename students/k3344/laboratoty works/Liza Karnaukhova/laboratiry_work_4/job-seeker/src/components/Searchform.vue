<template>
  <form @submit.prevent="filterVacancies" class="row mb-4 align-items-end" id="searchForm">
    <div class="col-lg-4 col-md-6 mt-2">
      <label for="searchQuery">Поиск</label>
      <input type="text" class="form-control" placeholder="Введите название вакансии" v-model="searchQuery" />
    </div>
    <div class="col-lg-4 col-md-6 mt-2">
      <label for="industry-filter">Отрасль</label>
      <select class="form-control" v-model="selectedIndustry">
        <option value="">Все</option>
        <option v-for="industry in industries" :key="industry" :value="industry">{{ industry }}</option>
      </select>
    </div>
    <div class="col-lg-3 col-md-6 mt-2">
      <label for="salary-filter">Зарплата</label>
      <select class="form-control" v-model="selectedSalary">
        <option value="">Любая</option>
        <option value="low">Низкая</option>
        <option value="medium">Средняя</option>
        <option value="high">Высокая</option>
      </select>
    </div>
    <div class="col-lg-1 col-md-2 mt-2">
      <button type="submit" class="btn btn-custom w-100">
        <SearchIcon />
        Найти
      </button>
    </div>
  </form>
</template>

<script>
import SearchIcon from "@/components/icons/IconSearch.vue";

export default {
  name: 'SearchForm',
  components: {
    SearchIcon,
  },
  data() {
    return {
      searchQuery: '',
      selectedIndustry: '',
      selectedSalary: '',
      industries: [],
    };
  },
  methods: {
    async fetchIndustries() {
      // Здесь вы можете получить уникальные отрасли из вашего API
      const response = await fetch('http://localhost:3000/vacancies');
      const vacancies = await response.json();
      const uniqueIndustries = new Set(vacancies.map(vacancy => vacancy.industry));
      this.industries = Array.from(uniqueIndustries);
    },
    filterVacancies() {
      this.$emit('filter', {
        searchQuery: this.searchQuery,
        industry: this.selectedIndustry,
        salary: this.selectedSalary,
      });
    },
  },
  created() {
    this.fetchIndustries();
  },
};
</script>

<style scoped>
  /* Добавьте стили для вашего компонента, если необходимо */
</style>

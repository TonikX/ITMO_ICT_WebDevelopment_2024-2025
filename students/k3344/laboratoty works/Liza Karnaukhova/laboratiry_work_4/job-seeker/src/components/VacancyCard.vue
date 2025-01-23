<template>
  <div class="col-md-4 mb-4 vacancy" v-for="vacancy in filteredVacancies" :key="vacancy.id" :data-industry="vacancy.industry" :data-salary="vacancy.salary">
    <div class="card h-100 w-100">
      <div class="card-body d-flex flex-column">
        <h5 class="card-title">{{ vacancy.title }}</h5>
        <p class="card-text">{{ vacancy.description }}</p>
        <p>Зарплата: {{ vacancy.salary }} руб.</p>
        <p>Опыт: {{ vacancy.experience }}</p>
        <router-link :to="{ path: '/vacancydetails', query: { id: vacancy.id } }" class="btn btn-custom mt-auto">Подробнее</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'VacancyCard',
  props: {
    filterCriteria: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      vacancies: [],
    };
  },
  computed: {
    filteredVacancies() {
      return this.vacancies.filter(vacancy => {
        const matchesSearch = vacancy.title.toLowerCase().includes(this.filterCriteria.searchQuery.toLowerCase());
        const matchesIndustry = this.filterCriteria.industry ? vacancy.industry === this.filterCriteria.industry : true;
        const matchesSalary = this.filterCriteria.salary ? this.filterBySalary(vacancy.salary) : true
        return matchesSearch && matchesIndustry && matchesSalary;
      });
    },
  },
  methods: {
    async fetchVacancies() {
      try {
        const response = await axios.get('http://localhost:3000/vacancies');
        this.vacancies = response.data.filter(vacancy => vacancy.title && vacancy.id);
      } catch (error) {
        console.error("Ошибка при загрузке вакансий:", error);
      }
    },
    filterBySalary(salary) {
      const salaryValue = parseInt(salary, 10);
      if (this.filterCriteria.salary === 'low') {
        return salaryValue < 30000;
      } else if (this.filterCriteria.salary === 'medium') {
        return salaryValue >= 30000 && salaryValue < 60000;
      } else if (this.filterCriteria.salary === 'high') {
        return salaryValue >= 60000;
      }
      return true; // Если фильтр не установлен, возвращаем все
    },
  },
  created() {
    this.fetchVacancies();
  },
};
</script>

<style scoped>
/* Добавьте стили для вашего компонента, если необходимо */
</style>

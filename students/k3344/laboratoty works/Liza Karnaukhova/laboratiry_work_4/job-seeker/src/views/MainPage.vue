<template>
  <base-layout>
    <HeaderComponent />
    <main-layout>
      <h1 class="text-center mb-4">Поиск вакансий</h1>
      <SearchForm @filter="updateFilter" />
      <vacancies-layout>
        <VacancyCard :filterCriteria="filterCriteria" />
      </vacancies-layout>
    </main-layout>
    <FooterComponent />
  </base-layout>
</template>

<script>
  import HeaderComponent from "../components/HeaderComponent.vue";
  import SearchForm from "@/components/Searchform.vue";
  import VacancyCard from "@/components/VacancyCard.vue";
  import FooterComponent from "@/components/FooterComponent.vue";
  import BaseLayout from "@/layout/BaseLayout.vue";
  import MainLayout from "@/layout/MainLayout.vue";
  import VacanciesLayout from "@/layout/VacanciesLayout.vue";

  export default {
    name: "MainPage",
    components: {
      HeaderComponent,
      SearchForm,
      VacancyCard,
      FooterComponent,
      BaseLayout,
      MainLayout,
      VacanciesLayout,
    },
    data() {
      return {
        filterCriteria: {
          searchQuery: '',
          industry: '',
          salary: '',
        },
      };
    },
    methods: {
      updateFilter(criteria) {
        this.filterCriteria = criteria;
      },
    },
  };
</script>

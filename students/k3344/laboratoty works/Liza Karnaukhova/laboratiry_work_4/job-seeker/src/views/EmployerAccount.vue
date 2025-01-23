<template>
  <base-layout>
    <HeaderComponent />
    <main-details-layout>
      <h1 class="text-center mb-4">Личный кабинет </h1>
      <section-layout>
        <CompanyInfo v-if="company" :company="company" />
      </section-layout>
      <section-layout>
        <VacanciesManagement :vacancies="vacancies" @add-vacancy="showVacancyModal" />
      </section-layout>
      <section-layout>
        <ResponsesManagement :responses="responses" />
      </section-layout>
    </main-details-layout>
    <VacancyModal v-if="isModalVisible" @close="isModalVisible = false" @submit="addVacancy" />
    <FooterComponent />
  </base-layout>
</template>

<script>
  import { ref, onMounted } from 'vue';
  import { useCompaniesStore } from '@/stores/companies';
  import { useVacanciesStore } from '@/stores/vacancies1';
  import { useResponsesStore } from '@/stores/responses';
  import HeaderComponent from '@/components/HeaderComponent.vue';
  import FooterComponent from '@/components/FooterComponent.vue';
  import CompanyInfo from '@/components/CompanyInfo.vue';
  import VacanciesManagement from '@/components/VacanciesManagement.vue';
  import ResponsesManagement from '@/components/ResponsesManagement.vue';
  import VacancyModal from '@/components/VacancyModal.vue';
  import BaseLayout from "@/layout/BaseLayout.vue";
  import MainDetailsLayout from "@/layout/MainDetailsLayout.vue";
  import SectionLayout from "@/layout/SectionLayout.vue";

  export default {
    components: {
      HeaderComponent,
      FooterComponent,
      CompanyInfo,
      VacanciesManagement,
      ResponsesManagement,
      VacancyModal,
      BaseLayout,
      MainDetailsLayout,
      SectionLayout,
    },
    setup() {
      const companiesStore = useCompaniesStore();
      const vacanciesStore = useVacanciesStore();
      const responsesStore = useResponsesStore();

      const company = ref(null);
      const vacancies = ref([]);
      const responses = ref([]);
      const isModalVisible = ref(false);

      const fetchCompanyInfo = async () => {
        const currentUser = JSON.parse(localStorage.getItem('currentUser '));
        company.value = await companiesStore.getCompanyByUsername(currentUser.username);
      };

      const fetchVacancies = async () => {
        const currentUser = JSON.parse(localStorage.getItem('currentUser '));
        vacancies.value = await vacanciesStore.getVacanciesByUserId(currentUser.id);
      };

      const fetchResponses = async () => {
        responses.value = await responsesStore.getAllResponsesWithResumes();
      };

      const showVacancyModal = () => {
        isModalVisible.value = true;
      };

      const addVacancy = async (vacancyData) => {
      const currentUser = JSON.parse(localStorage.getItem('currentUser '));
      vacancyData.userId = currentUser.id; // Убедитесь, что id добавляется
      await vacanciesStore.addVacancy(vacancyData);
      vacancies.value = vacanciesStore.vacancies;
      isModalVisible.value = false;
};



      onMounted(async () => {
        await fetchCompanyInfo();
        await fetchVacancies();
        await fetchResponses();
      });

      return {
        company,
        vacancies,
        responses,
        isModalVisible,
        showVacancyModal,
        addVacancy
      };
    }
  };
</script>

<style scoped>
  /* Добавьте стили, если необходимо */
</style>

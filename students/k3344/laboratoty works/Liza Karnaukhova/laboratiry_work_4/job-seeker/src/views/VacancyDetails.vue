<template>
  <base-layout>
    <HeaderComponent />
    <main-details-layout>
      <VacancyContainer @open-response-modal="handleOpenModal" />
      <!-- Компонент модального окна -->
      <ResponseModal
          v-if="isModalOpen"
          :vacancyId="selectedVacancyId"
          @close="isModalOpen = false"
      />
    </main-details-layout>
    <FooterComponent />
  </base-layout>
</template>

<script>
import HeaderComponent from "../components/HeaderComponent.vue";
import FooterComponent from "@/components/FooterComponent.vue";
import VacancyContainer from "@/components/VacancyContainer.vue";
import ResponseModal from "@/components/ResponseModal.vue";
import BaseLayout from "@/layout/BaseLayout.vue";
import MainDetailsLayout from "@/layout/MainDetailsLayout.vue";

export default {
  name: "VacancyDetails",
  components: {
    VacancyContainer,
    ResponseModal,
    BaseLayout,
    MainDetailsLayout,
    HeaderComponent,
    FooterComponent,
  },
  data() {
    return {
      isModalOpen: false,
      selectedVacancyId: null,
    };
  },
  methods: {
    handleOpenModal(vacancyId) {
      this.selectedVacancyId = vacancyId;
      this.isModalOpen = true;
    },
  },
};
</script>

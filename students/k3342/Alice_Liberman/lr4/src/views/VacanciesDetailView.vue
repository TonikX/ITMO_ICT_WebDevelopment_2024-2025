<template>
  <div v-if="!isAuthenticated">
    <auth-required/>
  </div>

  <div v-else-if="vacancies">
    <VacancyViewer :vacancy="vacancies"/>
    <div v-if="isHR && applicants">
      <h1>Applicants:</h1>
      <application-card v-for="applicant in applicants" :application="applicant" />
    </div>
  </div>
</template>

<script setup>
import {onMounted, ref} from "vue";
import axiosInstance from "@/services/axios.js";
import {useRoute} from "vue-router";
import {isAuthenticated} from "@/composables/useAuth.js";
import AuthRequired from "@/components/AuthRequired.vue";
import {isHR} from "@/stores/globalState.js";
import VacancyViewer from "@/components/VacancyViewer.vue";
import ApplicationCard from "@/components/applicationCard.vue";

const vacancyID = useRoute().params.vacancyID;

const vacancies = ref(null)
const applicants = ref(null)


onMounted(async () => {
  if (isAuthenticated) {
    const responseData = (await axiosInstance.get(`/vacancies/${vacancyID}`)).data
    if (isHR.value) {

      vacancies.value = responseData.vacancy
      applicants.value = responseData.applications
    }
    else {
      vacancies.value = responseData
    }
  }
})
</script>
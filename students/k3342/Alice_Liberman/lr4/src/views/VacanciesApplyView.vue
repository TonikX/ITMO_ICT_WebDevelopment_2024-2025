<template>
  <div class="container">
    <h1>Select CV</h1>

    <div class="row">
      <div v-for="cv in cvs" :key="cv.id" class="cv-item col-4">
        <CVList :cv="cv" @click="selectCV(cv)"/>
      </div>
    </div>

    <div v-if="selectedCV">
      <h2>Selected CV:</h2>
      <div class="row">
        <CVList :cv="selectedCV" class="cv-item col-4 me-2"></CVList>
          <textarea
              ref="largeTextField"
              v-model="text"
              rows="10"
              cols="50"
              placeholder="Type something..."
              class="col-7"
          ></textarea>
      </div>
      <button @click="applyCV" class="btn btn-primary">Apply to the vacancy</button>
    </div>
  </div>
</template>

<script setup>
import {onMounted, ref} from 'vue';
import CVList from "@/components/CVList.vue";
import axiosInstance from "@/services/axios.js";
import {useRoute} from "vue-router";
import router from "@/router/index.js";

const cvs = ref([]);
const selectedCV = ref(null);
const text = ref('');
const route = useRoute();
const vacancyID = route.params.vacancyID;

onMounted(async () => {
  try {
    const response = await axiosInstance.get('/cvs');
    cvs.value = response.data;
  } catch (error) {
    console.error('Error fetching CVs:', error);
  }
});

const selectCV = (cv) => {
  selectedCV.value = {...cv};
};

async function applyCV() {
  const response = await axiosInstance.post(`vacancies/${vacancyID}/`, {
    "CV_id": selectedCV.value.id,
    "message": text.value
  })
  if (response.status === 200) {
    alert('Successfully applied!');
    router.push({path: '/', force: true});
  }
}
</script>

<style scoped>
.cv-item:hover {
  background-color: #f0f0f0;
}
</style>

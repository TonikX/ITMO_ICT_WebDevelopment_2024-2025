<script setup>
import Navigation from "@/components/Navigation.vue";
import { ref, onMounted } from "vue";

const countHensByBreedWorkshop = ref([]);
const avgEggsPerWorker = ref([]);
const breedVsFactoryDiff = ref([]);
const workshopMaxHensByBreed = ref([]);

const fetchData = async (url) => {
  try {
    const response = await fetch(url);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error loading data:", error);
    return null;
  }
};

onMounted(async () => {
  countHensByBreedWorkshop.value = await fetchData("http://127.0.0.1:8000/hens/count-by-breed-workshop/");
  avgEggsPerWorker.value = await fetchData("http://127.0.0.1:8000/employees/avg-eggs/");
  breedVsFactoryDiff.value = await fetchData("http://127.0.0.1:8000/breeds/vs-factory-average/");
  workshopMaxHensByBreed.value = await fetchData("http://127.0.0.1:8000/workshops/max-hen/");
});
</script>

<template>
  <h1>Reports</h1>
  <Navigation />
  <div class="wrapper">
    <section class="workshop">
    <h2 class="section-title">Number of Hens by Breed and Workshop</h2>
    <table class="styled-table">
      <thead>
        <tr>
          <th>ID Workshop</th>
          <th>Breed</th>
          <th>Total Hens</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="workshop in countHensByBreedWorkshop" :key="workshop.cage__workshop__id">
          <td>{{ workshop.cage__workshop__id }}</td>
          <td>{{ workshop.breed__name }}</td>
          <td>{{ workshop.total_hens }}</td>
        </tr>
      </tbody>
    </table>
  </section>

  <section class="breed-diff">
    <h2 class="section-title">Difference between breed and factory</h2>
    <table class="styled-table">
      <thead>
        <tr>
          <th>Breed</th>
          <th>Average number of eggs (Breed)</th>
          <th>Difference from factory</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="breed in breedVsFactoryDiff" :key="breed.breed">
          <td>{{ breed.breed }}</td>
          <td>{{ breed.avg_eggs_breed }}</td>
          <td>{{ breed.diff_from_factory }}</td>
        </tr>
      </tbody>
    </table>
  </section>

  <section class="workshop-max-hens">
    <h2 class="section-title">Workshop with the most hens by breed</h2>
    <table class="styled-table">
      <thead>
        <tr>
          <th>Breed</th>
          <th>ID Workshop</th>
          <th>Total Hens</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="workshop in workshopMaxHensByBreed" :key="workshop.breed">
          <td>{{ workshop.breed }}</td>
          <td>{{ workshop.workshop }}</td>
          <td>{{ workshop.total_hens }}</td>
        </tr>
      </tbody>
    </table>
  </section>

  <section class="avg-eggs">
    <h2 class="section-title">Average number of eggs collected by worker</h2>
    <table class="styled-table">
      <thead>
        <tr>
          <th>Worker name</th>
          <th>Average number of eggs</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="worker in avgEggsPerWorker" :key="worker.name">
          <td>{{ worker.name }}</td>
          <td>{{ worker.avg_eggs }}</td>
        </tr>
      </tbody>
    </table>
  </section>
  </div>
</template>

<style scoped>
.workshop, .avg-eggs, .breed-diff, .workshop-max-hens {
  margin: 80px auto;
}

.wrapper {
  padding-bottom: 40px;
}

.styled-table {
  width: 100%;
  border-collapse: collapse;
  margin: 10px 0;
  font-size: 1rem;
  text-align: left;
}

.styled-table thead tr {
  background-color: hsla(160, 100%, 37%, 1);
  color: #ffffff;
  text-align: left;
  font-weight: bold;
}

.styled-table th, .styled-table td {
  padding: 12px 15px;
  border-bottom: 1px solid #ddd;
}

.styled-table tbody tr:hover {
  background-color: #f1f1f1;
}

.styled-table tbody tr:nth-of-type(even) {
  background-color: #f9f9f9;
}

.styled-table tbody td {
  color: #555;
}
</style>


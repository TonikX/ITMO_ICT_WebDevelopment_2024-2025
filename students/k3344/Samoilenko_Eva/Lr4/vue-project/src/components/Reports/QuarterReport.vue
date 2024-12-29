<script setup>
import {ref, watch} from "vue";
import instance from "@/AxiosInstance";

const quarters = [1, 2, 3, 4]
const reportParts = [
  "All Clients",
  "Rooms on every Floor Count",
  "Every Room Income",
  "Full Hotel Income",
]

const selectedQuarter = ref(null)
const selectedPart = ref(null)
const reportData = ref(null)
const loading = ref(false)

function fetchReport() {
  if (selectedQuarter.value && selectedPart.value) {
    loading.value = true;
    instance
      .get(`/hotel/report/${selectedQuarter.value}/`)
      .then((response) => {
        reportData.value = response.data[selectedPart.value];
      })
      .catch((error) => {
        console.error("Error fetching report:", error);
        reportData.value = "Failed to load report.";
      })
      .finally(() => {
        loading.value = false;
      });
  }
}

watch([selectedQuarter, selectedPart], fetchReport);
</script>

<template>
  <div class="d-flex align-center flex-column ga-10">
    <div class="report-page">
      <h1>Hotel Report</h1>

      <div class="selectors">
        <v-select
          v-model="selectedQuarter"
          :items="quarters"
          label="Select Quarter"
          class="select-field"
        ></v-select>
        <v-select
          v-model="selectedPart"
          :items="reportParts"
          label="Select Report Part"
          class="select-field"
        ></v-select>
      </div>

      <div v-if="loading" class="loading">Loading report...</div>
      <div v-else-if="reportData" class="report-result">
        <h2>{{ selectedPart }}</h2>
        <div v-if="selectedPart === 'Full Hotel Income' && reportData === 0">
          <p>You gotta work harder next year, because your income for this quarter in NILL</p>
        </div>
        <div v-else>
          <pre>{{ reportData }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
h1 {
  text-align: center;
}

.report-page {
  min-width: 1000px;
  min-height: 600px;
  margin: 0 auto;
  padding: 20px;
}

.selectors {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 20px;
}

.select-field {
  flex: 1;
}

.loading {
  text-align: center;
  font-size: 18px;
  color: #888;
}

.report-result {
  background: #f9f9f9;
  border: 1px solid #ddd;
  padding: 20px;
  border-radius: 8px;
}
</style>

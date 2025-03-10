<script setup lang="ts">
import { ref, onMounted } from "vue";
import api from "@/services/AxiosService";

interface Step {
  step_number: number;
  step_description: string;
  attachment: string;
}

const props = defineProps<{ id: number }>();
const steps = ref<Step[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);

const fetchSteps = async () => {
  try {
    const response = await api.get<Step[]>(`recipes/${props.id}/steps`);
    steps.value = response.data;
  } catch (err) {
    error.value = "Failed to load recipe steps.";
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchSteps();
});
</script>

<template>
  <div class="recipe-steps mt-4">
    <h3>Recipe Steps:</h3>

    <div v-if="loading" class="text-center my-3">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger text-center">{{ error }}</div>

    <ol v-else class="list-group list-group-numbered">
      <li v-for="step in steps" :key="step.step_number" class="list-group-item">
        <p class="mb-2"><strong>Step {{ step.step_number }}:</strong> {{ step.step_description }}</p>
        <img v-if="step.attachment" :src="step.attachment" class="img-fluid rounded shadow-sm" alt="Step Image" />
      </li>
    </ol>
  </div>
</template>

<style scoped>
.img-fluid {
  max-width: 100%;
  height: auto;
  margin-top: 10px;
}
</style>

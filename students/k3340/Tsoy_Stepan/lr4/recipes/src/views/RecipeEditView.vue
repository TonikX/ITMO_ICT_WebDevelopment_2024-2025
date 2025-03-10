<script setup lang="ts">
import {ref, onMounted} from "vue";
import {useRoute, useRouter} from "vue-router";
import api from "@/services/AxiosService";

const route = useRoute();
const router = useRouter();
const recipe = ref({
  title: "",
  headline: "",
  banner: "",
  difficulty: "",
  ingredients: "",
  video: "",
});
const steps = ref<{ step_number: number; step_description: string; attachment: string }[]>([]);
const newStep = ref({step_description: "", attachment: ""});
const loading = ref(true);
const error = ref<string | null>(null);
const success = ref<string | null>(null);

async function fetchRecipe() {
  try {
    const {id} = route.params;
    const response = await api.get(`recipes/${id}`);
    recipe.value = {
      ...response.data,
      ingredients: response.data.ingredients.join(", "),
    };
  } catch (e) {
    console.log(e);
    error.value = "Failed to load recipe.";
  }
}

async function fetchSteps() {
  try {
    const {id} = route.params;
    const response = await api.get(`recipes/${id}/steps`);
    steps.value = response.data;
  } catch {
    error.value = "Failed to load steps.";
  }
}

async function updateRecipe() {
  try {
    const {id} = route.params;

    await api.put(`recipes/${id}/`, {
      ...recipe.value,
      ingredients: recipe.value.ingredients.split(",").map(i => i.trim()),
    });
    success.value = "Recipe updated successfully!";
    setTimeout(() => router.push(`/recipes/${id}`), 2000);
  } catch {
    error.value = "Failed to update recipe.";
  }
}

async function addStep() {
  try {
    const {id} = route.params;
    const response = await api.post(`recipes/${id}/steps/`, newStep.value);
    steps.value.push(response.data);
    newStep.value = {step_description: "", attachment: ""};
  } catch {
    error.value = "Failed to add step.";
  }
}

onMounted(async () => {
  await fetchRecipe();
  await fetchSteps();
  loading.value = false;
});
</script>

<template>
  <div>
    <h1 class="text-center my-4">Edit Recipe</h1>

    <div v-if="loading" class="text-center my-4">
      <div class="spinner-border text-primary"></div>
    </div>

    <div v-else>
      <form @submit.prevent="updateRecipe" class="card p-4 shadow-sm">
        <div class="mb-3">
          <label class="form-label">Title</label>
          <input v-model="recipe.title" type="text" class="form-control" required/>
        </div>

        <div class="mb-3">
          <label class="form-label">Headline</label>
          <input v-model="recipe.headline" type="text" class="form-control" required/>
        </div>

        <div class="mb-3">
          <label class="form-label">Banner URL</label>
          <input v-model="recipe.banner" type="url" class="form-control"/>
        </div>

        <div class="mb-3">
          <label class="form-label">Difficulty</label>
          <select v-model="recipe.difficulty" class="form-control">
            <option value="Easy">Easy</option>
            <option value="Medium">Medium</option>
            <option value="Hard">Hard</option>
          </select>
        </div>

        <div class="mb-3">
          <label class="form-label">Ingredients</label>
          <textarea v-model="recipe.ingredients" class="form-control" rows="3"></textarea>
        </div>

        <div class="mb-3">
          <label class="form-label">Video URL</label>
          <input v-model="recipe.video" type="url" class="form-control"/>
        </div>

        <button type="submit" class="btn btn-success">Save Changes</button>
        <p v-if="error" class="text-danger mt-3">{{ error }}</p>
        <p v-if="success" class="text-success mt-3">{{ success }}</p>
      </form>

      <!-- Steps Section -->
      <div class="mt-5">
        <h2>Steps</h2>
        <ul class="list-group">
          <li v-for="step in steps" :key="step.step_number" class="list-group-item">
            <strong>Step {{ step.step_number }}:</strong> {{ step.step_description }}
            <div v-if="step.attachment">
              <img :src="step.attachment" class="img-fluid mt-2" style="max-width: 200px;"/>
            </div>
          </li>
        </ul>
      </div>

      <!-- Add New Step Form -->
      <div class="mt-4 card p-3 shadow-sm">
        <h3>Add New Step</h3>
        <div class="mb-3">
          <label class="form-label">Step Description</label>
          <input v-model="newStep.step_description" type="text" class="form-control" required/>
        </div>

        <div class="mb-3">
          <label class="form-label">Attachment (Optional, Image URL)</label>
          <input v-model="newStep.attachment" type="url" class="form-control"/>
        </div>

        <button @click="addStep" class="btn btn-primary">➕ Add Step</button>
      </div>
    </div>
  </div>
</template>

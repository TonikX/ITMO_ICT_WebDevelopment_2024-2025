<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/services/AxiosService";

const route = useRoute();
const router = useRouter();
const loading = ref(true);
const error = ref<string | null>(null);
const recipeTitle = ref<string>("");

async function fetchRecipe() {
  try {
    const { id } = route.params;
    const response = await api.get(`recipes/${id}`);
    recipeTitle.value = response.data.title;
  } catch {
    error.value = "Failed to load recipe.";
  } finally {
    loading.value = false;
  }
}

async function deleteRecipe() {
  try {
    const { id } = route.params;
    await api.delete(`recipes/${id}/`);
    router.push("/");
  } catch {
    error.value = "Failed to delete recipe.";
  }
}

onMounted(fetchRecipe);
</script>

<template>
  <div>
    <h1 class="text-center my-4 text-danger">Delete Recipe</h1>

    <div v-if="loading" class="text-center my-4">
      <div class="spinner-border text-danger"></div>
    </div>

    <div v-else class="card p-4 shadow-sm text-center">
      <p class="fs-5">Are you sure you want to delete <strong>{{ recipeTitle }}</strong>?</p>
      <button @click="deleteRecipe" class="btn btn-danger me-2">Yes, Delete</button>
      <button @click="router.back()" class="btn btn-secondary">Cancel</button>
      <p v-if="error" class="text-danger mt-3">{{ error }}</p>
    </div>
  </div>
</template>

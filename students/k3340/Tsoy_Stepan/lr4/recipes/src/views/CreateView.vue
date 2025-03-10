<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "@/services/AxiosService";

const router = useRouter();

const newRecipe = ref({
  title: "",
  headline: "",
  banner: "",
  ingredients: "" as string,
  video: "",
  difficulty: null as string | null,
});

const difficultyOptions = [
  { label: "Easy", value: "ez" },
  { label: "Medium", value: "md" },
  { label: "Hard", value: "hd" },
];


const error = ref<string | null>(null);
const success = ref<string | null>(null);
const loading = ref(false);

async function createRecipe() {
  if (!newRecipe.value.title || !newRecipe.value.headline) {
    error.value = "Title and headline are required!";
    return;
  }

  loading.value = true;
  error.value = null;
  success.value = null;

  try {
    const response = await api.post("/recipes/", {
      ...newRecipe.value,
      ingredients: newRecipe.value.ingredients
          ? newRecipe.value.ingredients.split(",").map(i => i.trim())
          : [],
      difficulty: newRecipe.value.difficulty || null,
    });

    success.value = "Recipe created successfully!";
    setTimeout(() => router.push(`/recipes/${response.data.id}`), 2000);
  } catch {
    error.value = "Failed to create recipe.";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div>
    <h1 class="text-center my-4">Create a New Recipe</h1>

    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary"></div>
    </div>

    <form v-else @submit.prevent="createRecipe" class="card p-4 shadow-sm">
      <div class="mb-3">
        <label class="form-label">Title</label>
        <input v-model="newRecipe.title" type="text" class="form-control" required />
      </div>

      <div class="mb-3">
        <label class="form-label">Headline</label>
        <input v-model="newRecipe.headline" type="text" class="form-control" required />
      </div>

      <div class="mb-3">
        <label class="form-label">Banner URL</label>
        <input v-model="newRecipe.banner" type="url" class="form-control" />
      </div>

      <div class="mb-3">
        <label class="form-label">Ingredients (comma-separated)</label>
        <textarea v-model="newRecipe.ingredients" class="form-control" rows="3"></textarea>
      </div>

      <div class="mb-3">
        <label class="form-label">Video URL</label>
        <input v-model="newRecipe.video" type="url" class="form-control" />
      </div>

      <div class="mb-3">
        <label class="form-label">Difficulty</label>
        <select v-model="newRecipe.difficulty" class="form-control">
          <option :value="null">Select Difficulty</option>
          <option v-for="option in difficultyOptions" :key="option.value" :value="option.value">
            {{ option.label }}
          </option>
        </select>
      </div>

      <button type="submit" class="btn btn-success">Create Recipe</button>
      <p v-if="error" class="text-danger mt-3">{{ error }}</p>
      <p v-if="success" class="text-success mt-3">{{ success }}</p>
    </form>
  </div>
</template>

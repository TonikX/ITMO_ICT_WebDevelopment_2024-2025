<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "@/services/AxiosService";
import RecipeCard from "@/components/RecipeCard.vue";

const router = useRouter();
const user = ref<{ username: string } | null>(null);
const recipes = ref<any[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);

async function fetchAccountData() {
  try {
    const accountResponse = await api.get("/account/");
    user.value = accountResponse.data;

    const recipesResponse = await api.get("/account/posts/");
    recipes.value = recipesResponse.data.results;
  } catch {
    error.value = "Failed to load account data.";
  } finally {
    loading.value = false;
  }
}

onMounted(fetchAccountData);
</script>

<template>
  <div>
    <h1 class="text-center my-4">My Account</h1>

    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary"></div>
    </div>

    <div v-else>
      <div v-if="user" class="card p-4 shadow-sm">
        <h3>Welcome, {{ user.username }}!</h3>
      </div>

      <div class="d-flex justify-content-between align-items-center mt-4">
        <h2>My Recipes</h2>
        <button class="btn btn-success" @click="router.push('/account/new')">➕ Create New Recipe</button>
      </div>

      <div v-if="recipes.length === 0" class="alert alert-warning mt-3">
        You haven't posted any recipes yet.
      </div>

      <div class="row mt-3">
        <div v-for="recipe in recipes" :key="recipe.id" class="col-md-4 mb-4">
          <RecipeCard
              :id="recipe.id"
              :title="recipe.title"
              :headline="recipe.headline"
              :image="recipe.banner"
              :difficulty="recipe.difficulty"
              :author="recipe.author.username"
          />
        </div>
      </div>
    </div>

    <p v-if="error" class="text-danger mt-3">{{ error }}</p>
  </div>
</template>

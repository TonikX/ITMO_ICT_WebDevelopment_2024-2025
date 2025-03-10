<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import api from "@/services/AxiosService";
import RecipeCard from "@/components/RecipeCard.vue";

interface Author {
  id: number;
  username: string;
}

interface Recipe {
  id: number;
  title: string;
  headline: string;
  banner: string;
  difficulty: string;
  author: Author;
}

interface ApiResponse {
  meal: Recipe;
  status: boolean;
}

const recipes = ref<Recipe[]>([]);
const loading = ref(true);
const error = ref<string | null>(null);


const fetchRecipes = async (url: string = "account/likes/") => {
  try {
    loading.value = true;
    const response = await api.get<ApiResponse[]>(url);
    console.log(response);
    recipes.value = response.data.map((res) => res.meal);

  } catch (err) {
    error.value = "Failed to load recipes.";
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchRecipes();
});

</script>

<template>
  <div class="recipe-list">
    <h1 class="text-center my-4">Recipes</h1>

    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger text-center">{{ error }}</div>

    <div v-else class="row">
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
</template>

<style scoped>
input {
  max-width: 500px;
  margin: 0 auto;
  display: block;
}
</style>

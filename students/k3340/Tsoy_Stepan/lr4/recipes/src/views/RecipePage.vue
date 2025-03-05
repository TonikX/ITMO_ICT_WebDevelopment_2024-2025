<script setup lang="ts">
import {ref, onMounted} from "vue";
import {useRoute} from "vue-router";
import api from "@/services/AxiosService";
import StepsList from "@/components/StepsList.vue";
import LikeButton from "@/components/LikeButton.vue";
import {isAuthenticated} from "@/services/AuthService.ts";
import RecipeActions from "@/components/RecipeActions.vue";

interface Author {
  id: number;
  username: string;
}

interface Recipe {
  id: number;
  title: string;
  headline: string;
  difficulty: string;
  banner: string;
  ingredients: string[];
  video: string;
  author: Author;
}

const route = useRoute();
const recipe = ref<Recipe | null>(null);
const loading = ref(true);
const error = ref<string | null>(null);
const canEdit = ref<boolean>(false);


const fetchRecipe = async () => {
  try {
    const recipeId = route.params.id;
    const response = await api.get<Recipe>(`recipes/${recipeId}`);
    recipe.value = response.data;
  } catch (err) {
    error.value = "Failed to load recipe.";
  } finally {
    loading.value = false;
  }
};

async function fetchEditable() {
  const recipeId = route.params.id;
  const response = await api.get<boolean>(`recipes/${recipeId}/can_edit/`);
  canEdit.value = response.data;
}

onMounted(() => {
  fetchRecipe();
  fetchEditable();
});
</script>

<template>
  <div v-if="loading" class="text-center my-5">
    <div class="spinner-border text-primary" role="status"></div>
  </div>

  <div v-else-if="error" class="alert alert-danger text-center">{{ error }}</div>

  <div v-else class="recipe-detail">
    <div class="row">
      <div class="col">
        <h1 class="my-4">{{ recipe?.title }}</h1>
        <h5 class="">{{ recipe?.headline }}</h5>
      </div>
      <div class="col-2" v-if="isAuthenticated && recipe">
        <LikeButton/>
        <RecipeActions :recipeId="recipe.id" :canEdit="canEdit" />

      </div>
    </div>

    <div class="text-center">
      <img :src="recipe?.banner" class="img-fluid rounded shadow-lg mb-4" alt="Recipe Image"/>
    </div>

    <p class="text-center">
      <strong>Difficulty:</strong> <span class="badge bg-secondary">{{ recipe?.difficulty }}</span>
    </p>
    <p class="text-center"><strong>Author:</strong> {{ recipe?.author.username }}</p>

    <div class="mt-4">
      <h3>Ingredients:</h3>
      <ul class="list-group">
        <li v-for="(ingredient, index) in recipe?.ingredients" :key="index" class="list-group-item">
          {{ ingredient }}
        </li>
      </ul>
    </div>

    <StepsList v-if="recipe" :id="recipe.id"/>

    <div v-if="recipe?.video" class="text-center my-4">
      <h3>Recipe Video:</h3>
      <iframe
          :src="recipe.video.replace('watch?v=', 'embed/')"
          class="video-iframe"
          frameborder="0"
          allowfullscreen
      ></iframe>
    </div>
  </div>
</template>

<style scoped>
.img-fluid {
  max-width: 80%;
  height: auto;
}

.video-iframe {
  width: 80%;
  height: 400px;
  max-width: 800px;
}

.list-group-item {
  font-size: 1.1rem;
}
</style>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import cookingImage from '@/assets/images/cooking.png';

const savedRecipes = ref([]);

const getUserIdFromToken = async () => {
  try {
    const token = localStorage.getItem("auth_token");
    if (!token) throw new Error("Токен не найден.");

    const response = await axios.get("http://localhost:8000/auth/users/me/", {
      headers: { Authorization: `Token ${token}` },
    });
    return response.data.id;
  } catch (error) {
    console.error("Ошибка получения ID пользователя:", error);
    throw error;
  }
};

const fetchSavedRecipes = async () => {
  try {
    const userId = await getUserIdFromToken();
    const response = await axios.get(`http://127.0.0.1:8000/users/${userId}/saved-recipes/`);
    savedRecipes.value = response.data;
  } catch (error) {
    console.error("Ошибка при загрузке сохранённых рецептов:", error);
  }
};

onMounted(() => {
  fetchSavedRecipes();
});
</script>

<template>
  <section>
    <h3>Сохранённые рецепты</h3>
    <div class="row">
      <div v-for="savedRecipe in savedRecipes" :key="savedRecipe.id" class="col-md-4">
        <div class="recipe-card">
          <a :href="'/recipes/' + savedRecipe.recipe.id">
            <img
              :src="savedRecipe.recipe.image ? savedRecipe.recipe.image : cookingImage"
              :alt="savedRecipe.recipe.title"
              class="recipe-image img-fluid"
            />
          </a>
          <h5 class="recipe-title">{{ savedRecipe.recipe.title }}</h5>
          <p>Автор: <strong> {{ savedRecipe.recipe.author.username }}</strong></p>
          <ul class="ingredient-list">
            <li v-for="ingredient in savedRecipe.recipe.description.split(',')" :key="ingredient">{{ ingredient.trim() }}</li>
          </ul>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>

</style>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import cookingImage from '@/assets/images/cooking.png';

const recipes = ref([]);

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

const fetchRecipes = async () => {
  try {
    const userId = await getUserIdFromToken();
    const response = await axios.get(`http://127.0.0.1:8000/users/${userId}/recipes/`);
    recipes.value = response.data;
  } catch (error) {
    console.error("Ошибка при загрузке рецептов:", error);
  }
};

onMounted(() => {
  fetchRecipes();
});
</script>

<template>
  <section>
    <h3>Мои рецепты</h3>
    <div class="row">
      <div v-for="recipe in recipes" :key="recipe.id" class="col-md-4">
        <div class="recipe-card">
          <a :href="'/recipes/' + recipe.id">
          <img
            :src="recipe.image ? recipe.image : cookingImage"
            :alt="recipe.title"
            class="recipe-image img-fluid"
          />
          </a>
          <h5 class="recipe-title">{{ recipe.title }}</h5>
          <ul class="ingredient-list">
            <li v-for="ingredient in recipe.description.split('\r\n')" :key="ingredient">{{ ingredient }}</li>
          </ul>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>

</style>

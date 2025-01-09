<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const recipe = ref(null);
const isSaved = ref(false);

const fetchRecipe = async (id) => {
  try {
    const response = await axios.get(`http://localhost:8000/recipes/${id}/`);
    recipe.value = response.data;
    await checkSavedRecipe(id);
  } catch (error) {
    console.error("Ошибка при загрузке рецепта:", error);
  }
};

const getCurrentUserId = async () => {
  try {
    const token = localStorage.getItem('auth_token');
    if (!token) return null;

    const response = await axios.get('http://localhost:8000/auth/users/me/', {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data.id;
  } catch (error) {
    console.error('Ошибка при получении данных о пользователе:', error);
    return null;
  }
};

const checkSavedRecipe = async (recipeId) => {
  try {
    const response = await axios.get('http://localhost:8000/save-recipe/');
    const savedRecipes = response.data;
    const userId = await getCurrentUserId();
    isSaved.value = savedRecipes.some(
      (saved) => saved.recipe === recipeId && saved.user === userId
    );
  } catch (error) {
    console.error("Ошибка при проверке сохранения рецепта:", error);
  }
};

const saveRecipe = async () => {
  try {
    const token = localStorage.getItem('auth_token');
    if (!token) {
      alert("Вы не авторизованы! Пожалуйста, войдите в систему.");
      return;
    }

    const userId = await getCurrentUserId();
    if (!userId || !recipe.value?.id) return;

    if (isSaved.value) {
      console.log("Рецепт уже сохранён.");
      return;
    }

    await axios.post(
  'http://localhost:8000/save-recipe/',
  {
    user: userId,
    recipe: recipe.value.id
  },
  { headers: { Authorization: `Bearer ${token}` } }
);

    isSaved.value = true;
    alert("Рецепт сохранён в ваш профиль!");
  } catch (error) {
    console.error("Ошибка при сохранении рецепта:", error);
  }
};

onMounted(() => {
  const recipeId = route.params.id;
  fetchRecipe(recipeId);
});
</script>

<template>
  <div v-if="recipe">
    <button v-if="!isSaved" @click="saveRecipe" class="subscribe-button">Сохранить рецепт</button>
    <button v-else class="subscribe-button">Рецепт сохранён</button>
  </div>
  <div v-else>
    <p>Загрузка...</p>
  </div>
</template>

<style scoped>
.subscribe-button {
  display: inline-block;
  background-color: var(--divider-color);
  color: var(--bg-color);
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 10px;
  margin-left: 10px;
}
.subscribe-button:hover {
  background-color: var(--btn-hover-color);
}
</style>

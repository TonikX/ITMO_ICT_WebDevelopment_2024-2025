<script setup>
import { onMounted } from 'vue';
import { useRecipes } from '@/composables/useRecipes';

const { recipes, loading, error, fetchRecipes } = useRecipes('http://localhost:8000/recipes/high-rating/');

onMounted(async () => {
  await fetchRecipes();
});
</script>

<template>
  <section class="suggestion-section" aria-label="Рейтинговые рецепты">
    <h2>Рейтинговые рецепты</h2>
    <div v-if="loading">Загрузка...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-for="(suggestion, index) in recipes" :key="index" class="row mb-4">
      <div class="col-12 col-md-3">
        <a :href="'/recipes/' + suggestion.id">
          <img :src="'http://localhost:8000' + suggestion.image" class="square-image" :alt="suggestion.title" />
        </a>
      </div>
      <div class="col-12 col-md-9">
        <h3 class="h31">{{ suggestion.title }}</h3>
        <p class="text-recipe">Автор: {{ suggestion.author_name }}</p>
        <p class="text-recipe">{{ suggestion.description }}</p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.square-image {
  width: 100%;
  height: 100%;
  max-width: 300px;
  max-height: 300px;
  object-fit: cover;
  border-radius: 15px;
  text-align: center;
  border: 2px solid var(--divider-color);
}

@media (max-width: 768px) {
  .square-image {
    max-width: 200px;
    max-height: 200px;
  }
}

@media (max-width: 576px) {
  .square-image {
    max-width: 150px;
    max-height: 150px;
  }
}

h2 {
  font-family: Quicksand, sans-serif;
  color: var(--divider-color);
  font-size: 28px;
  font-weight: bold;
  margin-top: 25px;
  margin-bottom: 25px;
}

.h31 {
    font-family: Quicksand, sans-serif;
    font-weight: bold;
    font-size: 20px;
    color: var(--h3-text-color);
    margin-top: 10px;
    text-align: left;
}

.text-recipe {
  font-size: 16px;
  color: var(--card-text-color);
}

.text-recipe:first-of-type {
  font-weight: bold;
}
</style>

<script setup>
import { onMounted } from 'vue';
import { useRecipes } from '@/composables/useRecipes';

const { recipes, loading, error, fetchRecipes } = useRecipes('http://localhost:8000/recipes/');

onMounted(async () => {
  await fetchRecipes();
});
</script>

<template>
  <section class="all-section" aria-label="Все рецепты">
    <h2>Все рецепты</h2>
    <div v-if="loading">Загрузка...</div>
    <div v-else-if="error">{{ error }}</div>
    <div class="row">
      <article
        v-for="(recipe) in recipes"
        :key="recipe.id"
        class="col-md-3 recipe"
        :data-author="recipe.author"
        :data-name="recipe.title"
        :data-difficulty="recipe.complexity"
      >
        <a :href="'/recipes/' + recipe.id">
          <img :src="recipe.image" class="square-image" :alt="recipe.title" />
        </a>
        <h3 class="h3-recipe">{{ recipe.title }}</h3>
        <p class="text-recipe">Автор: {{ recipe.author?.username || 'Неизвестен' }}</p>
        <p class="text-recipe">Ингредиенты: {{ recipe.description }}</p>
      </article>
    </div>
  </section>
</template>

<style scoped>
.all-section {
  padding: 20px;
}

.row {
  display: flex;
  flex-wrap: wrap;
}

.recipe {
  flex: 1 1 calc(25% - 20px);
  max-width: 25%;
  border-radius: 15px;
  padding: 15px;
  box-sizing: border-box;
  overflow: hidden;
  margin-bottom: 20px;
}

.square-image {
  width: 100%;
  height: auto;
  max-height: 300px;
  object-fit: cover;
  border-radius: 15px;
  text-align: center;
  border: 2px solid var(--divider-color);
}

@media (max-width: 1200px) {
  .recipe {
    flex: 1 1 calc(33.33% - 20px);
  }
}

@media (max-width: 768px) {
  .recipe {
    flex: 1 1 calc(50% - 20px);
  }
  .square-image {
    max-width: 200px;
    max-height: 200px;
  }
}

@media (max-width: 576px) {
  .recipe {
    flex: 1 1 100%;
  }
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

.h3-recipe {
  font-family: Quicksand, sans-serif;
  font-weight: bold;
  font-size: 20px;
  color: var(--h3-text-color);
  margin-top: 10px;
  text-align: center;
}

.text-recipe {
  font-size: 16px;
  color: var(--card-text-color);
}
</style>




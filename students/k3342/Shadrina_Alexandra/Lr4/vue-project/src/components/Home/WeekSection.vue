<script setup>
import { onMounted, ref } from 'vue';
import { useRecipes } from '@/composables/useRecipes';

const { recipes, loading, error, fetchRecipes } = useRecipes('http://localhost:8000/recipes/recent/');

const recipeGroups = ref([]);

onMounted(async () => {
  recipeGroups.value = await fetchRecipes();
});
</script>

<template>
  <section class="popular-section" aria-label="Популярные рецепты">
    <h2 class="h2">На этой неделе</h2>
    <div v-if="loading">Загрузка...</div>
    <div v-else-if="error">{{ error }}</div>
    <div id="popularSlider" class="carousel slide" data-bs-ride="carousel">
      <div class="carousel-inner">
        <div
          class="carousel-item"
          :class="{ active: index === 0 }"
          v-for="(recipeGroup, index) in recipeGroups"
          :key="index"
        >
          <div class="row justify-content-center">
            <div
              class="col-12 col-sm-6 col-md-4 col-lg-3"
              v-for="recipe in recipeGroup"
              :key="recipe.id"
            >
              <a :href="'/recipes/' + recipe.id">
                <img
                  :src="recipe.image"
                  class="square-image"
                  :alt="recipe.title"
                />
              </a>
              <p class="text-center">{{ recipe.title }}</p>
            </div>
          </div>
        </div>
      </div>
      <button
        class="carousel-control-prev"
        type="button"
        data-bs-target="#popularSlider"
        data-bs-slide="prev"
      >
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button
        class="carousel-control-next"
        type="button"
        data-bs-target="#popularSlider"
        data-bs-slide="next"
      >
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
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

.carousel-control-prev,
.carousel-control-next {
  width: 80px;
}

.carousel-control-prev-icon,
.carousel-control-next-icon {
  background-color: var(--header-text-color);
  border-radius: 50%;
  width: 40px;
  height: 40px;
}

h2 {
  font-family: Quicksand, sans-serif;
  color: var(--divider-color);
  font-size: 28px;
  font-weight: bold;
  margin-top: 25px;
  margin-bottom: 25px;
}

.text-center {
  text-align: center;
  margin-top: 10px;
  color: var(--card-text-color);
  font-size: 16px;
  font-weight: normal;
}
</style>

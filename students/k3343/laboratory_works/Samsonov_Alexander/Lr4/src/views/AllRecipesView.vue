<script setup>

import {onMounted, ref} from "vue";
import {fetchAndReturn} from "@/composables/serverActions.js";
import RecipeCard from "@/components/genericInterface/ListCard.vue";

const Recipes = ref(null)
const rLoading = ref(true);
const rError = ref(null);

onMounted(async () => {
  await fetchAndReturn(`recipes/`, Recipes, rLoading, rError)
})
</script>

<template>
  <div v-if="rLoading">Loading recipe...</div>
  <div v-else-if="rError">{{ rError }}</div>
  <div v-else>
    <h1>Все рецепты:</h1>
    <div class="row row-cols-1 row-cols-sm-1 row-cols-md-3 row-cols-lg-4">
      <div v-for="recipe in Recipes" class="col-3">
        <RecipeCard :recipe="recipe"/>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
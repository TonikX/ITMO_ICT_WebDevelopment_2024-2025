<script setup>
import {ref} from "vue";

const props = defineProps(['recipe'])
const recipe = ref(props.recipe)
</script>


<template>
  <div class="row mb-3">
    <div class="col-8">
      <div class="position-relative" style="width: 100%; height: 350px; overflow: hidden">
        <img :src="recipe.thumbnail_link" class="card-img-top" :alt="recipe.header"
             style="width: 100%; height: 100%; object-fit: cover; border-radius: 10px">
      </div>
    </div>
    <div class="col-4">
      <div class="h1">Блюдо дня</div>
      <hr>
      <strong class="h5">{{ recipe.header }}</strong><br>
      <small>By {{ recipe.author.username }}</small>

      <p>difficulty: {{ recipe.difficulty }}</p>
      <p>rating: {{ (recipe.stars_sum / recipe.number_ratings).toFixed(1) }}/10</p>
      <router-link :to="`/recipe/${recipe.id}`" class="btn btn-primary">
        View Recipe
      </router-link>
    </div>
  </div>
</template>


<style scoped>

</style>
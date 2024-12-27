<template>
  <div class="card">
    <img :src="recipe.thumbnail_link" class="card-img-top" :alt="recipe.header" />
    <div class="card-body">
      <h5 class="card-title">{{ recipe.header }}</h5>
      <p class="card-text">
        This is a delicious recipe. Click below to learn more!
      </p>
      <router-link :to="`/recipe/${recipe.id}`" class="btn btn-primary">
        View Recipe
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "RecipeCard",
  props: {
    recipe: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped></style>

<script setup>
import Header from "@/components/Header.vue";
import RecipeInfo from "@/components/RecipePage/RecipeInfo.vue";
import SaveRateRecipe from "@/components/RecipePage/SaveRateRecipe.vue";
</script>

<template>
  <Header />
  <div class="recipe-container">
    <main>
      <RecipeInfo />
      <SaveRateRecipe />
    </main>
  </div>
</template>

<style scoped>
.recipe-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  background-color: var(--recipe-bg-color);
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
</style>

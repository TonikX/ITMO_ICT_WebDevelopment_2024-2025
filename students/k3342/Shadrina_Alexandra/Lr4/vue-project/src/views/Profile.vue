<script setup>
import Header from "@/components/Header.vue";
import UserInfo from '@/components/Profile/UserInfo.vue';
import UserRecipes from "@/components/Profile/UserRecipes.vue";
import UserSavedRecipes from "@/components/Profile/UserSavedRecipes.vue";
</script>

<template>
  <Header />
  <div class="container">
    <main>
      <UserInfo/>
      <UserRecipes/>
      <UserSavedRecipes/>
    </main>
  </div>
</template>

<style>
h3 {
  font-family: Quicksand, sans-serif;
  font-weight: bold;
  font-size: 20px;
  color: var(--header-text-color);
  margin-top: 20px;
  margin-bottom: 20px;
  text-align: center;
}

.recipe-card {
  background-color: var(--card-bg-color);
  border-radius: 15px;
  padding: 15px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  text-align: center;
}

.recipe-image {
  border-radius: 10px;
  width: 100%;
  height: 100%;
  max-width: 300px;
  max-height: 300px;
  object-fit: cover;
  border: 2px solid var(--divider-color);
}

.recipe-title {
  font-size: 1.2rem;
  margin-top: 10px;
  font-family: Quicksand, sans-serif;
  color: var(--divider-color);
  font-weight: bold;
}

.ingredient-list {
  list-style: none;
  padding: 0;
}
</style>

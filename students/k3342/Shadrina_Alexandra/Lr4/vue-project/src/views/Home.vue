<script setup>
import Header from "@/components/Header.vue";
import WeekSection from '../components/Home/WeekSection.vue'
import RatingSection from '../components/Home/RatingSection.vue'
import RecipesSection from '../components/Home/RecipesSection.vue'
</script>

<template>
  <Header />
  <div class="container">
    <main>
      <WeekSection />
      <hr class="divider" />
      <RatingSection />
      <hr class="divider" />
      <RecipesSection />
    </main>
  </div>
</template>

<style scoped>
.divider {
    color: var(--divider-color);
}
</style>

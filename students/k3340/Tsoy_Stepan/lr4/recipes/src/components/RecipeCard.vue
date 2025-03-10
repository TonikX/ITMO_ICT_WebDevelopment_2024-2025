<script setup lang="ts">
defineProps<{
  id: number;
  title: string;
  headline: string;
  image: string;
  difficulty: string;
  author: string;
}>();
</script>

<template>
  <RouterLink :to="`/recipes/${id}`" class="text-decoration-none">
    <div class="card shadow-sm">
      <img :src="image" class="card-img-top" alt="Recipe Image"/>
      <div class="card-body">
        <h5 class="card-title">{{ title }}</h5>
        <p class="card-text">{{ headline }}</p>
        <p class="text-muted"><strong>Difficulty:</strong> {{ difficulty.toUpperCase() }}</p>
        <p class="text-muted"><strong>Author:</strong> {{ author }}</p>
      </div>
    </div>
  </RouterLink>
</template>

<style scoped>
.card {
  border-radius: 10px;
  overflow: hidden;
  transition: transform 0.2s ease-in-out;
}

.card:hover {
  transform: scale(1.05);
}

.card-img-top {
  height: 180px;
  object-fit: cover;
}
</style>

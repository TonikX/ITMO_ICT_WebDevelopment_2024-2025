<template>
  <router-link :to="`/workouts/${cardData.id}`" class="card" style="width: 18rem;">
    <div class="card-body">
      <h5 class="card-title">{{ cardData.title }}</h5>
      <h6 class="card-subtitle mb-2 text-muted">By: {{ cardData.author.username }}</h6>
      <p class="card-text">Estimated time: {{ formattedTime }}</p>
      <p class="card-text" v-if="cardData.rating > 0">Rating: {{ cardData.rating }} / 10</p>
      <p class="card-text" v-else>Rating: no data</p>
    </div>
  </router-link>
</template>

<script setup>
import {computed, ref} from "vue";

const props = defineProps(['cardData']);
const cardData = ref(props.cardData)

const formattedTime = computed(() => {
  const totalMinutes = cardData.value.time_takes * 15;
  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;
  return `${hours}h ${minutes}m`;
});
</script>

<style scoped>
.card {
  margin: 1rem;
  text-decoration: none;
  color: inherit;
}
</style>

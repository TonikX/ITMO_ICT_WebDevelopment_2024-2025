<script setup>

import {onMounted, ref} from "vue";
import {fetchWithLoading} from "@/composables/serverActions.js";
import SmallCard from "@/components/smallCard.vue";

const Workouts = ref(null)
const rLoading = ref(true);
const rError = ref(null);

onMounted( () => {
  fetchWithLoading(`account/favorites/`, Workouts, rLoading, rError)
})
</script>

<template>
  <div v-if="rLoading">Loading workouts...</div>
  <div v-else-if="rError">{{ rError }}</div>
  <div v-else>
    <h1>Your favorite workouts:</h1>
    <div class="row row-cols-1 row-cols-sm-1 row-cols-md-3 row-cols-lg-4">
      <div v-for="workout in Workouts" class="col-3">
        <small-card class="col-3" :cardData="workout" />
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
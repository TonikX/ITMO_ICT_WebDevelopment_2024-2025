<script setup>
import BigHero from "@/components/BigHero.vue";
import {onMounted, ref} from "vue";
import {fetchWithLoading} from "@/composables/serverActions.js";
import SmallCard from "@/components/smallCard.vue";

const workoutsData = ref(null)
const workoutsErrors = ref(null)
const workoutsLoading = ref(true)

onMounted(() => {
  fetchWithLoading('/workouts', workoutsData, workoutsLoading, workoutsErrors)
})
</script>

<template>
  <div class="container">
    <BigHero/>

    <h1>New posts</h1>
    <div v-if="workoutsLoading">
      Loading...
    </div>
    <div v-else-if="workoutsErrors">
      {{workoutsErrors}}
    </div>
    <div v-else class="row">
      <div v-for="workout in workoutsData.slice(-4)" class="col-3">
        <small-card :card-data="workout" />
      </div>
    </div>

  </div>
</template>

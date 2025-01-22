<script setup>

import {onMounted, ref} from "vue";
import {fetchWithLoading} from "@/composables/serverActions.js";
import SmallCard from "@/components/smallCard.vue";
import CommentCard from "@/components/workoutPage/commentCard.vue";

const Comments = ref(null)
const rLoading = ref(true);
const rError = ref(null);

onMounted( () => {
  fetchWithLoading(`account/comments/`, Comments, rLoading, rError)
})
</script>

<template>
  <div v-if="rLoading">Loading workouts...</div>
  <div v-else-if="rError">{{ rError }}</div>
  <div v-else>
    <h1>Your comments:</h1>
    <div class="row row-cols-1 row-cols-sm-1 row-cols-md-3 row-cols-lg-4">
      <div v-for="comment in Comments" class="col-3">
        <comment-card :comment="comment"/>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
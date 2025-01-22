<script setup>
import {onMounted, ref} from "vue";
import {fetchWithLoading} from "@/composables/serverActions.js";
import SmallCard from "@/components/smallCard.vue";
import {isAuthenticated} from "@/composables/tokenActions.js";

const workoutsData = ref(null)
const workoutsErrors = ref(null)
const workoutsLoading = ref(true)

onMounted(() => {
  fetchWithLoading('/workouts', workoutsData, workoutsLoading, workoutsErrors)
})
</script>

<template>
  <div class="container">
    <h1>All workouts</h1>
    <div v-if="workoutsLoading">
      Loading...
    </div>
    <div v-else-if="workoutsErrors">
      {{ workoutsErrors }}
    </div>
    <div v-else class="row">
      <div v-for="workout in workoutsData" class="col-3">
        <small-card :card-data="workout"/>
      </div>
    </div>

    <hr>
    <div class="publish-container text-center">
      <h1 class="mb-4">Want to publish your own workout?</h1>
      <div v-if="isAuthenticated">
        <router-link to="/account/publish" class="btn btn-primary btn-lg">Click here</router-link>
      </div>
      <div v-else>
        <small class="d-block mb-3 text-muted">You will need to authenticate</small>
        <router-link to="/login" class="btn btn-secondary btn-lg me-2">Log in</router-link>
        <router-link to="/register" class="btn btn-success btn-lg">Register account</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.publish-container {
  margin-top: 2rem;
  padding: 2rem;
  background-color: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h1 {
  font-size: 2rem;
  color: #343a40;
}

.btn {
  padding: 0.75rem 1.5rem;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-secondary {
  background-color: #6c757d;
  border-color: #6c757d;
}

.btn-success {
  background-color: #28a745;
  border-color: #28a745;
}

.text-muted {
  font-size: 0.875rem;
}
</style>
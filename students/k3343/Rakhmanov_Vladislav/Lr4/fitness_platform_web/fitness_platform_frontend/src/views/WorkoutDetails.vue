<template>
  <div class="container mt-4" v-if="workout">
    <h1 class="mb-4">{{ workout.title }}</h1>

    <div class="card">
      <div class="card-body">
        <p class="card-text">{{ workout.description }}</p>
        <div class="mb-3">
          <strong>Level:</strong> {{ workout.level }}
        </div>
        <div class="mb-3">
          <strong>Type:</strong> {{ workout.workout_type }}
        </div>
        <div class="mb-3">
          <strong>Duration:</strong> {{ workout.duration_minutes }} minutes
        </div>
        <div class="mb-3">
          <strong>Created At:</strong> {{ formatDate(workout.created_at) }}
        </div>
        <div class="mb-3">
          <strong>Video:</strong>
          <a :href="workout.video_url" target="_blank" class="btn btn-primary btn-sm ms-2">Watch Video</a>
        </div>
      </div>
    </div>

    <div class="mt-4" v-if="can_edit">
      <router-link :to="`/workouts/${workout.id}/edit`" class="btn btn-warning me-2">Edit</router-link>
      <button @click="deleteWorkout" class="btn btn-danger">Delete</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref, onMounted} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import api from "@/services/axios.ts";
import {getWorkout, type workoutData} from "@/composables/WorkoutActions.ts";
import {isAdmin} from "@/composables/AccountActions.ts";

const can_edit = ref<boolean>(false);
const route = useRoute();
const router = useRouter();
const workout = ref<workoutData | null>(null);

onMounted(async () => {
  const workoutId = (route.params.id).toString();
  try {
    const res = await getWorkout(workoutId)
    if (res) {
      workout.value = res
    }
  } catch (error) {
    console.error(error);
  }
  can_edit.value = await isAdmin();
});

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString();
};

const deleteWorkout = async () => {
  if (confirm('Are you sure you want to delete this workout?')) {
    try {
      const response = await api.delete(`fitness/workouts/${workout.value?.id}/`);
      if (response.status === 204) {
        alert('Workout was deleted');
        router.push('/workouts');
      }
    } catch (error) {
      console.error('Failed to delete workout:', error);
    }
  }
};
</script>

<style scoped>
</style>
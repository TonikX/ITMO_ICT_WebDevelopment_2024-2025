<script setup lang="ts">
defineProps<{
  workout: {
    id: number;
    title: string;
    description: string;
    video_url: string;
    level: string;
    workout_type: string;
    duration_minutes: number;
    created_at: string;
  };
}>();
</script>

<template>
  <div class="card shadow-sm">
    <img :src="workout.video_url" class="card-img-top" alt="Workout video thumbnail" />
    <div class="card-body">
      <h5 class="card-title">{{ workout.title }}</h5>
      <p class="card-text text-muted">{{ workout.description.substring(0,100)+".." }}</p>
      <div class="d-flex justify-content-between align-items-center">
        <span class="badge bg-primary">{{ workout.workout_type }}</span>
        <span class="badge bg-success">{{ workout.level }}</span>
      </div>
      <div class="mt-2 text-muted small">Duration: {{ workout.duration_minutes }} min</div>
      <router-link :to="`/workouts/${workout.id}`" class="btn btn-outline-primary w-100 mt-3">View Workout</router-link>
    </div>
  </div>
</template>


<style scoped>
.card-img-top {
  height: 200px;
  object-fit: cover;
}
</style>

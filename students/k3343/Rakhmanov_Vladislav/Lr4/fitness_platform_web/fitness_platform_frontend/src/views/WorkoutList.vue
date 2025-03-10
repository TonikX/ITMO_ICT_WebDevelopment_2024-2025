<script setup lang="ts">
import WorkoutCard from "@/components/WorkoutCard.vue";
import { getAllWorkouts, type workoutData } from "@/composables/WorkoutActions.ts";
import {onMounted, ref, watch} from "vue";
import { convertVideoToThumbnail } from "@/composables/YoutubeActions.ts";
import {isAdmin} from "@/composables/AccountActions.ts";

const can_create_new = ref<boolean>(false);
const workouts = ref<workoutData[]>([]);
const searchQuery = ref("");
const filters = ref({
  level: "",
  workout_type: "",
  duration_minutes: "",
});

const fetchWorkouts = async () => {
  const queryParams = new URLSearchParams();
  if (searchQuery.value) queryParams.append("search", searchQuery.value);
  if (filters.value.level) queryParams.append("level", filters.value.level);
  if (filters.value.workout_type) queryParams.append("workout_type", filters.value.workout_type);
  if (filters.value.duration_minutes) queryParams.append("duration_minutes", filters.value.duration_minutes);

  workouts.value = await getAllWorkouts(queryParams.toString());
  workouts.value.forEach((workout: workoutData) => {
    workout.video_url = convertVideoToThumbnail(workout.video_url);
  });

  can_create_new.value = await isAdmin()
};

onMounted(fetchWorkouts);

watch([searchQuery, filters], fetchWorkouts, { deep: true });
</script>

<template>
  <div class="container">
    <h1>View Workouts</h1>
    <hr>
    <p>Unlock your full potential with expertly designed workout routines. Whether you're aiming to build strength,
      improve flexibility, or boost endurance, our workouts cater to all fitness levels. Stay consistent, track your
      progress, and achieve your fitness goals with structured exercises that keep you motivated and engaged.</p>

    <div class="row mb-4">
      <div class="col-md-6">
        <input
            v-model="searchQuery"
            type="text"
            class="form-control"
            placeholder="Search by title or description..."
        />
      </div>
      <div class="col-md-2">
        <select v-model="filters.level" class="form-select">
          <option value="">All Levels</option>
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="advanced">Advanced</option>
        </select>
      </div>
      <div class="col-md-2">
        <select v-model="filters.workout_type" class="form-select">
          <option value="">All Types</option>
          <option value="strength">Strength</option>
          <option value="flexibility">Flexibility</option>
          <option value="cardio">Cardio</option>
        </select>
      </div>
      <div class="col-md-2" v-if="can_create_new">
        <router-link to="/workouts/new/" class="btn btn-outline-primary">Create a new workout</router-link>
      </div>
    </div>

    <div class="row row-cols-1 row-cols-md-3 g-3">
      <div class="col" v-for="workout in workouts" :key="workout.id">
        <WorkoutCard :workout="workout" />
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Add custom styles if needed */
</style>
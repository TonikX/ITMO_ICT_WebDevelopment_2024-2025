<template>
  <div class="container mt-4">
    <h1>Create New Workout</h1>
    <hr />

    <form @submit.prevent="submitForm">
      <div class="mb-3">
        <label for="title" class="form-label">Title</label>
        <input
            v-model="workout.title"
            type="text"
            class="form-control"
            id="title"
            required
        />
      </div>

      <div class="mb-3">
        <label for="description" class="form-label">Description</label>
        <textarea
            v-model="workout.description"
            class="form-control"
            id="description"
            rows="3"
            required
        ></textarea>
      </div>

      <div class="mb-3">
        <label for="video_url" class="form-label">Video URL</label>
        <input
            v-model="workout.video_url"
            type="url"
            class="form-control"
            id="video_url"
            required
        />
      </div>

      <div class="mb-3">
        <label for="level" class="form-label">Level</label>
        <select
            v-model="workout.level"
            class="form-select"
            id="level"
            required
        >
          <option value="" disabled>Select Level</option>
          <option value="beginner">Beginner</option>
          <option value="intermediate">Intermediate</option>
          <option value="advanced">Advanced</option>
        </select>
      </div>

      <div class="mb-3">
        <label for="workout_type" class="form-label">Workout Type</label>
        <select
            v-model="workout.workout_type"
            class="form-select"
            id="workout_type"
            required
        >
          <option value="" disabled>Select Type</option>
          <option value="cardio">Cardio</option>
          <option value="strength">Strength</option>
          <option value="flexibility">Flexibility</option>
        </select>
      </div>

      <div class="mb-3">
        <label for="duration_minutes" class="form-label">Duration (Minutes)</label>
        <input
            v-model.number="workout.duration_minutes"
            type="number"
            class="form-control"
            id="duration_minutes"
            required
        />
      </div>

      <button type="submit" class="btn btn-primary">Create Workout</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import {createWorkout, type workoutCreateData} from "@/composables/WorkoutActions.ts";

const workout = ref<workoutCreateData>({
  title: "",
  description: "",
  video_url: "",
  level: "",
  workout_type: "",
  duration_minutes: 0,
});

const submitForm = async () => {
  await createWorkout(workout.value)
};
</script>

<style scoped>
</style>
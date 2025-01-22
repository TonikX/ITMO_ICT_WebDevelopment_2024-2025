<template>
  <div class="container mt-5">
    <form @submit.prevent="handleSubmit">
      <div class="mb-3">
        <label for="title" class="form-label">Title</label>
        <input
            type="text"
            id="title"
            class="form-control"
            v-model="form.title"
            placeholder="Enter the title"
        />
      </div>
      <div class="mb-3">
        <label for="description" class="form-label">Description</label>
        <textarea
            id="description"
            class="form-control"
            v-model="form.description"
            rows="4"
            placeholder="Enter the description"
        ></textarea>
      </div>

      <div class="mb-3">
        <label for="tags" class="form-label">Tags (comma-separated)</label>
        <input
            type="text"
            id="tags"
            class="form-control"
            v-model="tagInput"
            placeholder="Enter tags separated by commas"
            @blur="splitTags"
        />
        <small class="form-text text-muted">Tags will be split into a list automatically.</small>
      </div>

      <div class="mb-3">
        <label for="steps" class="form-label">Steps (newline-separated)</label>
        <textarea
            id="steps"
            class="form-control"
            v-model="stepsInput"
            rows="6"
            placeholder="Enter steps, one per line"
            @blur="splitSteps"
        ></textarea>
        <small class="form-text text-muted">Steps will be split into a list automatically.</small>
      </div>

      <div class="mb-3">
        <label for="time_takes" class="form-label">Time Takes (in minutes)</label>
        <input
            type="number"
            id="time_takes"
            class="form-control"
            v-model="form.time_takes"
            placeholder="Enter time in minutes"
            @blur="roundToInterval"
        />
        <small class="form-text text-muted">
          Time will be rounded to the nearest 15-minute interval.
        </small>
      </div>

      <div class="mb-3">
        <label for="video_link" class="form-label">Video Link</label>
        <input
            type="url"
            id="video_link"
            class="form-control"
            v-model="form.video_link"
            placeholder="Enter a valid video URL"
        />
      </div>

      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>
</template>

<script setup>
import {ref} from "vue";
import {CreateWorkout} from "@/composables/serverActions.js";
import router from "@/router/index.js";

const form = ref({
  tags: [],
  steps: [],
  time_takes: 0,
  title: "",
  description: "",
  video_link: "",
});

const tagInput = ref("");
const stepsInput = ref("");

const splitTags = () => {
  form.value.tags = tagInput.value
      .split(",")
      .map(tag => tag.trim())
      .filter(tag => tag !== "");
};

const splitSteps = () => {
  form.value.steps = stepsInput.value
      .split("\n")
      .map(step => step.trim())
      .filter(step => step !== "");
};

const roundToInterval = () => {
  if (form.value.time_takes !== null) {
    const time = parseInt(form.value.time_takes, 10);
    form.value.time_takes = Math.round(time / 15) * 15;
  }
};

const handleSubmit = async () => {
  const response = await CreateWorkout(form.value)
  if (response) {
    form.value = {
      tags: [],
      steps: [],
      time_takes: 0,
      title: "",
      description: "",
      video_link: "",
    }
    tagInput.value = ''
    stepsInput.value = ''
    router.push(`/workouts/${response}`)
  }
};
</script>

<style>
</style>

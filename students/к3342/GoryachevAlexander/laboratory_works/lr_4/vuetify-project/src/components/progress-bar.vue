<template>
  <div class="progress-bar-container">
    <div
      class="progress-bar"
      :style="{
        width: `${progress}%`,
        backgroundColor: color
      }"
    ></div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

// Props to customize the progress bar
const props = defineProps({
  progress: {
    type: Number,
    required: true,
    validator: (value) => value >= 0 && value <= 100, // Ensures progress is between 0 and 100
  },
  color: {
    type: String,
    default: 'blue', // Default color if not provided
  },
});
</script>

<style scoped>
.progress-bar-container {
  width: 100%;
  height: 10px;
  background-color: #e0e0e0; /* Light gray background */
  border-radius: 5px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  transition: width 0.3s ease;
}
</style>

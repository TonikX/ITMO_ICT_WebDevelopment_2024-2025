<template>
  <div class="container mt-4">
    <ul class="list-group">
      <li v-for="(item, index) in workoutList" :key="index" class="list-group-item">
        {{ item }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  workoutList: {
    type: Array,
    required: true
  }
});
</script>

<style scoped>
</style>

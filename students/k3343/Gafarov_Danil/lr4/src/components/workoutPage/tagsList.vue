<template>
  <div class="tag-container">
    <div class="tag-bubble" v-for="(tag, index) in tags" :key="index">
      {{ tag }}
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  tags: {
    type: Array,
    required: true
  }
});
</script>

<style scoped>
.tag-container {
  display: flex;
  flex-wrap: nowrap;
  overflow-x: auto;
  gap: 10px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.tag-bubble {
  background-color: #007bff;
  color: white;
  border-radius: 20px;
  padding: 8px 15px;
  font-size: 1rem;
  display: inline-block;
  white-space: nowrap;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.tag-bubble:hover {
  background-color: #0056b3;
}
</style>

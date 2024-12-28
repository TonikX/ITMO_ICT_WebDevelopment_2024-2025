<script setup>

import {ref} from "vue";

const props = defineProps(["commentInfo"])
const commentInfo = ref(props.commentInfo)
</script>

<template>
  <div class="custom-comment-container">
    <!-- Comment Header with Title and Rating -->
    <div class="custom-comment-header">
      <h5 class="custom-comment-title">{{ commentInfo.header }}</h5>
      <span class="custom-comment-rating">★ {{ commentInfo.rating }}</span>
    </div>

    <!-- Comment Content -->
    <p class="custom-comment-text">
      {{ commentInfo.content_text }}
    </p>

    <!-- Author Info -->
    <div class="custom-comment-author">
      <small>By: <span class="custom-author-name">{{ commentInfo.author.username }}</span></small>
    </div>
  </div>
</template>

<style scoped>
.custom-comment-container {
  max-width: 800px;
  margin: 10px auto;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-family: Arial, sans-serif;
}

.custom-comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ddd;
  padding-bottom: 8px;
  margin-bottom: 8px;
}

.custom-comment-title {
  font-size: 1.1rem;
  font-weight: bold;
  margin: 0;
}

.custom-comment-rating {
  background-color: #ffc107;
  color: #000;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: bold;
}

.custom-comment-text {
  font-size: 0.95rem;
  color: #333;
  line-height: 1.5;
  margin: 0 0 10px 0;
}

.custom-comment-author {
  text-align: right;
  font-size: 0.85rem;
  color: #666;
}

.custom-author-name {
  font-weight: bold;
  color: #000;
}
</style>
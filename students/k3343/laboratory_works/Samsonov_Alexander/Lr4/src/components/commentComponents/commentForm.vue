<script setup>
import { ref } from "vue";
import {useRoute} from "vue-router";
import {postComment} from "@/composables/serverActions.js";
import { defineEmits } from 'vue';

const emit = defineEmits(['submit-comment']);

const recipeId = useRoute().params.recipeId;
const header = ref("");
const rating = ref("");
const content_text = ref("");
const error = ref(null)

const submit = async () => {
  try {
    Number(rating.value);
  } catch (error) {
    error.value = 'Rating must be from 0 to 10';
    return;
  }
  const result = postComment(recipeId, rating.value ,header.value, content_text.value);
  if (result !== null) {
    emit("submit-comment", result);
    rating.value = "";
    header.value = "";
    content_text.value = "";
  }
}
</script>



<template>
  <form class="comment-form border p-3 rounded shadow-sm bg-light" @submit.prevent="submit">
    <div class="mb-3">
      <label for="header" class="form-label fw-bold">Title</label>
      <input
      type="text"
      id="header"
      class="form-control"
      placeholder="Enter comment title"
      v-model="header"
      />
    </div>
    <div class="mb-3">
      <label for="rating" class="form-label fw-bold">Rating</label>
      <input
      type="number"
      id="rating"
      class="form-control"
      placeholder="Enter rating (1-10)"
      v-model="rating"
      min="1"
      max="10"
      />
    </div>
    <div class="mb-3">
      <label for="content" class="form-label fw-bold">Comment</label>
      <textarea
      id="content"
      class="form-control"
      rows="4"
      placeholder="Write your comment..."
      v-model="content_text"
      ></textarea>
    </div>
    <button type="submit" class="btn btn-primary w-100">
      Submit
    </button>
  </form>
  <div v-if="error">{{error}}</div>
</template>

<style scoped>
.comment-form {
  max-width: 800px;
  margin: 20px auto;
}
</style>

<template>
  <div class="card my-3 shadow-sm">
    <div class="card-body">
      <h4 class="card-title mb-4">Submit a Comment</h4>


      <form @submit.prevent="submitForm">
        <div class="mb-3">
          <label for="title" class="form-label">Title</label>
          <input
            type="text"
            id="title"
            class="form-control"
            v-model="form.title"
            placeholder="Enter title"
            required
          />
        </div>

        <div class="mb-3">
          <label for="comment" class="form-label">Comment</label>
          <textarea
            id="comment"
            class="form-control"
            v-model="form.comment"
            rows="4"
            placeholder="Write your comment here"
            required
          ></textarea>
        </div>

        <div class="mb-3">
          <label for="rating" class="form-label">Rating (1-10)</label>
          <input
            type="number"
            id="rating"
            class="form-control"
            v-model.number="form.rating"
            min="1"
            max="10"
            placeholder="Enter rating"
            required
          />
        </div>

        <button type="submit" class="btn btn-primary">Submit</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue';
import axiosInstance from "@/services/axios.js";

const form = reactive({
  title: '',
  comment: '',
  rating: null,
});

const props = defineProps(['workout_id'])
const emit = defineEmits(['submitComment'])


const submitForm = async () => {
  if (form.title && form.comment && form.rating >= 1 && form.rating <= 10) {
    const response = await axiosInstance.post(`comment/workout_comment/${props.workout_id}/`, {
      "title": form.title,
    "comment": form.comment,
    "rating": form.rating,
    })
    if (response.status === 201) {
      emit('submitComment')
      form.title = '';
      form.comment = '';
      form.rating = null;
    }
  } else {
  }
};
</script>

<style scoped>
</style>

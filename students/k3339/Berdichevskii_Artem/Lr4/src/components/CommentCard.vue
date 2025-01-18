<script setup>
import { computed } from "vue";

// Props
const props = defineProps({
  review: {
    type: Object,
    required: true,
  },
});
const review = props.review;

// Computed property to format the publication date
const formattedDate = computed(() =>
  new Date(review.dt_published).toLocaleDateString(undefined, {
    year: "numeric",
    month: "long",
    day: "numeric",
  })
);
</script>

<template>
  <div class="card mb-3 shadow-sm">
    <div class="card-body">
      <h5 class="card-title">
        <strong>Rating:</strong>
        <span class="text-warning">{{ review.rating }} / 10</span>
      </h5>

      <p class="card-text">
        <strong>Review:</strong> {{ review.description }}
      </p>

      <p class="card-text">
        <small class="text-muted">Published on: {{ formattedDate }}</small>
      </p>
    </div>
  </div>
</template>

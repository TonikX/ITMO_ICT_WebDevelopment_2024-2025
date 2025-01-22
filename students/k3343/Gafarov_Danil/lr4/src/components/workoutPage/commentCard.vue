<template>
  <div class="card my-3 shadow-sm">
    <div class="card-body">

      <h5 class="card-title mb-1">
        {{ comment.title }}
      </h5>
      <h6 class="card-subtitle text-muted">
        by {{ comment.author.username }} on {{ formatDate(comment.dt_published) }}
      </h6>

      <p class="card-text mt-3">
        {{ comment.comment }}
      </p>


      <div class="mt-3">
        <span class="badge bg-primary">
          Rating: {{ comment.rating }}/10
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>

defineProps({
  comment: {
    type: Object,
    required: true
  }
});

const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'long', day: 'numeric' };
  return new Date(dateString).toLocaleDateString(undefined, options);
};
</script>

<style scoped>

</style>

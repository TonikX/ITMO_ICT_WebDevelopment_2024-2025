<template>
  <router-link :to="`/vacancies/${job.id}/`" class="card no-decoration">
    <div class="card-body">
      <h5 class="card-title">{{ job.title }}</h5>
      <h6 class="card-subtitle mb-2 text-muted">{{ job.company }}</h6>
      <p class="card-text">
        <strong>Salary:</strong> ${{ job.salary }}
      </p>
      <p class="card-text">
        <small class="text-muted">Job ID: {{ job.id }}</small>
      </p>
    </div>
  </router-link>
</template>

<script setup>
defineProps({
  job: {
    type: Object,
    required: true,
    validator: (value) =>
        value.id &&
        value.company &&
        value.title &&
        value.salary !== undefined,
  },
});
</script>
<style scoped>
.no-decoration {
  text-decoration: none;
}
</style>

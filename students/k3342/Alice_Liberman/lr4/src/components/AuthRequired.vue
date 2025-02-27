<script setup>

</script>

<template>
  <div class="container text-center mt-5">
    <div class="card p-4 shadow">
      <h2 class="card-title">Access Restricted</h2>
      <p class="card-text mt-3">
        To access this resource, you need to be authenticated. Please log in or create a new account to proceed.
      </p>
      <div class="mt-4">
        <router-link to="/login" class="btn btn-primary me-2">
          Log In
        </router-link>
        <router-link to="/register" class="btn btn-secondary">
          Create Account
        </router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
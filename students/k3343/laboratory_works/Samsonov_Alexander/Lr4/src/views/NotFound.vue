<template>
  <div class="not-found text-center">
    <div class="container mt-5">
      <h1 class="display-1 text-danger">404</h1>
      <h2 class="text-secondary">Page Not Found</h2>
      <p class="lead">
        Oops! The page you're looking for doesn't exist.
      </p>
      <router-link to="/" class="btn btn-primary mt-3">
        Go Back Home
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: "NotFound",
};
</script>

<style scoped>
body {
  background-color: #f8f9fa;
}

.not-found {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}
</style>

<template>
  <div class="not-found d-flex align-items-center">
    <div class="container text-center">
      <div class="row">
        <div class="col-lg-6 mx-auto">
          <!-- Icon or Illustration -->
          <div class="display-1 text-warning">
            <i class="bi bi-exclamation-circle"></i>
          </div>

          <!-- Main Message -->
          <h1 class="display-3 text-danger fw-bold">404</h1>
          <h2 class="text-secondary">Oops! Page Not Found</h2>
          <p class="lead text-muted">
            We can't seem to find the page you're looking for. It might have been moved, deleted, or never existed.
          </p>

          <div class="mt-4">
            <router-link to="/" class="btn btn-primary btn-lg me-2">
              Go Back Home
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "NotFound",
};
</script>

<style scoped>
.not-found {
  background-color: white;
}
</style>

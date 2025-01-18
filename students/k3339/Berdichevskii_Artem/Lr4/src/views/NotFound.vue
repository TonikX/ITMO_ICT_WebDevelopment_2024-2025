<template>
  <div class="not-found">
    <h1>404</h1>
    <h2>Page Not Found</h2>
    <p>Sorry, the page you are looking for does not exist.</p>
    <router-link to="/">Go back to Home</router-link>
  </div>
</template>

<script>
export default {
  name: 'NotFound'
}
</script>

<style scoped>
.not-found {
  text-align: center;
  margin-top: 50px;
}

.not-found h1 {
  font-size: 5rem;
  color: #ff4d4f;
}

.not-found h2 {
  font-size: 2rem;
}

.not-found p {
  font-size: 1.2rem;
}

.not-found a {
  text-decoration: none;
  color: #007bff;
}
</style>

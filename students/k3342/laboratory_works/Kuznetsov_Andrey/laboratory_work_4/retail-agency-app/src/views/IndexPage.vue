<template>
  <div class="index-background">
    <header class="index-header">
      <a class="logo" href="/" aria-label="Go to homepage">
        <svg class="logo-icon">
          <use xlink:href="#homeIcon"></use>
        </svg>
      </a>

      <nav>
        <ul class="menu index-menu">
          <li class="active">
            <router-link to="/profile" aria-label="Go to your account page">Account</router-link>
          </li>
          <li>
            <router-link to="/about" aria-label="Learn more about us">About</router-link>
          </li>
          <li>
            <router-link to="/contact" aria-label="Contact us">Contact</router-link>
          </li>
        </ul>
      </nav>
    </header>

    <main>
      <div class="index-title">
        <h1>Retail Agency</h1>
        <h2>Your partner in building happiness</h2>
      </div>

      <div class="index-button">
        <router-link to="/search" class="index-btn" aria-label="Search for your dream home">
          Search your dream
        </router-link>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'IndexPage',
};
</script>

<style scoped>
@import '../assets/css/index.css';
</style>

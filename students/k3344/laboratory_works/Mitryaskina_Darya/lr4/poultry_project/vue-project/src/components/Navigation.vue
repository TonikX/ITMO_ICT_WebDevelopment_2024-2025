<template>
  <nav>
    <ul class="menu">
      <!-- <li>
        <RouterLink to="/">Home</RouterLink>
      </li> -->
      <li>
        <RouterLink to="/hens/">Hens</RouterLink>
      </li>
      <li>
        <RouterLink to="/employees/">Employees</RouterLink>
      </li>
      <li>
        <RouterLink to="/cages/">Workshops and Cages</RouterLink>
      </li>
      <li>
        <RouterLink to="/diets/">Diets</RouterLink>
      </li>
      <li>
        <RouterLink to="/breeds/">Breeds</RouterLink>
      </li>
      <li>
        <RouterLink to="/reviews/">Reports</RouterLink>
      </li>
      <li>
        <RouterLink to="/profile/">My Account</RouterLink>
      </li>
    </ul>
  </nav>
</template>

<script setup>
import { RouterLink } from 'vue-router';

</script>

<style scoped>
  .menu {
    list-style: none;
    padding: 0;
    margin-bottom: 20px;
    display: flex;
    gap: 20px;
  }
</style>


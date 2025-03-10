<script setup lang="ts">

</script>

<template>
  <div class="px-4 py-5 my-5 text-center">
    <img class="d-block mx-auto mb-4" src="../assets/logo.webp" alt="" width="72" height="57">
    <h1 class="display-5 fw-bold text-body-emphasis">Centered hero</h1>
    <div class="col-lg-6 mx-auto">
      <p class="lead mb-4"><strong>Готовь с вдохновением!</strong> 🍽️
        <br>
        Открой для себя простые и вкусные рецепты на каждый день. Готовим легко, едим с удовольствием! 🚀✨
        </p>

      <div class="d-grid gap-2 d-sm-flex justify-content-sm-center">
        <router-link to="/recipes" class="btn btn-primary btn-lg px-4 gap-3">Посмотреть рецепты</router-link>
        <router-link to="/recipes" class="btn btn-outline-secondary btn-lg px-4">Поиск по рецептам</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
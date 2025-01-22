<script setup>

</script>

<template>
<div class="px-4 py-5 my-5 text-center">
    <img class="d-block mx-auto mb-4" src="https://getbootstrap.com/docs/5.3/assets/brand/bootstrap-logo.svg" alt="" width="72" height="57">
    <h1 class="display-5 fw-bold text-body-emphasis">Сайт с тренировками</h1>
    <div class="col-lg-6 mx-auto">
      <p class="lead mb-4">Лабораторная работа 4 по предмету "веб-разработка".
      Тема:  Платформа для фитнес-тренировок и здоровья
      Сделано с бутстрапом</p>
      <div class="d-grid gap-2 d-sm-flex justify-content-sm-center">
        <router-link type="button" class="btn btn-primary btn-lg px-4 gap-3" to="/workouts">Посмотреть все тренировки</router-link>
        <router-link type="button" class="btn btn-outline-secondary btn-lg px-4" to="/routines">Посмотреть курсы тренировок</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
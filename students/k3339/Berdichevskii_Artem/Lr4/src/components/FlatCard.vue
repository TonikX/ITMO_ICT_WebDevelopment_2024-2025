<script setup>
const data = defineProps(['unit'])
</script>

<template>
<div class="card" style="width: 18rem;">
  <div class="card-body">
    <h5 class="card-title">{{ data.unit.area_sq_m }} square meter apartment</h5>
    <h6 class="card-subtitle mb-2 text-body-secondary">{{ data.unit.area_sq_m }}$/{{data.unit.per_period}}</h6>
    <p class="card-text">{{ data.unit.address }}</p>
    <router-link :to="`/tenant/${data.unit.id}`" class="card-link btn btn-primary">Check it out</router-link>
    <slot />
  </div>
</div>
</template>

<style scoped>

</style>
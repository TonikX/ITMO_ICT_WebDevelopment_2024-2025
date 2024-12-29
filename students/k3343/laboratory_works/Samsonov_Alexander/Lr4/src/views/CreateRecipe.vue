<script setup>
import {onMounted} from "vue";
import router from "@/router/index.js";
import {isAuthenticated} from "@/composables/useAuth.js";



onMounted(async () => {
  if (! isAuthenticated.value ) {
    router.push('/');
  }
})
</script>

<template>
<!--TODO this-->
</template>

<style scoped>

</style>
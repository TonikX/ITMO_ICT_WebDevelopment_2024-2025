<script setup>
import axiosInstance from "@/services/axios.js";
import {onMounted, ref} from "vue";
import {isAuthenticated} from "@/composables/tokenActions.js";

const AccountInfo = ref(null)


onMounted(async () => {
  let res = await axiosInstance.get('auth/users/me/')
  AccountInfo.value = res.data
})
</script>

<template>

  <div v-if="AccountInfo && isAuthenticated" class="container">
    <h1>Hello, {{ AccountInfo.username }}</h1>
  </div>

</template>

<style scoped>

</style>
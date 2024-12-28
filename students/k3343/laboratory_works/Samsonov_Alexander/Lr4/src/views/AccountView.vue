<script setup>
import axiosInstance from "@/services/axios.js";
import {ref} from "vue";

const AccountInfo = ref(axiosInstance.get('auth/users/me/'))
</script>

<template>
<h1>Hello, {{AccountInfo.username}}</h1>

</template>

<style scoped>

</style>
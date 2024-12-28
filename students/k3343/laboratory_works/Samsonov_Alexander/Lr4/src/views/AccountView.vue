<script setup>
import axiosInstance from "@/services/axios.js";
import {ref} from "vue";

const AccountInfo = ref(axiosInstance.get('auth/users/me/'))
</script>

<template>
<h1>Hello, {{AccountInfo.username}}</h1>
<!--  TODO add my recipes endpoint-->
<!--  TODO add liked recipes endpoint-->
</template>

<style scoped>

</style>
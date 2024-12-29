<script setup>
import {onMounted} from "vue";
import {canEdit} from "@/composables/serverActions.js";
import {useRoute} from "vue-router";
import router from "@/router/index.js";
import {isAuthenticated} from "@/composables/useAuth.js";


const recipeId = useRoute().params.recipeId;

onMounted(async () => {
  if (! isAuthenticated.value ||!await canEdit(recipeId)) {
    router.push('/');
  }
})
</script>

<template>

</template>

<style scoped>

</style>
<template>
  <div class="log"></div>
</template>

<script setup>
  import { useStore } from 'vuex';
  import { useRouter } from 'vue-router';

  const router = useRouter();
  const store = useStore();

  store.dispatch('userLogout').then(() => {
    router.push({ name: 'login' });
  });
</script>

<style scoped></style>

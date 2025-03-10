<template>
  <div class="log"></div>
</template>

<script setup>
import { useAppStore } from '@/stores/app';
import { useRouter } from 'vue-router';

const store = useAppStore();
const router = useRouter();

store.logout();

router.push('/login');
</script>


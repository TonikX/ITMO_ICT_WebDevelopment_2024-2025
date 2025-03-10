<template>
  <v-app>
    <Navigation v-if="store.user"></Navigation>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import Navigation from '@/components/navigation.vue';
import { useAppStore } from '@/stores/app';

const store = useAppStore();
</script>

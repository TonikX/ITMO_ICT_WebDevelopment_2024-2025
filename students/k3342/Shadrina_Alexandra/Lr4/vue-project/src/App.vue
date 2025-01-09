<script setup>
import { ref } from 'vue';

const theme = ref('');

function toggleTheme() {
  theme.value = theme.value === 'dark' ? '' : 'dark';
}
</script>

<template>
  <div id="app" :data-theme="theme">
    <main>
      <router-view />
    </main>
  </div>
</template>

<style>
:root {
  --bg-color: #FFFAF3;
  --text-color: #946A49;
  --text-center-color: #946A49;
  --form-bg-color: #ffebce;
  --form-border-color: rgba(0, 0, 0, 0.1);
  --highlight-color: #a0522d;
  --btn-bg-color: #946A49;
  --btn-hover-color: #a0522d;
  --link-color: #a0522d;
  --header-bg-color: #ffebce;
  --header-text-color: #946A49;
  --h3-text-color: #946A49;
  --divider-color: #CF9363;
  --card-bg-color: #FFEFD9;
  --card-text-color: #946A49;
  --recipe-bg-color: #fff8f2;
}

body[data-theme="dark"] {
  --bg-color: #5B4D42;
  --text-color: #f0e6d2;
  --form-bg-color: #5B4D42;
  --form-border-color: rgba(255, 255, 255, 0.1);
  --highlight-color: #8b4513;
  --btn-bg-color: #9f5e43;
  --btn-hover-color: #ee9d78;
  --link-color: #ffa07a;
  --header-bg-color: #4A3B31;
  --header-text-color: #E2C8A7;
  --h3-text-color: #CF9363;
  --divider-color: #dfcab1;
  --card-bg-color: #4A3B31;
  --card-text-color: #FFEFD9;
  --recipe-bg-color: #625243;
}

body {
  font-family: Quicksand, sans-serif;
  background-color: var(--bg-color);
  color: var(--text-color);
  transition: background-color 0.3s, color 0.3s;
}
</style>

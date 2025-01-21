<template>
  <div id="app">
    <SvgIcons />
    <router-view />
  </div>
</template>

<script>
import SvgIcons from './components/SvgIcons.vue';

export default {
  components: {
    SvgIcons,
  },
};
</script>

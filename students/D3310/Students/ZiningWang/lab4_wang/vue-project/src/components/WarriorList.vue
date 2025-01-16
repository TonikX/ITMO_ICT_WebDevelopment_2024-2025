<template>
  <div class="warrior" v-for="warrior in warriors" :key="warrior.name">
    <div><strong>Имя:</strong> {{ warrior.name }}</div>
    <div><strong>Расса:</strong> {{ warrior.race }}</div>
  </div>
</template>

<script>
export default {
  props: {
    warriors: {
      type: Array,
      required: true
    }
  }
};
</script>

<style scoped>
/* 可根据需要添加样式 */
</style>

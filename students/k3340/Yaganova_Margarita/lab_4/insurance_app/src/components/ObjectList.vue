<template>
  <div class="page-container">
    <h1>{{ title }}</h1>
    <div v-for="(item, index) in infoArray" :key="index" class="info-card">
      <data-card :dict="item" :title="titleKey"></data-card>
    </div>
  </div>
  <hr>
</template>

<script>
import DataCard from './DataCard.vue';

export default {
  props: {
    title: {
      type: String,
      required: true,
    },
    infoArray: {
      type: Array,
      required: true,
    },
    titleKey: {
      type: String,
      required: true,
    },
  },
  components: {
    DataCard,
  },
};
</script>

<style scoped>.page-container {
  margin: 20px;
}

h1 {
  font-size: 24px;
  margin-bottom: 20px;
}

.info-card {
  margin-bottom: 20px;
}
</style>

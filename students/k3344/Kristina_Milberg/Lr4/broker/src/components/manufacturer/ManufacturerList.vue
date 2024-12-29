<script setup>
import router from "@/utils/router.js";


defineProps({
  manufacturers: Array,
});

</script>

<template>
  <div class="manufacturer-list">
    <template v-for="manufacturer in manufacturers" :key="manufacturer.id">
      <v-card class="manufacturer-card" width="400" @click="router.push(`/manufacturers/${manufacturer.id}`)">
        <template #title>{{ manufacturer.name }}</template>
        <template #text>
          Страна: {{ manufacturer.country }}<br/>
        </template>
      </v-card>
    </template>
  </div>
</template>

<style scoped>
.manufacturer-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.manufacturer-card {
  background-color: #424242;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.6);
  padding: 16px;
  color: #ffffff;
}

.manufacturer-card v-card-title {
  color: #ffffff;
}

.manufacturer-card v-card-text {
  color: #bdbdbd;
}

v-btn {
  color: #ffffff;
}
</style>

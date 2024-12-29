<script setup>
import {ref} from "vue";
import {tokenStore} from "@/stores/token.js";
import router from "@/utils/router.js";

tokenStore();
defineProps({
  agencies: Array,
});


ref(false);
ref({});
</script>

<template>
  <div class="agency-list">
    <template v-for="agency in agencies" :key="agency.id">
      <v-card class="agency-card" width="400" @click="router.push(`/agency/${agency.id}`)">
        <template #title>{{ agency.name }}</template>
        <template #text>
          Страна: {{ agency.country }}<br/>
          Контактный номер: {{ agency.contact_number }}
        </template>
      </v-card>
    </template>
  </div>
</template>

<style scoped>
.agency-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.agency-card {
  background-color: #424242;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.6);
  padding: 16px;
  color: #ffffff;
}

.agency-card v-card-title {
  color: #ffffff;
}

.agency-card v-card-text {
  color: #bdbdbd;
}

v-btn {
  color: #ffffff;
}
</style>

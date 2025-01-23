<script setup>
import {tokenStore} from "@/stores/token.js";

const token = tokenStore()
defineProps({
  employees: Array,
});

defineEmits("delete-employee");

</script>

<template>
  <div class="employee-list">
    <template v-for="employee in employees" :key="employee.id">
      <v-card class="employee-card" width="400">
        <template #title>{{ employee.full_name }}</template>
        <template #text>
          Данные паспорта: {{ employee.passport_number }}<br/>
        </template>
        <v-card-actions>
          <v-btn @click="$emit('delete-employee', employee.id)" color="error">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </template>
  </div>
</template>

<style scoped>
.employee-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.employee-card {
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 16px;
}
</style>

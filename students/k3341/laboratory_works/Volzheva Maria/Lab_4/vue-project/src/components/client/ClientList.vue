<script setup>
import {ref} from "vue";
import ClientModal from "@/components/client/ClientModal.vue";
defineProps({
  clients: {
    type: Array
  }
})
const emits = defineEmits(["delete-client", "update-client"]);
const isEditModalVisible = ref(false);
const selectedClient = ref({});
function handleEdit(client) {
  selectedClient.value = {...client};
  isEditModalVisible.value = true;
}
function handleUpdateClient(client) {
  emits("update-client", client);
  isEditModalVisible.value = false
}
function deleteClient(id) {
  emits("delete-client", id);
}
</script>

<template>
  <div class="client-list">
    <template v-for="client in clients" :key="client.id">
      <v-card class="client-card" width="600">
        <v-card-title>
          {{ client.first_name }} {{ client.second_name }} {{ client.patronymic }}
        </v-card-title>
        <v-card-subtitle>
          Возраст (лет): {{ client.age }}
        </v-card-subtitle>
        <v-card-actions class="client-card-actions">
          <v-btn
              size="x-small"
              icon
              :to="`/clients/${client.id}`"
          >
            <v-icon size="18">mdi-eye</v-icon>
          </v-btn>
          <v-btn
              size="x-small"
              icon
              @click="handleEdit(client)"
          >
            <v-icon size="18">mdi-pencil</v-icon>
          </v-btn>
          <v-btn
              size="x-small"
              icon
              color="error"
              @click="deleteClient(client.id)"
          >
            <v-icon size="18">mdi-delete</v-icon>
          </v-btn>
        </v-card-actions>
      </v-card>
      <div v-if="clients.length === 0">
        Нет данных для отображения.
      </div>
    </template>

    <ClientModal
        v-model="isEditModalVisible"
        :individualClientData="selectedClient"
        mode="edit"
        @submit-client="handleUpdateClient"
    />
  </div>
</template>

<style scoped>
.mountain-card {
  margin-bottom: 16px;
  position: relative;
  padding-bottom: 50px;
}
.mountain-card-actions {
  position: absolute;
  bottom: 10px;
  right: 10px;
  display: flex;
  gap: 8px;
}
</style>

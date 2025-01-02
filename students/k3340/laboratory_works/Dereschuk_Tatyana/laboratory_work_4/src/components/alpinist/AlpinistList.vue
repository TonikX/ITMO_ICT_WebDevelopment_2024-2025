<script setup>

import AlpinistModal from "@/components/alpinist/AlpinistModal.vue";
import {ref} from "vue";

defineProps({
  alpinists: {
    type: Array
  },
  clubs: {
    clubs: Array
  }
})

const emits = defineEmits(["delete-alpinist", "update-alpinist"]);

const isEditModalVisible = ref(false);
const selectedAlpinist = ref({});

function handleEdit(alpinist) {
  selectedAlpinist.value = {...alpinist};
  isEditModalVisible.value = true;
}

function handleUpdateAlpinist(alpinist) {
  emits("update-alpinist", alpinist);
  isEditModalVisible.value = false
}

function deleteAlpinist(id) {
  emits("delete-alpinist", id);
}

</script>

<template>
  <div class="alpinist-list">
    <template v-for="alpinist in alpinists" :key="alpinist.id">
      <v-card class="alpinist-card" width="600">
        <v-card-title>
          {{ alpinist.last_name }} {{ alpinist.first_name }}
          {{ alpinist.patronymic ?? "" }}
        </v-card-title>
        <v-card-subtitle>Клуб: {{ alpinist.club.name }}</v-card-subtitle>
        <v-card-actions class="alpinist-card-actions">
          <v-btn
              size="x-small"
              icon
              :to="`/alpinists/${alpinist.id}`"
          >
            <v-icon size="18">mdi-eye</v-icon>
          </v-btn>
          <v-btn
              size="x-small"
              icon
              @click="handleEdit(alpinist)"
          >
            <v-icon size="18">mdi-pencil</v-icon>
          </v-btn>
          <v-btn
              size="x-small"
              icon
              color="error"
              @click="deleteAlpinist(alpinist.id)"
          >
            <v-icon size="18">mdi-delete</v-icon>
          </v-btn>
        </v-card-actions>
      </v-card>
      <div v-if="alpinists.length === 0">
        Нет данных для отображения.
      </div>
    </template>

    <AlpinistModal
        v-model="isEditModalVisible"
        :alpinistData="selectedAlpinist"
        :clubs="clubs"
        mode="edit"
        @submit-alpinist="handleUpdateAlpinist"
    />
  </div>
</template>

<style scoped>
.alpinist-card {
  margin-bottom: 16px;
  position: relative;
  padding-bottom: 50px;
}

.alpinist-card-actions {
  position: absolute;
  bottom: 10px;
  right: 10px;
  display: flex;
  gap: 8px;
}
</style>

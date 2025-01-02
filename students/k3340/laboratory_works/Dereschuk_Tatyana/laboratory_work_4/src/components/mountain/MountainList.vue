<script setup>

import {ref} from "vue";
import MountainModal from "@/components/mountain/MountainModal.vue";

defineProps({
  mountains: {
    type: Array
  }
})

const emits = defineEmits(["delete-mountain", "update-mountain"]);

const isEditModalVisible = ref(false);
const selectedMountain = ref({});

function handleEdit(mountain) {
  selectedMountain.value = {...mountain};
  isEditModalVisible.value = true;
}

function handleUpdateMountain(mountain) {
  emits("update-mountain", mountain);
  isEditModalVisible.value = false
}

function deleteMountain(id) {
  emits("delete-mountain", id);
}

</script>

<template>
  <div class="mountain-list">
    <template v-for="mountain in mountains" :key="mountain.id">
      <v-card class="mountain-card" width="600">
        <v-card-title>
          {{ mountain.name }}
        </v-card-title>
        <v-card-subtitle>
          Высота: {{ mountain.height }}
        </v-card-subtitle>
        <v-card-actions class="mountain-card-actions">
          <v-btn
              size="x-small"
              icon
              :to="`/mountains/${mountain.id}`"
          >
            <v-icon size="18">mdi-eye</v-icon>
          </v-btn>
          <v-btn
              size="x-small"
              icon
              @click="handleEdit(mountain)"
          >
            <v-icon size="18">mdi-pencil</v-icon>
          </v-btn>
          <v-btn
              size="x-small"
              icon
              color="error"
              @click="deleteMountain(mountain.id)"
          >
            <v-icon size="18">mdi-delete</v-icon>
          </v-btn>
        </v-card-actions>
      </v-card>
      <div v-if="mountains.length === 0">
        Нет данных для отображения.
      </div>
    </template>

    <MountainModal
        v-model="isEditModalVisible"
        :mountainData="selectedMountain"
        mode="edit"
        @submit-mountain="handleUpdateMountain"
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

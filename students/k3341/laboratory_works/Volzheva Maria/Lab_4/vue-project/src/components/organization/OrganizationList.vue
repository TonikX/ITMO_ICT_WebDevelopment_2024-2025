<script setup>
import {ref} from "vue";
import OrganizationModal from "@/components/organization/OrganizationModal.vue";
defineProps({
  organizations: {
    type: Array
  }
})
const emits = defineEmits(["delete-organization", "update-organization"]);
const isEditModalVisible = ref(false);
const selectedOrganization = ref({});
function handleEdit(organization) {
  selectedOrganization.value = {...organization};
  isEditModalVisible.value = true;
}
function handleUpdateOrganization(organization) {
  emits("update-organization", organization);
  isEditModalVisible.value = false
}
function deleteOrganization(id) {
  emits("delete-organization", id);
}
</script>

<template>
  <div class="organization-list">
    <template v-for="organization in organizations" :key="organization.id">
      <v-card class="organization-card" width="600">
        <v-card-title>
          {{ organization.full_name }} ( {{ organization.short_name }} )
        </v-card-title>
        <v-card-subtitle>
          Специализация: {{ organization.specialization }}
        </v-card-subtitle>
        <v-card-actions class="specialization-card-actions">
          <v-btn
              size="x-small"
              icon
              :to="`/organizations/${organization.id}`"
          >
            <v-icon size="18">mdi-eye</v-icon>
          </v-btn>
          <v-btn
              size="x-small"
              icon
              @click="handleEdit(organization)"
          >
            <v-icon size="18">mdi-pencil</v-icon>
          </v-btn>
          <v-btn
              size="x-small"
              icon
              color="error"
              @click="deleteOrganization(organization.id)"
          >
            <v-icon size="18">mdi-delete</v-icon>
          </v-btn>
        </v-card-actions>
      </v-card>
      <div v-if="organizations.length === 0">
        Нет данных для отображения.
      </div>
    </template>

    <OrganizationModal
        v-model="isEditModalVisible"
        :organizationData="selectedOrganization"
        mode="edit"
        @submit-organization="handleUpdateOrganization"
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

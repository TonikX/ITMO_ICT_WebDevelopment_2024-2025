<script setup>
import {onMounted, ref} from "vue";
import axios from "axios";
import OrganizationList from "@/components/organization/OrganizationList.vue";
import OrganizationModal from "@/components/organization/OrganizationModal.vue";
const organizations = ref([]);
const isLoading = ref(false);
const isError = ref(false);
const isAddModalVisible = ref(false);
let token; // Объявляем переменную на уровне, доступном для обеих функций

async function fetchOrganizations() {
  isLoading.value = true;
  await axios
      .get('http://127.0.0.1:8000/insurance/organizations/')
      .then(response => {
        organizations.value = response.data;
        console.log(response.data);
      })
      .catch(error => {
        console.error("Ошибка загрузки", error);
        isError.value = true;
      })
      .finally(() => {
        isLoading.value = false;
      });
}


async function addOrganization(organization) {
  await axios.post(`insurance/organizations/`, organization).then(fetchOrganizations).catch(error => {
    isError.value = true;
    console.error(`Ошибка добавления клиента: ${error}`);
  })
}
async function deleteOrganization(id) {
  await axios.delete(`http://127.0.0.1:8000/insurance/organizations/${id}`).then(() => {
    organizations.value = organizations.value.filter(item => item.id !== id);
  }).catch(error => {
    isError.value = true;
    console.error(`Ошибка удаления клиента: ${error}`);
  })
}
async function updateOrganization(organization) {
  try {
    await axios.put(`http://127.0.0.1:8000/insurance/organizations/${organization.id}`, organization);
    await fetchOrganizations();
  } catch (error) {
    isError.value = true;
    console.error('Ошибка обновления клиента: ${error}');
  }
}



onMounted(fetchOrganizations);
</script>


<template>
  <div class="d-flex align-center flex-column ga-10">
    <template v-if="isLoading">
      <v-skeleton-loader type="card" class="mt-4" max-width="500"></v-skeleton-loader>
    </template>
    <template v-else>
      <h2>Список организаций</h2>
      <v-btn color="#4CAF50" @click="isAddModalVisible = true">Добавить организацию</v-btn>
      <OrganizationList :organizations="organizations" @delete-organization="deleteOrganization" @update-organization="updateOrganization"/>
      <OrganizationModal v-model="isAddModalVisible" mode="add" @submit-organization="addOrganization" />
      <div v-if="isError" class="error-message">
        Произошла ошибка при загрузке данных. Пожалуйста, попробуйте позже.
      </div>
    </template>
  </div>
</template>

<style scoped>
.actions > .v-btn {
  min-width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>

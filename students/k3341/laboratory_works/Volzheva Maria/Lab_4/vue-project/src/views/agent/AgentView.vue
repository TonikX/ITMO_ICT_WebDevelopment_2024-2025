<script setup>
import {onMounted, ref} from "vue";
import axios from "axios";
import AgentList from "@/components/agent/AgentList.vue";
import AgentModal from "@/components/agent/AgentModal.vue";
const agents = ref([]);
const isLoading = ref(false);
const isError = ref(false);
const isAddModalVisible = ref(false);
let token; // Объявляем переменную на уровне, доступном для обеих функций

async function fetchAgents() {
  isLoading.value = true;
  await axios
      .get('http://127.0.0.1:8000/insurance/agents/')
      .then(response => {
        agents.value = response.data;
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


async function addAgent(agent) {
  await axios.post(`insurance/agents/`, agent).then(fetchAgents).catch(error => {
    isError.value = true;
    console.error(`Ошибка добавления агента: ${error}`);
  })
}
async function deleteAgent(id) {
  await axios.delete(`http://127.0.0.1:8000/insurance/agents/${id}`).then(() => {
    agents.value = agents.value.filter(item => item.id !== id);
  }).catch(error => {
    isError.value = true;
    console.error(`Ошибка удаления агента: ${error}`);
  })
}
async function updateAgent(agent) {
  try {
    await axios.put(`http://127.0.0.1:8000/insurance/agents/${agent.id}`, agent);
    await fetchAgents();
  } catch (error) {
    isError.value = true;
    console.error('Ошибка обновления агента: ${error}');
  }
}



onMounted(fetchAgents);
</script>

<template>
  <div class="d-flex align-center flex-column ga-10">
    <template v-if="isLoading">
      <v-skeleton-loader type="card" class="mt-4" max-width="500"></v-skeleton-loader>
    </template>
    <template v-else>
      <h2>Список агентов</h2>
      <v-btn color="#4CAF50" @click="isAddModalVisible = true">Добавить агента</v-btn>
      <AgentList :agents="agents" @delete-agent="deleteAgent" @update-agent="updateAgent"/>
      <AgentModal v-model="isAddModalVisible" mode="add" @submit-agent="addAgent" />
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

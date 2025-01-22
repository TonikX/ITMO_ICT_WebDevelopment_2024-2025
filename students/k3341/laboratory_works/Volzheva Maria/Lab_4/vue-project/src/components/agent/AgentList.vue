<script setup>
import {ref} from "vue";
import AgentModal from "@/components/agent/AgentModal.vue";
defineProps({
  agents: {
    type: Array
  }
})
const emits = defineEmits(["delete-agent", "update-agent"]);
const isEditModalVisible = ref(false);
const selectedAgent = ref({});
function handleEdit(agent) {
  selectedAgent.value = {...agent};
  isEditModalVisible.value = true;
}
function handleUpdateAgent(agent) {
  emits("update-agent", agent);
  isEditModalVisible.value = false
}
function deleteAgent(id) {
  emits("delete-agent", id);
}
</script>

<template>
  <div class="agent-list">
    <template v-for="agent in agents" :key="agent.id">
      <v-card class="agent-card" width="600">
        <v-card-title>
          {{ agent.first_name }} {{ agent.second_name }} {{ agent.patronymic }}
        </v-card-title>
        <v-card-subtitle>
          Номер телефона: {{ agent.phone_number }}
        </v-card-subtitle>
        <v-card-actions class="agent-card-actions">
          <v-btn
              size="x-small"
              icon
              :to="`/agents/${agent.id}`"
          >
            <v-icon size="18">mdi-eye</v-icon>
          </v-btn>
          <v-btn
              size="x-small"
              icon
              @click="handleEdit(agent)"
          >
            <v-icon size="18">mdi-pencil</v-icon>
          </v-btn>
          <v-btn
              size="x-small"
              icon
              color="error"
              @click="deleteAgent(agent.id)"
          >
            <v-icon size="18">mdi-delete</v-icon>
          </v-btn>
        </v-card-actions>
      </v-card>
      <div v-if="agents.length === 0">
        Нет данных для отображения.
      </div>
    </template>

    <AgentModal
        v-model="isEditModalVisible"
        :agentData="selectedAgent"
        mode="edit"
        @submit-agent="handleUpdateAgent"
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

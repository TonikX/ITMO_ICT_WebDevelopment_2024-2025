<script setup>

import {getGroupStatus} from "@/utils/functions.js";
import GroupCreateModal from "@/components/ascending/GroupModal.vue";
import AscendingMembersTable from "@/components/ascending/AscendingMembersTable.vue";
import {ref} from "vue";
import MemberAddModal from "@/components/ascending/MemberAddModal.vue";

defineProps({
  groups: {
    type: Array,
    required: true
  },
  alpinists: {
    type: Array,
  }
});
const emits = defineEmits(["delete-group", "update-group", "add-member", "delete-member", "update-member"])
const isEditGroupModalOpen = ref(false);
const isAddMemberModalOpen = ref(false);
const selectedGroup = ref({});

function handleDeleteGroup(groupId) {
  emits("delete-group", groupId);
}

function handleUpdateGroup(groupData) {
  emits("update-group", {...groupData, group: selectedGroup.value.value.id});
  isEditGroupModalOpen.value = false;
}

function handleDeleteMember(groupId, memberId) {
  emits("delete-member", groupId, memberId)
}

function handleAddMember(memberData) {
  emits("add-member", selectedGroup.value.value.id, memberData)
  isAddMemberModalOpen.value = false;
}

function handleUpdateMember(groupId, memberData) {
  emits("update-member", groupId, memberData)
}


</script>

<template>
  <v-list>
    <v-list-item v-for="group in groups" :key="group.id" class="group-item mb-4">
      <v-card outlined>
        <v-card-title class="group-title">
          <span>Группа {{ group.id }}</span>
          <v-chip v-if="group.group_result === 's'" color="green" text-color="white" outlined>
            {{ getGroupStatus(group.group_result) }}
          </v-chip>
          <v-chip v-else color="red" text-color="white" outlined>
            {{ getGroupStatus(group.group_result) }}
          </v-chip>
        </v-card-title>

        <v-card-subtitle v-if="group.description_of_result">
          Описание результата: {{ group.description_of_result }}
        </v-card-subtitle>

        <v-card-actions class="action-buttons">
          <v-btn color="success" outlined small @click="() => { selectedGroup.value = group; isAddMemberModalOpen = true; }">
            Добавить участника
          </v-btn>
          <v-btn color="primary" outlined small @click="() => { selectedGroup.value = {...group}; isEditGroupModalOpen = true; }">
            Изменить
          </v-btn>
          <v-btn color="error" outlined small @click="handleDeleteGroup(group.id)">
            Удалить
          </v-btn>
        </v-card-actions>

        <div class="participants">
          <h4>Участники</h4>
          <AscendingMembersTable :group="group" @delete-member="handleDeleteMember" @update-member="handleUpdateMember"/>
        </div>
      </v-card>

      <GroupCreateModal
          :group-data="selectedGroup.value"
          v-model="isEditGroupModalOpen"
          @submit="handleUpdateGroup"
          mode="edit"
      />
      <MemberAddModal
          :alpinists="alpinists"
          v-model="isAddMemberModalOpen"
          @submit="handleAddMember"
      />
      <v-divider></v-divider>
    </v-list-item>
  </v-list>
</template>

<style scoped>
.group-item {
  width: 100%;
}
.group-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.action-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}
.participants {
  margin-top: 16px;
}
.mb-4 {
  margin-bottom: 16px;
}
</style>
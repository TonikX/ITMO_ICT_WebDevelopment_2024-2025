<script setup>

import {ref} from "vue";
import {getEmergencyStatus, getMemberStatus} from "@/utils/functions.js";
import MemberEditModal from "@/components/ascending/MemberEditModal.vue";
const props = defineProps({
  group: {
    type: Object
  }
});
const emits = defineEmits(["delete-member", "update-member"]);
const currentMember = ref({});

const isEditMemberModalOpen = ref(false);

function handleUpdateMember(memberData) {
  console.log(memberData)
  emits("update-member", props.group.id, memberData)
  isEditMemberModalOpen.value = false
}

</script>

<template>
  <v-table>
    <thead>
    <tr>
      <th>Имя</th>
      <th>Фамилия</th>
      <th>Результат</th>
      <th>Чрезвычайные ситуации</th>
      <th>Действия</th>
    </tr>
    </thead>
    <tbody>
    <tr v-for="member in group.members" :key="member.alpinist.id">
      <td>{{ member.alpinist.first_name }}</td>
      <td>{{ member.alpinist.last_name }}</td>
      <td>{{ getMemberStatus(member.result) }}</td>
      <td>{{ getEmergencyStatus(member.emergency_situations) ?? "Отсутствуют" }}</td>
      <td>
        <div class="action-buttons">
          <v-btn color="grey darken-1" outlined small @click="() => { currentMember.value = member; isEditMemberModalOpen = true; }">
            Изменить
          </v-btn>
          <v-btn color="grey darken-1" outlined small @click="$emit('delete-member', group.id, member.alpinist.id)">
            Удалить
          </v-btn>
        </div>
      </td>
    </tr>
    </tbody>
  </v-table>

  <MemberEditModal
      :alpinist-data="currentMember.value"
      v-model="isEditMemberModalOpen"
      @submit="handleUpdateMember"
  />
</template>

<style scoped>
.action-buttons {
  display: flex;
  gap: 8px;
  justify-content: center;
}

v-table {
  border-collapse: collapse;
  width: 100%;
}

v-table thead {
  background-color: #f9f9f9;
}

v-table th {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

v-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

v-table tbody tr:last-child td {
  border-bottom: none;
}

v-table tbody + tbody {
  margin-top: 16px;
  border-top: 2px solid #ddd;
}
</style>

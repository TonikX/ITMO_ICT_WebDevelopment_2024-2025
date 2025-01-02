<script setup>
import {onMounted, ref} from 'vue';
import {useRoute} from 'vue-router';
import axios from 'axios';
import AscendingDatesModal from "@/components/ascending/AscendingDatesModal.vue";
import GroupCreateModal from "@/components/ascending/GroupModal.vue";
import GroupsList from "@/components/ascending/GroupsList.vue";

const route = useRoute();
const ascendingId = route.params.id;

const ascendingDetails = ref(null);
const alpinists = ref([])
const isLoading = ref(true);
const isError = ref(false);

const isEditAscendingModalOpen = ref(false);
const isAddGroupModalOpen = ref(false);



async function fetchAscendingDetails() {
  isLoading.value = true;
  await axios.get(`/club/ascendings/${ascendingId}`).then(response => {
    ascendingDetails.value = response.data;
  }).catch(error => {
    console.error('Ошибка загрузки данных', error);
    isError.value = true;
  }).finally(isLoading.value = false);

}

async function saveFactDates(dates) {
  await axios.patch(`/club/ascendings/${ascendingId}`, dates).then(() => {
    ascendingDetails.value.fact_start_date = dates.fact_start_date;
    ascendingDetails.value.fact_end_date = dates.fact_end_date;
    isEditAscendingModalOpen.value = false;
  }).catch(error => {
    console.error('Ошибка сохранения данных', error);
  });
}

async function createGroup(groupData) {
  await axios.post('/club/groups/', {...groupData, ascending: ascendingId}).then(response => {
    ascendingDetails.value.groups.push(response.data);
    isAddGroupModalOpen.value = false;
  }).catch(error => {
    console.error('Ошибка создания группы', error);
  });
}

async function deleteGroup(groupId) {
  await axios.delete(`/club/groups/${groupId}/`).then(() => {
    ascendingDetails.value.groups = ascendingDetails.value.groups.filter(group => group.id !== groupId);
  }).catch(error => {
    console.error('Ошибка удаления группы', error);
  });
}

async function updateGroup(groupData) {
  await axios.patch(`/club/groups/${groupData.group}/`, {...groupData, ascending: ascendingId}).then(() => {
    fetchAscendingDetails();
  }).catch(error => {
    console.error('Ошибка обновления группы', error);
  })
}

async function fetchAlpinists() {
  axios.get(`/club/alpinists`).then(response => {
    alpinists.value = response.data
  }).catch(error => {
    console.error('Ошибка подгрузки альпинистов', error)
  })
}

async function addMemberToGroup(groupId, memberData) {
  await axios.post(`/club/groups/${groupId}/members/`, memberData).then(
      fetchAscendingDetails).catch(error => {
    console.error('Ошибка добавления участника', error);
  });
}

async function updateMember(groupId, memberData) {
  console.log(memberData)
  await axios.patch(`/club/groups/${groupId}/members/${memberData.alpinist.id}/`, memberData).then(
      fetchAscendingDetails).catch(error => {
    console.error('Ошибка обновления участника', error);
  });
}

async function deleteMember(groupId, memberId) {
  await axios.delete(`/club/groups/${groupId}/members/${memberId}/`).then(() => {
    const group = ascendingDetails.value.groups.find(group => group.id === groupId);
    group.members = group.members.filter(member => member.alpinist.id !== memberId);
  }).catch(error => {
    console.error('Ошибка удаления участника', error);
  });
}

onMounted(async () => {
  await fetchAscendingDetails()
  await fetchAlpinists()
});
</script>

<template>
  <v-container class="pa-4 d-flex justify-center">
    <div v-if="isLoading">Загрузка...</div>
    <div v-if="isError">Произошла ошибка при загрузке данных.</div>
    <div v-if="!isLoading && !isError">
      <h1 class="text-center mb-4">Детали восхождения</h1>
      <v-card outlined class="mb-4 details-card">
        <v-card-title>
          {{ ascendingDetails.description }}
        </v-card-title>
        <v-card-text>
          <p>Запланированное начало: {{ ascendingDetails.planned_start_date }}</p>
          <p>Запланированное завершение: {{ ascendingDetails.planned_end_date }}</p>
          <p>Фактическое начало: {{ ascendingDetails.fact_start_date ?? "Не установлено" }}</p>
          <p>Фактическое завершение: {{ ascendingDetails.fact_end_date ?? "Не установлено" }}</p>
          <p>Гора: {{ ascendingDetails.mountain.name }}</p>
        </v-card-text>
        <v-card-actions class="justify-end">
          <v-btn text="Изменить" color="primary" @click="isEditAscendingModalOpen = true"/>
        </v-card-actions>
      </v-card>

      <h2 class="text-center mb-4">Группы</h2>
      <div class="d-flex justify-center mb-4">
        <v-btn color="primary" @click="isAddGroupModalOpen = true">Добавить группу</v-btn>
      </div>
      <GroupsList
          :groups="ascendingDetails.groups"
          :alpinists="alpinists"
          @delete-group="deleteGroup"
          @update-group="updateGroup"
          @add-member="addMemberToGroup"
          @update-member="updateMember"
          @delete-member="deleteMember"

      />
      <GroupCreateModal v-model="isAddGroupModalOpen" @submit="createGroup"/>
      <AscendingDatesModal :end-date="ascendingDetails.fact_end_date"
                           :start-date="ascendingDetails.fact_start_date"
                           v-model="isEditAscendingModalOpen"
                           @submit-date="saveFactDates"
      />
    </div>
  </v-container>
</template>

<style scoped>
.details-wrapper {
  max-width: 800px;
  width: 100%;
}
.details-card {
  padding: 16px;
}
.pa-4 {
  padding: 16px;
}
.mb-4 {
  margin-bottom: 16px;
}
.text-center {
  text-align: center;
}
.justify-end {
  justify-content: flex-end;
}
</style>
<script setup>
import {onMounted, ref} from "vue";
import axios from "axios";
import ScheduleTable from "@/components/ScheduleTable.vue";
import {tokenStore} from "@/stores/token.js";
import ScheduleModal from "@/components/ScheduleModal.vue";

const token = tokenStore()

const schedules = ref([]);
const employees = ref([]);
const isModalVisible = ref(false);
const isLoading = ref(true);

async function fetchSchedules() {
  await axios.get('hotel/employees/schedule', {
    headers: {
      Authorization: `Token ${token.token}`
    }
  }).then(response => {
    schedules.value = response.data;
  }).catch(error => {
    console.log(error);
  });
}


async function fetchEmployees() {
  await axios.get('hotel/employees', {
    headers: {
      Authorization: `Token ${token.token}`
    }
  }).then(response => {
    employees.value = response.data;
  }).catch(error => {
    console.log(error);
  });
}

function handleAddSchedule(schedule) {
  axios
      .post("hotel/employees/schedule", schedule, {
        headers: {
          Authorization: `Token ${token.token}`,
        },
      })
      .then(() => {
        fetchSchedules();
        isModalVisible.value = false;
      })
      .catch((error) => {
        console.log(error);
      });
}

function handleEditSchedule(schedule) {
  axios
      .put(`hotel/employees/schedule/${schedule.id}/update`, schedule, {
        headers: {
          Authorization: `Token ${token.token}`,
        },
      })
      .then(() => {
        fetchSchedules();
        isModalVisible.value = false;
      })
      .catch((error) => {
        console.log(error);
      });

}

onMounted(async () => {
  isLoading.value = true;
  await Promise.all([fetchSchedules(), fetchEmployees()])
  isLoading.value = false;
});
</script>

<template>
  <v-app>
  <v-container>
    <template v-if="isLoading">
      <v-skeleton-loader
          type="card"
          class="mt-4"
          max-width="500"
      />
    </template>
    <template v-else>
      <h2>Расписание уборок</h2>
      <v-btn color="primary" class="mb-4" @click="isModalVisible = true">Добавить</v-btn>
      <ScheduleTable
          :schedules="schedules"
          :employees="employees"
          @edit-schedule="handleEditSchedule"
      />
      <ScheduleModal
          v-model="isModalVisible"
          :employees="employees"
          @save-schedule="handleAddSchedule"
      />
    </template>
  </v-container>
</v-app>
</template>

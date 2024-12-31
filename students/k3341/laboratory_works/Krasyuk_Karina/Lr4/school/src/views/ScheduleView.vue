<script setup>
import {onMounted, ref} from "vue";
import axios from "axios";
import ScheduleTable from "@/components/ScheduleTable.vue";
import ScheduleModal from "@/components/ScheduleModal.vue";

const selectedClass = ref();
const classList = ref([]);
const schedules = ref([]);
const teachers = ref([]);
const subjects = ref([]);
const rooms = ref([]);
const isLoading = ref(false);
const error = ref(null);
const currentSchedule = ref([]);
const isModalVisible = ref(false);
const modalMode = ref("add");
const selectedLesson = ref();

async function fetchClassList() {
  await axios.get("/school/groups").then(response => {
    classList.value = response.data.map(group => ({
      id: group.id,
      label: `${group.group_grade}${group.group_name}`,
    }));
    fetchSchedules();
  }).catch(error => {
    error.value = "Ошибка загрузки списка классов";
    console.error(error);
  })
}

async function fetchSchedules() {
  isLoading.value = true;
  await axios.get("/school/schedules").then(response => {
    schedules.value = response.data;
    isLoading.value = false
  }).catch(error => {
    error.value = "Ошибка загрузки расписания";
    console.error(error);
  })
}

async function fetchTeachers() {
  isLoading.value = true;
  await axios.get("/school/teachers").then(response => {
    teachers.value = response.data;
    isLoading.value = false
  }).catch(error => {
    error.value = "Ошибка загрузки учителей";
    console.error(error);
  })
}

async function fetchSubjects() {
  isLoading.value = true;
  await axios.get("/school/subjects").then(response => {
    subjects.value = response.data;
    isLoading.value = false
  }).catch(error => {
    error.value = "Ошибка загрузки предметов";
    console.error(error);
  })
}

async function fetchRooms() {
  isLoading.value = true;
  await axios.get("/school/rooms").then(response => {
    rooms.value = response.data;
    isLoading.value = false
  }).catch(error => {
    error.value = "Ошибка загрузки кабинетов";
    console.error(error);
  })
}

function getClassSchedule() {
  if (!selectedClass.value) {
    currentSchedule.value = [];
    return;
  }
  currentSchedule.value = schedules.value.filter(
      schedule => schedule.group.id === selectedClass.value
  );
}

function openAddModal() {
  modalMode.value = "add";
  selectedLesson.value = {
    day_of_week: "",
    number_of_lesson: "",
    time: "",
  };
  isModalVisible.value = true;
}


function openEditModal(lesson) {
  modalMode.value = "edit";
  selectedLesson.value = {
    ...lesson, group: {
      id: lesson.group.id,
      label: `${lesson.group.group_grade}${lesson.group.group_name}`,
    }
  };
  isModalVisible.value = true;
}

async function saveLesson(lesson) {
  if (modalMode.value === "add") {
    await axios.post("/school/schedules", lesson).then(response => {
      if (response.status === 201) {
        schedules.value.push(response.data);
      }
    }).catch(error => {
      console.error("Ошибка сохранения урока:", error);
    });
  } else {
    await axios.put(`/school/schedules/${lesson.id}/update`, lesson).then(response => {
      if (response.status === 200) {
        const index = schedules.value.findIndex(l => l.id === lesson.id);
        schedules.value[index] = response.data;
      }
    });
  }
  await fetchSchedules()
  getClassSchedule();
  isModalVisible.value = false;
}


async function deleteLesson(lessonId) {
  await axios.delete(`/school/schedules/${lessonId}/delete`).then(() => {
    schedules.value = schedules.value.filter(l => l.id !== lessonId);
    getClassSchedule();
  }).catch(error => {
    console.error("Ошибка удаления урока:", error);
  });
}

onMounted(async () => {
  await fetchClassList()
  await fetchTeachers()
  await fetchSubjects()
  await fetchRooms()
});
</script>

<template>
  <div>
    <h1>Расписание</h1>
    <v-select
        v-model="selectedClass"
        :items="classList"
        item-value="id"
        item-title="label"
        label="Выберите класс"
        @update:modelValue="getClassSchedule"
    />

    <v-alert v-if="error" type="error">{{ error }}</v-alert>

    <v-progress-linear v-if="isLoading" indeterminate/>

    <v-btn color="primary" class="mt-4" @click="openAddModal">Добавить урок</v-btn>

    <ScheduleTable
        v-if="currentSchedule.length"
        :schedule="currentSchedule"
        :lesson="selectedLesson"
        :mode="modalMode"
        :subjects="subjects"
        :teachers="teachers"
        :rooms="rooms"
        :groups="classList"
        @edit-lesson="openEditModal"
        @delete-lesson="deleteLesson"
    />

    <ScheduleModal
        v-model="isModalVisible"
        :lesson="selectedLesson"
        :mode="modalMode"
        :subjects="subjects"
        :teachers="teachers"
        :rooms="rooms"
        :groups="classList"
        @save-lesson="saveLesson"
    />
  </div>
</template>

<style scoped>
</style>

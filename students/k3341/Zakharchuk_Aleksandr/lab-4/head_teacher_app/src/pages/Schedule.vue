<template>
  <v-container>
    <v-row justify="start">
      <v-btn color="primary" class="mt-4 mb-2" @click="openAddModal">
        Добавить занятие
      </v-btn>
    </v-row>
    <ScheduleDay
      day-name="Понедельник"
      :schedule-records="scheduleRecords.monday"
      :edit-handler="openEditModal"
      :delete-handler="confirmDelete"
    />
    <ScheduleDay
      day-name="Вторник"
      :schedule-records="scheduleRecords.tuesday"
      :edit-handler="openEditModal"
      :delete-handler="confirmDelete"
    />
    <ScheduleDay
      day-name="Среда"
      :schedule-records="scheduleRecords.wednesday"
      :edit-handler="openEditModal"
      :delete-handler="confirmDelete"
    />
    <ScheduleDay
      day-name="Четверг"
      :schedule-records="scheduleRecords.thursday"
      :edit-handler="openEditModal"
      :delete-handler="confirmDelete"
    />
    <ScheduleDay
      day-name="Пятница"
      :schedule-records="scheduleRecords.friday"
      :edit-handler="openEditModal"
      :delete-handler="confirmDelete"
    />
    <ScheduleDay
      day-name="Суббота"
      :schedule-records="scheduleRecords.saturday"
      :edit-handler="openEditModal"
      :delete-handler="confirmDelete"
    />
    <ScheduleDay
      day-name="Воскресенье"
      :schedule-records="scheduleRecords.sunday"
      :edit-handler="openEditModal"
      :delete-handler="confirmDelete"
    />
    <v-dialog v-model="showModal" max-width="500">
      <v-card>
        <v-alert
          v-if="errorMessage"
          type="error"
          dismissible
          class="mb-4"
          @click:close="clearError"
        >
          {{ errorMessage }}
        </v-alert>
        <v-card-title>
          <span v-if="modalType === 'add'">Добавить занятие</span>
          <span v-else>Изменить занятие</span>
        </v-card-title>
        <v-card-text class="pb-0">
          <v-form ref="formRef">
            <v-select
              v-model="formData.student_class_id"
              :items="classesData"
              label="Класс"
              :rules="[rules.required]"
              required
            ></v-select>
            <v-select
              v-model="formData.subject_id"
              :items="subjectsData"
              label="Предмет"
              :rules="[rules.required]"
              required
            ></v-select>
            <v-select
              v-model="formData.teacher_id"
              :items="teachersData"
              label="Учитель"
              :rules="[rules.required]"
              required
            ></v-select>
            <v-select
              v-model="formData.room_number_id"
              :items="roomsData"
              label="Кабинет"
              :rules="[rules.required]"
              required
            ></v-select>
            <v-select
              v-model="formData.day_of_week"
              :items="dayOfWeekOptions"
              label="День недели"
              :rules="[rules.required]"
              required
            ></v-select>
            <v-text-field
              v-model="formData.lesson_number"
              label="Номер урока"
              :rules="[rules.required, rules.positiveInteger]"
              required
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="saveSchedule">Сохранить</v-btn>
          <v-btn color="secondary" @click="closeModal">Отменить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="showDeleteDialog" max-width="400">
      <v-card>
        <v-card-title>Подтвердите удаление</v-card-title>
        <v-card-text>
          Удалить занятие по предмету {{ scheduleRecordToDelete.subject.name }}?
        </v-card-text>
        <v-card-actions>
          <v-btn color="error" @click="performDelete">Удалить</v-btn>
          <v-btn color="secondary" @click="showDeleteDialog = false">Отменить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import axios from "axios";
import ScheduleDay from "@/components/ScheduleDay.vue";

const token = localStorage.getItem("token");
axios.defaults.headers.common["Authorization"] = `Token ${token}`;

const dayOfWeekOptions = [
  { title: "Понедельник", value: "Monday" },
  { title: "Вторник", value: "Tuesday" },
  { title: "Среда", value: "Wednesday" },
  { title: "Четверг", value: "Thursday" },
  { title: "Пятница", value: "Friday" },
  { title: "Суббота", value: "Saturday" },
  { title: "Воскресенье", value: "Sunday" },
];

const scheduleRecords = reactive({
  monday: [],
  tuesday: [],
  wednesday: [],
  thursday: [],
  friday: [],
  saturday: [],
  sunday: [],
});

const formRef = ref(null);
const formData = reactive({
  student_class_id: null,
  subject_id: null,
  teacher_id: null,
  room_number_id: null,
  day_of_week: "Monday",
  lesson_number: null,
});
const currentScheduleRecordId = ref(0);
const showModal = ref(false);
const modalType = ref("add");
const errorMessage = ref("");

const classesData = ref([]);
const subjectsData = ref([]);
const teachersData = ref([]);
const roomsData = ref([]);

const showDeleteDialog = ref(false);
const scheduleRecordToDelete = ref(null);

const confirmDelete = (scheduleRecord) => {
  scheduleRecordToDelete.value = scheduleRecord;
  showDeleteDialog.value = true;
};

const performDelete = async () => {
  try {
    await axios.delete(
      `http://localhost:8000/schedule/${scheduleRecordToDelete.value.id}/`
    );
    showDeleteDialog.value = false;
    fetchSchedule();
  } catch (err) {
    console.error("Error deleting schedule record:", err);
  }
};

const clearError = () => {
  errorMessage.value = "";
};

const openAddModal = () => {
  clearError();
  modalType.value = "add";
  formData.student_class_id = null;
  formData.subject_id = null;
  formData.teacher_id = null;
  formData.room_number_id = null;
  formData.day_of_week = "Monday";
  formData.lesson_number = null;
  showModal.value = true;
};

const openEditModal = (scheduleRecord) => {
  clearError();
  modalType.value = "edit";
  currentScheduleRecordId.value = scheduleRecord.id;
  formData.student_class_id = scheduleRecord.student_class_id;
  formData.subject_id = scheduleRecord.subject_id;
  formData.teacher_id = scheduleRecord.teacher_id;
  formData.room_number_id = scheduleRecord.room_number_id;
  formData.day_of_week = scheduleRecord.day_of_week;
  formData.lesson_number = scheduleRecord.lesson_number;
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
};

const groupScheduleByDay = (scheduleData) => {
  scheduleData.forEach((scheduleRecord) => {
    switch (scheduleRecord.day_of_week.toLowerCase()) {
      case "monday":
        scheduleRecords.monday.push(scheduleRecord);
        break;
      case "tuesday":
        scheduleRecords.tuesday.push(scheduleRecord);
        break;
      case "wednesday":
        scheduleRecords.wednesday.push(scheduleRecord);
        break;
      case "thursday":
        scheduleRecords.thursday.push(scheduleRecord);
        break;
      case "friday":
        scheduleRecords.friday.push(scheduleRecord);
        break;
      case "saturday":
        scheduleRecords.saturday.push(scheduleRecord);
        break;
      case "sunday":
        scheduleRecords.sunday.push(scheduleRecord);
        break;
    }
  });
  scheduleRecords.monday = scheduleRecords.monday.slice().sort((record1, record2) => record1.lesson_number - record2.lesson_number);
  scheduleRecords.tuesday = scheduleRecords.tuesday.slice().sort((record1, record2) => record1.lesson_number - record2.lesson_number);
  scheduleRecords.wednesday = scheduleRecords.wednesday.slice().sort((record1, record2) => record1.lesson_number - record2.lesson_number);
  scheduleRecords.thursday  = scheduleRecords.thursday.slice().sort((record1, record2) => record1.lesson_number - record2.lesson_number);
  scheduleRecords.friday = scheduleRecords.friday.slice().sort((record1, record2) => record1.lesson_number - record2.lesson_number);
  scheduleRecords.saturday = scheduleRecords.saturday.slice().sort((record1, record2) => record1.lesson_number - record2.lesson_number);
  scheduleRecords.sunday = scheduleRecords.sunday.slice().sort((record1, record2) => record1.lesson_number - record2.lesson_number);
};

const fetchSchedule = async () => {
  try {
    const response = await axios.get("http://localhost:8000/schedule/");
    scheduleRecords.monday = [];
    scheduleRecords.tuesday = [];
    scheduleRecords.wednesday = [];
    scheduleRecords.thursday = [];
    scheduleRecords.friday = [];
    scheduleRecords.saturday = [];
    scheduleRecords.sunday = [];
    groupScheduleByDay(response.data.results);
  } catch (err) {
    console.error("Error fetching schedule: ", err);
  }
};

const saveSchedule = async () => {
  const { valid } = await formRef.value.validate();
  if (!valid) return;
  console.log(formData);
  try {
    if (modalType.value === "add") {
      await axios.post("http://localhost:8000/schedule/", formData);
    } else if (modalType.value === "edit") {
        await axios.put(
          `http://localhost:8000/schedule/${currentScheduleRecordId.value}/`,
          formData,
        );
    }
    closeModal();
    fetchSchedule();
  } catch (err) {
    errorMessage.value = "Не удалось сохранить расписание";
  }
};

const fetchClasses = async () => {
  try {
    const response = await axios.get("http://localhost:8000/classes/", {
      params: { limit: 100 },
    });
    classesData.value = response.data.results.map((classItem) => ({
      title: classItem.class_name,
      value: classItem.id,
    }));
  } catch (err) {
    console.error("Error fetching classes: ", err);
  }
};

const fetchSubjects = async () => {
  try {
    const response = await axios.get("http://localhost:8000/subjects/", {
      params: { limit: 100 },
    });
    subjectsData.value = response.data.results.map((subjectItem) => ({
      title: subjectItem.name,
      value: subjectItem.id,
    }));
  } catch (err) {
    console.error("Error fetching subjects: ", err);
  }
};

const fetchTeachers = async () => {
  try {
    const response = await axios.get(`http://localhost:8000/teachers/`, {
      params: { limit: 100 },
    });
    teachersData.value = response.data.results.map((teacherItem) => ({
      title: `${teacherItem.last_name} ${teacherItem.first_name} ${teacherItem.patronymic}`,
      value: teacherItem.id,
    }));
  } catch (err) {
    console.error("Error fetching data: ", err);
  }
};

const fetchRooms = async () => {
  try {
    const response = await axios.get(`http://localhost:8000/rooms/`, {
      params: { limit: 100 },
    });
    roomsData.value = response.data.results.map((roomItem) => ({
      title: `Кабинет №${roomItem.room_number}`,
      value: roomItem.room_number,
    }));
  } catch (err) {
    console.error("Error fetching data: ", err);
  }
};

const rules = {
  required: (value) => !!value || "Обязательное значение",
  positiveInteger: (value) =>
    (Number.isInteger(+value) && +value > 0) ||
    "Значение должно быть положительным целым числом",
};

onMounted(() => {
  fetchSchedule();
  fetchClasses();
  fetchSubjects();
  fetchTeachers();
  fetchRooms();
});
</script>

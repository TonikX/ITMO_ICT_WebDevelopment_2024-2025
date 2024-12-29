<template>
  <v-container>
    <v-row justify="start">
      <v-btn color="primary" class="mt-4 mb-2" @click="openAddModal">
        Добавить учителя
      </v-btn>
    </v-row>

    <v-row>
      <v-col v-for="teacher in teachers" :key="teacher.id" cols="4">
        <v-card>
          <v-card-title>
            {{ teacher.last_name }} {{ teacher.first_name }}
            {{ teacher.patronymic }}
          </v-card-title>
          <v-card-text>
            Пол: {{ teacher.gender === "M" ? "Мужской" : "Женский" }}<br />
            Кабинет: {{ teacher.assigned_room_id || "Не назначен" }}<br />
            Классный руководитель:
            {{ teacher.is_homeroom_teacher ? "Да" : "Нет" }}
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="openEditModal(teacher)"
              >Изменить</v-btn
            >
            <v-btn color="error" @click="confirmDelete(teacher.id)"
              >Удалить</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title>Подтвердите удаление</v-card-title>
        <v-card-text> Удалить учителя {{ teacherToDeleteName }}? </v-card-text>
        <v-card-actions>
          <v-btn color="error" @click="performDelete">Удалить</v-btn>
          <v-btn color="secondary" @click="closeDeleteDialog">Отменить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

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
          <span v-if="modalType === 'add'">Добавить учителя</span>
          <span v-else>Изменить учителя</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="formRef">
            <v-text-field
              v-model="currentTeacher.first_name"
              label="Имя"
              :rules="[rules.required]"
              required
            ></v-text-field>
            <v-text-field
              v-model="currentTeacher.last_name"
              label="Фамилия"
              :rules="[rules.required]"
              required
            ></v-text-field>
            <v-text-field
              v-model="currentTeacher.patronymic"
              label="Отчество"
            ></v-text-field>
            <v-select
              v-model="currentTeacher.gender"
              label="Пол"
              :items="genderOptions"
              :rules="[rules.required]"
              required
            ></v-select>
            <v-select
              v-model="currentTeacher.assigned_room_id"
              label="Кабинет"
              :items="roomOptions"
              item-text="room_number"
              item-value="id"
            ></v-select>
            <v-switch
              v-model="currentTeacher.is_homeroom_teacher"
              label="Классный руководитель"
            ></v-switch>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="saveTeacher">Сохранить</v-btn>
          <v-btn color="secondary" @click="closeModal">Отменить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-row>
      <v-pagination
        v-model="currentPage"
        :length="totalPages"
        color="primary"
        class="mt-4"
      ></v-pagination>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from "vue";
import axios from "axios";

const teachers = ref([]);
const roomOptions = ref([]);
const genderOptions = [
  { title: "Мужской", value: "M" },
  { title: "Женский", value: "F" },
];

const showModal = ref(false);
const modalType = ref("add");
const errorMessage = ref("");
const currentTeacher = reactive({
  first_name: "",
  last_name: "",
  patronymic: "",
  gender: { title: "Мужской", value: "M" },
  assigned_room: null,
  is_homeroom_teacher: false,
});

const formRef = ref(null);

const token = localStorage.getItem("token");
axios.defaults.headers.common["Authorization"] = `Token ${token}`;

const currentPage = ref(1);
const totalPages = ref(1);
const itemsPerPage = ref(10);

const fetchTeachers = async () => {
  try {
    const response = await axios.get("http://localhost:8000/teachers/", {
      params: {
        offset: (currentPage.value - 1) * itemsPerPage.value,
        limit: itemsPerPage.value,
      },
    });
    teachers.value = response.data.results;
    totalPages.value = Math.ceil(response.data.count / itemsPerPage.value);
  } catch (err) {
    console.error("Error fetching teachers:", err);
  }
};

const fetchRooms = async () => {
  try {
    const response = await axios.get("http://localhost:8000/rooms/", {
      params: { limit: 100 },
    });
    roomOptions.value = response.data.results.map((room) => room.room_number);
  } catch (err) {
    console.error("Error fetching rooms:", err);
  }
};

watch(currentPage, () => fetchTeachers());

const openAddModal = () => {
  modalType.value = "add";
  clearError();
  Object.assign(currentTeacher, {
    first_name: "",
    last_name: "",
    patronymic: "",
    gender: { title: "Мужской", value: "M" },
    assigned_room_id: null,
    is_homeroom_teacher: false,
  });
  showModal.value = true;
};

const openEditModal = (teacher) => {
  modalType.value = "edit";
  clearError();
  Object.assign(currentTeacher, teacher);
  showModal.value = true;
};

const saveTeacher = async () => {
  const { valid } = await formRef.value.validate();
  if (!valid) return;
  const teacherData = {...currentTeacher};
  teacherData.gender = currentTeacher.gender.value;
  try {
    if (modalType.value === "add") {
      await axios.post("http://localhost:8000/teachers/", teacherData);
    } else if (modalType.value === "edit") {
      await axios.put(
        `http://localhost:8000/teachers/${currentTeacher.id}/`,
        currentTeacher
      );
    }
    closeModal();
    fetchTeachers();
  } catch (err) {
    errorMessage.value = "Не удалось сохранить учителя";
  }
};

const deleteDialog = ref(false);
const teacherToDelete = ref(null);
const teacherToDeleteName = ref("");

const confirmDelete = (teacherId) => {
  const teacher = teachers.value.find((t) => t.id === teacherId);
  teacherToDelete.value = teacherId;
  teacherToDeleteName.value = `${teacher.last_name} ${teacher.first_name}`;
  deleteDialog.value = true;
};

const performDelete = async () => {
  try {
    await axios.delete(
      `http://localhost:8000/teachers/${teacherToDelete.value}/`
    );
    deleteDialog.value = false;
    fetchTeachers();
  } catch (err) {
    console.error("Error deleting teacher:", err);
  }
};

const closeDeleteDialog = () => {
  deleteDialog.value = false;
};

const closeModal = () => {
  showModal.value = false;
};

const clearError = () => {
  errorMessage.value = "";
};

const rules = {
  required: (value) => !!value || "Обязательное значение",
};

onMounted(() => {
  fetchTeachers();
  fetchRooms();
});
</script>

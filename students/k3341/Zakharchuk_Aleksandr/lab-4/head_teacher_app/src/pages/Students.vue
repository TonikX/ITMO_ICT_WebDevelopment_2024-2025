<template>
  <v-container>
    <v-row justify="start">
      <v-btn color="primary" class="mt-4 mb-2" @click="openAddModal">
        Добавить ученика
      </v-btn>
    </v-row>
    <v-row>
      <v-col v-for="student in students" :key="student.id" cols="4">
        <v-card>
          <v-card-title
            >{{ student.last_name }} {{ student.first_name }}
            {{ student.patronymic }}</v-card-title
          >
          <v-card-text>
            Пол: {{ student.gender === "M" ? "Мужской" : "Женский" }} <br />
            Класс: {{ student.student_class.class_name || "Не указан" }}
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="openEditModal(student)"
              >Изменить</v-btn
            >
            <v-btn color="error" @click="confirmDelete(student.id)"
              >Удалить</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title>Подтвердите удаление</v-card-title>
        <v-card-text>
          Удалить ученика "{{ studentToDelete.last_name }}
          {{ studentToDelete.first_name }} {{ studentToDelete.patronymic }}"?
        </v-card-text>
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
          <span v-if="modalType === 'add'">Добавить ученика</span>
          <span v-else>Изменить ученика</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="formRef">
            <v-text-field
              v-model="currentStudent.first_name"
              label="Имя"
              :rules="[rules.required]"
              required
            ></v-text-field>
            <v-text-field
              v-model="currentStudent.last_name"
              label="Фамилия"
              :rules="[rules.required]"
              required
            ></v-text-field>
            <v-text-field
              v-model="currentStudent.patronymic"
              label="Отчество"
              :rules="[rules.required]"
              required
            ></v-text-field>
            <v-select
              v-model="currentStudent.gender"
              :items="genderOptions"
              label="Пол"
              :rules="[rules.required]"
              required
            ></v-select>
            <v-autocomplete
              v-model="currentStudent.student_class"
              :items="classes"
              label="Класс"
              :rules="[rules.required]"
              required
            ></v-autocomplete>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="saveStudent">Сохранить</v-btn>
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

const students = ref([]);
const classes = ref([]);
const showModal = ref(false);
const modalType = ref("add");
const errorMessage = ref("");
const currentStudent = reactive({
  id: null,
  first_name: "",
  last_name: "",
  patronymic: "",
  gender: { title: "Мужской", value: "M" },
  student_class: null,
  student_class_name: null,
});

const genderOptions = [
  { title: "Мужской", value: "M" },
  { title: "Женский", value: "F" },
];

const formRef = ref(null);

const token = localStorage.getItem("token");
axios.defaults.headers.common["Authorization"] = `Token ${token}`;

const currentPage = ref(1);
const totalPages = ref(1);
const itemsPerPage = ref(9);

const fetchStudents = async () => {
  try {
    const response = await axios.get("http://localhost:8000/students/", {
      params: {
        offset: (currentPage.value - 1) * itemsPerPage.value,
        limit: itemsPerPage.value,
      },
    });
    students.value = response.data.results;
    totalPages.value = Math.ceil(response.data.count / itemsPerPage.value);
  } catch (err) {
    console.error("Error fetching students:", err);
  }
};

const fetchClasses = async () => {
  try {
    const response = await axios.get("http://localhost:8000/classes/");
    classes.value = response.data.results.map((classItem) => ({
      title: classItem.class_name,
      value: classItem.id,
    }));
  } catch (err) {
    console.error("Error fetching classes:", err);
  }
};

watch(currentPage, fetchStudents);

const openAddModal = () => {
  modalType.value = "add";
  clearError();
  Object.assign(currentStudent, {
    id: null,
    first_name: "",
    last_name: "",
    patronymic: "",
    gender: { title: "Мужской", value: "M" },
    student_class: null,
  });
  showModal.value = true;
};

const openEditModal = (student) => {
  modalType.value = "edit";
  clearError();
  Object.assign(currentStudent, {
    id: student.id,
    first_name: student.first_name,
    last_name: student.last_name,
    patronymic: student.patronymic,
    gender: student.gender,
    student_class: student.student_class.class_name,
    student_class_id: student.student_class.id,
  });
  showModal.value = true;
};

const saveStudent = async () => {
  const { valid } = await formRef.value.validate();
  if (!valid) return;
  const studentData = { ...currentStudent };
  studentData.student_class_id = currentStudent.student_class;
  try {
    if (modalType.value === "add") {
      await axios.post("http://localhost:8000/students/", studentData);
    } else if (modalType.value === "edit") {
      await axios.put(
        `http://localhost:8000/students/${currentStudent.id}/`,
        studentData
      );
    }
    closeModal();
    fetchStudents();
  } catch (err) {
    errorMessage.value = "Не удалось сохранить ученика";
  }
};

const clearError = () => {
  errorMessage.value = "";
};

const deleteDialog = ref(false);
const studentToDelete = ref(null);

const confirmDelete = (id) => {
  studentToDelete.value = students.value.find((student) => student.id === id);
  deleteDialog.value = true;
};

const performDelete = async () => {
  try {
    await axios.delete(
      `http://localhost:8000/students/${studentToDelete.value.id}/`
    );
    deleteDialog.value = false;
    fetchStudents();
  } catch (err) {
    console.error("Error deleting student:", err);
  }
};

const closeDeleteDialog = () => {
  deleteDialog.value = false;
};

const closeModal = () => {
  showModal.value = false;
};

const rules = {
  required: (value) => !!value || "Обязательное значение",
};

onMounted(() => {
  fetchStudents();
  fetchClasses();
});
</script>

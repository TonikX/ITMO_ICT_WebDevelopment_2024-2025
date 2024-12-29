<template>
  <v-container>
    <v-row justify="start">
      <v-btn color="primary" class="mt-4 mb-2" @click="openAddModal">
        Добавить класс
      </v-btn>
    </v-row>
    <v-row>
      <v-col v-for="classItem in classes" :key="classItem.id" cols="4">
        <v-card>
          <v-card-title>{{ classItem.class_name }}</v-card-title>
          <v-card-text>
            Классный руководитель:
            {{
              classItem.homeroom_teacher
                ? classItem.homeroom_teacher.first_name +
                  " " +
                  classItem.homeroom_teacher.last_name
                : "Не назначен"
            }}
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="openEditModal(classItem)"
              >Изменить</v-btn
            >
            <v-btn color="error" @click="confirmDelete(classItem.id)"
              >Удалить</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title>Подтвердите удаление</v-card-title>
        <v-card-text
          >Удалить класс "{{ classToDelete.class_name }}"?</v-card-text
        >
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
          <span v-if="modalType === 'add'">Добавить класс</span>
          <span v-else>Изменить класс</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="formRef">
            <v-text-field
              v-model="currentClass.class_name"
              label="Название класса"
              :rules="[rules.required]"
              required
            ></v-text-field>
            <v-autocomplete
              v-model="currentClass.homeroom_teacher"
              :items="teachers"
              label="Классный руководитель"
              :rules="[rules.required]"
              required
            ></v-autocomplete>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="saveClass">Сохранить</v-btn>
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

const classes = ref([]);
const teachers = ref([]);
const showModal = ref(false);
const modalType = ref("add");
const errorMessage = ref("");
const currentClass = reactive({
  id: null,
  class_name: "",
  homeroom_teacher: null,
});

const formRef = ref(null);

const token = localStorage.getItem("token");
axios.defaults.headers.common["Authorization"] = `Token ${token}`;

const currentPage = ref(1);
const totalPages = ref(1);
const itemsPerPage = ref(9);

const fetchClasses = async () => {
  try {
    const response = await axios.get("http://localhost:8000/classes/", {
      params: {
        offset: (currentPage.value - 1) * itemsPerPage.value,
        limit: itemsPerPage.value,
      },
    });
    classes.value = response.data.results;
    totalPages.value = Math.ceil(response.data.count / itemsPerPage.value);
  } catch (err) {
    console.error("Error fetching classes:", err);
  }
};

const fetchTeachers = async () => {
  try {
    const response = await axios.get("http://localhost:8000/teachers/", {
      params: { limit: 100 },
    });
    teachers.value = response.data.results.map(teacher => ({
      title: `${teacher.last_name} ${teacher.first_name} ${teacher.patronymic}`,
      value: teacher.id,
    }));
  } catch (err) {
    console.error("Error fetching teachers:", err);
  }
};

watch(currentPage, fetchClasses);

const openAddModal = () => {
  modalType.value = "add";
  clearError();
  Object.assign(currentClass, {
    id: null,
    class_name: "",
    homeroom_teacher: null,
  });
  showModal.value = true;
};

const openEditModal = (classItem) => {
  modalType.value = "edit";
  clearError();
  Object.assign(currentClass, {
    id: classItem.id,
    class_name: classItem.class_name,
    homeroom_teacher:
      classItem.homeroom_teacher.first_name +
      " " +
      classItem.homeroom_teacher.last_name,
    homeroom_teacher_id: classItem.homeroom_teacher.id,
  });
  showModal.value = true;
};

const saveClass = async () => {
  const { valid } = await formRef.value.validate();
  if (!valid) return;
  const classData = {
    homeroom_teacher_id: currentClass.homeroom_teacher,
    class_name: currentClass.class_name,
  };
  try {
    if (modalType.value === "add") {
      await axios.post("http://localhost:8000/classes/", classData);
    } else if (modalType.value === "edit") {
      await axios.put(
        `http://localhost:8000/classes/${currentClass.id}/`,
        classData,
      );
    }
    closeModal();
    fetchClasses();
  } catch (err) {
    errorMessage.value = "Не удалось сохранить класс";
  }
};

const clearError = () => {
  errorMessage.value = "";
};

const deleteDialog = ref(false);
const classToDelete = ref(null);

const confirmDelete = (id) => {
  classToDelete.value = classes.value.find((classItem) => classItem.id === id);
  deleteDialog.value = true;
};

const performDelete = async () => {
  try {
    await axios.delete(
      `http://localhost:8000/classes/${classToDelete.value.id}/`
    );
    deleteDialog.value = false;
    fetchClasses();
  } catch (err) {
    console.error("Error deleting class:", err);
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
  fetchClasses();
  fetchTeachers();
});
</script>

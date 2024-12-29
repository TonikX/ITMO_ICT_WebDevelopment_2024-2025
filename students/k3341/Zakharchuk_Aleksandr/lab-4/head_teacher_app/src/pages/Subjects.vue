<template>
  <v-container>
    <v-row justify="start">
      <v-btn color="primary" class="mt-4 mb-2" @click="openAddModal">
        Добавить предмет
      </v-btn>
    </v-row>
    <v-row>
      <v-col v-for="subject in subjects" :key="subject.id" cols="4">
        <v-card>
          <v-card-title>{{ subject.name }}</v-card-title>
          <v-card-actions>
            <v-btn color="primary" @click="openEditModal(subject)">Изменить</v-btn>
            <v-btn color="error" @click="confirmDelete(subject.id)">Удалить</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title>Подтвердите удаление</v-card-title>
        <v-card-text>Удалить предмет "{{ subjectToDelete?.name }}"?</v-card-text>
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
          <span v-if="modalType === 'add'">Добавить предмет</span>
          <span v-else>Изменить предмет</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="formRef">
            <v-text-field
              v-model="currentSubject.name"
              label="Название предмета"
              :rules="[rules.required]"
              required
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="saveSubject">Сохранить</v-btn>
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

const subjects = ref([]);
const showModal = ref(false);
const modalType = ref("add");
const errorMessage = ref("");
const currentSubject = reactive({
  id: null,
  name: "",
});

const formRef = ref(null);

const token = localStorage.getItem("token");
axios.defaults.headers.common["Authorization"] = `Token ${token}`;

const currentPage = ref(1);
const totalPages = ref(1);
const itemsPerPage = ref(12);

const fetchSubjects = async () => {
  try {
    const response = await axios.get("http://localhost:8000/subjects/", {
      params: {
        offset: (currentPage.value - 1) * itemsPerPage.value,
        limit: itemsPerPage.value,
      },
    });
    subjects.value = response.data.results;
    totalPages.value = Math.ceil(response.data.count / itemsPerPage.value);
  } catch (err) {
    console.error("Error fetching subjects:", err);
  }
};

watch(currentPage, fetchSubjects);

const openAddModal = () => {
  modalType.value = "add";
  clearError();
  Object.assign(currentSubject, { id: null, name: "" });
  showModal.value = true;
};

const openEditModal = (subject) => {
  modalType.value = "edit";
  clearError();
  Object.assign(currentSubject, { id: subject.id, name: subject.name });
  showModal.value = true;
};

const saveSubject = async () => {
  const { valid } = await formRef.value.validate();
  if (!valid) return;
  try {
    if (modalType.value === "add") {
      await axios.post("http://localhost:8000/subjects/", currentSubject);
    } else if (modalType.value === "edit") {
      await axios.put(`http://localhost:8000/subjects/${currentSubject.id}/`, {
        name: currentSubject.name,
      });
    }
    closeModal();
    fetchSubjects();
  } catch (err) {
    errorMessage.value = "Не удалось сохранить предмет";
  }
};

const clearError = () => {
  errorMessage.value = "";
};

const deleteDialog = ref(false);
const subjectToDelete = ref(null);

const confirmDelete = (id) => {
  subjectToDelete.value = subjects.value.find((subject) => subject.id === id);
  deleteDialog.value = true;
};

const performDelete = async () => {
  try {
    await axios.delete(`http://localhost:8000/subjects/${subjectToDelete.value.id}/`);
    deleteDialog.value = false;
    fetchSubjects();
  } catch (err) {
    console.error("Error deleting subject:", err);
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

onMounted(fetchSubjects);
</script>

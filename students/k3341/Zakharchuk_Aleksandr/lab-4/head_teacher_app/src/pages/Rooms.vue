<template>
  <v-container>
    <v-row justify="start">
      <v-btn color="primary" class="mt-4 mb-2" @click="openAddModal"
        >Добавить кабинет</v-btn
      >
    </v-row>
    <v-row>
      <v-col v-for="room in rooms" :key="room.room_number" cols="4">
        <v-card>
          <v-card-title>Кабинет {{ room.room_number }}</v-card-title>
          <v-card-text>
            Специализированный: {{ room.is_specialized ? "Да" : "Нет" }}
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="openEditModal(room)">Изменить</v-btn>
            <v-btn color="error" @click="confirmDelete(room.room_number)">
              Удалить
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title>Подтвердите удаление</v-card-title>
        <v-card-text> Удалить кабинет №{{ roomToDelete }}? </v-card-text>
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
          <span v-if="modalType === 'add'">Добавить кабинет</span>
          <span v-else>Изменить кабинет</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="formRef">
            <v-text-field
              v-model="currentRoom.room_number"
              label="Номер кабинета"
              :disabled="modalType === 'edit'"
              :rules="[rules.required, rules.positiveInteger]"
              required
            ></v-text-field>
            <v-switch
              v-model="currentRoom.is_specialized"
              label="Специализированный"
            ></v-switch>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="saveRoom">Сохранить</v-btn>
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

const rooms = ref([]);
const showModal = ref(false);
const modalType = ref("add");
const errorMessage = ref("");
const currentRoom = reactive({
  room_number: null,
  is_specialized: false,
});

const formRef = ref(null);

const token = localStorage.getItem("token");
axios.defaults.headers.common["Authorization"] = `Token ${token}`;

const currentPage = ref(1);
const totalPages = ref(1);
const itemsPerPage = ref(9);

const fetchRooms = async () => {
  try {
    const response = await axios.get("http://localhost:8000/rooms/", {
      params: {
        offset: (currentPage.value - 1) * itemsPerPage.value,
        limit: itemsPerPage.value,
      },
    });
    rooms.value = response.data.results;
    totalPages.value = Math.ceil(response.data.count / itemsPerPage.value);
  } catch (err) {
    console.error("Error fetching rooms:", err);
  }
};

watch(currentPage, () => fetchRooms());

const openAddModal = () => {
  modalType.value = "add";
  clearError();
  currentRoom.room_number = null;
  currentRoom.is_specialized = false;
  showModal.value = true;
};

const openEditModal = (room) => {
  modalType.value = "edit";
  clearError();
  currentRoom.room_number = room.room_number;
  currentRoom.is_specialized = room.is_specialized;
  showModal.value = true;
};

const saveRoom = async () => {
  const { valid } = await formRef.value.validate();
  if (!valid) return;
  try {
    if (modalType.value === "add") {
      await axios.post("http://localhost:8000/rooms/", currentRoom);
    } else if (modalType.value === "edit") {
      await axios.put(
        `http://localhost:8000/rooms/${currentRoom.room_number}/`,
        currentRoom
      );
    }
    closeModal();
    fetchRooms();
  } catch (err) {
    errorMessage.value = "Не удалось сохранить кабинет";
  }
};

const clearError = () => {
  errorMessage.value = "";
};

const rules = {
  required: (value) => !!value || "Обязательное значение",
  positiveInteger: (value) =>
    (Number.isInteger(+value) && +value > 0) ||
    "Значение должно быть положительным целым числом",
};

const deleteDialog = ref(false);
const roomToDelete = ref(null);

const confirmDelete = (roomNumber) => {
  roomToDelete.value = roomNumber;
  deleteDialog.value = true;
};

const performDelete = async () => {
  try {
    await axios.delete(`http://localhost:8000/rooms/${roomToDelete.value}/`);
    deleteDialog.value = false;
    fetchRooms();
  } catch (err) {
    console.error("Error deleting room:", err);
  }
};

const closeDeleteDialog = () => {
  deleteDialog.value = false;
};

const closeModal = () => {
  showModal.value = false;
};

onMounted(fetchRooms);
</script>

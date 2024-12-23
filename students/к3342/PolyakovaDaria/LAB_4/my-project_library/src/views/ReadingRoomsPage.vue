<template>
  <v-container>
    <!-- Заголовок страницы -->
    <v-row>
      <v-col cols="12">
        <v-card class="pa-5 mb-5" elevation="5">
          <v-card-title class="text-h5 text-center">
            📖 Управление читальными залами
          </v-card-title>
          <v-card-text>
            <!-- Форма добавления зала -->
            <v-form @submit.prevent="addRoom">
              <v-text-field
                v-model="newRoom.number"
                label="Номер зала"
                type="number"
                placeholder="Введите номер зала"
                required
              ></v-text-field>
              <v-text-field
                v-model="newRoom.name"
                label="Название зала"
                placeholder="Введите название зала"
                required
              ></v-text-field>
              <v-text-field
                v-model="newRoom.capacity"
                label="Вместимость"
                type="number"
                placeholder="Введите вместимость"
                required
              ></v-text-field>
              <v-btn
                type="submit"
                color="primary"
                block
                class="mt-3"
                :disabled="isLoading"
              >
                Добавить зал
              </v-btn>
            </v-form>

            <!-- Сообщение об ошибке -->
            <v-alert v-if="errorMessage" type="error" class="mt-3">
              {{ errorMessage }}
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Список читальных залов -->
    <v-row>
      <v-col cols="12">
        <v-card elevation="3">
          <v-card-title>📋 Список читальных залов</v-card-title>
          <v-data-table
            :headers="headers"
            :items="rooms"
            item-value="id"
            class="elevation-1"
            :loading="isLoading"
            loading-text="Загрузка залов..."
            no-data-text="Нет доступных читальных залов."
          >
            <template #item="{ item }">
              <tr>
                <td>{{ item.number }}</td>
                <td>{{ item.name }}</td>
                <td>{{ item.capacity }}</td>
                <td>
                  <v-btn
                    color="red"
                    icon
                    @click="deleteRoom(item.id)"
                  >
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </td>
              </tr>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <!-- Индикатор загрузки -->
    <v-row v-if="isLoading" justify="center" class="mt-5">
      <v-progress-circular
        indeterminate
        color="primary"
        size="50"
      ></v-progress-circular>
    </v-row>
  </v-container>
</template>

<script>
import axiosBooks from "@/axiosBooks";

export default {
  name: 'ReadingRoomsPage',
  data() {
    return {
      headers: [
        { text: 'Номер зала', value: 'number' },
        { text: 'Название', value: 'name' },
        { text: 'Вместимость', value: 'capacity' },
        { text: 'Действия', value: 'actions', sortable: false }
      ],
      rooms: [],
      newRoom: {
        number: '',
        name: '',
        capacity: ''
      },
      errorMessage: '',
      isLoading: false
    };
  },
  methods: {
    async fetchRooms() {
      this.isLoading = true;
      try {
        const response = await axiosBooks.get("/reading_rooms/");
        this.rooms = response.data;
        this.errorMessage = "";
      } catch (error) {
        this.errorMessage = "Ошибка загрузки залов. Попробуйте снова.";
        console.error("Ошибка загрузки залов:", error.response?.data || error);
      } finally {
        this.isLoading = false;
      }
    },
    async addRoom() {
      try {
        if (!this.newRoom.number || !this.newRoom.name || this.newRoom.capacity <= 0) {
          this.errorMessage = "Пожалуйста, заполните все поля корректно.";
          return;
        }

        await axiosBooks.post("/reading_rooms/", this.newRoom);
        await this.fetchRooms();
        this.clearForm();
        this.errorMessage = "";
      } catch (error) {
        this.errorMessage =
          error.response?.data?.message ||
          "Ошибка добавления зала. Проверьте данные.";
        console.error("Ошибка добавления зала:", error.response?.data || error);
      }
    },
    async deleteRoom(roomId) {
      try {
        await axiosBooks.delete(`/reading_rooms/${roomId}/`);
        await this.fetchRooms();
        this.errorMessage = "";
      } catch (error) {
        this.errorMessage = "Ошибка удаления зала. Попробуйте снова.";
        console.error("Ошибка удаления зала:", error.response?.data || error);
      }
    },
    clearForm() {
      this.newRoom = { number: '', name: '', capacity: '' };
    },
  },
  mounted() {
    this.fetchRooms();
  },
};
</script>

<style scoped>
.v-data-table tr td {
  vertical-align: middle;
  text-align: center;
}

.v-form {
  max-width: 600px;
  margin: 0 auto;
}

.v-btn {
  padding: 10px 20px;
}

.error-message {
  color: red;
}

.loading-indicator {
  margin-top: 20px;
}
</style>

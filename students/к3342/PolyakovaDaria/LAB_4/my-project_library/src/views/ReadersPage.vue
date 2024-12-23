<template>
  <v-container>
    <!-- Форма добавления читателя -->
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-card class="pa-5 mb-5" elevation="5">
          <v-card-title class="text-h5 text-center">👤 Управление читателями</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="addReader">
              <v-text-field
                v-model="newReader.ticket_number"
                label="Номер билета"
                required
              ></v-text-field>
              <v-text-field
                v-model="newReader.full_name"
                label="ФИО"
                required
              ></v-text-field>
              <v-text-field
                v-model="newReader.passport_number"
                label="Номер паспорта"
                required
              ></v-text-field>
              <v-text-field
                v-model="newReader.birth_date"
                label="Дата рождения (дд.мм.гггг)"
                required
              ></v-text-field>
              <v-textarea
                v-model="newReader.address"
                label="Адрес"
                required
              ></v-textarea>
              <v-text-field
                v-model="newReader.phone_number"
                label="Номер телефона"
                required
              ></v-text-field>
              <v-text-field
                v-model="newReader.education_level"
                label="Уровень образования"
                required
              ></v-text-field>
              <v-switch
                v-model="newReader.has_academic_degree"
                label="Имеет ученую степень"
              ></v-switch>
              <v-select
                v-model.number="newReader.assigned_room"
                :items="readingRooms"
                item-title="name"
                item-value="id"
                label="Закрепленный читальный зал"
                :disabled="!readingRooms.length"
                required
              ></v-select>
              <v-text-field
                v-model="newReader.registration_date"
                label="Дата регистрации (дд.мм.гггг)"
                required
              ></v-text-field>
              <v-switch
                v-model="newReader.re_registered"
                label="Пройдена повторная регистрация"
              ></v-switch>
              <v-btn type="submit" color="primary" block class="mt-3" :disabled="isLoading">
                Добавить читателя
              </v-btn>
            </v-form>
            <v-alert v-if="errorMessage" type="error" class="mt-3">{{ errorMessage }}</v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Список читателей -->
    <v-row>
      <v-col cols="12">
        <v-card elevation="3">
          <v-card-title class="text-h6">📋 Список читателей</v-card-title>
          <v-card-text>
            <reader-list
              v-if="readers.length && readingRooms.length"
              :readers="readers"
              :reading-rooms="readingRooms"
              @delete="deleteReader"
              @assign-room="assignRoom"
            />
            <v-alert v-else-if="!isLoading" type="info">Список читателей пуст.</v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Индикатор загрузки -->
    <v-row v-if="isLoading" justify="center" class="mt-5">
      <v-progress-circular indeterminate color="primary" size="50"></v-progress-circular>
    </v-row>
  </v-container>
</template>

<script>
import axiosBooks from "@/axiosBooks";
import ReaderList from "@/components/ReaderList.vue";

export default {
  components: { ReaderList },
  data() {
    return {
      readers: [],
      readingRooms: [],
      newReader: {
        ticket_number: "",
        full_name: "",
        passport_number: "",
        birth_date: "",
        address: "",
        phone_number: "",
        education_level: "",
        has_academic_degree: false,
        assigned_room: null,
        registration_date: "",
        re_registered: false,
      },
      errorMessage: "",
      isLoading: false,
    };
  },
  methods: {
    async fetchReaders() {
      this.isLoading = true;
      try {
        const response = await axiosBooks.get("/readers/");
        this.readers = response.data;
        this.errorMessage = "";
      } catch (error) {
        console.error("Ошибка загрузки читателей:", error.response?.data || error);
        this.errorMessage = "Ошибка загрузки читателей. Попробуйте снова.";
      } finally {
        this.isLoading = false;
      }
    },
    async fetchRooms() {
      try {
        const response = await axiosBooks.get("/rooms/");
        this.readingRooms = response.data;
        this.errorMessage = "";
      } catch (error) {
        console.error("Ошибка загрузки залов:", error.response?.data || error);
        this.errorMessage = "Ошибка загрузки залов. Попробуйте снова.";
      }
    },
    async addReader() {
      this.isLoading = true;
      try {
        const formattedBirthDate = this.formatDate(this.newReader.birth_date);
        const formattedRegistrationDate = this.formatDate(this.newReader.registration_date);

        if (!formattedBirthDate || !formattedRegistrationDate) {
          this.errorMessage = "Некорректный формат даты. Используйте дд.мм.гггг.";
          return;
        }

        const payload = {
          ...this.newReader,
          birth_date: formattedBirthDate,
          registration_date: formattedRegistrationDate,
        };

        await axiosBooks.post("/readers/", payload);
        await this.fetchReaders();
        this.clearForm();
        this.errorMessage = "";
      } catch (error) {
        console.error("Ошибка добавления читателя:", error.response?.data || error.message);
        this.errorMessage =
          error.response?.data?.message ||
          "Ошибка добавления читателя. Проверьте данные и повторите попытку.";
      } finally {
        this.isLoading = false;
      }
    },
    async deleteReader(readerId) {
      try {
        await axiosBooks.delete(`/readers/${readerId}/`);
        await this.fetchReaders();
        this.errorMessage = "";
      } catch (error) {
        console.error("Ошибка удаления читателя:", error.response?.data || error);
        this.errorMessage = "Ошибка удаления читателя.";
      }
    },
    async assignRoom(readerId, roomId) {
      try {
        if (!roomId) {
          alert("Выберите зал для закрепления.");
          return;
        }

        await axiosBooks.patch(`/readers/${readerId}/`, {
          assigned_room: roomId,
        });

        alert(`Читатель ID ${readerId} успешно закреплен за залом ID ${roomId}.`);
        await this.fetchReaders();
      } catch (error) {
        console.error("Ошибка закрепления читателя за залом:", error.response?.data || error);
        this.errorMessage =
          error.response?.data?.message || "Ошибка закрепления читателя за залом.";
      }
    },
    formatDate(dateString) {
      if (!dateString) return null;
      const parts = dateString.split(".");
      if (parts.length !== 3) return null; // Ожидаем формат дд.мм.гггг
      const [day, month, year] = parts;
      if (
        isNaN(day) ||
        isNaN(month) ||
        isNaN(year) ||
        parseInt(day) > 31 ||
        parseInt(month) > 12
      ) {
        return null;
      }
      return `${year}-${month.padStart(2, "0")}-${day.padStart(2, "0")}`;
    },
    clearForm() {
      this.newReader = {
        ticket_number: "",
        full_name: "",
        passport_number: "",
        birth_date: "",
        address: "",
        phone_number: "",
        education_level: "",
        has_academic_degree: false,
        assigned_room: null,
        registration_date: "",
        re_registered: false,
      };
    },
  },
  mounted() {
    this.fetchReaders();
    this.fetchRooms();
  },
};
</script>

<style scoped>
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

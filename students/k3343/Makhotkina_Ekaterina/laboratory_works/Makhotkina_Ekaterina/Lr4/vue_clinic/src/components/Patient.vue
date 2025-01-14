<template>
  <Header />
  <div class="patient-list-container">
    <h1 class="title">Список пациентов</h1>

    <v-btn color="primary" class="add-patient-btn" @click="openCreateModal">Добавить пациента</v-btn>


    <v-text-field
      v-model="searchQuery"
      label="Поиск пациента"
      class="search-field"
      @input="searchPatients"
    />

    <div v-if="filteredPatients.length" class="patient-cards">
      <div v-for="patient in filteredPatients" :key="patient.id" class="patient-card">
        <h2>{{ patient.first_name }} {{ patient.last_name }}</h2>
        <p>Дата рождения: {{ patient.birth_date }}</p>
        <p>Телефон: {{ patient.phone }}</p>

        <div class="action-buttons">
          <v-btn color="yellow" @click="openEditModal(patient)" class="action-btn">Ред.</v-btn>
          <v-btn color="red" @click="deletePatient(patient.id)" class="action-btn">Удалить</v-btn>
        </div>
      </div>
    </div>

    <p v-else class="no-data">Нет данных о пациентах</p>

    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <v-card-title>
          <span class="headline">{{ isEditing ? 'Редактировать' : 'Добавить' }} пациента</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-text-field
              v-model="formData.first_name"
              label="Имя"
              required
            ></v-text-field>

            <v-text-field
              v-model="formData.last_name"
              label="Фамилия"
              required
            ></v-text-field>

            <v-text-field
              v-model="formData.middle_name"
              label="Отчество"
            ></v-text-field>

            <v-text-field
              v-model="formData.birth_date"
              label="Дата рождения"
              type="date"
              required
            ></v-text-field>

            <v-select
              v-model="formData.gender"
              :items="genders"
              label="Пол"
              required
            ></v-select>

            <v-text-field
              v-model="formData.phone"
              label="Телефон"
              required
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn color="blue darken-1" text @click="savePatient">Сохранить</v-btn>
          <v-btn color="blue darken-1" text @click="closeDialog">Отмена</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>


  </div>
</template>

<script>
import axios from "axios";
import Header from "@/components/Visual/Header.vue";

export default {
  components: {Header},
  data() {
    return {
      patients: [],
      filteredPatients: [],
      searchQuery: "",
      genders: ["Male", "Female"],
      dialog: false,
      isEditing: false,
      formData: {
        id: null,
        first_name: "",
        last_name: "",
        middle_name: "",
        birth_date: "",
        gender: "",
        phone: "",
      },
    };
  },
  async created() {
    await this.fetchPatients();
  },
  methods: {
    async fetchPatients() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/clinic/patients/");
        this.patients = response.data;
        this.filteredPatients = this.patients;
      } catch (error) {
        console.error("Ошибка при получении данных пациентов:", error);
      }
    },

    searchPatients() {
      if (this.searchQuery.trim() === "") {
        this.filteredPatients = this.patients;
      } else {
        this.filteredPatients = this.patients.filter(patient =>
          `${patient.first_name} ${patient.last_name}`.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          patient.phone.toLowerCase().includes(this.searchQuery.toLowerCase())
        );
      }
    },

    openCreateModal() {
      this.isEditing = false;
      this.formData = {
        id: null,
        first_name: "",
        last_name: "",
        middle_name: "",
        birth_date: "",
        gender: "",
        phone: "",
      };
      this.dialog = true;
    },

    openEditModal(patient) {
      this.isEditing = true;
      this.formData = { ...patient };
      this.dialog = true;
    },

    async savePatient() {
      try {
        if (!this.formData.first_name || !this.formData.last_name || !this.formData.birth_date || !this.formData.phone || !this.formData.gender) {
          console.error("Ошибка: Пожалуйста, заполните все обязательные поля.");
          return;
        }

        const payload = { ...this.formData };

        if (this.isEditing) {
          await axios.put(`http://127.0.0.1:8000/clinic/patients/${this.formData.id}/`, payload);
        } else {
          await axios.post("http://127.0.0.1:8000/clinic/patients/", payload);
        }

        this.dialog = false;
        await this.fetchPatients();
      } catch (error) {
        console.error("Ошибка при сохранении данных пациента:", error);
        if (error.response) {
          console.error("Ошибка от сервера:", error.response.data);
        }
      }
    },

    async deletePatient(patientId) {
      try {
        await axios.delete(`http://127.0.0.1:8000/clinic/patients/${patientId}/`);
        await this.fetchPatients();
      } catch (error) {
        console.error("Ошибка при удалении пациента:", error);
      }
    },

    closeDialog() {
      this.dialog = false;
    },
  },
};
</script>

<style scoped>
body {
  background-color: #ffffff;
  margin: 0;
  font-family: Arial, sans-serif;
}

.patient-list-container {
  padding: 20px;
  text-align: center;
}

.title {
  text-align: center;
}

.add-patient-btn {
  margin-bottom: 20px;
  margin-left: auto;
  margin-right: auto;
  display: block;
}

.search-field {
  width: 100%;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
  display: block;
}

.patient-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
  justify-items: center;
}

.patient-card {
  border: 1px solid #ccc;
  padding: 30px;
  width: 300px;
  box-sizing: border-box;
  text-align: left;
}

.action-buttons {
  display: flex;
  justify-content: space-between;
}

.action-btn {
  width: 90px;
  margin-top: 10px;
  font-size: 12px;
}

.no-data {
  text-align: center;
  font-size: 18px;
}

v-btn {
  margin-top: 10px;
}
</style>

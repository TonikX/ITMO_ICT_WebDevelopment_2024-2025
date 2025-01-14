<template>
  <div class="page-layout">
    <Header />

    <main class="main-content">
      <v-container class="visit-management-container">
        <v-card>
          <v-card-title class="title">Список посещений</v-card-title>
          <v-card-text>
            <v-btn color="primary" class="add-visit-btn" @click="openCreateModal">
              Добавить посещение
            </v-btn>

            <v-data-table
              :headers="headers"
              :items="appointments"
              class="elevation-1"
              item-value="id"
            >
              <template #item.actions="{ item }">
                <v-btn icon color="warning" @click="openEditModal(item)" class="action-btn">
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>

                <v-btn icon color="red" @click="deleteAppointment(item.id)" class="action-btn">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>

        <v-dialog v-model="dialog" max-width="600">
          <v-card>
            <v-card-title>
              <span class="headline">{{ isEditing ? "Редактировать" : "Создать" }} посещение</span>
            </v-card-title>
            <v-card-text>
              <v-form ref="form" v-model="formValid">
                <v-select
                  v-model="formData.patient_id"
                  :items="patients.id"
                  item-value="id"
                  item-text="name"
                  label="Пациент"
                  required
                ></v-select>
                <v-select
                  v-model="formData.medical_card_id"
                  :items="medicalCards"
                  item-value="id"
                  item-text="id"
                  label="Медицинская карта"
                  required
                ></v-select>
                <v-text-field
                  v-model="formData.appointment_datetime"
                  label="Дата и время приема"
                  type="datetime-local"
                  required
                ></v-text-field>
                <v-textarea
                  v-model="formData.anamnesis"
                  label="Анамнез"
                ></v-textarea>
                <v-textarea
                  v-model="formData.recommendations"
                  label="Рекомендации"
                ></v-textarea>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-btn color="blue darken-1" text @click="closeDialog">Отмена</v-btn>
              <v-btn color="blue darken-1" text :disabled="!formValid" @click="saveAppointment">
                Сохранить
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-container>
    </main>
  </div>
</template>


<script>
import axios from "axios";
import Header from "@/components/Visual/Header.vue";

export default {
  components: { Header},
  data() {
    return {
      appointments: [],
      patients: [],
      medicalCards: [],
      dialog: false,
      isEditing: false,
      formValid: false,
      formData: {
        id: null,
        patient_id: null,
        medical_card_id: null,
        appointment_datetime: "",
        anamnesis: "",
        recommendations: "",
      },
      headers: [
        { text: "Пациент", value: "patientName" },
        { text: "Медицинская карта", value: "medicalCardId" },
        { text: "Дата и время", value: "appointmentDateTime" },
        { text: "Анамнез", value: "anamnesis" },
        { text: "Рекомендации", value: "recommendations" },
        { text: "Действия", value: "actions", sortable: false },
      ],
      rules: {
        required: (value) => !!value || "Обязательное поле",
      },
    };
  },
  methods: {
    async fetchAppointments() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/clinic/appointments/");
        this.appointments = response.data.map((appointment) => ({
          id: appointment.id,
          patientName: `${appointment.patient.last_name} ${appointment.patient.first_name}`,
          medicalCardId: appointment.medical_card.id,
          appointmentDateTime: new Date(appointment.appointment_datetime).toLocaleString(),
          anamnesis: appointment.anamnesis || "Не указан",
          recommendations: appointment.recommendations || "Не указаны",
        }));
      } catch (error) {
        console.error("Ошибка загрузки посещений:", error);
      }
    },
    async fetchPatients() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/clinic/patients/");
        this.patients = response.data.map((patient) => ({
          id: patient.id,
          name: `${patient.last_name} ${patient.first_name} ${patient.middle_name || ""}`,
        }));
        console.log(this.patients)
      } catch (error) {
        console.error("Ошибка загрузки пациентов:", error);
      }
    },
    async fetchMedicalCards() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/clinic/medical_cards/");
        this.medicalCards = response.data;
      } catch (error) {
        console.error("Ошибка загрузки медицинских карт:", error);
      }
    },
    openCreateModal() {
      this.isEditing = false;
      this.formData = {
        id: null,
        patient_id: null,
        medical_card_id: null,
        appointment_datetime: "",
        anamnesis: "",
        recommendations: "",
      };
      this.dialog = true;
    },
    openEditModal(appointment) {
      this.isEditing = true;
      this.formData = {
        id: appointment.id,
        patient_id: appointment.patientName,
        medical_card_id: appointment.medicalCardId,
        appointment_datetime: appointment.appointmentDateTime,
        anamnesis: appointment.anamnesis,
        recommendations: appointment.recommendations,
      };
      this.dialog = true;
    },
    async saveAppointment() {
      try {
        if (this.isEditing) {
          await axios.put(
            `http://127.0.0.1:8000/clinic/appointments/${this.formData.id}/`,
            this.formData
          );
        } else {
          await axios.post("http://127.0.0.1:8000/clinic/appointments/", this.formData);
        }
        this.dialog = false;
        await this.fetchAppointments();
      } catch (error) {
        console.error("Ошибка сохранения посещения:", error);
      }
    },
    async deleteAppointment(id) {
      try {
        await axios.delete(`http://127.0.0.1:8000/clinic/appointments/${id}/`);
        await this.fetchAppointments();
      } catch (error) {
        console.error("Ошибка удаления посещения:", error);
      }
    },
    closeDialog() {
      this.dialog = false;
    },
  },
  async created() {
    await this.fetchAppointments();
    await this.fetchPatients();
    await this.fetchMedicalCards();
  },
};
</script>

<style scoped>
.page-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  background-color: #f9f9f9;
}

.visit-management-container {
  max-width: 900px;
  width: 100%;
  text-align: center;
  background-color: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  padding: 20px;
}

.title {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
}

.add-visit-btn {
  margin-bottom: 20px;
}

.elevation-1 {
  margin-top: 20px;
}

.action-btn {
  margin: 0 5px;
}
</style>


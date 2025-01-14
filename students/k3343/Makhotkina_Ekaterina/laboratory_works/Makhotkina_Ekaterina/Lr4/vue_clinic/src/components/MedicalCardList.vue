<template>
  <v-container>
    <HeaderComponent />
    <v-card>
      <v-card-title>Список медицинских обращений</v-card-title>
      <v-card-text>
        <v-data-table
          :headers="headers"
          :items="medicalCards"
          class="elevation-1"
          item-value="id"
          @click:row="viewMedicalCard"
        >
        </v-data-table>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import HeaderComponent from "@/components/Visual/Header.vue";
import axios from 'axios';

export default {
  components: {
    HeaderComponent,
  },
  data() {
    return {
      medicalCards: [],
      patients: [],
      diagnoses: [],
      headers: [
        { text: "Дата создания", value: "creation_date" },
        { text: "Пациент", value: "patient_name" },
        { text: "Диагноз", value: "diagnosis_name" },
      ],
      dialog: false,
      isEditing: false,
      formData: {
        id: null,
        creation_date: "",
        patient_id: null,
        diagnosis_id: null,
      },
    };
  },
  methods: {
    async fetchMedicalCards() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/clinic/medical_cards/");
        this.medicalCards = response.data.map((card) => {
          const patient = card.patient
            ? `${card.patient.last_name} ${card.patient.first_name}`
            : 'Неизвестен';
          const diagnosis = card.diagnosis ? card.diagnosis.diagnosis : 'Неизвестен';

          return {
            ...card,
            patient_name: patient,
            diagnosis_name: diagnosis,
          };
        });
      } catch (error) {
        console.error("Ошибка загрузки карт:", error);
      }
    },
    async fetchPatients() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/clinic/patients/");
        this.patients = response.data.map((patient) => ({
          id: patient.id,
          fullName: `${patient.last_name} ${patient.first_name}`,
        }));
      } catch (error) {
        console.error("Ошибка загрузки пациентов:", error);
      }
    },

    async fetchDiagnoses() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/clinic/diagnosis/");
        this.diagnoses = response.data.map((diagnosis) => ({
          id: diagnosis.id,
          diagnosis: diagnosis.diagnosis,
        }));
      } catch (error) {
        console.error("Ошибка загрузки диагнозов:", error);
      }
    },
    },
  async created() {
    await this.fetchMedicalCards();
    await this.fetchPatients();
    await this.fetchDiagnoses();
  },
};
</script>

<template>
  <v-container class="patient-phone-list-container">
    <v-card>
      <v-card-title class="title">Телефоны пациентов, посещавших ревматологов</v-card-title>
      <v-card-text>
        <v-data-table
          :headers="headers"
          :items="phoneNumbers"
          class="elevation-1"
        >
          <template v-slot:item.phone="{ item }">
            <span>{{ item }}</span>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      phoneNumbers: [],
      headers: [{ text: "Телефон", value: "phone" }],
    };
  },
  methods: {
    async fetchPhoneNumbers() {
      try {
        const response = await axios.get(
          "http://127.0.0.1:8000/clinic/phones_of_revmalogist_patients/"
        );
        this.phoneNumbers = response.data.phone_numbers;
      } catch (error) {
        console.error("Ошибка при загрузке данных:", error);
      }
    },
  },
  created() {
    this.fetchPhoneNumbers();
  },
};
</script>

<style scoped>
.patient-phone-list-container {
  max-width: 100%;
  width: 100%;
}

.title {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
}

.elevation-1 {
  margin-top: 20px;
}
</style>

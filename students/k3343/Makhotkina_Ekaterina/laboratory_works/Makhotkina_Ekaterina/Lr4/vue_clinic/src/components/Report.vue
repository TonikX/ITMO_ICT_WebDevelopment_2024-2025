<template>
  <v-app>
    <header class="header">
      <Header />
    </header>

    <main class="main-content">
      <v-container class="patient-phone-list-container">
        <v-card>
          <v-card-title class="title">
            Телефоны пациентов, посещавших ревматологов
          </v-card-title>
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
    </main>

  </v-app>
</template>

<script>
import axios from "axios";
import Header from "@/components/Visual/Header.vue";

export default {
  components: {
    Header,
  },
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
v-app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header {
  flex-shrink: 0;
  height: 60px;
  background-color: #fff;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  z-index: 10;
}


.main-content {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  box-sizing: border-box;
  background-color: #ffffff;
}

.patient-phone-list-container {
  max-width: 100%;
  width: 100%;
  text-align: center;
}


.footer {
  flex-shrink: 0;
  height: 50px;
  background-color: #fff;
  box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.title {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
}

.elevation-1 {
  margin-top: 20px;
}

.no-data {
  text-align: center;
  font-size: 18px;
}
</style>


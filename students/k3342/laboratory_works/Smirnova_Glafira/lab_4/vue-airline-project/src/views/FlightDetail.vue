<template>
  <v-container>
    <v-row v-if="flight">
      <v-col cols="12">
        <h1 class="text-center">Информация о перелете {{ flight.number }}</h1>
      </v-col>
    </v-row>

    <v-row v-if="flight">
      <v-col cols="12" md="6">
        <v-card class="compact-card mb-6" elevation="2">
          <v-card-title>
            <strong>Номер перелета:</strong> {{ flight.number }}
          </v-card-title>
          <v-card-text>
            <p><strong>Аэропорт вылета:</strong> {{ flight.route.departure_airport }}</p>
            <v-divider class="my-2"></v-divider>
            <p><strong>Аэропорт прилета:</strong> {{ flight.route.destination_airport }}</p>
            <v-divider class="my-2"></v-divider>
            <p><strong>Дата и время вылета:</strong> {{ flight.route.departure_time }} {{ flight.departure_date }}</p>
            <v-divider class="my-2"></v-divider>
            <p><strong>Дата и время прилета:</strong> {{ flight.route.arrival_time }} {{ flight.arrival_date }}</p>
            <v-divider class="my-2"></v-divider>
            <template v-if="flight.route.stops.length > 0">
                <p><strong>Остановки:</strong></p>
                <ul class="stops-list">
                  <li v-for="stop in flight.route.stops" :key="stop.id">
                    {{ stop.airport }} - {{ stop.arrival_time || 'неизвестно' }}
                  </li>
                </ul>
              </template>
              <template v-else>
                <p><strong>Остановки:</strong> Нет остановок</p>
              </template>
            <v-divider class="my-2"></v-divider>
            <p><strong>Экипаж:</strong> {{ flight.crew }}</p>
            <v-divider class="my-2"></v-divider>
            <p>
              <strong>Самолет:</strong> {{ flight.plane.number }} - {{ flight.plane.airline }} - {{ flight.plane.model.name }}
            </p>
            <v-divider class="my-2"></v-divider>
            <p><strong>Количество мест:</strong> {{ flight.plane.model.seats_capacity }}</p>
            <v-divider class="my-2"></v-divider>
            <p><strong>Проданные билеты:</strong> {{ flight.sold_tickets_number }}</p>
            <v-divider class="my-2"></v-divider>
            <p><strong>Статус:</strong> {{ flight.status }}</p>
            <v-divider class="my-2"></v-divider>
            <p><strong>Расстояние:</strong> {{ flight.route.distance_km }} км</p>
          </v-card-text>
          <v-card-actions class="justify-center">
            <v-btn color="warning" @click="openEditDialog">Изменить перелет</v-btn>
            <v-btn color="error" @click="openDeleteDialog">Удалить перелет</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <SeatsTable :flightId="flightId" />
      </v-col>
    </v-row>

    <EditFlightDialog
      v-if="flight"
      ref="editFlightDialog"
      :dialog="editDialog"
      @update:dialog="editDialog = $event"
      :initial-flight="flight"
      :choices="choices"
      @flight-updated="updateFlight"
    />
    <DeleteFlightDialog
      v-if="flight"
      :dialog="deleteDialog"
      :flight="flight"
      @update:dialog="deleteDialog = $event"
      @flight-deleted="handleFlightDeleted"
    />

  </v-container>
</template>

<script>
import apiClient from '@/services/api';
import SeatsTable from "@/components/flights/SeatsTable.vue";
import EditFlightDialog from "@/components/flights/EditFlightDialog.vue";
import CreateFlightDialog from "@/components/flights/CreateFlightDialog.vue";
import DeleteFlightDialog from "@/components/flights/DeleteFlightDialog.vue";


export default {
  components: {DeleteFlightDialog, CreateFlightDialog, EditFlightDialog, SeatsTable},
  data() {
    return {
      flight: null,
      choices: {},
      editDialog: false,
      deleteDialog: false,
    };
  },
  props: {
    flightId: {
      type: String,
      required: true,
    },
  },
  methods: {
    async fetchFlight() {
      try {
        const response = await apiClient.get(`/flights/${this.flightId}/`);
        console.log(response)
        this.flight = response.data;
      } catch (error) {
        console.error('Ошибка загрузки информации о перелете:', error.response?.data || error.message);
      }
    },

    openEditDialog() {
      this.editDialog = true;
    },
    openDeleteDialog() {
      this.deleteDialog = true;
    },

    async updateFlight(updatedFlight) {
      try {
        await apiClient.put(`/flights/${this.flightId}/`, updatedFlight);
        this.$refs.editFlightDialog.closeDialog();
        this.editDialog = false;
        await this.fetchFlight();
      } catch (error) {
        if (error.response && error.response.status === 400) {
          this.$refs.editFlightDialog.setErrors(error.response.data);
        } else {
          console.error("Ошибка обновления перелета:", error.response?.data || error.message);
          alert("Ошибка обновления перелета");
        }
      }
    },

    async fetchChoices() {
      try {
        const response = await apiClient.get("/flights/choices/");
        console.log(response.data)
        this.choices = response.data;
      } catch (error) {
        console.error('Ошибка загрузки данных для выбора:', error.response?.data || error.message);
      }
    },

    async handleFlightDeleted(flightId) {
      try {
        await apiClient.delete(`/flights/${flightId}/`);
        this.$router.push('/flights');
      } catch (error) {
        console.error("Ошибка удаления перелета:", error.response?.data || error.message);
      }
    },
  },
  async created() {
    console.log("Получен flightId:", this.flightId);
    await Promise.all([this.fetchFlight(), this.fetchChoices()]);
  },
};
</script>

<style scoped>
.text-center {
  text-align: center;
}
.stops-list {
  padding-left: 20px;
  margin: 0;
  list-style-position: inside;
}

.stops-list li {
  margin: 2px 0;
}

.compact-card {
  max-width: 700px;
  padding: 50px;
  margin: 0 auto;
  font-size: 40px;
}

.compact-card .v-card-title {
  font-size: 16px;
}

.compact-card .v-card-subtitle {
  font-size: 14px;
}

.compact-card p {
  margin: 4px 0;
}

.compact-card .v-card-actions {
  padding: 5px;
}
</style>


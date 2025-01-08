<template>
  <v-container>
    <v-row class="mb-4">
      <v-col>
        <div class="d-flex justify-space-between align-center">
          <h1 class="text-h4">Список водителей</h1>
          <v-btn
            color="primary"
            prepend-icon="mdi-plus"
            to="/drivers/add"
          >
            ДОБАВИТЬ ВОДИТЕЛЯ
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-card>
          <div class="custom-table">
            <table>
              <thead>
                <tr>
                  <th>ФИО</th>
                  <th>Класс</th>
                  <th>Зарплата</th>
                  <th>Действия</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="driver in drivers" :key="driver.id">
                  <td>{{ driver.last_name }} {{ driver.first_name }}</td>
                  <td>{{ driver.driver_class.name }}</td>
                  <td>{{ driver.salary_rub ? `${driver.salary_rub} ₽` : 'Не указана' }}</td>
                  <td class="text-center">
                    <v-btn
                      icon
                      variant="text"
                      :to="`/drivers/${driver.id}`"
                      color="primary"
                    >
                      <v-icon>mdi-eye</v-icon>
                    </v-btn>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <v-overlay
            :model-value="loading"
            class="align-center justify-center"
          >
            <v-progress-circular
              indeterminate
              color="primary"
            ></v-progress-circular>
          </v-overlay>
        </v-card>
      </v-col>
    </v-row>

    <v-snackbar
      v-model="showError"
      color="error"
      timeout="3000"
    >
      {{ errorMessage }}
    </v-snackbar>
  </v-container>
</template>

<script>
import { api } from '@/services/api'
import PageWrapper from '@/components/PageWrapper.vue'

export default {
  name: 'DriversList',
  components: {
    PageWrapper
  },
  
  data: () => ({
    drivers: [],
    loading: true,
    showError: false,
    errorMessage: ''
  }),

  async created() {
    await this.fetchDrivers()
  },

  methods: {
    async fetchDrivers() {
      try {
        const { data } = await api.get('/drivers')
        this.drivers = data
        console.log('Drivers loaded:', data)
      } catch (error) {
        console.error('Error loading drivers:', error)
        this.errorMessage = 'Ошибка при загрузке списка водителей'
        this.showError = true
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.custom-table {
  width: 100%;
  overflow-x: auto;
}

.custom-table table {
  width: 100%;
  border-collapse: collapse;
}

.custom-table th,
.custom-table td {
  padding: 16px 24px;
  text-align: left;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}

.custom-table th {
  font-weight: 500;
  color: rgba(0, 0, 0, 0.87);
  background-color: #f5f5f5;
}

.custom-table tr:hover {
  background-color: #f5f5f5;
}

.custom-table td:last-child {
  text-align: center;
}
</style>
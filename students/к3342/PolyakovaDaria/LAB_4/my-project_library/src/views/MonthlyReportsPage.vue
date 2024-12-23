<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-card class="pa-5" elevation="5">
          <v-card-title class="text-h5 text-center">
            📅 Ежемесячные отчёты
          </v-card-title>
          <v-card-text>
            <!-- Форма для выбора месяца и года -->
            <v-form @submit.prevent="fetchMonthlyReports">
              <v-text-field
                v-model="filters.year"
                label="Год"
                type="number"
                placeholder="2024"
                required
                class="mb-3"
              ></v-text-field>
              <v-text-field
                v-model="filters.month"
                label="Месяц"
                type="number"
                placeholder="1-12"
                min="1"
                max="12"
                required
                class="mb-3"
              ></v-text-field>
              <v-btn
                type="submit"
                color="primary"
                block
                :disabled="isLoading"
              >
                Сформировать отчёт
              </v-btn>
            </v-form>
            
            <!-- Сообщение об ошибке -->
            <v-alert
              v-if="errorMessage"
              type="error"
              class="mt-3"
            >
              {{ errorMessage }}
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Отображение отчётов -->
    <v-row v-if="reports" class="mt-5">
      <v-col cols="12">
        <v-card elevation="3">
          <v-card-title class="text-h6">📊 Результаты отчёта</v-card-title>
          <v-card-text>
            <v-table>
              <tbody>
                <tr v-if="reports.total_books !== undefined">
                  <th>📚 Общее количество книг</th>
                  <td>{{ reports.total_books.total }}</td>
                </tr>
                <tr v-if="reports.new_readers !== undefined">
                  <th>👥 Новые читатели</th>
                  <td>{{ reports.new_readers }}</td>
                </tr>
              </tbody>
            </v-table>

            <h3
              v-if="reports.room_data && reports.room_data.length"
              class="mt-4"
            >
              🏢 Посещения читальных залов
            </h3>
            <v-table v-if="reports.room_data && reports.room_data.length">
              <thead>
                <tr>
                  <th>Название зала</th>
                  <th>Количество посещений</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="room in reports.room_data" :key="room.room__name">
                  <td>{{ room.room__name }}</td>
                  <td>{{ room.count }}</td>
                </tr>
              </tbody>
            </v-table>
          </v-card-text>
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

    <v-row v-else-if="!reports && !isLoading">
      <v-col cols="12" class="text-center mt-5">
        <v-alert type="info">Отчёты пока не загружены.</v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axiosBooks from '@/axiosBooks';

export default {
  name: 'MonthlyReportsPage',
  data() {
    return {
      reports: null,
      errorMessage: null,
      isLoading: false,
      filters: {
        year: new Date().getFullYear(),
        month: '',
      },
    };
  },
  methods: {
    async fetchMonthlyReports() {
      this.isLoading = true;
      this.errorMessage = null;
      this.reports = null;

      try {
        const { year, month } = this.filters;
        const params = { report_type: 'monthly', year, month };
        const response = await axiosBooks.get('/reports/', { params });
        this.reports = response.data;
      } catch (error) {
        console.error('Ошибка загрузки отчетов:', error.response?.data || error);
        this.errorMessage =
          error.response?.data?.error || 'Произошла ошибка при загрузке отчетов.';
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

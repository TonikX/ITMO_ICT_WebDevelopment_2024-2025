<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card class="pa-5 mb-5" elevation="5">
          <v-card-title class="text-h5 text-center">📊 Сводные и сложные отчёты</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="fetchReports">
              <v-text-field
                v-model="filters.year"
                label="Год"
                type="number"
                placeholder="Например, 2024"
                required
              ></v-text-field>
              <v-btn
                type="submit"
                color="primary"
                block
                class="mt-3"
                :disabled="isLoading"
              >
                Сформировать отчёт
              </v-btn>
            </v-form>
            <v-alert v-if="errorMessage" type="error" class="mt-3">
              {{ errorMessage }}
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-if="reports">
      <v-col cols="12">
        <v-card elevation="3" class="mb-5">
          <v-card-title>📊 Результаты отчёта</v-card-title>
          <v-card-text>
            <table class="report-table">
              <tbody>
                <tr v-if="reports.readers_under_20 !== undefined">
                  <th>👶 Читатели младше 20 лет</th>
                  <td>{{ reports.readers_under_20 }}</td>
                </tr>
                <tr v-if="reports.total_books !== undefined">
                  <th>📚 Общее количество книг</th>
                  <td>{{ reports.total_books }}</td>
                </tr>
              </tbody>
            </table>
            <h3 v-if="reports.education_statistics" class="mt-4">🎓 Образовательная статистика</h3>
            <table class="report-table" v-if="reports.education_statistics">
              <thead>
                <tr>
                  <th>Уровень образования</th>
                  <th>Процент</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(percent, level) in translatedEducationStatistics" :key="level">
                  <td>{{ level }}</td>
                  <td>{{ percent }}%</td>
                </tr>
              </tbody>
            </table>
            <h3 v-if="reports.room_data?.length" class="mt-4">🏢 Посещения читальных залов</h3>
            <table class="report-table" v-if="reports.room_data?.length">
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
            </table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-if="isLoading" justify="center" class="mt-5">
      <v-progress-circular indeterminate color="primary" size="50"></v-progress-circular>
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
  name: 'ReportsPage',
  data() {
    return {
      reports: null,
      filters: {
        report_type: 'summary', // Тип отчёта по умолчанию
        year: new Date().getFullYear(),
      },
      isLoading: false,
      errorMessage: '',
    };
  },
  computed: {
    translatedEducationStatistics() {
      if (!this.reports || !this.reports.education_statistics) return {};
      return Object.keys(this.reports.education_statistics).reduce((acc, key) => {
        const translatedKey = this.translateEducationKey(key);
        acc[translatedKey] = this.reports.education_statistics[key];
        return acc;
      }, {});
    },
  },
  methods: {
    async fetchReports() {
      this.isLoading = true;
      try {
        if (!this.filters.year) {
          this.errorMessage = 'Укажите год отчёта.';
          return;
        }
        const params = {
          report_type: this.filters.report_type, // Используется только "summary"
          year: String(this.filters.year),
        };
        console.log('Отправляем параметры:', params);
        const response = await axiosBooks.get('/reports/complex/', { params });
        this.reports = response.data;
        this.errorMessage = '';
      } catch (error) {
        console.error('Ошибка загрузки отчётов:', error.response?.data || error);
        this.errorMessage = error.response?.data?.error || 'Произошла ошибка при загрузке отчётов.';
      } finally {
        this.isLoading = false;
      }
    },
    translateEducationKey(key) {
      const translations = {
        bachelor: 'Бакалавр',
        master: 'Магистр',
        phd: 'Кандидат наук',
      };
      return translations[key] || key;
    },
  },
};
</script>

<style scoped>
.report-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}
.report-table th, .report-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
.report-table th {
  background-color: #f8f9fa;
  font-weight: bold;
  text-transform: uppercase;
}
</style>

<template>
  <v-container>
    <!-- Заголовок страницы -->
    <v-row>
      <v-col cols="12">
        <v-card class="pa-5 mb-5" elevation="5">
          <v-card-title class="text-h5 text-center">📊 Отчёты по библиотеке</v-card-title>
        </v-card>
      </v-col>
    </v-row>

    <!-- Форма фильтрации отчётов -->
    <v-row>
      <v-col cols="12">
        <v-card class="pa-4 mb-4" elevation="2">
          <v-form @submit.prevent="fetchReports">
            <v-select
              v-model="filters.report_type"
              :items="reportTypes"
              label="Тип отчёта"
              required
            ></v-select>
            <v-text-field
              v-model="filters.year"
              label="Год"
              type="number"
              placeholder="Например, 2024"
              required
            ></v-text-field>
            <v-text-field
              v-if="filters.report_type === 'monthly'"
              v-model="filters.month"
              label="Месяц"
              type="number"
              min="1"
              max="12"
              placeholder="Введите месяц (1-12)"
            ></v-text-field>
            <v-btn
              color="primary"
              class="mt-3"
              type="submit"
              block
              :disabled="isLoading"
            >
              Сформировать отчёт
            </v-btn>
          </v-form>
        </v-card>
      </v-col>
    </v-row>

    <!-- Сообщение об ошибке -->
    <v-row v-if="errorMessage">
      <v-col cols="12">
        <v-alert type="error">{{ errorMessage }}</v-alert>
      </v-col>
    </v-row>

    <!-- Результаты отчёта -->
    <v-row v-if="reports">
      <v-col cols="12">
        <v-card class="pa-4" elevation="2">
          <v-card-title>📊 Результаты отчёта</v-card-title>
          <v-card-text>
            <v-table>
              <tbody>
                <tr v-if="reports.total_books !== undefined">
                  <th>📚 Общее количество книг</th>
                  <td>{{ reports.total_books }}</td>
                </tr>
                <tr v-if="reports.readers_under_20 !== undefined">
                  <th>👶 Читатели младше 20 лет</th>
                  <td>{{ reports.readers_under_20 }}</td>
                </tr>
              </tbody>
            </v-table>

            <!-- Образовательная статистика -->
            <h3 class="mt-4">🎓 Образовательная статистика</h3>
            <v-table v-if="reports.education_statistics">
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
            </v-table>

            <!-- Посещения залов -->
            <h3 class="mt-4">🏢 Посещения залов</h3>
            <v-table v-if="reports.room_data?.length">
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
    <v-row v-if="isLoading" justify="center">
      <v-progress-circular indeterminate color="primary" size="50"></v-progress-circular>
    </v-row>

    <!-- Сообщение при отсутствии данных -->
    <v-row v-if="!reports && !isLoading">
      <v-col cols="12" class="text-center">
        <v-alert type="info">Отчёты пока не загружены.</v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

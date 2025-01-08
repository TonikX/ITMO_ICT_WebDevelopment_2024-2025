<template>
  <v-container class="page-wrapper" fluid>
    <v-row justify="center">
      <v-col cols="12" xl="11">
        <div class="mb-4 d-flex justify-space-between align-center">
          <h1 class="text-h4">Список маршрутов</h1>
          <v-btn
            color="primary"
            prepend-icon="mdi-plus"
            to="/routes/add"
          >
            ДОБАВИТЬ МАРШРУТ
          </v-btn>
        </div>

        <v-card>
          <v-table hover>
            <thead>
              <tr>
                <th class="text-left" style="width: 15%">Название</th>
                <th class="text-left" style="width: 15%">Начальная точка</th>
                <th class="text-left" style="width: 15%">Конечная точка</th>
                <th class="text-left" style="width: 15%">Время работы</th>
                <th class="text-left" style="width: 12%">Интервал</th>
                <th class="text-left" style="width: 12%">Длительность</th>
                <th class="text-left" style="width: 8%">Длина (км)</th>
                <th class="text-center" style="width: 8%">Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="loading">
                <td colspan="8" class="text-center">
                  <v-progress-circular
                    indeterminate
                    color="primary"
                    class="my-4"
                  ></v-progress-circular>
                </td>
              </tr>
              <tr v-else-if="routes.length === 0">
                <td colspan="8" class="text-center py-4">
                  Маршруты не найдены
                </td>
              </tr>
              <tr v-else v-for="route in routes" :key="route.id">
                <td>{{ route.name }}</td>
                <td>{{ route.start_point_name }}</td>
                <td>{{ route.end_point_name }}</td>
                <td>{{ `${route.start_time} - ${route.end_time}` }}</td>
                <td>{{ formatSeconds(route.interval_seconds) }}</td>
                <td>{{ formatSeconds(route.duration_seconds) }}</td>
                <td>{{ route.length?.toFixed(1) || '—' }}</td>
                <td class="text-center">
                  <v-btn
                    icon="mdi-pencil"
                    variant="text"
                    color="primary"
                    size="small"
                    class="mr-2"
                    :to="`/routes/${route.id}`"
                  ></v-btn>
                  <v-btn
                    icon="mdi-delete"
                    variant="text"
                    color="error"
                    size="small"
                    @click="confirmDelete(route)"
                  ></v-btn>
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-card>

        <v-dialog v-model="showDeleteDialog" max-width="400">
          <v-card>
            <v-card-title>Подтверждение удаления</v-card-title>
            <v-card-text>
              Вы действительно хотите удалить этот маршрут?
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="grey"
                variant="text"
                @click="showDeleteDialog = false"
              >
                Отмена
              </v-btn>
              <v-btn
                color="error"
                variant="text"
                @click="deleteRoute"
                :loading="deleting"
              >
                Удалить
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <v-snackbar
          v-model="showError"
          color="error"
          timeout="3000"
        >
          {{ errorMessage }}
        </v-snackbar>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { api } from '@/services/api'

export default {
  name: 'RoutesList',

  data: () => ({
    routes: [],
    loading: true,
    deleting: false,
    showDeleteDialog: false,
    showError: false,
    errorMessage: '',
    selectedRoute: null
  }),

  async created() {
    await this.fetchRoutes()
  },

  methods: {
    async fetchRoutes() {
      this.loading = true
      try {
        const { data } = await api.get('/routes')
        this.routes = data
      } catch (error) {
        console.error('Error loading routes:', error)
        this.errorMessage = 'Ошибка при загрузке списка маршрутов'
        this.showError = true
      } finally {
        this.loading = false
      }
    },

    formatSeconds(seconds) {
      if (!seconds) return '—'
      const minutes = Math.round(seconds / 60)
      return `${minutes} мин`
    },

    confirmDelete(route) {
      this.selectedRoute = route
      this.showDeleteDialog = true
    },

    async deleteRoute() {
      if (!this.selectedRoute) return

      this.deleting = true
      try {
        await api.delete(`/routes/${this.selectedRoute.id}`)
        await this.fetchRoutes()
        this.showDeleteDialog = false
      } catch (error) {
        console.error('Error deleting route:', error)
        this.errorMessage = 'Ошибка при удалении маршрута'
        this.showError = true
      } finally {
        this.deleting = false
      }
    }
  }
}
</script> 
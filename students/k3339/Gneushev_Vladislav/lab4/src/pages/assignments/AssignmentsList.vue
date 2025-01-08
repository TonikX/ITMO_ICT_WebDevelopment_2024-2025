<template>
  <v-container class="page-wrapper" fluid>
    <v-row justify="center">
      <v-col cols="12" xl="11">
        <div class="mb-4 d-flex justify-space-between align-center">
          <h1 class="text-h4">Список назначений</h1>
          <v-btn
            color="primary"
            prepend-icon="mdi-plus"
            to="/assignments/add"
          >
            ДОБАВИТЬ НАЗНАЧЕНИЕ
          </v-btn>
        </div>

        <!-- Фильтры -->
        <v-card class="mb-4">
          <v-card-text>
            <v-row>
              <v-col cols="12" sm="6" md="3">
                <v-select
                  v-model="filters.active"
                  :items="[
                    { title: 'Все', value: null },
                    { title: 'Активные', value: true },
                    { title: 'Завершённые', value: false }
                  ]"
                  item-title="title"
                  item-value="value"
                  label="Статус"
                  hide-details
                  density="comfortable"
                ></v-select>
              </v-col>

              <v-col cols="12" sm="6" md="3">
                <v-select
                  v-model="filters.route_id"
                  :items="routes"
                  item-title="name"
                  item-value="id"
                  label="Маршрут"
                  hide-details
                  density="comfortable"
                  clearable
                ></v-select>
              </v-col>

              <v-col cols="12" sm="6" md="3">
                <v-select
                  v-model="filters.driver_id"
                  :items="drivers"
                  :item-title="driver => `${driver.last_name} ${driver.first_name}`"
                  item-value="id"
                  label="Водитель"
                  hide-details
                  density="comfortable"
                  clearable
                ></v-select>
              </v-col>

              <v-col cols="12" sm="6" md="3">
                <v-select
                  v-model="filters.bus_id"
                  :items="buses"
                  item-title="state_number"
                  item-value="id"
                  label="Автобус"
                  hide-details
                  density="comfortable"
                  clearable
                ></v-select>
              </v-col>

              <v-col cols="12" sm="6" md="3">
                <v-select
                  v-model="filters.day_of_week"
                  :items="daysOfWeek"
                  item-title="title"
                  item-value="value"
                  label="День недели"
                  hide-details
                  density="comfortable"
                  clearable
                ></v-select>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <!-- Таблица назначений -->
        <v-card>
          <v-table hover>
            <thead>
              <tr>
                <th class="text-left">Маршрут</th>
                <th class="text-left">Водитель</th>
                <th class="text-left">Автобус</th>
                <th class="text-left">День недели</th>
                <th class="text-left">Статус</th>
                <th class="text-left">Дата начала</th>
                <th class="text-left">Дата завершения</th>
                <th class="text-center">Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="assignment in assignments" :key="assignment.id">
                <td>{{ assignment.route.name }}</td>
                <td>{{ `${assignment.driver.last_name} ${assignment.driver.first_name}` }}</td>
                <td>{{ assignment.bus.state_number }}</td>
                <td>{{ getDayOfWeekTitle(assignment.day_of_week) }}</td>
                <td>
                  <v-chip
                    :color="assignment.to_date ? 'error' : 'success'"
                    size="small"
                  >
                    {{ assignment.to_date ? 'Завершено' : 'Активно' }}
                  </v-chip>
                </td>
                <td>{{ formatDate(assignment.from_date) }}</td>
                <td>{{ assignment.to_date ? formatDate(assignment.to_date) : '-' }}</td>
                <td class="text-center">
                  <v-btn
                    v-if="!assignment.to_date"
                    icon="mdi-stop-circle"
                    variant="text"
                    color="warning"
                    size="small"
                    class="mr-2"
                    @click="showEndDialog(assignment)"
                  ></v-btn>
                  <v-btn
                    icon="mdi-delete"
                    variant="text"
                    color="error"
                    size="small"
                    @click="confirmDelete(assignment)"
                  ></v-btn>
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-card>

        <!-- Диалог завершения назначения -->
        <v-dialog v-model="showEndAssignmentDialog" max-width="500">
          <v-card>
            <v-card-title>Завершение назначения</v-card-title>
            <v-card-text>
              <v-select
                v-model="endReason"
                :items="endReasons"
                label="Причина завершения"
                item-title="title"
                item-value="value"
                required
              ></v-select>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn
                color="grey"
                variant="text"
                @click="showEndAssignmentDialog = false"
              >
                Отмена
              </v-btn>
              <v-btn
                color="warning"
                variant="text"
                @click="endAssignment"
                :loading="ending"
                :disabled="!endReason"
              >
                Завершить
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!-- Диалог подтверждения удаления -->
        <v-dialog v-model="showDeleteDialog" max-width="400">
          <v-card>
            <v-card-title>Подтверждение удаления</v-card-title>
            <v-card-text>
              Вы действительно хотите удалить это назначение?
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
                @click="deleteAssignment"
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
import PageWrapper from '@/components/PageWrapper.vue'

export default {
  name: 'AssignmentsList',
  
  components: {
    PageWrapper
  },

  data: () => ({
    assignments: [],
    routes: [],
    drivers: [],
    buses: [],
    endReasons: [],
    filters: {
      active: null,
      route_id: null,
      driver_id: null,
      bus_id: null,
      day_of_week: null
    },
    daysOfWeek: [
      { title: 'Понедельник', value: 'monday' },
      { title: 'Вторник', value: 'tuesday' },
      { title: 'Среда', value: 'wednesday' },
      { title: 'Четверг', value: 'thursday' },
      { title: 'Пятница', value: 'friday' },
      { title: 'Суббота', value: 'saturday' },
      { title: 'Воскресенье', value: 'sunday' }
    ],
    showEndAssignmentDialog: false,
    showDeleteDialog: false,
    selectedAssignment: null,
    endReason: null,
    ending: false,
    deleting: false,
    showError: false,
    errorMessage: '',
    endReasonTitles: {
      driver_ill: 'Болезнь водителя',
      bus_broken: 'Поломка автобуса',
      route_canceled: 'Отмена маршрута',
      bus_write_off: 'Списание автобуса',
      other: 'Другое'
    }
  }),

  watch: {
    filters: {
      deep: true,
      handler() {
        this.fetchAssignments()
      }
    }
  },

  async created() {
    await Promise.all([
      this.fetchAssignments(),
      this.fetchRoutes(),
      this.fetchDrivers(),
      this.fetchBuses(),
      this.fetchEndReasons()
    ])
  },

  methods: {
    async fetchAssignments() {
      try {
        const params = {}
        Object.entries(this.filters).forEach(([key, value]) => {
          if (value !== null) {
            params[key] = value
          }
        })
        
        const { data } = await api.get('/assignments', { params })
        this.assignments = data
      } catch (error) {
        console.error('Error loading assignments:', error)
        this.errorMessage = 'Ошибка при загрузке списка назначений'
        this.showError = true
      }
    },

    async fetchRoutes() {
      try {
        const { data } = await api.get('/routes')
        this.routes = data
      } catch (error) {
        console.error('Error loading routes:', error)
      }
    },

    async fetchDrivers() {
      try {
        const { data } = await api.get('/drivers')
        this.drivers = data
      } catch (error) {
        console.error('Error loading drivers:', error)
      }
    },

    async fetchBuses() {
      try {
        const { data } = await api.get('/buses')
        this.buses = data
      } catch (error) {
        console.error('Error loading buses:', error)
      }
    },

    async fetchEndReasons() {
      try {
        const { data } = await api.get('/assignments/end/reasons')
        this.endReasons = data.map(reason => ({
          title: this.endReasonTitles[reason] || reason,
          value: reason
        }))
      } catch (error) {
        console.error('Error loading end reasons:', error)
      }
    },

    getDayOfWeekTitle(value) {
      const day = this.daysOfWeek.find(d => d.value === value)
      return day ? day.title : value
    },

    formatDate(date) {
      return new Date(date).toLocaleDateString()
    },

    showEndDialog(assignment) {
      this.selectedAssignment = assignment
      this.endReason = null
      this.showEndAssignmentDialog = true
    },

    async endAssignment() {
      if (!this.selectedAssignment || !this.endReason) return

      this.ending = true
      try {
        await api.post(`/assignments/${this.selectedAssignment.id}/end`, {
          reason: this.endReason.value
        })
        await this.fetchAssignments()
        this.showEndAssignmentDialog = false
      } catch (error) {
        console.error('Error ending assignment:', error)
        this.errorMessage = 'Ошибка при завершении назначения'
        this.showError = true
      } finally {
        this.ending = false
      }
    },

    confirmDelete(assignment) {
      this.selectedAssignment = assignment
      this.showDeleteDialog = true
    },

    async deleteAssignment() {
      if (!this.selectedAssignment) return

      this.deleting = true
      try {
        await api.delete(`/assignments/${this.selectedAssignment.id}`)
        await this.fetchAssignments()
        this.showDeleteDialog = false
      } catch (error) {
        console.error('Error deleting assignment:', error)
        this.errorMessage = 'Ошибка при удалении назначения'
        this.showError = true
      } finally {
        this.deleting = false
      }
    }
  }
}
</script>

<style>
.v-table {
  width: 100%;
}

.v-table > .v-table__wrapper > table {
  width: 100%;
  table-layout: fixed;
}

/* Настройка ширины колонок */
.v-table > .v-table__wrapper > table th {
  white-space: nowrap;
  padding: 0 16px;
}

.v-table > .v-table__wrapper > table td {
  padding: 0 16px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.v-btn--icon.v-btn--size-small {
  width: 34px;
  height: 34px;
  min-width: 0;
}

.v-btn--icon.v-btn--size-small .v-icon {
  font-size: 20px;
}
</style> 
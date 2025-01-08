<template>
  <page-wrapper>
    <v-card>
      <v-card-title>Добавление назначения</v-card-title>
      
      <v-card-text>
        <v-form @submit.prevent="handleSubmit">
          <v-select
            v-model="form.driver_id"
            :items="drivers"
            :item-title="driver => `${driver.last_name} ${driver.first_name}`"
            item-value="id"
            label="Водитель"
            :rules="[v => !!v || 'Обязательное поле']"
            :loading="loadingDrivers"
            required
          ></v-select>

          <v-select
            v-model="form.route_id"
            :items="routes"
            item-title="name"
            item-value="id"
            label="Маршрут"
            :rules="[v => !!v || 'Обязательное поле']"
            :loading="loadingRoutes"
            required
          >
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props">
                <v-list-item-title>
                  {{ item.raw.name }} ({{ formatRouteTime(item.raw) }})
                </v-list-item-title>
              </v-list-item>
            </template>
          </v-select>

          <v-select
            v-model="form.bus_id"
            :items="buses"
            item-title="state_number"
            item-value="id"
            label="Автобус"
            :rules="[v => !!v || 'Обязательное поле']"
            :loading="loadingBuses"
            required
          >
            <template v-slot:item="{ props, item }">
              <v-list-item v-bind="props">
                <v-list-item-title>
                  {{ item.raw.state_number }} ({{ item.raw.bus_type.name }})
                </v-list-item-title>
              </v-list-item>
            </template>
          </v-select>

          <v-select
            v-model="form.day_of_week"
            :items="daysOfWeek"
            item-title="title"
            item-value="value"
            label="День недели"
            :rules="[v => !!v || 'Обязательное поле']"
            required
          ></v-select>

          <div class="d-flex justify-end mt-4">
            <v-btn
              color="grey"
              variant="text"
              class="mr-2"
              to="/assignments"
            >
              Отмена
            </v-btn>
            <v-btn
              color="primary"
              type="submit"
              :loading="saving"
              :disabled="!isValid"
            >
              Сохранить
            </v-btn>
          </div>
        </v-form>
      </v-card-text>
    </v-card>

    <v-snackbar
      v-model="showError"
      color="error"
      timeout="3000"
    >
      {{ errorMessage }}
    </v-snackbar>
  </page-wrapper>
</template>

<script>
import { api } from '@/services/api'
import PageWrapper from '@/components/PageWrapper.vue'

export default {
  name: 'AddAssignment',
  
  components: {
    PageWrapper
  },

  data: () => ({
    form: {
      driver_id: null,
      route_id: null,
      bus_id: null,
      day_of_week: null
    },
    drivers: [],
    routes: [],
    buses: [],
    daysOfWeek: [
      { title: 'Понедельник', value: 'monday' },
      { title: 'Вторник', value: 'tuesday' },
      { title: 'Среда', value: 'wednesday' },
      { title: 'Четверг', value: 'thursday' },
      { title: 'Пятница', value: 'friday' },
      { title: 'Суббота', value: 'saturday' },
      { title: 'Воскресенье', value: 'sunday' }
    ],
    loadingDrivers: true,
    loadingRoutes: true,
    loadingBuses: true,
    saving: false,
    showError: false,
    errorMessage: ''
  }),

  computed: {
    isValid() {
      return (
        this.form.driver_id &&
        this.form.route_id &&
        this.form.bus_id &&
        this.form.day_of_week
      )
    }
  },

  async created() {
    await Promise.all([
      this.fetchDrivers(),
      this.fetchRoutes(),
      this.fetchBuses()
    ])
  },

  methods: {
    async fetchDrivers() {
      try {
        const { data } = await api.get('/drivers')
        this.drivers = data
      } catch (error) {
        console.error('Error loading drivers:', error)
        this.errorMessage = 'Ошибка при загрузке списка водителей'
        this.showError = true
      } finally {
        this.loadingDrivers = false
      }
    },

    async fetchRoutes() {
      try {
        const { data } = await api.get('/routes')
        this.routes = data
      } catch (error) {
        console.error('Error loading routes:', error)
        this.errorMessage = 'Ошибка при загрузке списка маршрутов'
        this.showError = true
      } finally {
        this.loadingRoutes = false
      }
    },

    async fetchBuses() {
      try {
        const { data } = await api.get('/buses')
        this.buses = data
      } catch (error) {
        console.error('Error loading buses:', error)
        this.errorMessage = 'Ошибка при загрузке списка автобусов'
        this.showError = true
      } finally {
        this.loadingBuses = false
      }
    },

    formatRouteTime(route) {
      return `${route.start_time} - ${route.end_time}`
    },

    async handleSubmit() {
      if (!this.isValid) return

      this.saving = true
      try {
        await api.post('/assignments', this.form)
        this.$router.push('/assignments')
      } catch (error) {
        console.error('Error saving assignment:', error)
        this.errorMessage = error.response?.data?.detail || 'Ошибка при сохранении назначения'
        this.showError = true
      } finally {
        this.saving = false
      }
    }
  }
}
</script> 
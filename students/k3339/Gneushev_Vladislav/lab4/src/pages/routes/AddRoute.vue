<template>
  <page-wrapper>
    <v-card>
      <v-card-title>Добавление маршрута</v-card-title>
      
      <v-card-text>
        <v-form @submit.prevent="handleSubmit">
          <v-text-field
            v-model="form.name"
            label="Название маршрута"
            :rules="[v => !!v || 'Обязательное поле']"
            required
          ></v-text-field>

          <v-text-field
            v-model="form.start_point_name"
            label="Начальная точка"
            :rules="[v => !!v || 'Обязательное поле']"
            required
          ></v-text-field>

          <v-text-field
            v-model="form.end_point_name"
            label="Конечная точка"
            :rules="[v => !!v || 'Обязательное поле']"
            required
          ></v-text-field>

          <v-text-field
            v-model="form.start_time"
            label="Время начала работы"
            type="time"
            :rules="[v => !!v || 'Обязательное поле']"
            required
          ></v-text-field>

          <v-text-field
            v-model="form.end_time"
            label="Время окончания работы"
            type="time"
            :rules="[v => !!v || 'Обязательное поле']"
            required
          ></v-text-field>

          <v-text-field
            v-model.number="form.interval_seconds"
            label="Интервал (в секундах)"
            type="number"
            :rules="[
              v => !!v || 'Обязательное поле',
              v => v > 0 || 'Значение должно быть больше 0'
            ]"
            required
          ></v-text-field>

          <v-text-field
            v-model.number="form.duration_seconds"
            label="Длительность (в секундах)"
            type="number"
            :rules="[
              v => !!v || 'Обязательное поле',
              v => v > 0 || 'Значение должно быть больше 0'
            ]"
            required
          ></v-text-field>

          <v-text-field
            v-model.number="form.length_km"
            label="Длина маршрута (км)"
            type="number"
            :rules="[
              v => !!v || 'Обязательное поле',
              v => v > 0 || 'Значение должно быть больше 0'
            ]"
            required
          ></v-text-field>

          <div class="d-flex justify-end mt-4">
            <v-btn
              color="grey"
              variant="text"
              class="mr-2"
              to="/routes"
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
  name: 'AddRoute',
  
  components: {
    PageWrapper
  },

  data: () => ({
    form: {
      name: '',
      start_point_name: '',
      end_point_name: '',
      start_time: '',
      end_time: '',
      interval_seconds: null,
      duration_seconds: null,
      length_km: null
    },
    saving: false,
    showError: false,
    errorMessage: ''
  }),

  computed: {
    isValid() {
      return (
        this.form.name &&
        this.form.start_point_name &&
        this.form.end_point_name &&
        this.form.start_time &&
        this.form.end_time &&
        this.form.interval_seconds > 0 &&
        this.form.duration_seconds > 0 &&
        this.form.length_km > 0
      )
    }
  },

  methods: {
    async handleSubmit() {
      if (!this.isValid) return

      this.saving = true
      try {
        await api.post('/routes', this.form)
        this.$router.push('/routes')
      } catch (error) {
        console.error('Error saving route:', error)
        this.errorMessage = 'Ошибка при сохранении маршрута'
        this.showError = true
      } finally {
        this.saving = false
      }
    }
  }
}
</script> 
<template>
  <v-container>
    <v-row>
      <v-col>
        <v-card>
          <v-card-title>Добавление водителя</v-card-title>
          
          <v-card-text>
            <v-form @submit.prevent="handleSubmit" ref="form">
              <v-text-field
                v-model="form.first_name"
                label="Имя"
                :rules="[rules.required]"
                required
              ></v-text-field>

              <v-text-field
                v-model="form.last_name"
                label="Фамилия"
                :rules="[rules.required]"
                required
              ></v-text-field>

              <v-text-field
                v-model="form.passport_info"
                label="Паспортные данные"
                :rules="[rules.required]"
                required
              ></v-text-field>

              <v-select
                v-model="form.driver_class_name"
                :items="driverClasses"
                item-title="name"
                item-value="name"
                label="Класс водителя"
                :rules="[rules.required]"
                :loading="loadingClasses"
                required
              ></v-select>

              <v-text-field
                v-model.number="form.work_experience_months"
                label="Стаж работы (месяцев)"
                type="number"
                :rules="[rules.required, rules.positive]"
                required
              ></v-text-field>

              <v-btn
                color="primary"
                type="submit"
                block
                :loading="loading"
                class="mt-4"
              >
                Добавить водителя
              </v-btn>
            </v-form>
          </v-card-text>
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

export default {
  name: 'AddDriver',
  
  data: () => ({
    form: {
      first_name: '',
      last_name: '',
      passport_info: '',
      driver_class_name: '',
      work_experience_months: null
    },
    driverClasses: [],
    loading: false,
    loadingClasses: false,
    showError: false,
    errorMessage: '',
    rules: {
      required: v => !!v || 'Обязательное поле',
      positive: v => v > 0 || 'Значение должно быть больше 0'
    }
  }),

  async created() {
    await this.fetchDriverClasses()
  },

  methods: {
    async fetchDriverClasses() {
      this.loadingClasses = true
      try {
        const { data } = await api.get('/drivers/classes')
        this.driverClasses = data
      } catch (error) {
        this.errorMessage = 'Ошибка при загрузке классов водителей'
        this.showError = true
      } finally {
        this.loadingClasses = false
      }
    },

    async handleSubmit() {
      if (!this.$refs.form.validate()) return

      this.loading = true
      try {
        await api.post('/drivers', this.form)
        this.$router.push('/drivers')
      } catch (error) {
        this.errorMessage = 'Ошибка при добавлении водителя'
        this.showError = true
      } finally {
        this.loading = false
      }
    }
  }
}
</script> 
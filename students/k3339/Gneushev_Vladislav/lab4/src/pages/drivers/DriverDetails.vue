<template>
  <page-wrapper>
    <v-card>
      <v-card-title class="d-flex justify-space-between align-center">
        <span>Информация о водителе</span>
        <div>
          <v-btn
            color="primary"
            class="mr-2"
            :disabled="isEditing"
            @click="startEdit"
            v-if="!isEditing"
          >
            Редактировать
          </v-btn>
          <v-btn
            color="error"
            variant="text"
            @click="confirmDelete"
            :loading="deleting"
            :disabled="isEditing"
          >
            Удалить
          </v-btn>
        </div>
      </v-card-title>

      <v-card-text v-if="loading">
        <v-progress-circular indeterminate></v-progress-circular>
      </v-card-text>

      <v-card-text v-else-if="driver">
        <v-form
          v-model="isFormValid"
          @submit.prevent="saveChanges"
          validate-on="input"
          ref="form"
        >
          <v-row>
            <v-col cols="12" md="6">
              <v-list>
                <v-list-item>
                  <template v-if="!isEditing">
                    <v-list-item-title>ФИО</v-list-item-title>
                    <v-list-item-subtitle>
                      {{ driver.last_name }} {{ driver.first_name }}
                    </v-list-item-subtitle>
                  </template>
                  <template v-else>
                    <v-text-field
                      v-model="editForm.last_name"
                      label="Фамилия"
                      :rules="requiredRule"
                      validate-on="input"
                    ></v-text-field>
                    <v-text-field
                      v-model="editForm.first_name"
                      label="Имя"
                      :rules="requiredRule"
                      validate-on="input"
                    ></v-text-field>
                  </template>
                </v-list-item>

                <v-list-item>
                  <template v-if="!isEditing">
                    <v-list-item-title>Паспортные данные</v-list-item-title>
                    <v-list-item-subtitle>{{ driver.passport_info }}</v-list-item-subtitle>
                  </template>
                  <template v-else>
                    <v-text-field
                      v-model="editForm.passport_info"
                      label="Паспортные данные"
                      :rules="requiredRule"
                      validate-on="input"
                    ></v-text-field>
                  </template>
                </v-list-item>

                <v-list-item>
                  <template v-if="!isEditing">
                    <v-list-item-title>Стаж работы</v-list-item-title>
                    <v-list-item-subtitle>
                      {{ driver.work_experience_months }} месяцев
                    </v-list-item-subtitle>
                  </template>
                  <template v-else>
                    <v-text-field
                      v-model.number="editForm.work_experience_months"
                      label="Стаж работы (месяцев)"
                      type="number"
                      :rules="experienceRules"
                      validate-on="input"
                    ></v-text-field>
                  </template>
                </v-list-item>

                <v-list-item>
                  <template v-if="!isEditing">
                    <v-list-item-title>Класс водителя</v-list-item-title>
                    <v-list-item-subtitle>{{ driver.driver_class.name }}</v-list-item-subtitle>
                  </template>
                  <template v-else>
                    <v-select
                      v-model="editForm.driver_class_name"
                      :items="driverClasses"
                      item-title="name"
                      item-value="name"
                      label="Класс водителя"
                      :rules="requiredRule"
                      validate-on="input"
                    ></v-select>
                  </template>
                </v-list-item>

                <v-list-item v-if="driver.salary_rub">
                  <v-list-item-title>Зарплата</v-list-item-title>
                  <v-list-item-subtitle>{{ driver.salary_rub }} ₽</v-list-item-subtitle>
                </v-list-item>
              </v-list>

              <div v-if="isEditing" class="d-flex justify-end mt-4">
                <v-btn
                  color="grey"
                  variant="text"
                  class="mr-2"
                  @click="cancelEdit"
                >
                  Отмена
                </v-btn>
                <v-btn
                  color="primary"
                  :loading="saving"
                  :disabled="!isValidForm"
                  @click="saveChanges"
                >
                  Сохранить
                </v-btn>
              </div>
            </v-col>

            <v-col cols="12" md="6">
              <h3 class="text-h6 mb-4">График работы</h3>
              <v-list v-if="workSchedule">
                <template v-for="(day, name) in workSchedule" :key="name">
                  <v-list-item v-if="day">
                    <v-list-item-title>{{ getDayName(name) }}</v-list-item-title>
                    <v-list-item-subtitle>
                      {{ formatTime(day.start_time) }} - {{ formatTime(day.end_time) }}
                    </v-list-item-subtitle>
                  </v-list-item>
                </template>
              </v-list>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>

    <!-- Диалог подтверждения удаления -->
    <v-dialog v-model="showDeleteDialog" max-width="400">
      <v-card>
        <v-card-title>Подтверждение удаления</v-card-title>
        <v-card-text>
          Вы действительно хотите удалить этого водителя?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" variant="text" @click="showDeleteDialog = false">
            Отмена
          </v-btn>
          <v-btn color="error" variant="text" @click="deleteDriver">
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
  </page-wrapper>
</template>

<script>
import { api } from '@/services/api'
import PageWrapper from '@/components/PageWrapper.vue'

export default {
  name: 'DriverDetails',
  components: { PageWrapper },
  
  data: () => ({
    driver: null,
    workSchedule: null,
    loading: true,
    deleting: false,
    saving: false,
    showDeleteDialog: false,
    showError: false,
    errorMessage: '',
    driverClasses: [],
    loadingClasses: false,
    isEditing: false,
    isFormValid: true,
    editForm: {
      first_name: '',
      last_name: '',
      passport_info: '',
      driver_class_name: '',
      work_experience_months: null
    },
    requiredRule: [
      v => !!v || 'Обязательное поле'
    ],
    experienceRules: [
      v => !!v || 'Обязательное поле',
      v => v > 0 || 'Значение должно быть больше 0'
    ]
  }),

  async created() {
    await Promise.all([
      this.fetchDriver(),
      this.fetchDriverClasses(),
      this.fetchWorkSchedule()
    ])
  },

  computed: {
    isValidForm() {
      return (
        this.editForm.first_name?.length > 0 &&
        this.editForm.last_name?.length > 0 &&
        this.editForm.passport_info?.length > 0 &&
        this.editForm.driver_class_name?.length > 0 &&
        this.editForm.work_experience_months > 0
      )
    }
  },

  methods: {
    async fetchDriver() {
      try {
        const { data } = await api.get(`/drivers/${this.$route.params.id}`)
        this.driver = data
        this.initEditForm()
      } catch (error) {
        this.errorMessage = 'Ошибка при загрузке данных водителя'
        this.showError = true
      } finally {
        this.loading = false
      }
    },

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

    async fetchWorkSchedule() {
      try {
        const { data } = await api.get(`/drivers/${this.$route.params.id}/work_schedule`)
        this.workSchedule = data
      } catch (error) {
        this.errorMessage = 'Ошибка при загрузке графика работы'
        this.showError = true
      }
    },

    initEditForm() {
      this.editForm = {
        first_name: this.driver.first_name || '',
        last_name: this.driver.last_name || '',
        passport_info: this.driver.passport_info || '',
        driver_class_name: this.driver.driver_class.name || '',
        work_experience_months: this.driver.work_experience_months || 0
      }
    },

    startEdit() {
      this.isEditing = true
      this.initEditForm()
      this.isFormValid = false
    },

    cancelEdit() {
      this.isEditing = false
      this.initEditForm()
    },

    async saveChanges() {
      this.saving = true
      try {
        const { data } = await api.put(`/drivers/${this.driver.id}`, {
          first_name: this.editForm.first_name,
          last_name: this.editForm.last_name,
          passport_info: this.editForm.passport_info,
          driver_class_name: this.editForm.driver_class_name,
          work_experience_months: this.editForm.work_experience_months
        })
        this.driver = data
        this.isEditing = false
        this.initEditForm()
      } catch (error) {
        console.error('Error saving driver:', error)
        this.errorMessage = 'Ошибка при сохранении изменений'
        this.showError = true
      } finally {
        this.saving = false
      }
    },

    confirmDelete() {
      this.showDeleteDialog = true
    },

    async deleteDriver() {
      this.deleting = true
      try {
        await api.delete(`/drivers/${this.driver.id}`)
        this.$router.push('/drivers')
      } catch (error) {
        this.errorMessage = 'Ошибка при удалении водителя'
        this.showError = true
      } finally {
        this.deleting = false
        this.showDeleteDialog = false
      }
    },

    getDayName(day) {
      const days = {
        monday: 'Понедельник',
        tuesday: 'Вторник',
        wednesday: 'Среда',
        thursday: 'Четверг',
        friday: 'Пятница',
        saturday: 'Суббота',
        sunday: 'Воскресенье'
      }
      return days[day]
    },

    formatTime(time) {
      return time
    }
  }
}
</script> 
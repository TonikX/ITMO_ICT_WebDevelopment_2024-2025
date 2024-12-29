<template>
  <v-container>
    <h2 class="mb-4">Сотрудники</h2>
    <!-- Кнопка для открытия диалога создания сотрудника -->
    <v-btn
      variant="outlined"
      color="primary"
      class="mb-4"
      @click="openCreateDialog"
    >
      Нанять сотрудника
    </v-btn>

    <v-row>
      <v-col
        v-for="(person, index) in staff"
        :key="person.staff_id"
        cols="12"
        md="6"
        lg="4"
      >
        <v-card class="mb-4 elevated-card pa-2">
          <v-card-item>
            <div>
              <div class="text-h6">{{ person.last_name }} {{ person.first_name }} {{ person.middle_name }}</div>
              <div class="text-caption" v-if="person.middle_name">
                ID: {{ person.staff_id }}
              </div>
            </div>
          </v-card-item>
          <v-card-actions>
            <v-btn variant="outlined" color="primary" @click="editStaff(person)">
              Редактировать
            </v-btn>
            <v-btn variant="outlined" color="error" @click="deleteStaff(person.staff_id)">
              Удалить
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Диалог для редактирования/добавления -->
    <v-dialog
      v-model="dialog"
      max-width="600px"
      persistent
      >
      <v-card class="dialog-card pa-6">
        <v-card-title class="my-dialog-title dialog-title">
          {{ staffForm.staff_id ? 'Редактирование' : 'Новый' }} сотрудник
        </v-card-title>
        <v-card-text>
          <v-text-field v-model="staffForm.last_name" label="Фамилия" />
          <v-text-field v-model="staffForm.first_name" label="Имя" />
          <v-text-field v-model="staffForm.middle_name" label="Отчество" />
        </v-card-text>
        <v-card-actions>
          <v-btn variant="outlined" color="primary" @click="createOrUpdateStaff">
            Сохранить
          </v-btn>
          <v-btn variant="outlined" color="error" @click="dialog = false">
            Отмена
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Staff',
  data() {
    return {
      staff: [],
      dialog: false,
      staffForm: {
        staff_id: null,
        last_name: '',
        first_name: '',
        middle_name: ''
      }
    }
  },
  async created() {
    this.fetchStaff()
  },
  methods: {
    // Метод для получения списка сотрудников
    async fetchStaff() {
      const token = localStorage.getItem('token')
      try {
        const res = await axios.get('http://127.0.0.1:8000/api/staff/', {
          headers: { Authorization: `Token ${token}` }
        })
        this.staff = res.data
      } catch (error) {
        console.error(error)
      }
    },
    // Открытие диалога для создания нового сотрудника
    openCreateDialog() {
      this.clearForm()
      this.dialog = true
    },
    // Очистка формы
    clearForm() {
      this.staffForm = {
        staff_id: null,
        last_name: '',
        first_name: '',
        middle_name: ''
      }
    },
    // Открытие диалога для редактирования существующего сотрудника
    editStaff(person) {
      this.staffForm = { ...person }
      this.dialog = true
    },
    // Метод для создания или обновления сотрудника
    async createOrUpdateStaff() {
      const token = localStorage.getItem('token')
      try {
        if (this.staffForm.staff_id) {
          await axios.put(`http://127.0.0.1:8000/api/staff/${this.staffForm.staff_id}/`, this.staffForm, {
            headers: { Authorization: `Token ${token}` }
          })
        } else {
          await axios.post('http://127.0.0.1:8000/api/staff/', this.staffForm, {
            headers: { Authorization: `Token ${token}` }
          })
        }
        this.dialog = false
        this.fetchStaff()
      } catch (error) {
        console.error(error)
      }
    },
    // Метод для удаления сотрудника
    async deleteStaff(id) {
      const token = localStorage.getItem('token')
      try {
        await axios.delete(`http://127.0.0.1:8000/api/staff/${id}/`, {
          headers: { Authorization: `Token ${token}` }
        })
        this.fetchStaff()
      } catch (error) {
        console.error(error)
      }
    }
  }
}
</script>
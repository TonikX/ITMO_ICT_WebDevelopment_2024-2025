<template>
  <v-container>
    <v-card>
      <v-card-title class="d-flex align-center">
        Сотрудники
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="openDialogForCreate">Добавить сотрудника</v-btn>
      </v-card-title>
      <v-card-text>
        <v-data-table :headers="headers" :items="employees" class="elevation-1">
          <template #item.cleaning_assignments="{ item }">
            <div v-for="assignment in item.cleaning_assignments" :key="assignment.id">
              Убирает {{ assignment.floor_schedule.floor }} этаж в
              {{ formatDayOfWeek(assignment.floor_schedule.day_of_week) }}
            </div>
          </template>
          <template #item.actions="{ item, index }">
            <v-icon small class="mr-2" @click="openDialogForEdit(item, index)">mdi-pencil</v-icon>
            <v-icon small @click="openDeleteDialog(item, index)">mdi-delete</v-icon>

          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline">
            {{ isEditing ? 'Редактировать сотрудника' : 'Добавить сотрудника' }}
          </span>
        </v-card-title>
        <v-card-text>
          <v-form ref="employeeForm" v-model="formValid">
            <v-text-field
              label="Фамилия"
              v-model="editedEmployee.last_name"
              :rules="[v => !!v || 'Обязательно']"
            ></v-text-field>
            <v-text-field
              label="Имя"
              v-model="editedEmployee.first_name"
              :rules="[v => !!v || 'Обязательно']"
            ></v-text-field>
            <v-divider class="my-4"></v-divider>
            <div>
              <div class="d-flex justify-space-between align-center">
                <span>Расписание уборки</span>
                <v-btn text small color="primary" @click="addAssignment">
                  Добавить расписание
                </v-btn>
              </div>
              <div
                v-for="(assignment, aIndex) in editedEmployee.cleaning_assignments"
                :key="aIndex"
                class="d-flex align-center mb-2"
              >
                <v-select
                  :items="floors"
                  label="Этаж"
                  item-title="number"
                  item-value="number"
                  v-model="assignment.floor"
                  :rules="[v => v !== null && v !== undefined ? true : 'Обязательно']"
                  class="mr-2"
                />
                <v-select
                  :items="daysOfWeek"
                  label="День недели"
                  item-text="text"
                  item-value="value"
                  v-model="assignment.day_of_week"
                  :rules="[v => !!v || 'Обязательно']"
                  class="mr-2"
                ></v-select>
                <v-btn icon color="red" @click="removeAssignment(aIndex)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </div>
            </div>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" text @click="saveEmployee" :disabled="!formValid">
            Сохранить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title class="headline">
          Подтверждение удаления
        </v-card-title>
        <v-card-text>
          Вы уверены, что хотите удалить сотрудника
          <strong>
            {{
              employeeToDelete ? employeeToDelete.last_name + ' ' + employeeToDelete.first_name : ''
            }}
          </strong>?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="cancelDelete">Отмена</v-btn>
          <v-btn color="red" text @click="confirmDeleteEmployee">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Employees',
  data() {
    return {
      employees: [],
      floors: [
        {},
        {},
        {},

      ],
      headers: [
        {title: 'Фамилия', value: 'last_name', sortable: true},
        {title: 'Имя', value: 'first_name', sortable: true},
        {title: 'Расписание уборки', value: 'cleaning_assignments'},
        {title: 'Действия', value: 'actions', sortable: false}
      ],
      dialog: false,
      deleteDialog: false,
      isEditing: false,
      editedIndex: -1,
      employeeToDelete: null,
      employeeToDeleteIndex: -1,
      editedEmployee: {
        last_name: '',
        first_name: '',
        cleaning_assignments: []
      },
      daysOfWeek: [
        {title: 'Понедельник', value: 'Monday'},
        {title: 'Вторник', value: 'Tuesday'},
        {title: 'Среда', value: 'Wednesday'},
        {title: 'Четверг', value: 'Thursday'},
        {title: 'Пятница', value: 'Friday'},
        {title: 'Суббота', value: 'Saturday'},
        {title: 'Воскресенье', value: 'Sunday'}
      ],
      formValid: false
    }
  },
  methods: {
    formatDayOfWeek(value) {
      const types = {
        Monday: 'понедельник',
        Tuesday: 'вторник',
        Wednesday: 'среду',
        Thursday: 'четверг',
        Friday: 'пятницу',
        Saturday: 'субботу',
        Sunday: 'воскресенье'
      }
      return types[value] || 'Неизвестно'
    },
    fetchEmployees() {
      axios.get('http://localhost:8000/api/employees/')
        .then(response => {
          this.employees = response.data
        })
        .catch(error => {
          console.error(error)
        })
    },
    fetchFloors() {
      axios.get('http://localhost:8000/api/floors/')
        .then(response => {
          this.floors = response.data
        })
        .catch(error => {
          console.error(error)
        })
    },
    openDialogForCreate() {
      this.isEditing = false
      this.editedEmployee = {
        last_name: '',
        first_name: '',
        cleaning_assignments: []
      }
      this.dialog = true
    },
    openDialogForEdit(item, index) {
      this.isEditing = true
      this.editedEmployee = JSON.parse(JSON.stringify(item))
      this.editedIndex = index
      if (this.editedEmployee.cleaning_assignments) {
        this.editedEmployee.cleaning_assignments = this.editedEmployee.cleaning_assignments.map(a => ({
          floor: a.floor_schedule.floor,
          day_of_week: a.floor_schedule.day_of_week
        }))
      }
      this.dialog = true
    },
    closeDialog() {
      this.dialog = false
      if (this.$refs.employeeForm) {
        this.$refs.employeeForm.reset()
      }
    },
    addAssignment() {
      this.editedEmployee.cleaning_assignments.push({
        floor: null,
        day_of_week: ''
      })
    },
    removeAssignment(index) {
      this.editedEmployee.cleaning_assignments.splice(index, 1)
    },
    saveEmployee() {
      const payload = {
        last_name: this.editedEmployee.last_name,
        first_name: this.editedEmployee.first_name,
        cleaning_assignments: this.editedEmployee.cleaning_assignments.map(assignment => ({
          floor_schedule: {
            floor: assignment.floor,
            day_of_week: assignment.day_of_week
          }
        }))
      }
      if (this.isEditing) {
        axios.put(`http://localhost:8000/api/employees/${this.editedEmployee.id}`, payload)
          .then(response => {
            this.employees.splice(this.editedIndex, 1, response.data)
            this.dialog = false
          })
          .catch(error => {
            console.error(error)
          })
      } else {
        axios.post('http://localhost:8000/api/employees/', payload)
          .then(response => {
            this.employees.push(response.data)
            this.dialog = false
          })
          .catch(error => {
            console.error(error)
          })
      }
    },
    openDeleteDialog(item, index) {
      this.employeeToDelete = item
      this.employeeToDeleteIndex = index
      this.deleteDialog = true
    },
    cancelDelete() {
      this.deleteDialog = false
      this.employeeToDelete = null
      this.employeeToDeleteIndex = -1
    },
    confirmDeleteEmployee() {
      axios.delete(`http://localhost:8000/api/employees/${this.employeeToDelete.id}`)
        .then(() => {
          this.employees.splice(this.employeeToDeleteIndex, 1)
          this.cancelDelete()
        })
        .catch(error => {
          console.error(error)
        })
    }
  },
  created() {
    this.fetchEmployees()
    this.fetchFloors()
  }
}
</script>

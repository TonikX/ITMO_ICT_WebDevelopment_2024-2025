<template>
  <v-dialog
    :model-value="dialog"
    @update:model-value="emitDialogUpdate"
    max-width="600"
  >
    <v-card>
      <v-card-title>Редактирование информации о сотруднике</v-card-title>
      <v-card-text>
        <v-form ref="form">
          <v-text-field
            v-model="employee.first_name"
            label="Имя"
            required
          ></v-text-field>
          <v-text-field
            v-model="employee.last_name"
            label="Фамилия"
            required
          ></v-text-field>
          <v-text-field
            v-model="employee.age"
            label="Возраст"
            type="number"
            required
          ></v-text-field>
          <v-text-field
            v-model="employee.education"
            label="Образование"
            required
          ></v-text-field>
          <v-text-field
            v-model="employee.work_experience_years"
            label="Опыт работы (лет)"
            type="number"
            required
          ></v-text-field>
          <v-text-field
            v-model="employee.passport_data"
            label="Паспортные данные"
            required
          ></v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn variant="text" @click="closeDialog">Отмена</v-btn>
        <v-btn color="primary" @click="updateEmployee">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: {
    dialog: {
      type: Boolean,
      required: true,
    },
    employee: {
      type: Object,
      required: true,
    },
  },
  emits: ['update:dialog', 'employees-updated'],
  methods: {
    emitDialogUpdate(value) {
      this.$emit('update:dialog', value);
    },
    closeDialog() {
      this.$emit('update:dialog', false);
    },
    async updateEmployee() {
      if (
        !this.employee.first_name ||
        !this.employee.last_name ||
        !this.employee.age ||
        !this.employee.education ||
        !this.employee.work_experience_years ||
        !this.employee.passport_data
      ) {
        alert('Заполните все поля');
        return;
      }

      try {
        this.$emit('employees-updated', { ...this.employee });
        this.closeDialog();
      } catch (error) {
        console.error('Ошибка изменения сотрудника:', error);
        alert('Ошибка изменения сотрудника');
      }
    },
  },
};
</script>

<style>
.v-card-title {
  font-weight: bold;
}
</style>

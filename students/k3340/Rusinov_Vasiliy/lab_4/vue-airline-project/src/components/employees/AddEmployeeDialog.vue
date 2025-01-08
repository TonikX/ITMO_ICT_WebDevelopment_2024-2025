<template>
  <v-dialog
    :model-value="dialog"
    @update:model-value="emitDialogUpdate"
    max-width="500"
  >
    <v-card>
      <v-card-title>Добавление нового сотрудника</v-card-title>
      <v-card-text>
        <v-form ref="form">
          <v-text-field
            v-model="newEmployee.first_name"
            label="Имя"
            required
          ></v-text-field>

          <v-text-field
            v-model="newEmployee.last_name"
            label="Фамилия"
            required
          ></v-text-field>

          <v-text-field
            v-model="newEmployee.age"
            label="Возраст"
            type="number"
            required
          ></v-text-field>

          <v-text-field
            v-model="newEmployee.education"
            label="Образование"
            required
          ></v-text-field>

          <v-text-field
            v-model="newEmployee.work_experience_years"
            label="Опыт работы (лет)"
            type="number"
            required
          ></v-text-field>

          <v-text-field
            v-model="newEmployee.passport_data"
            label="Паспортные данные"
            required
          ></v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn variant="text" @click="closeDialog">Отмена</v-btn>
        <v-btn color="primary" @click="createEmployee">Сохранить</v-btn>
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
  },
  emits: ["update:dialog", "employees-added"],

  data() {
    return {
      newEmployee: {
        first_name: "",
        last_name: "",
        age: null,
        education: "",
        work_experience_years: null,
        passport_data: "",
      },
    };
  },

  methods: {
    emitDialogUpdate(value) {
      this.$emit("update:dialog", value);
    },

    closeDialog() {
      this.$emit("update:dialog", false);
      this.resetForm();
    },

    resetForm() {
      this.newEmployee = {
        first_name: "",
        last_name: "",
        age: null,
        education: "",
        work_experience_years: null,
        passport_data: "",
      };
    },

    createEmployee() {
      const { first_name, last_name, age, education, work_experience_years, passport_data } =
        this.newEmployee;

      if (!first_name || !last_name || !age || !education || !work_experience_years || !passport_data) {
        alert("Заполните все поля");
        return;
      }

      this.$emit("employees-added", { ...this.newEmployee });
      this.closeDialog();
    },
  },

  watch: {
    dialog(val) {
      if (!val) this.resetForm();
    },
  },
};
</script>


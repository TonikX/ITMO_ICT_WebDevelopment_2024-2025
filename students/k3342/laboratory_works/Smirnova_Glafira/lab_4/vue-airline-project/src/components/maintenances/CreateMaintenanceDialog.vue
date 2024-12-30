<template>
  <v-dialog
    :model-value="dialog"
    @update:model-value="emitDialogUpdate"
    max-width="600"
  >
    <v-card>
      <v-card-title>Добавление нового ремонта</v-card-title>
      <v-card-text>
        <v-form ref="form">
          <v-select
            v-model="newMaintenance.plane"
            :items="choices.planes"
            label="Самолет"
            item-value="id"
            item-title="name"
            :error-messages="errors.plane || []"
            @update:model-value="clearFieldError('plane')"
            required
          />
          <v-text-field
            v-model="newMaintenance.start_date"
            label="Дата начала"
            type="datetime-local"
            :error-messages="errors.start_date || []"
            @input="clearFieldError('start_date')"
            required
          />
          <v-text-field
            v-model="newMaintenance.end_date"
            label="Дата завершения"
            type="datetime-local"
            :error-messages="errors.end_date || []"
            @input="clearFieldError('end_date')"
          />
          <v-select
            v-model="newMaintenance.status"
            :items="choices.statuses"
            label="Статус"
            item-value="value"
            item-title="label"
            :error-messages="errors.status || []"
            @update:model-value="clearFieldError('status')"
            required
          />
          <v-textarea
            v-model="newMaintenance.description"
            label="Описание"
            :error-messages="errors.description || []"
            @input="clearFieldError('description')"
            required
          />
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="closeDialog">Отмена</v-btn>
        <v-btn color="primary" @click="createMaintenance">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: {
    dialog: { type: Boolean, required: true },
    choices: { type: Object, required: true },
  },
  emits: ["update:dialog", "maintenance-created"],
  data() {
    return {
      newMaintenance: {
        plane: null,
        start_date: "",
        end_date: "",
        status: null,
        description: "",
      },
      errors: {},
    };
  },
  methods: {
    setErrors(serverErrors) {
      this.errors = serverErrors;
    },
    emitDialogUpdate(value) {
      this.$emit("update:dialog", value);
    },
    closeDialog() {
      this.$emit("update:dialog", false);
      this.resetForm();
    },
    resetForm() {
      this.newMaintenance = {
        plane: null,
        start_date: "",
        end_date: "",
        status: null,
        description: "",
      };
      this.errors = {};
    },
    clearFieldError(fieldName) {
      if (this.errors[fieldName]) {
        delete this.errors[fieldName];
      }
    },
    async createMaintenance() {
      if (
        !this.newMaintenance.plane ||
        !this.newMaintenance.start_date ||
        !this.newMaintenance.status ||
        !this.newMaintenance.description
      ) {
        alert("Заполните все обязательные поля!");
        return;
      }
      try {
        await this.$emit("maintenance-created", { ...this.newMaintenance });
      } catch (error) {
        if (error.response && error.response.data) {
          this.errors = error.response.data;
        }
      }
    },
  },
};
</script>

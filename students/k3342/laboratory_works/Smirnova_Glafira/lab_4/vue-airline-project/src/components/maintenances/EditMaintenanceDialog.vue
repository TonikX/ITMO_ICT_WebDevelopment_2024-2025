<template>
  <v-dialog
    :model-value="dialog"
    @update:model-value="emitDialogUpdate"
    max-width="600"
  >
    <v-card>
      <v-card-title>Редактирование ремонта</v-card-title>
      <v-card-text>
        <v-form ref="form">
          <v-textarea
            v-model="maintenance.description"
            label="Описание ремонта"
            :error-messages="errors.description || []"
            @input="clearFieldError('description')"
            required
          />
          <v-text-field
            v-model="maintenance.start_date"
            label="Дата начала"
            type="datetime-local"
            :error-messages="errors.start_date || []"
            @input="clearFieldError('start_date')"
            required
          />
          <v-text-field
            v-model="maintenance.end_date"
            label="Дата завершения"
            type="datetime-local"
            :error-messages="errors.end_date || []"
            @input="clearFieldError('end_date')"
          />
          <v-select
            v-model="maintenance.status"
            :items="choices.statuses"
            label="Статус"
            item-value="value"
            item-title="label"
            :error-messages="errors.status || []"
            @update:model-value="clearFieldError('status')"
            required
          />
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="closeDialog">Отмена</v-btn>
        <v-btn color="primary" @click="updateMaintenance">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: {
    dialog: { type: Boolean, required: true },
    choices: { type: Object, required: true },
    initialMaintenance: { type: Object, required: true },
  },
  emits: ["update:dialog", "maintenance-updated"],
  data() {
    return {
      maintenance: { ...this.initialMaintenance,
      start_date: this.formatDateTime(this.initialMaintenance.start_date),
      end_date: this.formatDateTime(this.initialMaintenance.end_date),},
      errors: {},
    };
  },
  watch: {
    dialog(val) {
      if (val) {
        this.initializeMaintenance();
      }
    },
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
      this.maintenance = { ...this.initialMaintenance };
      this.errors = {};
      console.log()
    },
    clearFieldError(fieldName) {
      if (this.errors[fieldName]) {
        delete this.errors[fieldName];
      }
    },
    initializeMaintenance() {
      this.maintenance = {
        ...this.initialMaintenance,
        start_date: this.formatDateTime(this.initialMaintenance.start_date),
        end_date: this.formatDateTime(this.initialMaintenance.end_date),
      };
    },
    async updateMaintenance() {
      try {
        const updatedMaintenance = {
          ...this.maintenance,
          start_date: this.unformatDateTime(this.maintenance.start_date),
          end_date: this.unformatDateTime(this.maintenance.end_date),
        };
        delete updatedMaintenance.plane;

        this.maintenance.id = this.initialMaintenance.id

        await this.$emit("maintenance-updated", updatedMaintenance);
      } catch (error) {
        console.error("Ошибка обновления ремонта:", error.response?.data || error.message);
        if (error.response && error.response.data) {
          this.errors = error.response.data;
        }
      }
    },
    formatDateTime(datetime) {
    if (!datetime) return "";
    const date = new Date(datetime);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");
    return `${year}-${month}-${day}T${hours}:${minutes}`;
  },
    unformatDateTime(formattedDateTime) {
    return new Date(formattedDateTime).toISOString();
  },
  },
};
</script>

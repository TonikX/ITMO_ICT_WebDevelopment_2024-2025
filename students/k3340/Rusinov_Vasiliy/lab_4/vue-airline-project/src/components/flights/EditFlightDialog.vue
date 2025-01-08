<template>
  <v-dialog
    :model-value="dialog"
    @update:model-value="emitDialogUpdate"
    max-width="600"
  >
    <v-card>
      <v-card-title>Редактирование перелета</v-card-title>
      <v-card-text>
        <v-form ref="form">
          <v-text-field
            v-model="flight.number"
            label="Номер перелета"
            :error-messages="errors.number || []"
            @input="clearFieldError('number')"
            required
          />

          <v-text-field
            v-model="flight.departure_date"
            label="Дата вылета"
            type="date"
            :error-messages="errors.departure_date || []"
            @input="clearFieldError('departure_date')"
            required
          />
          <v-select
            v-model="flight.status"
            :items="choices.status_choices"
            label="Статус"
            item-value="id"
            item-title="name"
            required
          />
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="closeDialog">Отмена</v-btn>
        <v-btn color="primary" @click="updateFlight">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  props: {
    dialog: { type: Boolean, required: true },
    choices: { type: Object, required: true },
    initialFlight: { type: Object, required: true },
  },
  emits: ["update:dialog", "flight-updated"],
  data() {
    return {
      flight: { ...this.initialFlight },
      errors: {},
    };
  },
  watch: {
    dialog(val) {
      if (val) {
        this.initializeFlight();
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
      this.flight = {...this.initialFlight};
      this.errors = {};
    },
    clearFieldError(fieldName) {
      if (this.errors[fieldName]) {
        delete this.errors[fieldName];
      }
    },
    initializeFlight() {
      this.flight = {...this.initialFlight};
    },
    async updateFlight() {
      try {
        console.log(this.flight)
        const updatedFlight = {
          ...this.flight,
          plane: this.flight.plane.id,
          crew: this.flight.crew.id,
        };

        await this.$emit("flight-updated", updatedFlight);
      } catch (error) {
        console.error("Ошибка обновления перелета:", error.response?.data || error.message);
        if (error.response && error.response.data) {
          this.errors = error.response.data;
        }
      }
    },
  },
};
</script>

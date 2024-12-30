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
            @input="updateField('number')"
            required
          />

                    <v-select
            v-model="flight.plane"
            :items="choices.plane_choices"
            label="Самолет"
            item-value="id"
            item-title="plane_str"
            :error-messages="errors.plane || []"
            @update:model-value="updateField('plane')"
            required
          />
          <v-select
            v-model="flight.crew"
            :items="choices.crew_choices"
            label="Экипаж"
            item-value="id"
            item-title="name"
            :error-messages="errors.crew || []"
            @update:model-value="updateField('crew')"
            required
          />

          <v-text-field
            v-model="flight.departure_date"
            label="Дата вылета"
            type="date"
            :error-messages="errors.departure_date || []"
            @input="updateField('departure_date')"
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
      flight: {},
      errors: {},
      updatedFlight: {}
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
      this.errors = {};
    },
    updateField(fieldName) {
      if (this.errors[fieldName]) {
        delete this.errors[fieldName];
      }
       if (fieldName === 'crew') {
        this.updatedFlight['crew'] = this.flight.crew;
      } else if (fieldName === 'plane') {
        this.updatedFlight['plane'] = this.flight.plane;
      }
    },
    initializeFlight() {
      this.flight = {...this.initialFlight};
    },
    async updateFlight() {
      try {
        console.log(this.flight)

        this.updatedFlight.departure_date = this.flight.departure_date
        this.updatedFlight.status = this.flight.status
        this.updatedFlight.number = this.flight.number

        console.log("sending to update", this.updatedFlight)

        await this.$emit("flight-updated", this.updatedFlight);
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

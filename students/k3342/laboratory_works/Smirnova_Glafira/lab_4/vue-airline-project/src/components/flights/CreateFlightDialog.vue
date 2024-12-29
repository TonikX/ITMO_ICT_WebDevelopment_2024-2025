<template>
  <v-dialog
    :model-value="dialog"
    @update:model-value="emitDialogUpdate"
    max-width="600"
  >
    <v-card>
      <v-card-title>Добавление нового перелета</v-card-title>
      <v-card-text>
        <v-form ref="form">
          <v-text-field v-model="newFlight.number" label="Номер перелета"
                        :error-messages="errors.number || []" @input="clearFieldError('number')" required />
          <v-select
            v-model="newFlight.route"
            :items="choices.route_choices"
            label="Маршрут"
            item-value="id"
            item-title="name"
            :error-messages="errors.route || []"
            @update:model-value="clearFieldError('route')"
            required
          />
          <v-select
            v-model="newFlight.plane"
            :items="choices.plane_choices"
            label="Самолет"
            item-value="id"
            item-title="plane_str"
            :error-messages="errors.plane || []"
            @update:model-value="clearFieldError('plane')"
            required
          />
          <v-select
            v-model="newFlight.crew"
            :items="choices.crew_choices"
            label="Экипаж"
            item-value="id"
            item-title="name"
            :error-messages="errors.crew || []"
            @update:model-value="clearFieldError('crew')"
            required
          />
          <v-text-field v-model="newFlight.departure_date" label="Дата вылета" type="date"
                        :error-messages="errors.departure_date || []" @input="clearFieldError('departure_date')" required />
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="closeDialog">Отмена</v-btn>
        <v-btn color="primary" @click="createFlight">Сохранить</v-btn>
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
  emits: ["update:dialog", "flight-created"],
  data() {
    return {
      newFlight: {
        number: "",
        route: null,
        plane: null,
        crew: null,
        departure_date: "",
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
        this.newFlight = {
          number: "",
          route: null,
          plane: null,
          crew: null,
          departure_date: "",
        };
      this.errors = {};
    },
    clearFieldError(fieldName) {
      console.log("deleting error", fieldName)
      if (this.errors[fieldName]) {
        delete this.errors[fieldName];
      }
    },
    async createFlight() {
      console.log(this.newFlight)
      if (
        !this.newFlight.number ||
        !this.newFlight.route ||
        !this.newFlight.plane ||
        !this.newFlight.crew ||
        !this.newFlight.departure_date
      ) {
        alert("Заполните все поля!");
        return;
      }
       try {
      await this.$emit("flight-created", { ...this.newFlight });
    } catch (error) {
      console.error("Ошибка создания перелета:", error.response?.data || error.message);

      if (error.response && error.response.data) {
        this.errors = error.response.data;
      }
    }
  },
  },
};
</script>

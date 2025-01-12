<!-- AddFlight.vue (модальное окно) -->
<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3>{{ flight ? 'Редактировать рейс' : 'Добавить рейс' }}</h3>
      <form @submit.prevent="saveFlight">
        <label for="flight_number">Номер рейса</label>
        <input type="number" v-model="form.flight_number" required />

        <label for="departure_date">Дата и время вылета</label>
        <input type="datetime-local" v-model="form.departure_date" required />

        <label for="arrival_date">Дата и время прилета</label>
        <input type="datetime-local" v-model="form.arrival_date" required />

        <label for="status">Статус</label>
        <input type="text" v-model="form.status" required />

        <label for="onBoard_number">Номер борта</label>
        <input type="text" v-model="form.onBoard_number" required />

        <label for="schedule_number">Номер расписания</label>
        <input type="text" v-model="form.schedule_number" required />

        <button type="submit">{{ flight ? 'Обновить рейс' : 'Добавить рейс' }}</button>
        <button type="button" @click="close">Закрыть</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  props: ['flight'],
  data() {
    return {
      form: {
        flight_number: this.flight ? this.flight.flight_number : "",
        departure_date: this.flight ? this.flight.departure_date : "",
        arrival_date: this.flight ? this.flight.arrival_date : "",
        status: this.flight ? this.flight.status : "",
        onBoard_number: this.flight ? this.flight.onBoard_number : "",
        schedule_number: this.flight ? this.flight.schedule_number : "",
      },
    };
  },
  methods: {
    saveFlight() {
      this.$emit("save", this.form);
    },
    close() {
      this.$emit("close");
    },
  },
};
</script>

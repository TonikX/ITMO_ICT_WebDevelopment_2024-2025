<template>
  <div class="modal fade show d-block" tabindex="-1" role="dialog" aria-labelledby="addIncidentModalLabel" aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="addIncidentModalLabel">Добавить инцидент</h5>
          <button type="button" class="close" @click="closeModal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <div class="form-group">
              <label for="schedule">Расписание</label>
              <select id="schedule" class="form-control" v-model="newIncident.schedule" required>
                <option v-for="schedule in schedules" :key="schedule.id" :value="schedule.id">
                  {{ schedule.driver }} - {{ schedule.bus }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label for="incident_date">Дата инцидента</label>
              <input
                type="date"
                id="incident_date"
                class="form-control"
                v-model="newIncident.incident_date"
                required
              />
            </div>
            <div class="form-group">
              <label for="reason">Причина</label>
              <textarea
                id="reason"
                class="form-control"
                v-model="newIncident.reason"
                required
              ></textarea>
            </div>
          </form>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="closeModal">Закрыть</button>
          <button type="submit" class="btn btn-primary" @click="handleSubmit">Добавить инцидент</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    schedules: Array,
  },
  data() {
    return {
      newIncident: {
        schedule: '',
        incident_date: '',
        reason: '',
      },
    };
  },
  methods: {
    handleSubmit() {
      this.$emit('save', { ...this.newIncident });
      this.newIncident = {
        schedule: '',
        incident_date: '',
        reason: '',
      };
      this.closeModal();
    },
    closeModal() {
      this.$emit('close');
    },
  },
};
</script>

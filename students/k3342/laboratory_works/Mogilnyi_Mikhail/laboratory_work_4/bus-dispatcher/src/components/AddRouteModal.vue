<template>
  <div class="modal">
    <div class="modal-content">
      <h2>{{ schedule ? 'Edit Schedule' : 'Create Schedule' }}</h2>
      <form @submit.prevent="submitForm">
        <div>
          <label for="driver">Driver:</label>
          <select id="driver" v-model="form.driver" required>
            <option v-for="driver in drivers" :key="driver.id" :value="driver.id">
              {{ driver.name }}
            </option>
          </select>
        </div>

        <div>
          <label for="bus">Bus:</label>
          <select id="bus" v-model="form.bus" required>
            <option v-for="bus in buses" :key="bus.id" :value="bus.id">
              {{ bus.registration_number }}
            </option>
          </select>
        </div>

        <div>
          <label for="route">Route:</label>
          <select id="route" v-model="form.route" required>
            <option v-for="route in routes" :key="route.id" :value="route.id">
              {{ route.route_number }}
            </option>
          </select>
        </div>

        <div>
          <label for="status">Status:</label>
          <input
            id="status"
            v-model="form.status"
            required
            placeholder="Status"
          />
        </div>

        <button type="submit">{{ schedule ? 'Update' : 'Create' }}</button>
        <button type="button" @click="$emit('close')">Cancel</button>
      </form>
    </div>
  </div>
</template>

<script>
import { createSchedule, updateSchedule, getDrivers, getBuses, getRoutes } from '@/api/schedule.js';

export default {
  props: ['schedule'],
  data() {
    return {
      form: {
        driver: '',
        bus: '',
        route: '',
        status: '',
      },
      drivers: [],
      buses: [],
      routes: [],
    };
  },
  methods: {
    async fetchData() {
      try {
        const [driversResponse, busesResponse, routesResponse] = await Promise.all([
          getDrivers(),
          getBuses(),
          getRoutes(),
        ]);

        this.drivers = driversResponse.data;
        this.buses = busesResponse.data;
        this.routes = routesResponse.data;

        if (this.schedule) {
          this.form.driver = this.schedule.driver.id;
          this.form.bus = this.schedule.bus.id;
          this.form.route = this.schedule.route.id;
          this.form.status = this.schedule.status;
        }
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    async submitForm() {
      try {
        if (this.schedule) {
          await updateSchedule(this.schedule.id, this.form);
          alert('Schedule updated successfully!');
        } else {
          await createSchedule(this.form);
          alert('Schedule created successfully!');
        }
        this.$emit('save');
      } catch (error) {
        console.error('Error saving schedule:', error);
        alert('An error occurred while saving the schedule.');
      }
    },
  },
  created() {
    this.fetchData();
  },
};
</script>

<style>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
}
</style>

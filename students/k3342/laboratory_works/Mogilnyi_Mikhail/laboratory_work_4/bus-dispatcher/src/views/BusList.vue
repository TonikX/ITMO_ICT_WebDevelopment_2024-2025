<template>
  <div>
    <Navbar />

    <div class="container mt-5">
      <h1>Список автобусов</h1>
      <button class="btn btn-primary mb-3" @click="showAddBusModal">Добавить автобус</button>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>№</th>
            <th>Регистрационный номер</th>
            <th>Класс</th>
            <th>Вместимость</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(bus, index) in buses" :key="bus.registration_number">
            <td>{{ index + 1 }}</td>
            <td>
              <a href="#" @click.prevent="viewBusDetails(bus)">
                {{ bus.registration_number }}
              </a>
            </td>
            <td>{{ busTypeChoices[bus.bus_type] || bus.bus_type }}</td>
            <td>{{ bus.capacity }}</td>
            <td>
              <div class="button-group">
                <button class="btn btn-warning btn-sm action-button" @click="editBus(bus)">Редактировать</button>
                <button class="btn btn-danger btn-sm action-button" @click="removeBus(bus.registration_number)">Удалить</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <AddBusModal
        v-if="showAddBusModalFlag"
        :busTypeChoices="busTypeChoices"
        :newBus="newBus"
        @add-bus="addNewBus"
        @close="closeAddBusModal"
      />
    </div>

    <Footer />
  </div>
</template>

<script>
import AddBusModal from '@/components/AddBusModal.vue';
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import { fetchBuses, addBus, deleteBus } from '@/api/bus';

export default {
  components: {
    AddBusModal,
    Navbar,
    Footer,
  },
  data() {
    return {
      buses: [],
      newBus: {
        registration_number: '',
        bus_type: '',
        capacity: null,
      },
      busTypeChoices: {
        mb: 'Minibus',
        nb: 'Normal Bus',
        dd: 'Double-Decker',
        eb: 'Electric Bus',
      },
      showAddBusModalFlag: false,
    };
  },
  methods: {
    async loadBuses() {
      try {
        this.buses = await fetchBuses();
      } catch (error) {
        alert('Не удалось загрузить список автобусов.');
      }
    },
    async addNewBus(newBus) {
      try {
        await addBus(newBus);
        alert('Автобус успешно добавлен');
        this.loadBuses();
        this.newBus = { registration_number: '', bus_type: '', capacity: null };
        this.closeAddBusModal();
      } catch (error) {
        alert('Не удалось добавить автобус.');
      }
    },
    async removeBus(registration_number) {
      try {
        await deleteBus(registration_number);
        alert('Автобус успешно удален');
        this.loadBuses();
      } catch (error) {
        alert('Не удалось удалить автобус.');
      }
    },
    showAddBusModal() {
      this.showAddBusModalFlag = true;
    },
    closeAddBusModal() {
      this.showAddBusModalFlag = false;
    },
    editBus(bus) {
      this.$router.push({ name: 'BusDetails', params: { id: bus.registration_number } });
    },
    viewBusDetails(bus) {
      this.$router.push({ name: 'BusDetails', params: { id: bus.registration_number } });
    },
  },
  mounted() {
    this.loadBuses();
  },
};
</script>

<style scoped>
h1 {
  margin-bottom: 20px;
}

.table {
  margin-top: 20px;
}

a {
  color: #007bff;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

.button-group button {
  margin-right: 10px;
}
</style>

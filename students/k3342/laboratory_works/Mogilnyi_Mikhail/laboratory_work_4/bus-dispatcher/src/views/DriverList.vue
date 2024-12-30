<template>
  <div>
    <Navbar />

    <div class="container mt-5">
      <h1>Список водителей</h1>
      <button class="btn btn-primary mb-3" @click="showAddDriverModal">Добавить водителя</button>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>Имя</th>
            <th>Паспортный номер</th>
            <th>Класс водителя</th>
            <th>Опыт (лет)</th>
            <th>Зарплата</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="driver in drivers" :key="driver.passport_number">
            <td>{{ driver.name }}</td>
            <td>{{ driver.passport_number }}</td>
            <td>{{ driver.driver_class }}</td>
            <td>{{ driver.experience_years }}</td>
            <td>{{ driver.salary }}</td>
            <td>
              <div class="button-group">
                <button class="btn btn-warning btn-sm action-button" @click="editDriver(driver.passport_number)">Редактировать</button>
                <button class="btn btn-danger btn-sm action-button" @click="removeDriver(driver.passport_number)">Удалить</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <AddDriverModal v-if="showAddDriverModalFlag" @close="closeAddDriverModal" @add-driver="addNewDriver" />

    <Footer />
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import AddDriverModal from '@/components/AddDriverModal.vue';
import { fetchDrivers, addDriver, deleteDriver } from '@/api/driver';

export default {
  components: {
    Navbar,
    Footer,
    AddDriverModal,
  },
  data() {
    return {
      drivers: [],
      showAddDriverModalFlag: false,
    };
  },
  methods: {
    async loadDrivers() {
      try {
        this.drivers = await fetchDrivers();
      } catch (error) {
        alert('Не удалось загрузить список водителей.');
      }
    },
    async addNewDriver(newDriver) {
      try {
        await addDriver(newDriver);
        alert('Водитель успешно добавлен');
        this.loadDrivers();
        this.closeAddDriverModal();
      } catch (error) {
        alert('Не удалось добавить водителя.');
      }
    },
    async removeDriver(passport_number) {
      try {
        await deleteDriver(passport_number);
        alert('Водитель успешно удален');
        this.loadDrivers();
      } catch (error) {
        alert('Не удалось удалить водителя.');
      }
    },
    showAddDriverModal() {
      this.showAddDriverModalFlag = true;
    },
    closeAddDriverModal() {
      this.showAddDriverModalFlag = false;
    },
    editDriver(passport_number) {
      this.$router.push({ name: 'DriverDetails', params: { id: passport_number } });
    },
  },
  mounted() {
    this.loadDrivers();
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

.button-group button {
  margin-right: 10px;
}
</style>

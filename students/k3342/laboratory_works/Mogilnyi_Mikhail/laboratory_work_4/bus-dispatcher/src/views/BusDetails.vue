<template>
  <div>
    <Navbar />
    <div class="container mt-5">
      <h2>Информация об автобусе</h2>
      <form @submit.prevent="updateBus">
        <div class="form-group">
          <label>Регистрационный номер</label>
          <input type="text" class="form-control" v-model="bus.registration_number" readonly />
        </div>
        <div class="form-group">
          <label>Класс</label>
          <select class="form-control" v-model="bus.bus_type">
            <option v-for="(name, code) in busTypeChoices" :key="code" :value="code">
              {{ name }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label>Вместимость</label>
          <input type="number" class="form-control" v-model="bus.capacity" min="1" required />
        </div>
        <button type="submit" class="btn btn-primary mt-3">Сохранить изменения</button>
      </form>
    </div>
    <Footer />
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue';
import Footer from '@/components/Footer.vue';
import { fetchBus, updateBus } from '@/api/bus';  // Импортируем методы из API

export default {
  components: {
    Navbar,
    Footer,
  },
  data() {
    return {
      bus: {
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
    };
  },
  methods: {
    async fetchBusDetails() {
      try {
        // Используем API метод fetchBus для получения данных
        const response = await fetchBus(this.$route.params.id);
        this.bus = response;
      } catch (error) {
        console.error(error);
        alert('Не удалось загрузить данные автобуса.');
      }
    },
    async updateBus() {
      // Валидация данных перед отправкой
      if (!this.bus.capacity || this.bus.capacity <= 0) {
        alert('Вместимость должна быть больше 0');
        return;
      }

      try {
        // Используем API метод updateBus для обновления данных
        await updateBus(this.bus);
        alert('Изменения сохранены');
        this.$router.push({name: 'busList'}); // Редирект на страницу с автобусами
      } catch (error) {
        console.error(error);
        alert('Не удалось сохранить изменения.');
      }
    },
  },
  mounted() {
    this.fetchBusDetails();
  },
};
</script>

<style scoped>
h2 {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

button {
  width: 100%;
}
</style>

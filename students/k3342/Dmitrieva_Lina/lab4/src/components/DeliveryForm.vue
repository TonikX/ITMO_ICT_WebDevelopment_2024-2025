<template>
  <div class="delivery-form">
    <h3>{{ delivery.id ? "Редактировать доставку" : "Добавить доставку" }}</h3>
    <form @submit.prevent="handleSubmit">
      <!-- Выбор газеты -->
      <div>
        <label for="newspaper">Газета:</label>
        <select v-model="formData.newspaper" id="newspaper" required>
          <option value="" disabled>Выберите газету</option>
          <option v-for="newspaper in newspapers" :key="newspaper.id" :value="newspaper.id">
            {{ newspaper.name }}
          </option>
        </select>
      </div>

      <!-- Выбор типографии -->
      <div>
        <label for="printshop">Типография:</label>
        <select v-model="formData.printshop" id="printshop" required>
          <option value="" disabled>Выберите типографию</option>
          <option v-for="printshop in printshops" :key="printshop.id" :value="printshop.id">
            {{ printshop.name }}
          </option>
        </select>
      </div>

      <!-- Выбор почтового отделения -->
      <div>
        <label for="post_office">Почтовое отделение:</label>
        <select v-model="formData.post_office" id="post_office" required>
          <option value="" disabled>Выберите почтовое отделение</option>
          <option v-for="postOffice in postOffices" :key="postOffice.id" :value="postOffice.id">
            {{ postOffice.number }} - {{ postOffice.address }}
          </option>
        </select>
      </div>

      <!-- Количество -->
      <div>
        <label for="quantity">Количество:</label>
        <input
          v-model="formData.quantity"
          id="quantity"
          type="number"
          min="1"
          placeholder="Введите количество"
          required
        />
      </div>

      <!-- Дата доставки -->
      <div>
        <label for="delivery_date">Дата доставки:</label>
        <input
          v-model="formData.delivery_date"
          id="delivery_date"
          type="date"
          required
        />
      </div>

      <!-- Статус -->
      <div>
        <label for="status">Статус:</label>
        <select v-model="formData.status" id="status" required>
          <option value="pending">Ожидается</option>
          <option value="completed">Доставлено</option>
        </select>
      </div>

      <!-- Кнопки -->
      <button type="submit">Сохранить</button>
      <button type="button" @click="cancel">Отмена</button>
    </form>
  </div>
</template>

<script>
import { getNewspapers, getPrintShops, getPostalOffices } from "../api/api";

export default {
  props: {
    delivery: {
      type: Object,
      default: () => ({}),
    },
  },
  data() {
    return {
      formData: {
        ...this.delivery,
      },
      newspapers: [],
      printshops: [],
      postOffices: [],
    };
  },
  methods: {
    async handleSubmit() {
      this.$emit("save", this.formData);
    },
    cancel() {
      this.$emit("cancel");
    },
    async fetchData() {
      try {
        const [newspapersResponse, printshopsResponse, postOfficesResponse] = await Promise.all([
          getNewspapers(),
          getPrintShops(),
          getPostalOffices(),
        ]);

        this.newspapers = newspapersResponse.data;
        this.printshops = printshopsResponse.data;
        this.postOffices = postOfficesResponse.data;
      } catch (error) {
        console.error("Ошибка загрузки данных:", error);
      }
    },
  },
  mounted() {
    this.fetchData();
  },
};
</script>

<style scoped>
.delivery-form {
  background-color: #f9f9f9;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
  margin-top: 20px;
}

button {
  margin-top: 10px;
  margin-right: 10px;
  padding: 10px 15px;
  background-color: #4caf50;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>

<template>
  <div class="vacancy-container p-4">
    <div class="row">
      <div class="col-12">
        <h1 class="vacancy-title">{{ vacancy.title }}</h1>
      </div>
      <div class="col-lg-12">
        <p class="vacancy-subtitle fs-5">Компания: {{ vacancy.company }}</p>
      </div>
      <div class="col-lg-12">
        <p class="vacancy-subtitle fs-5">Зарплата: {{ vacancy.salary }} руб.</p>
      </div>
      <div class="col-lg-12">
        <p class="vacancy-subtitle fs-5">Опыт: {{ vacancy.experience }}</p>
      </div>
      <div class="col-lg-12">
        <p class="vacancy-subtitle fs-5">Адрес: {{ vacancy.address }}</p>
      </div>
      <div class="col-12">
        <h2 class="vacancy-title">Описание вакансии</h2>
      </div>
      <div class="col-lg-12">
        <p class="vacancy-subtitle fs-5">{{ vacancy.description }}</p>
      </div>
      <div v-if="vacancy.responsibility" class="col-12">
        <h3 class="vacancy-title">Обязанности:</h3>
        <div v-if="Array.isArray(vacancy.responsibility)">
          <ul>
            <li v-for="(item, index) in vacancy.responsibility" :key="index">{{ item }}</li>
          </ul>
        </div>
        <div v-else>
          <p>{{ vacancy.responsibility }}</p>
        </div>
      </div>

      <div v-if="vacancy.requirements" class="col-12">
        <h3 class="vacancy-title">Требования:</h3>
        <div v-if="Array.isArray(vacancy.requirements)">
          <ul>
            <li v-for="(item, index) in vacancy.requirements" :key="index">{{ item }}</li>
          </ul>
        </div>
        <div v-else>
          <p>{{ vacancy.requirements }}</p>
        </div>
      </div>

      <div v-if="vacancy.conditions" class="col-12">
        <h3 class="vacancy-title">Условия:</h3>
        <div v-if="Array.isArray(vacancy.conditions)">
          <ul>
            <li v-for="(item, index) in vacancy.conditions" :key="index">{{ item }}</li>
          </ul>
        </div>
        <div v-else>
          <p>{{ vacancy.conditions }}</p>
        </div>
      </div>
      <div class="col-12 pt-2">
        <button type="button" class="btn btn-custom" @click="openModal">
          Откликнуться на вакансию
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "VacancyContainer",
  data() {
    return {
      vacancy: {},
    };
  },
  async created() {
    const urlParams = new URLSearchParams(window.location.search);
    const vacancyId = urlParams.get("id");

    try {
      const response = await axios.get(
        `http://localhost:3000/vacancies/${vacancyId}`
      );
      this.vacancy = response.data;
    } catch (error) {
      console.error("Ошибка при загрузке данных о вакансии:", error);
    }
  },
  methods: {
    openModal() {
      // Открытие модального окна (можно подключить библиотеку или использовать emit для передачи события)
      this.$emit("open-response-modal", this.vacancy.id);
    },
  },
};
</script>

<style scoped>
</style>

<script setup>
import {ref} from "vue";
import instance from "@/AxiosInstance";
import index from "@/router";
import {Api} from "@/services/api";

const Token = Api();

const form = ref({
  captain: "",       // Капитан
  co_pilot: "",      // Помощник капитана
  navigator: "",     // Навигатор
  attendants: [],    // Бортпроводники
});

const captainChoices = ref([]);     // Возможные капитаны
const coPilotChoices = ref([]);     // Возможные помощники капитана
const navigatorChoices = ref([]);   // Возможные навигаторы
const attendantChoices = ref([]);   // Возможные бортпроводники

// Функция для загрузки всех ролей экипажа
function fetchCrewChoices() {
  instance.get('/crews/create/', {
    headers: {
      'Authorization': `Token ${Token.token}`,
    },
  })
      .then(response => {
        if (response.status === 200) {
          captainChoices.value = response.data.captain_choices;
          coPilotChoices.value = response.data.co_pilot_choices;
          navigatorChoices.value = response.data.navigator_choices;
          attendantChoices.value = response.data.attendant_choices;
        }
      })
      .catch(error => console.log(error));
}

// Функция для создания экипажа
function create() {
  instance.post('/crews/', form.value, {
    headers: {
      'Authorization': `Token ${Token.token}`,
    },
  })
      .then(response => {
        if (response.status === 201) {
          index.push('/crews'); // Перенаправление на страницу списка экипажей
        }
      })
      .catch(error => console.log(error));
}

// Загружаем возможных членов экипажа при монтировании компонента
fetchCrewChoices();
</script>

<template>
  <v-app>
    <div class="w-50 mx-auto">
      <h2>Создать экипаж</h2>

      <!-- Выбор капитана -->
      <v-select
          label="Капитан"
          v-model="form.captain"
          :items="captainChoices.map(choice => ({ text: choice.name, value: choice.id }))"
          item-text="text"
          item-value="value"
      ></v-select>

      <!-- Выбор помощника капитана -->
      <v-select
          label="Помощник капитана"
          v-model="form.co_pilot"
          :items="coPilotChoices.map(choice => ({ text: choice.name, value: choice.id }))"
          item-text="text"
          item-value="value"
      ></v-select>

      <!-- Выбор навигатора -->
      <v-select
          label="Навигатор"
          v-model="form.navigator"
          :items="navigatorChoices.map(choice => ({ text: choice.name, value: choice.id }))"
          item-text="text"
          item-value="value"
      ></v-select>

      <!-- Выбор бортпроводников -->
      <v-select
          label="Бортпроводники"
          v-model="form.attendants"
          :items="attendantChoices.map(choice => ({ text: choice.name, value: choice.id }))"
          item-text="text"
          item-value="value"
          multiple
      ></v-select>

      <!-- Кнопка создания экипажа -->
      <v-btn @click="create">Создать</v-btn>
    </div>
  </v-app>
</template>

<style scoped>
</style>

<script setup>
import { ref, onMounted } from "vue";
import instance from "@/AxiosInstance";
import index from "@/router";
import { Api } from "@/services/api";

const Token = Api();

const form = ref({
  number: "",
  model: "",
  seats_capacity: "",
  speed: "",
  airline: null,  // ID авиакомпании
});

const airlines = ref([]);  // Массив для хранения списка авиакомпаний
const error = ref(false);

// Получаем список авиакомпаний при монтировании компонента
onMounted(() => {
  instance.get('/airlines/', {
    headers: {
      'Authorization': `Token ${Token.token}`,
    },
  }).then(response => {
    console.log(response.data);  // Проверяем данные
    airlines.value = response.data; // Сохраняем данные об авиакомпаниях
  }).catch(err => {
    console.error("Ошибка при получении списка авиакомпаний", err);
  });
});

function create() {
  const planeData = {
    ...form.value,
    airline: form.value.airline.id,  // Передаем только ID авиакомпании
  };

  instance.post('/planes/', planeData, {
    headers: {
      'Authorization': `Token ${Token.token}`,
    },
  })
  .then(response => {
    if (response.status === 201) {
      index.push('/planes');
    }
  })
  .catch(err => {
    console.error(err);
    error.value = true; // Показываем ошибку в случае неудачи
  });
}
</script>

<template>
  <v-app>
    <div class="w-50 mx-auto">
      <h2>Добавить самолет</h2>
      <v-text-field label="Номер" v-model="form.number"></v-text-field>
      <v-text-field label="Модель" v-model="form.model"></v-text-field>
      <v-text-field label="Вместимость (количество мест)" v-model="form.seats_capacity"></v-text-field>
      <v-text-field label="Скорость (км/ч)" v-model="form.speed"></v-text-field>

      <!-- Выбор авиакомпании -->
      <v-select
        v-if="airlines.length > 0"
        label="Авиакомпания"
        v-model="form.airline"
        :items="airlines"
        item-value="id"
        item-text="name"
        return-object
      ></v-select>

      <div v-if="error" class="text-red">
        Возникла ошибка при добавлении самолета.
      </div>

      <v-btn @click="create">Создать</v-btn>
    </div>
  </v-app>
</template>

<style scoped>
</style>

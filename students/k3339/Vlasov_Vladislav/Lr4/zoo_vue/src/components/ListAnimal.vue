
<script setup>
import axios from "axios";
import { onMounted, ref } from 'vue';
import ConfirmDelete from './ConfirmDelete.vue';
import PetForm from './PetForm.vue';

const isCreateFormVisible = ref(false)
const isPetEditing = ref(null)

const defaultPet = ref({
      number: null,
      name: "",
      sex: null,
      animal_type: "",
      note_reptile_pet: {
          normal_temperature: null,
          begin_wintering: ""
      },
      note_bird_pet: {
          is_wintering: false,
          country_wintering: "",
          start_wintering: "",
          finish_wintering: ""
      },
      birtday: null,
      is_buy: false,
      buy_pet: {
          seller: "",
          date_buy: ""
      },
      is_rented: "",
      rent_pet: {
          zoo: "",
          price: null,
          start_rent: "",
          finish_rent: ""
      },
      valliere: {id: null},
      habited: {id: null},
      diet: {number: null}
  })

function submitPet(pet, isEditing) {
  console.log(pet)
  console.log(isEditing)
  let subPet = SubmitMap(pet)
  if (!isEditing)
  {
    axios.post('http://localhost:8000/zoo/pet/create', subPet)
  } else {
    axios.put('http://localhost:8000/zoo/pet/update/'+subPet.number, subPet)
  }
  isPetEditing.value = null
  isCreateFormVisible.value = false
  fetchPets();
}

function SubmitMap(pet) {
  var subPet = { ...pet }
  if (subPet.sex == "самец") {subPet.sex = "m"}
  else {subPet.sex = "f"}

  if (subPet.birtday == "") { delete subPet.birtday }

  if (subPet.animal_type != "reptile") { delete subPet.note_reptile_pet }
  if (subPet.animal_type != "bird") { delete subPet.note_bird_pet }
  if (!subPet.is_buy) { delete subPet.buy_pet }
  if (subPet.is_rented == "") { delete subPet.rent_pet; delete subPet.is_rented }
  console.log(subPet)
  return subPet
}

function cancelCreateForm() {
  isCreateFormVisible.value = false
}

function cancelUpdateForm() {
  isPetEditing.value = null
}

const isDeletingPet = ref(null)

function confirmDelete(petNumber) {
  isDeletingPet.value = petNumber;
}

function deletePet(petNumber) {
  pets.value = pets.value.filter(pet => pet.number !== petNumber);
  axios.delete('http://localhost:8000/zoo/pet/delete/'+petNumber)
  isDeletingPet.value = null;
}

function cancelDelete() {
  isDeletingPet.value = null;
}

const pets = ref([])

async function fetchPets() {
try {
    const response = await axios.get('http://localhost:8000/zoo/pets') // Выполнение GET-запроса Backend-серверу. Запрос вернет JSON.
    console.log(response.data)
    pets.value = response.data
  } catch  {
    alert('Ошибка')
  }
}

onMounted(() => {
  fetchPets();
});

</script>

<template>
  <div class="button_bar">
    <button @:click="fetchPets">Обновить список животных</button>
    <button @:click="()=>{isCreateFormVisible = !isCreateFormVisible}">Добавить нового</button>
  </div>

  <PetForm
      v-if="isCreateFormVisible"
      :petData="defaultPet"
      :isEditing="false"
      @submit="submitPet"
      @cancel="cancelCreateForm"
    />

  <div class="pet" v-for="pet in pets" :key="pet.number">

    <h2><strong>Питомец: {{ pet.number }} {{ pet.name }}</strong></h2>

    <p>{{ pet.animal_type }} {{ pet.sex }}</p>
    <p>Дата рождения: {{ pet.birtday }}</p>
    <p>Номер назначенного рациона {{ pet.diet.number }}</p>

    <div class="note" v-if="pet.animal_type == 'bird'">
 
      <h3>Дополнительная информация о птице:</h3>
      <p v-if="pet.note_bird_pet != null || pet.note_bird_pet.is_wintering == true">Птица зимует</p>
      <p v-if="pet.note_bird_pet != null || pet.note_bird_pet.is_wintering == true">Место зимовки: {{ pet.note_bird_pet.country_wintering }}</p>
      <p v-if="pet.note_bird_pet != null || pet.note_bird_pet.is_wintering == true">Время зимовки: {{ pet.note_bird_pet.start_wintering }} - {{ pet.note_bird_pet.finish_wintering }}</p>

      <p v-else>Птица не зимует</p>

    </div>

    <div class="note" v-else-if="pet.animal_type == 'reptile'">
 
      <h3>Дополнительная информация о рептилии:</h3>
      <p>Нормальная температура: {{ pet.note_reptile_pet.normal_temperature }}</p>
      <p>Дата впадения в спячку: {{ pet.note_reptile_pet.begin_wintering }}</p>

    </div>

    <div class="note" v-if="pet.is_buy == true">
      
      <h3>Информация о покупке:</h3>
      <p>Питомец приобретён у {{ pet.buy_pet.seller }}</p>
      <p>В дату {{ pet.buy_pet.date_buy }}</p>

    </div>

    <div class="note" v-if="pet.is_rented != null">
      
      <h3 v-if="pet.is_rented =='in'">Питомец взят в аренду</h3>
      <h3 v-else-if="pet.is_rented =='out'">Питомец сдан в аренду</h3>

      <p>Организация: {{ pet.rent_pet.zoo }}</p>
      <p>Цена {{ pet.rent_pet.price }}</p>
      <p>Время аренды {{ pet.rent_pet.start_rent }} - {{ pet.rent_pet.finish_rent }}</p>

    </div>

    <p>Адресс: Отдел {{ pet.valliere.building.depart }}, здание {{ pet.valliere.building.id }}, вольер {{ pet.valliere.id }} </p>

    <div class="note">

            
      <h3>Справка о зоне обитания. Номер {{ pet.habited.id }}</h3>

      <p>Тип местности {{ pet.habited.name }}</p>
      <p>Континент {{ pet.habited.continent }}</p>
      <p>Страна {{ pet.habited.country }}</p>
      
      <p>{{ pet.habited.description }}</p>

    </div>

    <div class="button_bar">
      <div>
        <button @:click="()=>{isPetEditing = pet.number}">Изменить</button>
      </div>
      <div>
        <button @click="confirmDelete(pet.number)">Удалить</button>
      </div>
    </div>

    <ConfirmDelete
      v-if="isDeletingPet == pet.number"
      :isVisible="true"
      :frameNumber="pet.number"
      @confirm="deletePet(pet.number)"
      @cancel="cancelDelete"
    />

    <PetForm
      v-if="isPetEditing == pet.number"
      :petData="pet"
      :isEditing="true"
      @submit="submitPet"
      @cancel="cancelUpdateForm"
    />

  </div>

</template>

<style scoped>
/* Общие стили для контейнера */
.pet {
    border: 1px solid #ccc; /* Рамка вокруг питомца */
    border-radius: 8px; /* Скругление углов */
    padding: 15px; /* Внутренние отступы */
    margin: 10px 0; /* Отступы между питомцами */
    background-color: #f9f9f9; /* Цвет фона */
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* Легкая тень */
}

/* Стили заголовков */
h2 {
    margin-bottom: 10px; /* Отступ снизу */
    color: #333; /* Цвет текста */
}

/* Стили для кнопок */
.button_bar {
    display: flex; /* Используем Flexbox для кнопок */
    justify-content: space-between; /* Распределение кнопок по краям */
    margin-top: 10px; /* Отступ между питомцем и кнопками */
}

button {
    padding: 10px 15px; /* Внутренние отступы кнопок */
    background-color: #007BFF; /* Цвет кнопок */
    color: white; /* Цвет текста */
    border: none; /* Убираем рамку */
    border-radius: 4px; /* Скругление углов */
    cursor: pointer; /* Указатель при наведении */
    transition: background-color 0.3s; /* Плавный переход цвета */
}

button:hover {
    background-color: #0056b3; /* Цвет кнопки при наведении */
}

/* Стили для дополнительных информационных блоков */
.note {
    background-color: #e9ecef; /* Цвет фона для заметок */
    border-left: 4px solid #007BFF; /* Левый бордер для акцента */
    padding: 10px; /* Внутренние отступы */
    margin: 10px 0; /* Отступы между заметками */
}

h3 {
    margin-top: 0; /* Убираем отступ сверху для заголовков в заметках */
}

/* Стили для форм */
.PetForm {
    margin-top: 20px; /* Отступ сверху для формы добавления/редактирования */
    padding: 15px; /* Внутренние отступы */
    border: 1px solid #ccc; /* Рамка вокруг формы */
    border-radius: 8px; /* Скругление углов */
    background-color: #fff; /* Цвет фона формы */
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* Легкая тень для формы */
}

/* Стили для кнопки динамического управления формами */
button[type="button"] {
    background-color: #28a745; /* Цвет кнопки для добавления */
}

button[type="button"]:hover {
    background-color: #218838; /* Цвет кнопки при наведении для добавления */
}
</style>

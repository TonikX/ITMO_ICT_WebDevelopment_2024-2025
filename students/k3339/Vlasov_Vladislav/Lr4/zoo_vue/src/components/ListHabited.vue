<script setup>
import axios from "axios";
import { onMounted, ref } from 'vue';
import ConfirmDelete from './ConfirmDelete.vue';
import HabitedForm from './HabitedForm.vue';

const defaultHabited = ref({
    id: null,
    name: "",
    continent: "",
    country: "",
    description: ""
})

const habiteds = ref([])
const isCreateFormVisible = ref(false)
const isHabitedEditing = ref(null)

async function fetchHabiteds() {
try {
    const response = await axios.get('http://localhost:8000/zoo/habiteds') // Выполнение GET-запроса Backend-серверу. Запрос вернет JSON.
    console.log(response.data)
    habiteds.value = response.data
  } catch  {
    alert('Ошибка')
  }
}

function submitHabited(habited, isEditing) {
  console.log(habited)
  console.log(isEditing)

  if (!isEditing)
  {
    axios.post('http://localhost:8000/zoo/habited/create', habited)
  } else {
    axios.put('http://localhost:8000/zoo/habited/update/'+habited.id, habited)
  }
  isHabitedEditing.value = null
  isCreateFormVisible.value = false
  fetchHabiteds();
}

function cancelCreateForm() {
  isCreateFormVisible.value = false
}

function cancelUpdateForm() {
  isHabitedEditing.value = null
}

const isDeletingHabited = ref(null)

function confirmDelete(habitedNumber) {
  isDeletingHabited.value = habitedNumber;
}

function deleteHabited(habitedNumber) {
  habiteds.value = habiteds.value.filter(habited => habited.id !== habitedNumber);
  axios.delete('http://localhost:8000/zoo/habited/delete/'+habitedNumber)
  isDeletingHabited.value = null;
}

function cancelDelete() {
  isDeletingHabited.value = null;
}

onMounted(() => {
    fetchHabiteds();
});
</script>

<template>
  <div class="button_bar">
    <button @:click="fetchHabiteds">Обновить список зон обитания</button>
    <button @:click="()=>{isCreateFormVisible = !isCreateFormVisible}">Добавить новую</button>
  </div>
  
    <HabitedForm
        v-if="isCreateFormVisible"
        :habitedData="defaultHabited"
        :isEditing="false"
        @submit="submitHabited"
        @cancel="cancelCreateForm"
      />
  
    <div class="habited" v-for="habited in habiteds" :key="habited.id">
  
     
        <h2>Зона обитания "{{ habited.name }}"</h2>
  
        <p>Номер зоны: {{ habited.name }}</p>
        <p>Континент: {{ habited.continent }}</p>
        <p>Страна: {{ habited.country }}</p>
        
        <p>{{ habited.description }}</p>
        
        <div class="button_bar">
            <div>
                <button @:click="()=>{isHabitedEditing = habited.id}">Изменить</button>
            </div>
            <div>
                <button @click="confirmDelete(habited.id)">Удалить</button>
            </div>
        </div>

      <ConfirmDelete
        v-if="isDeletingHabited == habited.id"
        :isVisible="true"
        :frameNumber="habited.id"
        @confirm="deleteHabited(habited.id)"
        @cancel="cancelDelete"
      />
  
      <HabitedForm
        v-if="isHabitedEditing == habited.id"
        :habitedData="habited"
        :isEditing="true"
        @submit="submitHabited"
        @cancel="cancelUpdateForm"
      />
  
    </div>
  
</template>

<style scoped>
/* Общие стили для кнопок */
button {
    background-color: #007BFF; /* Цвет фона кнопок */
    color: white; /* Цвет текста кнопок */
    border: none; /* Убираем границу */
    border-radius: 5px; /* Скругленные углы для кнопок */
    padding: 10px 15px; /* Внутренние отступы */
    cursor: pointer; /* Курсор при наведении */
    transition: background-color 0.3s; /* Плавный переход цвета фона */
}

/* Эффект при наведении на кнопки */
button:hover {
    background-color: #0056b3; /* Темнее при наведении */
}

/* Стили для верхней панели кнопок */
.button_bar {
    display: flex; /* Flex-контейнер для кнопок */
    justify-content: space-between; /* Равномерное распределение кнопок */
    margin-bottom: 15px; /* Отступ снизу для панели кнопок */
}

/* Основные стили для карточки "зона обитания" */
.habited {
    border: 1px solid #ddd; /* Граница для карточки зоны обитания */
    border-radius: 8px; /* Скругленные углы */
    padding: 15px; /* Внутренние отступы */
    margin: 10px 0; /* Отступы между карточками */
    background-color: #f9f9f9; /* Цвет фона для карточек */
    transition: box-shadow 0.3s; /* Плавный переход для теней */
}

/* Эффект тени при наведении на карточку */
.habited:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Тень при наведении */
}

/* Стилизация заголовков и параграфов */
.habited h2 {
    color: #333; /* Цвет заголовка */
    font-size: 1.5em; /* Размер шрифта для заголовка */
    margin-bottom: 5px; /* Отступ снизу */
}

.habited p {
    margin: 5px 0; /* Отступы между параграфами */
}

/* Стили для форм */
.habitedForm {
    margin: 15px 0; /* Отступы для формы */
}

/* Стили для окна подтверждения удаления */
.confirm-delete {
    background-color: #ffdddd; /* Светлый фон для подтверждения удаления */
    padding: 10px; /* Внутренние отступы */
    border: 1px solid #f00; /* Граница красного цвета */
    border-radius: 5px; /* Скругленные углы */
    margin-top: 10px; /* Отступ сверху */
    color: #d9534f; /* Красный текст */
}

/* Адаптивные стили */
@media (max-width: 768px) {
    .button_bar {
        flex-direction: column; /* Вертикальное расположение кнопок на мобильных устройствах */
    }

    button {
        width: 100%; /* Кнопки занимают всю ширину на мобильных устройствах */
        margin-bottom: 10px; /* Отступ между кнопками */
    }

    .habited {
        font-size: 0.9em; /* Уменьшение размера шрифта на мобильных устройствах */
    }
}
</style>
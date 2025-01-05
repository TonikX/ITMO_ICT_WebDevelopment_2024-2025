<script setup>
import axios from "axios";
import { onMounted, ref } from 'vue';
import ConfirmDelete from './ConfirmDelete.vue';
import DietForm from './DietForm.vue';

const defaultDiet = ref({
    number: null,
    products: [],
    name: "",
    type_diet: ""
})

const diets = ref([])
const isCreateFormVisible = ref(false)
const isDietEditing = ref(null)

async function fetchDiets() {
try {
    const response = await axios.get('http://localhost:8000/zoo/diets') // Выполнение GET-запроса Backend-серверу. Запрос вернет JSON.
    console.log(response.data)
    diets.value = response.data
  } catch  {
    alert('Ошибка')
  }
}

function submitDiet(diet, isEditing) {
  console.log(diet)
  console.log(isEditing)

  console.log(diet)
  if (!isEditing)
  {
    axios.post('http://localhost:8000/zoo/diet/create', diet)
  } else {
    axios.put('http://localhost:8000/zoo/diet/update/'+diet.number, diet)
  }
  isDietEditing.value = null
  isCreateFormVisible.value = false
  fetchDiets();
}

function cancelCreateForm() {
  isCreateFormVisible.value = false
}

function cancelUpdateForm() {
  isDietEditing.value = null
}

const isDeletingDiet = ref(null)

function confirmDelete(dietNumber) {
  isDeletingDiet.value = dietNumber;
}

function deleteDiet(dietNumber) {
  diets.value = diets.value.filter(diet => diet.number !== dietNumber);
  axios.delete('http://localhost:8000/zoo/diet/delete/'+dietNumber)
  isDeletingDiet.value = null;
}

function cancelDelete() {
  isDeletingDiet.value = null;
}

onMounted(() => {
    fetchDiets();
});
</script>

<template>
  <div class="button_bar">
    <button @:click="fetchDiets">Обновить список рационов</button>
    <button @:click="()=>{isCreateFormVisible = !isCreateFormVisible}">Добавить новый рацион</button>
  </div>
  
    <DietForm
        v-if="isCreateFormVisible"
        :dietData="defaultDiet"
        :isEditing="false"
        @submit="submitDiet"
        @cancel="cancelCreateForm"
      />
  
    <div class="diet" v-for="diet in diets" :key="diet.number">
  
     
        <h2>Рацион "{{ diet.name }}". Номер {{ diet.number }}</h2>
  
        <p>Тип рациона: {{ diet.type_diet }}</p>
        
        <h3 v-if="diet.products.length != 0">Продукты в рационе: </h3>

        <div class="note">
 
            <p v-for="product in diet.products" :key="product.id">{{ product.name }}</p>

        </div>
        
        <div class="button_bar">
            <div>
                <button @:click="()=>{isDietEditing = diet.number}">Изменить</button>
            </div>
            <div>
                <button @click="confirmDelete(diet.number)">Удалить</button>
            </div>
        </div>

      <ConfirmDelete
        v-if="isDeletingDiet == diet.number"
        :isVisible="true"
        :frameNumber="diet.number"
        @confirm="deleteDiet(diet.number)"
        @cancel="cancelDelete"
      />
  
      <DietForm
        v-if="isDietEditing == diet.number"
        :dietData="diet"
        :isEditing="true"
        @submit="submitDiet"
        @cancel="cancelUpdateForm"
      />
  
    </div>
  
</template>

<style scoped>
/* Основные стили для контейнера */
.diet {
    border: 1px solid #ddd;  /* Граница для карточки рациона */
    border-radius: 8px;  /* Скругленные углы */
    padding: 15px;  /* Внутренние отступы */
    margin: 10px 0;  /* Отступы между карточками */
    background-color: #f9f9f9;  /* Цвет фона для карточек */
    transition: box-shadow 0.3s;  /* Плавный переход для теней */
}

/* Эффект тени при наведении */
.diet:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);  /* Тень при наведении */
}

/* Стилизация заголовков */
.diet h2 {
    color: #333;  /* Цвет заголовка */
    font-size: 1.5em;  /* Размер шрифта для заголовка */
    margin-bottom: 5px;  /* Отступ снизу */
}

.diet h3 {
    color: #666;  /* Цвет подзаголовка */
    font-size: 1.2em;  /* Размер шрифта подзаголовка */
}

/* Стили для кнопок */
button {
    background-color: #007BFF;  /* Цвет фона кнопок */
    color: white;  /* Цвет текста кнопок */
    border: none;  /* Убираем границу */
    border-radius: 5px;  /* Скругленные углы для кнопок */
    padding: 10px 15px;  /* Внутренние отступы */
    cursor: pointer;  /* Курсор при наведении */
    transition: background-color 0.3s;  /* Плавный переход цвета фона */
}

/* Изменение цвета кнопок при наведении */
button:hover {
    background-color: #0056b3;  /* Темнее при наведении */
}

/* Стили для формы и элементов формы */
.note {
    background-color: #e9ecef;  /* Цвет фона для списка продуктов */
    padding: 10px;  /* Внутренние отступы */
    border-radius: 5px;  /* Скругленные углы */
    margin-bottom: 10px;  /* Отступы снизу */
}

/* Кнопка "Добавить новый рацион" */
.button_bar {
    display: flex;  /* Flex-контейнер для кнопок */
    justify-content: space-between;  /* Равномерное распределение кнопок */
}

.button_bar div {
    margin-top: 10px;  /* Отступ сверху для каждой кнопки */
}

/* Дополнительный стиль для Confirmation Delete */
.confirm-delete {
    background-color: #ffdddd;  /* Светлый фон для подтверждения удаления */
    padding: 10px;  /* Внутренние отступы */
    border: 1px solid #f00;  /* Граница красного цвета */
    border-radius: 5px;  /* Скругленные углы */
    margin-top: 10px;  /* Отступ сверху */
    color: #d9534f;  /* Красный текст */
}

/* Стили для медиазапросов */
@media (max-width: 768px) {
    .diet {
        font-size: 0.9em;  /* Уменьшение размера шрифта на мобильных устройствах */
    }

    button {
        width: 100%;  /* Кнопки занимают всю ширину на мобильных устройствах */
        margin-bottom: 10px;  /* Отступ между кнопками */
    }
}
</style>
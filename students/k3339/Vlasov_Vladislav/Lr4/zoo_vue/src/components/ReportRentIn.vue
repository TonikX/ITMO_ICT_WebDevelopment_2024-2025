<script setup>
import axios from "axios";
import { onMounted, ref } from 'vue';

const rentsIn = ref([])

async function fetchRentsIn() {
try {
    const response = await axios.get('http://localhost:8000/zoo/pets_rent_in/state')
    rentsIn.value = response.data.RentedPets
    console.log(rentsIn.value)
  } catch  {
    alert('Ошибка')
  }
}

onMounted(() => {
    fetchRentsIn();
});
</script>

<template>
    <button @:click="fetchHabiteds">Обновить отчёт</button>
  
    <div class="rentsIn" v-for="rentIn in rentsIn" :key="rentIn.zoo">
        <h2>Зоопарк "{{ rentIn.zoo }}"</h2>
  
        <p>Питомцев: {{ rentIn.num_pets }}</p>
        <p>Общая цена: {{ rentIn.cost }}</p>
    </div>
  
</template>

<style scoped>
/* Общий стиль для кнопки обновления отчета */
button {
    background-color: #007BFF; /* Зеленый цвет для кнопки */
    color: white; /* Цвет текста кнопки */
    border: none; /* Убираем границу */
    border-radius: 5px; /* Скругленные углы */
    padding: 10px 15px; /* Внутренние отступы */
    cursor: pointer; /* Курсор при наведении */
    transition: background-color 0.3s; /* Плавный переход цвета фона */
    margin-bottom: 20px; /* Отступ снизу */
}

/* Эффект при наведении на кнопку */
button:hover {
    background-color: #218838; /* Темнее при наведении */
}

/* Стили для блока с информацией о зоопарке */
.rentsIn {
    border: 1px solid #ddd; /* Граница для блока зоопарков */
    border-radius: 8px; /* Скругленные углы */
    padding: 15px; /* Внутренние отступы */
    margin-bottom: 15px; /* Отступ между блоками */
    background-color: #f9f9f9; /* Цвет фона для блока */
    transition: box-shadow 0.3s; /* Плавный переход для тени */
}

/* Эффект тени при наведении на блок зоопарка */
.rentsIn:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Тень при наведении */
}

/* Стили для заголовка и параграфов в блоке зоопарка */
.rentsIn h2 {
    color: #333; /* Цвет заголовка */
    font-size: 1.5em; /* Размер шрифта заголовка */
    margin-bottom: 10px; /* Отступ снизу для заголовка */
}

.rentsIn p {
    margin: 5px 0; /* Отступы между параграфами */
    color: #555; /* Цвет текста параграфов */
}

/* Адаптивные стили */
@media (max-width: 768px) {
    /* Кнопка занимает полную ширину на мобильных устройствах */
    button {
        width: 100%; 
    }

    /* Отступы для блока зоопарка на мобильных устройствах */
    .rentsIn {
        margin: 10px 0; /* Отступы снизу */
    }
}
</style>
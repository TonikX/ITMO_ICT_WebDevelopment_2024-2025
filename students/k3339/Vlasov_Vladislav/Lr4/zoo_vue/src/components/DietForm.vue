<template>
    <form @submit.prevent>
    <div class="diet-form">
      <h2>{{ isEditing ? 'Обновить информацию о рационе?' : 'Создать новый рацион?' }}</h2>

        <div>
          <label for="number" v-if="!isEditing">Номер:
          <input type="number" v-model="diet.number" required /></label>
        </div>

        <div>
          <label for="name">Наименование:
          <input type="text" v-model="diet.name" required /></label>
        </div>

        <div>
          <label for="type_diet">Тип:
          <input type="text" v-model="diet.type_diet" required /></label>
        </div>

        <p>Выберите продукты для рациона:</p>

        <div class="products">
            <label class="checkbox-label" v-for="product in products" :key="product.id">
                <input type="checkbox" v-model="product.taked"> {{ product.name }}
            </label>
        </div>

        <button type="submit" @click="submitForm(diet, isEditing)">{{ isEditing ? 'Обновить' : 'Добавить' }}</button>
        <button type="button" @click="cancel">Отменить</button>
    </div>
    </form>
  </template>

<script setup>
    import { onMounted, ref } from 'vue';
    import axios from "axios";

    const props = defineProps({
        dietData: Object,
        isEditing: Boolean
    })

    const diet = ref({ ...props.dietData })

    const emit = defineEmits(['submit', 'cancel'])
    
    function falidateForm() {
        return diet.value.number && diet.value.name && diet.value.type_diet
    }

    function submitForm() {
        if (!falidateForm()){return}
        diet.value.products = products.value.filter(product => product.taked).map(product => product.id)
        emit('submit', diet.value, props.isEditing);
    }

    function cancel() {
        emit('cancel');
    }

    const products = ref([])

    async function fetchProducts() {
        try {
            const response = await axios.get('http://localhost:8000/zoo/products') // Выполнение GET-запроса Backend-серверу. Запрос вернет JSON.
            console.log(response.data)
            products.value = response.data
            products.value.forEach(product => {
                product.taked = diet.value.products.some(elem => elem.id == product.id);
            });
            console.log(products.value)
        } catch  {
            alert('Ошибка')
        }
    }

    onMounted(() => {
        fetchProducts();
    });

</script>

<style scoped>
/* Стили для формы диеты */
.diet-form {
    display: flex;
    flex-direction: column; /* Вертикальное расположение элементов */
    max-width: 400px; /* Максимальная ширина формы */
    margin: 20px auto; /* Центрирование формы на странице */
    padding: 20px; /* Внутренние отступы */
    background-color: #f9f9f9; /* Цвет фона формы */
    border: 1px solid #ccc; /* Рамка формы */
    border-radius: 8px; /* Скругление углов формы */
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* Легкая тень */
}

/* Стили для заголовка формы */
.diet-form h2 {
    margin-bottom: 20px; /* Отступ снизу для заголовка */
    font-size: 20px; /* Размер шрифта заголовка */
    color: #333; /* Цвет текста заголовка */
}

/* Стили для меток и входных полей */
.diet-form label {
    margin-bottom: 10px; /* Отступ снизу для меток */
    color: #555; /* Цвет текста меток */
}

/* Устанавливаем стиль для входных полей */
.diet-form input[type="text"],
.diet-form input[type="number"] {
    width: 100%; /* Ширина полей на 100% */
    padding: 10px; /* Внутренние отступы для полей */
    border: 1px solid #ccc; /* Рамка полей */
    border-radius: 4px; /* Скругление углов полей */
    margin-bottom: 15px; /* Отступ снизу для полей */
    font-size: 16px; /* Размер шрифта */
}

/* Стили для блока с продуктами */
.products {
    margin: 15px 0; /* Отступы сверху и снизу */
}

/* Стили для меток чекбоксов */
.checkbox-label {
    display: block; /* Чекбоксы расположены по вертикали */
    margin-bottom: 10px; /* Отступ снизу для чекбоксов */
}

/* Стили для кнопок */
.diet-form button {
    padding: 10px 15px; /* Внутренние отступы для кнопок */
    margin-top: 10px; /* Отступ сверху для кнопок */
    border: none; /* Убираем рамку */
    border-radius: 4px; /* Скругление углов кнопок */
    cursor: pointer; /* Указатель при наведении */
    transition: background-color 0.3s; /* Плавный переход цвета */
}

.diet-form button[type="submit"] {
    background-color: #007BFF; /* Цвет фона для кнопки отправки */
    color: white; /* Цвет текста для кнопки отправки */
}

.diet-form button[type="button"] {
    background-color: #ccc; /* Цвет фона для кнопки отмены */
    color: #333; /* Цвет текста для кнопки отмены */
}

/* Эффекты при наведении на кнопки */
.diet-form button:hover {
    opacity: 0.9; /* Меняем прозрачность при наведении */
}
</style>
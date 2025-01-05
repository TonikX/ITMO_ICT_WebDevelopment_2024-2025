<template>
    <form @submit.prevent>
    <div class="habited-form">
      <h2>{{ isEditing ? 'Обновить информацию о зоне обитания?' : 'Добавить информацию?' }}</h2>


        <div>
          <label for="name">Наименование:
          <input type="text" v-model="habited.name" required /></label>
        </div>

        <div>
          <label for="continent">Континент:
          <input type="text" v-model="habited.continent" required /></label>
        </div>

        <div>
          <label for="country">Страна:
          <input type="text" v-model="habited.country" required /></label>
        </div>

        <div>
          <label for="description">Описание:
          <textarea rows="5" cols="33" v-model="habited.description" /></label>
        </div>

        <button type="submit" @click="submitForm(habited, isEditing)">{{ isEditing ? 'Обновить' : 'Добавить' }}</button>
        <button type="button" @click="cancel">Отменить</button>
    </div>
    </form>
  </template>

<script setup>
    import { ref } from 'vue';

    const props = defineProps({
        habitedData: Object,
        isEditing: Boolean
    })

    const habited = ref({ ...props.habitedData })

    const emit = defineEmits(['submit', 'cancel'])

    function falidateForm() {
        return habited.value.name && habited.value.continent && habited.value.country
    }

    function submitForm() {
        if (!falidateForm()){return}
        emit('submit', habited.value, props.isEditing);
    }

    function cancel() {
        emit('cancel');
    }
</script>

<style scoped>
/* Стили для формы обитания */
.habited-form {
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
.habited-form h2 {
    margin-bottom: 20px; /* Отступ снизу для заголовка */
    font-size: 20px; /* Размер шрифта заголовка */
    color: #333; /* Цвет текста заголовка */
}

/* Стили для меток и входных полей */
.habited-form label {
    margin-bottom: 10px; /* Отступ снизу для меток */
    color: #555; /* Цвет текста меток */
}

/* Устанавливаем стиль для входных полей */
.habited-form input[type="text"], 
.habited-form textarea {
    width: 100%; /* Ширина полей на 100% */
    padding: 10px; /* Внутренние отступы для полей */
    border: 1px solid #ccc; /* Рамка полей */
    border-radius: 4px; /* Скругление углов полей */
    margin-bottom: 15px; /* Отступ снизу для полей */
    font-size: 16px; /* Размер шрифта */
}

/* Стили для кнопок */
.habited-form button {
    padding: 10px 15px; /* Внутренние отступы для кнопок */
    margin-top: 10px; /* Отступ сверху для кнопок */
    border: none; /* Убираем рамку */
    border-radius: 4px; /* Скругление углов кнопок */
    cursor: pointer; /* Указатель при наведении */
    transition: background-color 0.3s; /* Плавный переход цвета */
}

.habited-form button[type="submit"] {
    background-color: #007BFF; /* Цвет фона для кнопки отправки */
    color: white; /* Цвет текста для кнопки отправки */
}

.habited-form button[type="button"] {
    background-color: #ccc; /* Цвет фона для кнопки отмены */
    color: #333; /* Цвет текста для кнопки отмены */
}

/* Эффекты при наведении на кнопки */
.habited-form button:hover {
    opacity: 0.9; /* Меняем прозрачность при наведении */
}
</style>
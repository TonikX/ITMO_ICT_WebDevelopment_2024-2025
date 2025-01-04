
<script setup>

const props = defineProps(['frameNumber', 'isVisible'])

const emit = defineEmits(['confirm', 'cancel'])

function onConfirm() {
    emit('confirm', props.frameNumber);
}

function onCancel() {
    emit('cancel');
}
</script>

<template>
    <div v-if="isVisible" class="confirm-delete">
        <p>Вы уверены, что хотите удалить этого питомца?</p>
        <button @click="onConfirm">Да</button>
        <button @click="onCancel">Нет</button>
    </div>
</template>


<style scoped>
/* Стили для окна подтверждения удаления */
.confirm-delete {
    display: flex; /* Используем Flexbox для выравнивания содержимого */
    flex-direction: column; /* Вертикальное расположение элементов */
    align-items: center; /* Центрируем элементы по горизонтали */
    padding: 20px; /* Внутренние отступы */
    background-color: #fff; /* Цвет фона окна */
    border: 1px solid #ccc; /* Рамка вокруг окна */
    border-radius: 8px; /* Скругление углов */
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2); /* Легкая тень */
    margin: 20px; /* Отступы вокруг окна */
}

/* Стили для текста в окне подтверждения */
.confirm-delete p {
    margin-bottom: 15px; /* Отступ снизу для текста */
    color: #333; /* Цвет текста */
    font-size: 16px; /* Размер шрифта */
}

/* Стили для кнопок в окне подтверждения */
.confirm-delete button {
    padding: 10px 15px; /* Внутренние отступы кнопок */
    margin: 5px; /* Отступы между кнопками */
    background-color: #007BFF; /* Цвет фона кнопок */
    color: white; /* Цвет текста */
    border: none; /* Убираем рамку */
    border-radius: 4px; /* Скругление углов кнопок */
    cursor: pointer; /* Указатель при наведении */
    transition: background-color 0.3s; /* Плавный переход цвета */
}

/* Эффекты при наведении на кнопки */
.confirm-delete button:hover {
    background-color: #0056b3; /* Цвет кнопки при наведении */
}
</style>
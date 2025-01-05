<script setup>
import { RouterLink } from 'vue-router';
</script>

<template>
    <div class="bar">
        <div><RouterLink to="/" exact-active-class="active-link">Животные</RouterLink></div>
        <div><RouterLink to="/diet" exact-active-class="active-link">Рационы</RouterLink></div>
        <div><RouterLink to="/habiteds" exact-active-class="active-link">Зоны обитания</RouterLink></div>
        <div><RouterLink to="/report" exact-active-class="active-link">Отчёт о взятых в аренду</RouterLink></div>
    </div>
</template>

<style scoped>
/* Стили для навигационной панели */
.bar {
    display: flex; /* Используем flex-контейнер для горизонтального расположения элементов */
    justify-content: space-around; /* Распределяем элементы равномерно по доступной ширине */
    background-color: #007BFF; /* Цвет фона панели */
    padding: 15px 0; /* Внутренние отступы сверху и снизу */
    margin: 10px;
}

.bar div {
    margin: 0 15px; /* Отступы между элементами навигации */
}

.bar a {
    color: white; /* Цвет текста для ссылок */
    text-decoration: none; /* Убираем подчеркивание */
    font-size: 18px; /* Размер шрифта */
    transition: color 0.3s; /* Плавный переход цвета при наведении */
}

/* Эффект при наведении на ссылки */
.bar a:hover {
    color: #00d1b2; /* Цвет текста при наведении */
}

.active-link {
    font-weight: bold; /* Увеличиваем толщину шрифта */
    color: #00d1b2; /* Цвет текста для активной ссылки */
    border-bottom: 2px solid #00d1b2; /* Подчеркивание активной ссылки */
}

/* Для Responsive Design */
@media (max-width: 768px) {
    .bar {
        flex-direction: column; /* Переход на вертикальное расположение на меньших экранах */
        align-items: center; /* Центрирование элементов */
    }

    .bar div {
        margin: 10px 0; /* Отступы для вертикального расположения */
    }
}
</style>

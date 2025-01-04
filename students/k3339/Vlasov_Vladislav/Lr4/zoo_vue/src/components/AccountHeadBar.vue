<script setup>
    import { useRouter } from 'vue-router';

    const router = useRouter();

    function logout() {
        localStorage.removeItem('access_token');
        router.push('/login');
    }

    function changeUser() {
        router.push('/user');
    }
</script>

<template>
    <div class="bar">
        <div><button @:click="changeUser">Изменить пользователя</button></div>
        <div><button @:click="logout">Выйти</button></div>
    </div>
</template>

<style scoped>
.router-link-active {
    color: black; /* Изменяем цвет текста для активной ссылки на чёрный */
}
/* Стили для панели управления пользователем */
.bar {
    display: flex; /* Используем Flexbox для выравнивания кнопок в строку */
    justify-content: space-between; /* Раздвигаем кнопки по краям */
    padding: 10px 20px; /* Внутренние отступы для панели */
    background-color: #f1f1f1; /* Цвет фона для панели */
    border-radius: 8px; /* Скругление углов панели */
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* Легкая тень */
    margin-bottom: 20px; /* Отступ снизу для разделения с другими элементами */
}

/* Стили для кнопок */
.bar button {
    padding: 10px 15px; /* Внутренние отступы кнопок */
    background-color: #007BFF; /* Цвет фона кнопок */
    color: white; /* Цвет текста */
    border: none; /* Убираем рамку */
    border-radius: 4px; /* Скругление углов кнопок */
    cursor: pointer; /* Указатель при наведении */
    transition: background-color 0.3s; /* Плавный переход цвета */
}

/* Эффекты при наведении на кнопки */
.bar button:hover {
    background-color: #0056b3; /* Цвет кнопки при наведении */
}
</style>

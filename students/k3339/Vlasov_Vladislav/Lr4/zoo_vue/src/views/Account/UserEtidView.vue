<template>
    <div class="update-container">
        <h2>Изменение учетных данных</h2>
        <form @submit.prevent="updateUser" class="update-form">
            <input v-model="email" type="email" placeholder="Новый Email" required />
            <input v-model="firstName" placeholder="Имя" />
            <input v-model="lastName" placeholder="Фамилия" />
            <button type="submit">Сохранить изменения</button>
        </form>
        <p class="back-link">
        <RouterLink to="/">На главную</RouterLink>
        </p>
    </div>
</template>
  
<script setup>
    import axios from 'axios';
    import { ref, onMounted } from 'vue';
    import { RouterLink } from 'vue-router';

    const email = ref("")
    const firstName = ref("")
    const lastName = ref("")
  
    async function updateUser()
    {
        const token = localStorage.getItem('access_token');
        const username = localStorage.getItem('username')
        try
        {
            await axios.put(`http://localhost:8000/account/user/update/${username}/`, {
                username: username,
                email: email.value,
                first_name: firstName.value,
                last_name: lastName.value,
            }, {
                headers: { Authorization: `Bearer ${token}` },
            });
                alert('Данные успешно обновлены!');

            } catch (error) {
                console.error(error);
                alert('Ошибка обновления данных');
        }
    }

    async function getUser() {
        const token = localStorage.getItem('access_token');
        console.log(`Bearer ${token}`)
        const username = localStorage.getItem('username')
        console.log(`http://localhost:8000/account/user/${username}/`)
        const response = await axios.get(`http://localhost:8000/account/user/${username}/`, {
            headers: {
                Authorization: "Bearer " + token
            }
        });
        email.value = response.data.email
        firstName.value = response.data.firstName
        lastName.value = response.data.lastName
    }

    onMounted(() => {
        getUser();
    });
  </script>


<style scoped>
.update-container {
    max-width: 400px; /* Максимальная ширина контейнера */
    margin: 20px auto; /* Центрирование контейнера по горизонтали */
    padding: 20px; /* Отступы вокруг контейнера */
    border: 1px solid #ccc; /* Рамка вокруг контейнера */
    border-radius: 8px; /* Скругление углов */
    box-shadow: 0 2px 5px rgba(0,0,0,0.1); /* Тень для контейнера */
}

.update-form {
    display: flex; /* Используем Flexbox */
    flex-direction: column; /* Вертикально расположенные элементы */
    gap: 10px; /* Промежуток между элементами */
}

.update-form input,
.update-form button {
    padding: 10px; /* Внутренние отступы */
    font-size: 16px; /* Размер шрифта */
}

.update-form button {
    cursor: pointer; /* Указатель на кнопке */
    background-color: #007BFF; /* Цвет фона кнопки */
    color: white; /* Цвет текста */
    border: none; /* Убираем рамку */
    border-radius: 4px; /* Скругление углов */
}

.update-container h2 {
    margin-bottom: 15px; /* Отступ снизу для заголовка */
}

.back-link {
    margin-top: 15px; /* Отступ сверху для ссылки на главную */
}

.back-link a {
    text-decoration: none; /* Убираем подчеркивание */
    color: #007BFF; /* Цвет ссылки */
}

.back-link a:hover {
    text-decoration: underline; /* Подчеркивание при наведении */
}
</style>
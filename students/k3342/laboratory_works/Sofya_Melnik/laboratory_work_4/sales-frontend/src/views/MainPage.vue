<template>
  <div class="main-page">
    <header>
      <h1>Добро пожаловать, {{ user.username }}!</h1>
      <nav>
        <router-link to="/profile" class="nav-link">Профиль</router-link>
        <router-link to="/orders" class="nav-link">Заявки</router-link>
        <router-link to="/services" class="nav-link">Услуги</router-link>
        <router-link to="/payments" class="nav-link">Платежи</router-link>
        <button @click="logout" class="logout-btn">Выйти</button>
      </nav>
    </header>

    <section class="main-content">
      <p class="info-text">Выберите раздел для работы с вашей учетной записью.</p>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api';

const router = useRouter();
const user = ref({ username: '', id: '' });

const fetchProfile = async () => {
  try {
    const { data } = await api.get('auth/users/me/');
    user.value = data;
  } catch (error) {
    console.error('Ошибка загрузки профиля:', error);
    router.push('/login');
  }
};

const logout = () => {
  localStorage.removeItem('token');
  router.push('/login');
};

onMounted(() => {
  fetchProfile();
});
</script>

<style scoped>

.main-page {
  font-family: 'Arial', sans-serif;
  background-color: #f4f6f9;
  padding: 40px 20px;
  max-width: 900px;
  margin: 0 auto;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}


header {
  text-align: center;
  margin-bottom: 30px;
}

header h1 {
  font-size: 28px;
  color: #333;
  margin-bottom: 20px;
}


nav {
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}

.nav-link {
  text-decoration: none;
  color: #007bff;
  font-size: 18px;
  padding: 10px;
  transition: color 0.3s ease, transform 0.3s ease;
}

.nav-link:hover {
  color: #0056b3;
  transform: translateY(-3px);
}

.logout-btn {
  background-color: #ff4d4d;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
  border-radius: 5px;
}

.logout-btn:hover {
  background-color: #e30000;
  transform: translateY(-3px);
}


.main-content {
  text-align: center;
  margin-top: 40px;
}

.info-text {
  font-size: 18px;
  color: #555;
  margin-top: 20px;
}
</style>

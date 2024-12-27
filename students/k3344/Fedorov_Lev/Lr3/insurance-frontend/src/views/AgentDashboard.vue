<template>
  <div class="agent-dashboard">
    <div class="profile-card">
      <h1>Кабинет агента</h1>
      <p class="welcome">Добро пожаловать, <strong>{{ user.username }}</strong>!</p>

      <div class="profile-info">
        <p><strong>Роль:</strong> {{ user.role || 'Агент' }}</p>
        <p><strong>Email:</strong> {{ user.email || 'Не указан' }}</p>
      </div>

      <button @click="$router.push('/profile/edit')" class="primary-btn">
        Редактировать профиль
      </button>
    </div>
  </div>
</template>

<script>
import UserService from '@/services/UserService';

export default {
  data() {
    return {
      user: {},
    };
  },
  async created() {
    this.user = await UserService.getProfile();
  },
};
</script>

<style scoped>
.agent-dashboard {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 90vh;
  background-color: #f4f7f6;
}

.profile-card {
  background-color: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 500px;
  width: 100%;
}

.profile-card h1 {
  margin-bottom: 15px;
  font-size: 2rem;
  color: #333;
}

.profile-card .welcome {
  font-size: 1.1rem;
  margin-bottom: 20px;
}

.profile-card .profile-info p {
  margin: 10px 0;
  font-size: 1rem;
  color: #666;
}

.primary-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 12px 30px;
  font-size: 1rem;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 20px;
  transition: background-color 0.3s ease;
}

.primary-btn:hover {
  background-color: #0056b3;
}
</style>

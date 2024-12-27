<template>
  <div>
    <h1>Админ панель</h1>
    <p>Добро пожаловать, {{ user.username }}!</p>
  </div>
  <button @click="$router.push('/profile/edit')">Редактировать профиль</button>
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

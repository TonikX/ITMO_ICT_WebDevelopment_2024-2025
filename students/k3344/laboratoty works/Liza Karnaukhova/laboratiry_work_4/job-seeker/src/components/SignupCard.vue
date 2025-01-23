<template>
  <div class="row justify-content-center">
    <div class="col-12 col-md-6 col-lg-4 signup-container p-4">
      <h3 class="mb-3 text-center">Регистрация</h3>
      <form @submit.prevent="handleRegister">
        <div class="mb-3">
          <label for="username" class="form-label">Придумайте логин</label>
          <input type="email" class="form-control" id="username" v-model="username" required />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Придумайте пароль</label>
          <input type="password" class="form-control" id="password" v-model="password" required />
        </div>
        <div class="mb-3">
          <label for="confirmPassword" class="form-label">Повторите пароль</label>
          <input type="password" class="form-control" id="confirmPassword" v-model="confirmPassword" required />
        </div>
        <div class="mb-3">
          <label for="role" class="form-label">Выберите роль</label>
          <select class="form-select" id="role" v-model="role" required>
            <option value="" disabled>Выберите роль</option>
            <option value="candidate">Кандидат</option>
            <option value="employer">Работодатель</option>
          </select>
        </div>
        <button type="submit" class="btn btn-custom me-2 mb-2">Зарегистрироваться</button>
        <div class="mt-3">
          <router-link to="/login">Уже есть аккаунт?</router-link>
        </div>
        <div v-if="registerError" class="text-danger mt-2">Ошибка регистрации: {{ registerError }}</div>
      </form>
    </div>
  </div>
</template>

<script>
  import { ref } from 'vue';
  import { useAuthStore } from '@/stores/authStore'; // Импортируем хранилище для авторизации
  import { useRouter } from 'vue-router'; // Импортируем useRouter

  export default {
    setup() {
      const username = ref('');
      const password = ref('');
      const confirmPassword = ref('');
      const role = ref('');
      const registerError = ref('');
      const authStore = useAuthStore();
      const router = useRouter(); // Получаем экземпляр маршрутизатора

      const handleRegister = async () => {
        if (password.value !== confirmPassword.value) {
          registerError.value = 'Пароли не совпадают';
          return;
        }
        try {
          await authStore.register({ username: username.value, password: password.value, role: role.value });
          // Перенаправление на главную страницу после успешной регистрации
          router.push('/'); // Используем router для перенаправления
        } catch (err) {
          registerError.value = 'Ошибка регистрации: ' + err.message;
        }
      };

      return {
        username,
        password,
        confirmPassword,
        role,
        registerError,
        handleRegister,
      };
    },
  };
</script>

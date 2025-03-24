<template>
  <div class="authorization-page">
    <div class="card p-5" style="max-width: 500px;">
      <h1 class="text-center mb-4">{{ isLogin ? 'Вход' : 'Регистрация' }}</h1>

      <!-- Форма входа -->
      <div v-if="isLogin">
        <LoginForm @switch-to-register="toggleMode" />
      </div>

      <!-- Форма регистрации -->
      <div v-else>
        <RegisterForm @switch-to-login="toggleMode" />
      </div>

      <div class="text-center mt-4">
        <button class="btn btn-link" @click="toggleMode">
          {{ isLogin ? 'Нет аккаунта? Зарегистрироваться' : 'Есть аккаунт? Войти' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import LoginForm from '@/components/LoginForm.vue';
import RegisterForm from '@/components/RegisterForm.vue';

export default {
  components: {
    LoginForm,
    RegisterForm
  },
  data() {
    return {
      isLogin: true // Изначально показываем форму входа
    };
  },
  methods: {
    toggleMode() {
      this.isLogin = !this.isLogin;
    }
  }
};
</script>

<style scoped>
/* Общий фон */
body {
  background-color: #f8f9fa;
  color: #333;
  font-family: 'Arial', sans-serif;
}

/* Центрируем контейнер и карточку */
.authorization-page {
  min-height: 100vh; /* Занимает всю высоту экрана */
  display: flex;
  justify-content: center; /* Центрируем по горизонтали */
  align-items: center; /* Центрируем по вертикали */
  padding: 0;
  margin: 0;
}

/* Стили для карточки */
.card {
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500px; /* Общая максимальная ширина для обеих форм */
  margin: 0 auto;
}

/* Кнопка переключения режимов */
.btn-link {
  text-decoration: none;
  color: #13263a;
}

.btn-link:hover {
  text-decoration: underline;
}
</style>

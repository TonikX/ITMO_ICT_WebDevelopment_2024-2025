<template>
  <div class="row justify-content-center">
    <div class="col-12 col-md-6 col-lg-4 login-container p-4">
      <h3 class="mb-3 text-center">Вход</h3>
      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label for="exampleInputEmail1" class="form-label">Логин</label>
          <input type="email"
                 class="form-control"
                 id="exampleInputEmail1"
                 v-model="username"
                 required />
        </div>
        <div class="mb-3">
          <label for="exampleInputPassword1" class="form-label">Пароль</label>
          <input type="password"
                 class="form-control"
                 id="exampleInputPassword1"
                 v-model="password"
                 required />
        </div>
        <div class="mb-3 form-check">
          <input type="checkbox" class="form-check-input" id="exampleCheck1" />
          <label class="form-check-label" for="exampleCheck1">Запомнить</label>
        </div>
        <button type="submit" class="btn btn-custom me-2 mb-2">Войти</button>
        <div class="mt-3">
          <router-link to="/signup">Еще нет аккаунта?</router-link>
        </div>
        <div v-if="loginError" class="text-danger mt-2">Неверный логин или пароль</div>
      </form>
    </div>
  </div>
</template>

<script>
  import { useAuthStore } from '@/stores/authStore'; // Импортируйте ваш authStore
  import authApi from '@/api/auth';

  export default {
    name: 'LoginCard',
    data() {
      return {
        username: '',
        password: '',
        loginError: false
      };
    },
    setup() {
      const authStore = useAuthStore(); // Получаем доступ к authStore

      return { authStore };
    },
    methods: {
      async handleLogin() {
        console.log('handleLogin вызван');
        console.log('Данные для входа:', { username: this.username, password: this.password });
        try {
          const data = await authApi.loginUser({ username: this.username, password: this.password });
          console.log('Ответ от API:', data);

          if (data && data.length > 0) {
            const user = data[0];
            localStorage.setItem('currentUser ', JSON.stringify(user));

            // Обновляем состояние пользователя в authStore
            this.authStore.user = user;

            // Перенаправляем в зависимости от роли
            if (user.role === 'candidate') {
              this.$router.push('/useraccount'); // Перенаправление на страницу кандидата
            } else if (user.role === 'employer') {
              this.$router.push('/employeraccount'); // Перенаправление на страницу работодателя
            }
          } else {
            this.showLoginError(); // Показываем ошибку, если пользователь не найден
          }
        } catch (error) {
          console.error('Ошибка входа:', error);
          this.showLoginError(); // Показываем ошибку при возникновении исключения
        }
      },
      showLoginError() {
        this.loginError = true; // Устанавливаем флаг ошибки
      }
    }
  };
</script>

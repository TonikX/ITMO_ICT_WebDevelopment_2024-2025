<template>
  <div class="modal fade" tabindex="-1" id="register-modal">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Регистрация</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="register">
            <div class="mb-3">
              <label for="name" class="form-label">Имя пользователя</label>
              <input
                type="text"
                class="form-control"
                id="name"
                v-model="registerForm.name"
                required
              />
            </div>
            <div class="mb-3">
              <label for="email" class="form-label">Ваш e-mail</label>
              <input
                type="email"
                class="form-control"
                id="email"
                v-model="registerForm.email"
                required
              />
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Пароль</label>
              <input
                type="password"
                class="form-control"
                id="password"
                v-model="registerForm.password"
                required
              />
            </div>
            <div class="mb-3">
              <label for="confirmPassword" class="form-label">Подтверждение пароля</label>
              <input
                type="password"
                class="form-control"
                id="confirmPassword"
                v-model="registerForm.confirmPassword"
                required
              />
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-secondary"
                data-bs-dismiss="modal"
              >
                Закрыть
              </button>
              <button type="submit" class="btn btn-primary">
                Зарегистрироваться
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RegisterModal',
  data() {
    return {
      registerForm: {
        name: '',
        email: '',
        password: '',
        confirmPassword: '',
      },
    };
  },
  methods: {
    async register() {
      if (this.registerForm.password !== this.registerForm.confirmPassword) {
        alert('Пароли не совпадают');
        return;
      }

      try {
        const response = await fetch('http://localhost:8000/auth/users/', { // правильный путь для регистрации
          method: 'POST',
          body: JSON.stringify({
            username: this.registerForm.name,  // в djoser используется "username"
            email: this.registerForm.email,
            password: this.registerForm.password,
          }),
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          const errorData = await response.json();
          alert(`Ошибка регистрации: ${errorData.detail || 'Неверные данные'}`);
          return;
        }

        // При успешной регистрации
        const { accessToken, user } = await response.json();
        localStorage.accessToken = accessToken;
        localStorage.user = JSON.stringify(user);

        this.$router.push('/dashboard');
      } catch (error) {
        console.error(error);
        alert('Ошибка регистрации.');
      }
    },
  },
};
</script>

<style scoped>
/* Стили для модального окна */
.modal-content {
  max-width: 500px;
  margin: auto;
}

.modal-footer {
  display: flex;
  justify-content: space-between;
}

button {
  width: 45%;
}
</style>

<template>
  <div class="modal fade" tabindex="-1" id="log-in-modal">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Вход для диспетчера</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="login">
            <div class="mb-3">
              <label for="username" class="form-label">Имя пользователя</label>
              <input
                type="text"
                class="form-control"
                id="username"
                v-model="loginForm.username"
                required
              />
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Ваш пароль</label>
              <input
                type="password"
                class="form-control"
                id="password"
                v-model="loginForm.password"
                required
              />
            </div>
            <div class="mb-3 form-check">
              <input
                type="checkbox"
                class="form-check-input"
                id="remember-me"
                v-model="loginForm.rememberMe"
              />
              <label class="form-check-label" for="remember-me">Запомнить меня</label>
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
                Войти
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
  name: 'LoginModal',
  data() {
    return {
      loginForm: {
        username: '',  // Имя пользователя (или email, если сервер настроен на это)
        password: '',
        rememberMe: false,
      },
    };
  },
  methods: {
    async login() {
      try {
        const response = await fetch('http://localhost:8000/auth/token/login/', {
          method: 'POST',
          body: JSON.stringify({
            username: this.loginForm.username,
            password: this.loginForm.password,
          }),
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          alert('Ошибка входа. Проверьте данные и попробуйте снова.');
          return;
        }

        const { auth_token } = await response.json();

        localStorage.setItem('accessToken', auth_token);

        this.$router.push('/dashboard');
      } catch (error) {
        console.error(error);
        alert('Ошибка входа.');
      }
    },
  },
};
</script>

<style scoped>
.modal-content {
  border-radius: 8px;
}

.modal-header {
  background-color: #f8f9fa;
}

.modal-footer {
  display: flex;
  justify-content: space-between;
}

.btn-close {
  font-size: 1.5rem;
  color: #000;
}

.form-label {
  font-weight: bold;
}

.form-control {
  border-radius: 5px;
  padding: 10px;
}

.form-check-label {
  font-size: 1rem;
}

.btn-primary {
  background-color: #007bff;
  border: none;
}

.btn-secondary {
  background-color: #6c757d;
  border: none;
}

.btn-primary:hover, .btn-secondary:hover {
  opacity: 0.9;
}
</style>

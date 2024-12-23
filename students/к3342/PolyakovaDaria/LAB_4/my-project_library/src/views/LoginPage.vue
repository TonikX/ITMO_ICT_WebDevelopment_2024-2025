<!-- src/views/LoginPage.vue -->
<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-card class="pa-5" elevation="5">
          <v-card-title class="text-center text-h5">🔐 Вход в систему</v-card-title>
          <v-card-text>
            <!-- Форма авторизации -->
            <v-form @submit.prevent="login">
              <v-text-field
                v-model="credentials.email"
                label="Email"
                type="email"
                placeholder="example@example.com"
                required
              ></v-text-field>
              <v-text-field
                v-model="credentials.password"
                label="Пароль"
                type="password"
                placeholder="Введите пароль"
                required
              ></v-text-field>
              <v-btn
                type="submit"
                color="primary"
                block
                :disabled="isLoading"
                class="mt-3"
              >
                Войти
              </v-btn>
            </v-form>
            <!-- Сообщение об ошибке -->
            <v-alert
              v-if="error"
              type="error"
              class="mt-3"
            >
              {{ error }}
            </v-alert>
          </v-card-text>
          <v-card-actions class="justify-center">
            <v-btn text to="/register">Нет аккаунта? Зарегистрируйтесь</v-btn>
          </v-card-actions>
        </v-card>
        <!-- Индикатор загрузки -->
        <v-row v-if="isLoading" class="mt-3" justify="center">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'LoginPage',
  data() {
    return {
      credentials: {
        email: '',
        password: '',
      },
      error: null,
      isLoading: false,
    };
  },
  methods: {
    async login() {
      this.isLoading = true;
      this.error = null;

      try {
        // Используем действие Vuex для входа
        await this.$store.dispatch('login', this.credentials);
        // Перенаправление после успешного входа
        this.$router.push('/profile');
      } catch (error) {
        // Обработка ошибок
        if (error.response?.data?.non_field_errors) {
          this.error = error.response.data.non_field_errors[0];
        } else if (error.response?.data?.email || error.response?.data?.password) {
          this.error = 'Email или пароль указаны неверно.';
        } else {
          this.error = 'Произошла ошибка. Попробуйте снова.';
        }
        console.error('Ошибка входа:', error.response?.data || error);
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

<style scoped>
</style>

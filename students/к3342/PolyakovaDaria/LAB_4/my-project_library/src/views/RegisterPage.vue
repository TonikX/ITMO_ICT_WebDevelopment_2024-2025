<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-card class="pa-5" elevation="5">
          <v-card-title class="text-h5 text-center">📝 Регистрация</v-card-title>
          <v-card-text>
            <!-- Форма регистрации -->
            <v-form @submit.prevent="register">
              <v-text-field
                v-model="username"
                label="Имя пользователя"
                placeholder="Введите имя пользователя"
                required
              ></v-text-field>
              <v-text-field
                v-model="email"
                label="Email"
                type="email"
                placeholder="example@example.com"
                required
              ></v-text-field>
              <v-text-field
                v-model="password"
                label="Пароль"
                type="password"
                placeholder="Введите пароль"
                required
              ></v-text-field>
              <v-text-field
                v-model="rePassword"
                label="Подтверждение пароля"
                type="password"
                placeholder="Повторите пароль"
                required
              ></v-text-field>
              <v-btn
                type="submit"
                color="primary"
                block
                class="mt-3"
                :disabled="isLoading"
              >
                Зарегистрироваться
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
            <v-btn text to="/login">Уже есть аккаунт? Войти</v-btn>
          </v-card-actions>
        </v-card>

        <!-- Индикатор загрузки -->
        <v-row v-if="isLoading" justify="center" class="mt-3">
          <v-progress-circular
            indeterminate
            color="primary"
            size="50"
          ></v-progress-circular>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axiosAuth from '@/axiosAuth';

export default {
  name: 'RegisterPage',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      rePassword: '',
      error: null,
      isLoading: false,
    };
  },
  methods: {
    async register() {
      this.isLoading = true;
      this.error = null;

      if (this.password !== this.rePassword) {
        this.error = 'Пароли не совпадают. Пожалуйста, проверьте и попробуйте снова.';
        this.isLoading = false;
        return;
      }

      try {
        const response = await axiosAuth.post('/auth/users/', {
          username: this.username,
          email: this.email,
          password: this.password,
          re_password: this.rePassword,
        });
        console.log('Registration successful:', response.data);
        this.$router.push('/login');
      } catch (error) {
        console.error('Registration error:', error.response?.data || error.message);
        this.error =
          error.response?.data?.detail ||
          Object.values(error.response?.data || { error: 'Неизвестная ошибка' }).join(' ');
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

<template>
  <v-card class="mx-auto mt-10" max-width="500">
    <v-card-title class="text-center text-h5 py-4">
      Регистрация
    </v-card-title>
    
    <v-card-text>
      <v-form @submit.prevent="handleSubmit" ref="form">
        <v-text-field
          v-model="username"
          label="Имя пользователя"
          :rules="[rules.required]"
          prepend-icon="mdi-account"
          required
        ></v-text-field>

        <v-text-field
          v-model="password"
          label="Пароль"
          :type="showPassword ? 'text' : 'password'"
          :rules="[rules.required]"
          prepend-icon="mdi-lock"
          :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          @click:append="showPassword = !showPassword"
          required
        ></v-text-field>

        <v-text-field
          v-model="confirmPassword"
          label="Подтвердите пароль"
          :type="showPassword ? 'text' : 'password'"
          :rules="[rules.required, rules.passwordMatch]"
          prepend-icon="mdi-lock"
          required
        ></v-text-field>

        <v-btn
          color="primary"
          block
          type="submit"
          :loading="loading"
          class="mt-4"
        >
          Зарегистрироваться
        </v-btn>
      </v-form>

      <div class="text-center mt-4">
        <router-link to="/login" class="text-decoration-none">
          Уже есть аккаунт? Войдите
        </router-link>
      </div>
    </v-card-text>

    <v-snackbar
      v-model="showError"
      color="error"
      timeout="3000"
    >
      {{ errorMessage }}
    </v-snackbar>
  </v-card>
</template>

<script>
export default {
  name: 'Register',
  data: () => ({
    username: '',
    password: '',
    confirmPassword: '',
    showPassword: false,
    loading: false,
    showError: false,
    errorMessage: '',
    rules: {
      required: v => !!v || 'Обязательное поле',
      passwordMatch: function(v) {
        return this.password === v || 'Пароли не совпадают'
      }
    }
  }),
  methods: {
    async handleSubmit() {
      if (!this.$refs.form.validate()) return

      this.loading = true
      try {
        await this.$store.dispatch('auth/register', {
          username: this.username,
          password: this.password
        })
        this.$router.push('/profile')
      } catch (error) {
        this.errorMessage = error.message || 'Произошла ошибка при регистрации'
        this.showError = true
      } finally {
        this.loading = false
      }
    }
  }
}
</script> 
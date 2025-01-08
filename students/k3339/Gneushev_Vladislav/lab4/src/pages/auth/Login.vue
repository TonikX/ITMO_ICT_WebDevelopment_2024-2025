<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card>
          <v-card-title class="text-center text-h5 py-4">
            Вход в систему
          </v-card-title>

          <v-card-text>
            <v-form @submit.prevent="handleSubmit">
              <v-text-field
                v-model="form.username"
                label="Имя пользователя"
                :rules="[v => !!v || 'Обязательное поле']"
                required
              ></v-text-field>

              <v-text-field
                v-model="form.password"
                label="Пароль"
                type="password"
                :rules="[v => !!v || 'Обязательное поле']"
                required
              ></v-text-field>

              <v-btn
                color="primary"
                type="submit"
                block
                class="mt-4"
                :loading="loading"
              >
                Войти
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>

        <v-snackbar
          v-model="showError"
          color="error"
          timeout="3000"
        >
          {{ errorMessage }}
        </v-snackbar>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'Login',

  data: () => ({
    form: {
      username: '',
      password: ''
    },
    loading: false,
    showError: false,
    errorMessage: ''
  }),

  created() {
    // Если пользователь уже авторизован, перенаправляем его
    if (this.$store.state.auth.isAuthenticated) {
      this.$router.push('/drivers')
    }
  },

  methods: {
    async handleSubmit() {
      this.loading = true
      try {
        await this.$store.dispatch('auth/login', this.form)
        this.$router.push('/drivers') // Перенаправляем после успешного входа
      } catch (error) {
        console.error('Login error:', error)
        this.errorMessage = 'Ошибка при входе в систему'
        this.showError = true
      } finally {
        this.loading = false
      }
    }
  }
}
</script> 
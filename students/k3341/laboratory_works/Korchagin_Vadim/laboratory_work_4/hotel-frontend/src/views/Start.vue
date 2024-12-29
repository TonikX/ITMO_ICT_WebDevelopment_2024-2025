<template>
  <v-container class="d-flex align-center justify-center fill-height">
    <v-card class="pa-5 elevated-card" width="400">
      <h2 class="text-center mb-4">Добро пожаловать</h2>
      <p class="text-center">
        Пожалуйста, выберите, что вы хотите сделать:
      </p>
      <v-btn
        variant="elevated"
        color="primary"
        class="mb-2"
        block
        @click="goToLogin"
      >
        Войти
      </v-btn>
      <v-btn
        variant="flat"
        color="warning"
        block
        @click="goToRegister"
      >
        Зарегистрироваться
      </v-btn>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: 'Start',
  methods: {
    goToLogin() {
      this.$router.push('/login')
    },
    goToRegister() {
      this.$router.push('/register')
    }
  }
}
</script>

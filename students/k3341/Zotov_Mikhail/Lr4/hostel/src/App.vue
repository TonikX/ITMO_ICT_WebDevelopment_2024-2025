<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-btn text to="/">Konpeki Plaza</v-btn>
      <v-spacer></v-spacer>

      <template v-if="authStore.isAuthenticated">
        <v-btn text to="/rooms">Комнаты</v-btn>
        <v-btn text to="/employees">Сотрудники</v-btn>
        <v-btn text to="/clients">Клиенты</v-btn>
        <v-btn text to="/check-ins">Регистрация</v-btn>
        <v-btn text to="/reports">Отчет</v-btn>

        <v-menu offset-y transition="slide-y-transition">
          <template v-slot:activator="{ props }">
            <v-btn v-bind="props" class="user-btn">
              <v-icon left>mdi-account</v-icon>
              {{ authStore.user?.username || "Профиль" }}
            </v-btn>
          </template>
          <v-card class="user-menu">
            <v-card-text>
              <v-btn block color="error" @click="logout">
                <v-icon left>mdi-logout</v-icon>
                Выйти
              </v-btn>
            </v-card-text>
          </v-card>
        </v-menu>
      </template>

      <template v-else>
        <v-btn text to="/login">Войти</v-btn>
        <v-btn text to="/register">Регистрация</v-btn>
      </template>
    </v-app-bar>

    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>
import {useAuthStore} from '@/stores/auth'
import {onMounted} from 'vue'
import {useRouter} from 'vue-router'

export default {
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()

    const logout = async () => {
      await authStore.logout()
      router.push('/')
    }

    onMounted(() => {
      authStore.checkAuth()
    })

    return {authStore, logout}
  }
}
</script>

<style scoped>
.user-btn {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 8px 16px;
}

.user-menu {
  min-width: 180px;
  border-radius: 10px;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.2);
  background: #2d2d2d;
  color: white;
}

.user-menu .v-btn {
  font-weight: bold;
  justify-content: start;
}
</style>

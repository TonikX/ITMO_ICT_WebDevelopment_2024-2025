<template>
  <page-wrapper>
    <v-card>
      <v-card-title class="text-h5 d-flex align-center">
        <v-icon icon="mdi-account" class="mr-2"></v-icon>
        Профиль пользователя
      </v-card-title>

      <v-card-text>
        <v-list>
          <v-list-item>
            <template v-slot:prepend>
              <v-icon icon="mdi-account-circle"></v-icon>
            </template>
            <v-list-item-title>
              Имя пользователя
            </v-list-item-title>
            <v-list-item-subtitle>
              {{ user?.username || 'Загрузка...' }}
            </v-list-item-subtitle>
          </v-list-item>

          <v-list-item>
            <template v-slot:prepend>
              <v-icon icon="mdi-identifier"></v-icon>
            </template>
            <v-list-item-title>
              ID пользователя
            </v-list-item-title>
            <v-list-item-subtitle>
              {{ user?.id || 'Загрузка...' }}
            </v-list-item-subtitle>
          </v-list-item>

          <v-list-item>
            <template v-slot:prepend>
              <v-icon icon="mdi-shield-account"></v-icon>
            </template>
            <v-list-item-title>
              Роль
            </v-list-item-title>
            <v-list-item-subtitle>
              <v-chip
                :color="user?.is_admin ? 'primary' : 'default'"
                size="small"
                class="mt-1"
              >
                {{ user?.is_admin ? 'Администратор' : 'Пользователь' }}
              </v-chip>
            </v-list-item-subtitle>
          </v-list-item>
        </v-list>

        <v-divider class="my-4"></v-divider>

        <v-btn
          color="error"
          prepend-icon="mdi-logout"
          @click="handleLogout"
          :loading="loading"
          block
        >
          Выйти из системы
        </v-btn>
      </v-card-text>
    </v-card>

    <v-snackbar
      v-model="showError"
      color="error"
      timeout="3000"
    >
      {{ errorMessage }}
    </v-snackbar>
  </page-wrapper>
</template>

<script>
import { api } from '@/services/api'
import PageWrapper from '@/components/PageWrapper.vue'

export default {
  name: 'Profile',

  components: {
    PageWrapper
  },

  data: () => ({
    user: null,
    loading: false,
    showError: false,
    errorMessage: ''
  }),

  async created() {
    await this.fetchUserInfo()
  },

  methods: {
    async fetchUserInfo() {
      try {
        const { data } = await api.get('/users/me')
        this.user = data
      } catch (error) {
        console.error('Error fetching user info:', error)
        this.errorMessage = 'Ошибка при загрузке информации о пользователе'
        this.showError = true
      }
    },

    async handleLogout() {
      this.loading = true
      try {
        await this.$store.dispatch('auth/logout')
        this.$router.push('/login')
      } catch (error) {
        console.error('Logout error:', error)
        this.errorMessage = 'Ошибка при выходе из системы'
        this.showError = true
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.v-list-item {
  min-height: 64px;
}
</style> 
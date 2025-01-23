<template>
  <header class="header">
    <nav class="navbar navbar-expand-lg">
      <div class="container navbar-container">
        <router-link to="/" class="navbar-brand text-center mx-auto">
          <img src="../assets/logo.png" alt="Логотип">
          <span class="brand fs-4">Сотка - будет работка</span>
        </router-link>
        <div class="d-none d-lg-flex justify-content-end flex-grow-1">
          <template v-if="user">
            <router-link :to="userRoleLink" class="btn btn-custom me-2">
              <AccountIcon />
              Перейти в аккаунт
            </router-link>
            <button @click="logout" class="btn btn-custom">
              <LogoutIcon />
              Выйти
            </button>
          </template>
          <template v-else>
            <router-link to="/login" class="btn btn-custom me-2">
              <AccountIcon />
              Войти
            </router-link>
            <router-link to="/signup" class="btn btn-custom">
              <SignupIcon />
              Регистрация
            </router-link>
          </template>
        </div>
        <div class="d-flex d-lg-none justify-content-center w-100">
          <template v-if="user">
            <router-link :to="userRoleLink" class="btn btn-custom me-2 mb-2">
              <AccountIcon />
              Перейти в аккаунт
            </router-link>
            <button @click="logout" class="btn btn-custom mb-2">
              <LogoutIcon />
              Выйти
            </button>
          </template>
          <template v-else>
            <router-link to="/login" class="btn btn-custom me-2 mb-2">
              <AccountIcon />
              Войти
            </router-link>
            <router-link to="/signup" class="btn btn-custom mb-2">
              <SignupIcon />
              Регистрация
            </router-link>
          </template>
        </div>
      </div>
    </nav>
  </header>
</template>

<script>
  import { useAuthStore } from '@/stores/authStore'; // Импортируйте ваш authStore
  import { computed } from 'vue'; // Импортируйте computed
  import AccountIcon from '@/components/icons/IconAccount.vue';
  import SignupIcon from '@/components/icons/IconSignup.vue';
  import LogoutIcon from '@/components/icons/IconLogout.vue';

  export default {
    name: 'HeaderComponent',
    components: {
      AccountIcon,
      SignupIcon,
      LogoutIcon,
    },
    setup() {
      const authStore = useAuthStore();

      // Используем реактивное свойство user из authStore
      const user = computed(() => authStore.user);

      const userRoleLink = computed(() => {
        if (user.value) {
          return user.value.role === 'employer' ? '/employeraccount' : '/useraccount';
        }
        return '/';
      });

      const logout = () => {
        authStore.logout();
      };

      return {
        user,
        userRoleLink,
        logout,
      };
    },
  };
</script>

<style scoped>
  /* Ваши стили для шапки */
</style>

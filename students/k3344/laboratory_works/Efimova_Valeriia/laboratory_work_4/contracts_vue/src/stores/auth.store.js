import { defineStore } from 'pinia';

import { fetchWrapper, router } from '@/helpers';

const baseUrl = `${import.meta.env.VITE_API_URL}`;

export const useAuthStore = defineStore({
  id: 'auth',
  state: () => ({
    access: JSON.parse(localStorage.getItem('access')),
    refresh: JSON.parse(localStorage.getItem('refresh')),
  }),
  actions: {
    async login(username, password) {
      try {
        const data = await fetchWrapper.post(`${baseUrl}/auth/jwt/create/`, {username: username, password: password});
        this.access = data.access;
        this.refresh = data.refresh;

        localStorage.setItem('access', JSON.stringify(data.access));
        localStorage.setItem('refresh', JSON.stringify(data.refresh));

        await router.push('/');
      } catch (error) {
        throw error;
      }
    },
    async logout() {
      this.access = null;
      this.refresh = null;

      localStorage.removeItem('access');
      localStorage.removeItem('refresh');

      await router.push('/login');
    }
  }
});

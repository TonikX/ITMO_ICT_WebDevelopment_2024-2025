import {defineStore} from 'pinia';
import axios from 'axios';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        accessToken: localStorage.getItem('accessToken') || null,
        user: null,
        loading: false,
        error: null,
    }),
    getters: {
        isAuthenticated: (state) => !!state.accessToken,
        userRole: (state) => state.user?.role?.name || null,
        isAdmin: (state) => state.userRole === 'ROLE_ADMIN',
    },
    actions: {
        async login(credentials) {
            this.loading = true;
            this.error = null;
            try {
                const response = await axios.post('http://localhost:8080/auth/login', credentials);
                const token = response.data.accessToken;

                localStorage.setItem('accessToken', token);
                this.accessToken = token;

                await this.fetchUser();

                return true;
            } catch (error) {
                this.error = error.response?.data?.message || 'Login failed';
                return false;
            } finally {
                this.loading = false;
            }
        },
        async fetchUser() {
            if (!this.accessToken) return;

            try {
                const response = await axios.get('http://localhost:8080/rest/me', {
                    headers: {
                        Authorization: `Bearer ${this.accessToken}`,
                    },
                });
                this.user = response.data;
            } catch (error) {
                this.logout();
            }
        },
        logout() {
            this.accessToken = null;
            this.user = null;
            localStorage.removeItem('accessToken');
        },
    },
});

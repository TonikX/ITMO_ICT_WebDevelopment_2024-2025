import {ref, computed} from 'vue';

export const authToken = ref(localStorage.getItem('authToken'));

export const isAuthenticated = computed(() => !!authToken.value);

export const setAuthToken = (token) => {
    authToken.value = token;
    localStorage.setItem('authToken', token);
};

export const clearAuthToken = () => {
    authToken.value = null;
    localStorage.removeItem('authToken');
};

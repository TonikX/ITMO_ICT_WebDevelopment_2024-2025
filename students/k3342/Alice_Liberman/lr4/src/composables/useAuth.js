import {computed, ref} from 'vue';
import {update} from "@/stores/globalState.js";

export const authToken = ref(localStorage.getItem('authToken'));

export const isAuthenticated = computed(() => !!authToken.value);


export const setAuthToken = (token) => {
    authToken.value = token;
    localStorage.setItem('authToken', token);
    update()
};

export const clearAuthToken = () => {
    authToken.value = null;
    localStorage.removeItem('authToken');
    update()
};